" Scratchpad object definition "

__all__ = ["Scratch"]

import logging
import os
from dataclasses import dataclass
from typing import Callable, cast

from aiofiles import open as aiopen
from aiofiles import os as aios

from ...common import CastBoolMixin, state
from ...ipc import notify_error
from ...types import ClientInfo, MonitorInfo, VersionInfo
from .helpers import OverridableConfig, get_match_fn


@dataclass
class MetaInfo:
    "Meta properties"
    initialized: bool = False
    should_hide: bool = False
    no_pid: bool = False
    last_shown: float | int = 0
    space_identifier: tuple[str, str] = ("", "")
    monitor_info: MonitorInfo = None  # type: ignore


class Scratch(CastBoolMixin):  # {{{
    "A scratchpad state including configuration & client state"
    log = logging.getLogger("scratch")
    get_client_props: Callable
    client_info: ClientInfo
    visible = False
    uid = ""
    monitor = ""
    pid = -1

    def __init__(self, uid, opts):
        self.uid = uid
        self.set_config(OverridableConfig(opts, opts.get("monitor", {})))
        self.client_info: ClientInfo = {}  # type: ignore
        self.meta = MetaInfo()
        self.extra_addr: set[str] = set()  # additional client addresses

    def set_config(self, opts):
        "Apply constraints to the configuration"
        if "class_match" in opts:  # NOTE: legacy, to be removed
            opts["match_by"] = "class"
        if self.cast_bool(opts.get("preserve_aspect")):
            opts["lazy"] = True
        if not opts.get("process_tracking", True):
            opts["lazy"] = True
            if "match_by" not in opts:
                opts["match_by"] = "class"
        if state.hyprland_version < VersionInfo(0, 39, 0):
            opts["allow_special_workspace"] = False

        self.conf = opts

    def have_address(self, addr):
        "Check if the address is the same as the client"
        return addr == self.full_address or addr in self.extra_addr

    async def initialize(self, ex):
        "Initialize the scratchpad"
        if self.meta.initialized:
            return
        self.meta.initialized = True
        await self.updateClientInfo()
        await ex.hyprctl(
            f"movetoworkspacesilent special:scratch_{self.uid},address:{self.full_address}"
        )
        if "class_match" in self.conf:  # NOTE: legacy, to be removed
            await notify_error(
                f'scratchpad {self.uid} should use match_by="class" instead of the deprecated class_match',
                logger=self.log,
            )

    async def isAlive(self) -> bool:
        "is the process running ?"
        if self.cast_bool(self.conf.get("process_tracking"), True):
            path = f"/proc/{self.pid}"
            if await aios.path.exists(path):
                async with aiopen(
                    os.path.join(path, "status"), mode="r", encoding="utf-8"
                ) as f:
                    for line in await f.readlines():
                        if line.startswith("State"):
                            proc_state = line.split()[1]
                            return (
                                proc_state not in "ZX"
                            )  # not "Z (zombie)"or "X (dead)"
        else:
            if self.meta.no_pid:
                return bool(await self.fetch_matching_client())
            return False

        return False

    async def fetch_matching_client(self, clients=None):
        "Fetch the first matching client properties"
        match_by, match_val = self.get_match_props()
        return await self.get_client_props(
            match_fn=get_match_fn(match_by, match_val),
            clients=clients,
            **{match_by: match_val},
        )

    def get_match_props(self):
        "Returns the match properties for the scratchpad"
        match_by = self.conf.get("match_by", "pid")
        return match_by, self.pid if match_by == "pid" else self.conf[match_by]

    def reset(self, pid: int) -> None:
        "clear the object"
        self.pid = pid
        self.visible = False
        self.client_info = {}  # type: ignore
        self.meta.initialized = False

    @property
    def address(self) -> str:
        "Returns the client address"
        return self.client_info.get("address", "")[2:]

    @property
    def full_address(self) -> str:
        "Returns the client address"
        return cast(str, self.client_info.get("address", ""))

    async def updateClientInfo(
        self,
        client_info: ClientInfo | None = None,
        clients: list[ClientInfo] | None = None,
    ) -> None:
        "update the internal client info property, if not provided, refresh based on the current address"
        if client_info is None:
            client_info = await self.get_client_props(
                addr=self.full_address, clients=clients
            )
        if not isinstance(client_info, dict):
            if client_info is None:
                self.log.error("The client window %s vanished", self.full_address)
                raise KeyError(f"Client window {self.full_address} not found")
            self.log.error(
                "client_info of %s must be a dict: %s", self.address, client_info
            )
            raise AssertionError(f"Not a dict: {client_info}")

        self.client_info.update(client_info)

    def __str__(self):
        return f"{self.uid} {self.address} : {self.client_info} / {self.conf}"


# }}}
# }}}

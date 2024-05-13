#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Dict, List, Optional, Type

from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.interface.MprisInterfacePlayer import MprisInterfacePlayer
from mpris_api.interface.MprisInterfacePlayLists import MprisInterfacePlayLists
from mpris_api.interface.MprisInterfaceRoot import MprisInterfaceRoot
from mpris_api.interface.MprisInterfaceTrackList import MprisInterfaceTrackList


class _NullInterface(MprisInterfaceBase):
    pass


_NULL_INTERFACE = _NullInterface(name='')


class MprisUpdateNotifier:

    def __init__(self, interfaces: List[MprisInterfaceBase]) -> None:
        self._interfaces: Dict[Type[MprisInterfaceBase], MprisInterfaceBase] = {
            type(interface): interface
            for interface in interfaces
        }

    def notifyAll(self) -> None:
        for interface in self._interfaces.values():
            interface.emitAll()

    def notifyRoot(self, fields: Optional[List[str]] = None) -> None:
        self._notifyInterface(interfaceType=MprisInterfaceRoot, fields=fields)

    def notifyPlayer(self, fields: Optional[List[str]] = None) -> None:
        self._notifyInterface(interfaceType=MprisInterfacePlayer, fields=fields)

    def notifyTracklist(self, fields: Optional[List[str]] = None) -> None:
        self._notifyInterface(interfaceType=MprisInterfaceTrackList, fields=fields)

    def notifyPlaylists(self, fields: Optional[List[str]] = None) -> None:
        self._notifyInterface(interfaceType=MprisInterfacePlayLists, fields=fields)

    def _notifyInterface(
        self,
        interfaceType: Type[MprisInterfaceBase],
        fields: Optional[List[str]]
    ) -> None:
        self._interfaces.get(interfaceType, _NULL_INTERFACE).emitFields(names=fields)

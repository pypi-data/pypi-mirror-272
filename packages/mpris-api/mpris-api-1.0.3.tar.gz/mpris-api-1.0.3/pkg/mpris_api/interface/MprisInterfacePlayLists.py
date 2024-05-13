#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterPlayLists import IMprisAdapterPlayLists
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisPlaylistOrdering import MprisPlaylistOrdering


class MprisPlayListsSignal:
    PLAYLIST_CHANGED: str = 'PlaylistChanged'


class MprisPlayListsProperty:
    PLAYLIST_COUNT: str = 'PlaylistCount'
    ORDERINGS: str = 'Orderings'
    ACTIVE_PLAYLIST: str = 'ActivePlaylist'


class MprisPlayListsMethod:
    ACTIVATE_PLAYLIST: str = 'ActivatePlaylist'
    GET_PLAYLISTS: str = 'GetPlaylists'


class MprisInterfacePlayLists(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterPlayLists) -> None:
        super().__init__(f'{MprisConstant.NAME}.Playlists')
        self._adapter: IMprisAdapterPlayLists = adapter

    @dbusSignal(name=MprisPlayListsSignal.PLAYLIST_CHANGED)
    @no_type_check
    def playlistChanged(self, playlist: DbusType.TUPLE_OSS) -> None:
        pass

    @dbusProperty(name=MprisPlayListsProperty.PLAYLIST_COUNT, access=PropertyAccess.READ)
    @no_type_check
    def playlistCount(self) -> DbusType.UINT32:
        return self._adapter.getPlaylistCount()

    @dbusProperty(name=MprisPlayListsProperty.ORDERINGS, access=PropertyAccess.READ)
    @no_type_check
    def orderings(self) -> DbusType.STRING_ARRAY:
        return [ordering.value for ordering in self._adapter.getAvailableOrderings()]

    @dbusProperty(name=MprisPlayListsProperty.ACTIVE_PLAYLIST, access=PropertyAccess.READ)
    @no_type_check
    def activePlaylist(self) -> DbusType.MAYBE_TUPLE_OSS:
        activePlaylist = self._adapter.getActivePlaylist()
        return (False, None) if activePlaylist is None\
            else (True, activePlaylist.toTuple())

    @dbusMethod(name=MprisPlayListsMethod.ACTIVATE_PLAYLIST)
    @no_type_check
    def activatePlaylist(self, playlistId: DbusType.OBJECT) -> None:
        self._adapter.activatePlaylist(playlistId=playlistId)

    @dbusMethod(name=MprisPlayListsMethod.GET_PLAYLISTS)
    @no_type_check
    def getPlaylists(
        self,
        index: DbusType.UINT32,
        maxCount: DbusType.UINT32,
        order: DbusType.STRING,
        reverseOrder: DbusType.BOOL
    ) -> DbusType.TUPLE_OSS_ARRAY:
        self._adapter.getPlaylists(
            index=index,
            maxCount=maxCount,
            order=MprisPlaylistOrdering(order),
            reverseOrder=reverseOrder
        )

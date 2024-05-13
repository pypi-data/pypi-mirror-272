#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterTrackList import IMprisAdapterTrackList
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant


class MprisTrackListSignal:
    TRACK_LIST_REPLACED: str = 'TrackListReplaced'
    TRACK_ADDED: str = 'TrackAdded'
    TRACK_REMOVED: str = 'TrackRemoved'
    TRACK_METADATA_CHANGED: str = 'TrackMetadataChanged'


class MprisTrackListProperty:
    TRACKS: str = 'Tracks'
    CAN_EDIT_TRACKS: str = 'CanEditTracks'


class MprisTrackListMethod:
    GET_TRACKS_METADATA: str = 'GetTracksMetadata'
    ADD_TRACK: str = 'AddTrack'
    REMOVE_TRACK: str = 'RemoveTrack'
    GO_TO: str = 'GoTo'


class MprisInterfaceTrackList(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterTrackList) -> None:
        super().__init__(f'{MprisConstant.NAME}.TrackList')
        self._adapter: IMprisAdapterTrackList = adapter

    @dbusSignal(name=MprisTrackListSignal.TRACK_LIST_REPLACED)
    @no_type_check
    def trackListReplaced(self, tracks: DbusType.OBJECT_ARRAY, currentTrack: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignal.TRACK_ADDED)
    @no_type_check
    def trackAdded(self, metaData: DbusType.VARIANT_DICT, afterTrack: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignal.TRACK_REMOVED)
    @no_type_check
    def trackRemoved(self, trackId: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignal.TRACK_METADATA_CHANGED)
    @no_type_check
    def trackMetadataChanged(self, trackId: DbusType.OBJECT, metaData: DbusType.VARIANT_DICT) -> None:
        pass

    @dbusProperty(name=MprisTrackListProperty.CAN_EDIT_TRACKS, access=PropertyAccess.READ)
    @no_type_check
    def canEditTracks(self) -> DbusType.BOOL:
        return self._adapter.canEditTracks()

    @dbusProperty(name=MprisTrackListProperty.TRACKS, access=PropertyAccess.READ)
    @no_type_check
    def tracks(self) -> DbusType.OBJECT_ARRAY:
        return [str(track) for track in self._adapter.getTracks()]

    @dbusMethod(name=MprisTrackListMethod.GET_TRACKS_METADATA)
    @no_type_check
    def getTracksMetadata(self, trackIds: DbusType.OBJECT_ARRAY) -> DbusType.VARIANT_DICT_ARRAY:
        metaDataList = self._adapter.getTracksMetadata(trackIds=trackIds)
        return [metaData.toVariantDict() for metaData in metaDataList]

    @dbusMethod(name=MprisTrackListMethod.ADD_TRACK)
    @no_type_check
    def addTrack(self, uri: DbusType.STRING, afterTrack: DbusType.OBJECT, goTo: DbusType.BOOL) -> None:
        afterTrackIdOpt = afterTrack if afterTrack != MprisConstant.NO_TRACK_PATH else None
        self._adapter.addTrack(
            uri=uri,
            afterTrackId=afterTrackIdOpt,
            goTo=goTo
        )

    @dbusMethod(name=MprisTrackListMethod.REMOVE_TRACK)
    @no_type_check
    def removeTrack(self, trackId: DbusType.OBJECT) -> None:
        self._adapter.removeTrack(trackId=trackId)

    @dbusMethod(name=MprisTrackListMethod.GO_TO)
    @no_type_check
    def goTo(self, trackId: DbusType.OBJECT) -> None:
        self._adapter.gotTo(trackId=trackId)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess
from tunit.unit import Microseconds

from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer
from mpris_api.common.DbusObjectSpec import DbusObjectSpec
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisLoopStatus import MprisLoopStatus
from mpris_api.model.MprisMetaData import MprisMetaDataField
from mpris_api.model.MprisPlaybackStatus import MprisPlaybackStatus


class MprisInvalidTrackException(Exception):
    pass


class MprisPlayerSignal:
    SEEKED: str = 'Seeked'


class MprisPlayerProperty:
    CAN_CONTROL: str = 'CanControl'
    CAN_PLAY: str = 'CanPlay'
    CAN_PAUSE: str = 'CanPause'
    CAN_GO_NEXT: str = 'CanGoNext'
    CAN_GO_PREVIOUS: str = 'CanGoPrevious'
    CAN_SEEK: str = 'CanSeek'
    MINIMUM_RATE: str = 'MinimumRate'
    MAXIMUM_RATE: str = 'MaximumRate'
    RATE: str = 'Rate'
    VOLUME: str = 'Volume'
    METADATA: str = 'Metadata'
    PLAYBACK_STATUS: str = 'PlaybackStatus'
    POSITION: str = 'Position'
    LOOP_STATUS: str = 'LoopStatus'
    SHUFFLE: str = 'Shuffle'


class MprisPlayerMethod:
    STOP: str = 'Stop'
    PLAY: str = 'Play'
    PAUSE: str = 'Pause'
    PLAY_PAUSE: str = 'PlayPause'
    NEXT: str = 'Next'
    PREVIOUS: str = 'Previous'
    SEEK: str = 'Seek'
    SET_POSITION: str = 'SetPosition'
    OPEN_URI: str = 'OpenUri'


class MprisInterfacePlayer(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterPlayer) -> None:
        super().__init__(f'{MprisConstant.NAME}.Player')
        self._adapter: IMprisAdapterPlayer = adapter

    @dbusSignal(name=MprisPlayerSignal.SEEKED)
    @no_type_check
    def seeked(self, position: DbusType.INT64) -> None:
        return

    @dbusProperty(name=MprisPlayerProperty.CAN_CONTROL, access=PropertyAccess.READ)
    @no_type_check
    def canControl(self) -> DbusType.BOOL:
        return self._adapter.canControl()

    @dbusProperty(name=MprisPlayerProperty.CAN_PLAY, access=PropertyAccess.READ)
    @no_type_check
    def canPlay(self) -> DbusType.BOOL:
        return self._adapter.canPlay()

    @dbusProperty(name=MprisPlayerProperty.CAN_PAUSE, access=PropertyAccess.READ)
    @no_type_check
    def canPause(self) -> DbusType.BOOL:
        return self._adapter.canPause()

    @dbusProperty(name=MprisPlayerProperty.CAN_GO_NEXT, access=PropertyAccess.READ)
    @no_type_check
    def canGoNext(self) -> DbusType.BOOL:
        return self._adapter.canGoNext()

    @dbusProperty(name=MprisPlayerProperty.CAN_GO_PREVIOUS, access=PropertyAccess.READ)
    @no_type_check
    def canGoPrevious(self) -> DbusType.BOOL:
        return self._adapter.canGoPrevious()

    @dbusProperty(name=MprisPlayerProperty.CAN_SEEK, access=PropertyAccess.READ)
    @no_type_check
    def canSeek(self) -> DbusType.BOOL:
        return self._adapter.canSeek()

    @dbusProperty(name=MprisPlayerProperty.MINIMUM_RATE, access=PropertyAccess.READ)
    @no_type_check
    def minimumRate(self) -> DbusType.DOUBLE:
        return self._adapter.getMinimumRate()

    @dbusProperty(name=MprisPlayerProperty.MAXIMUM_RATE, access=PropertyAccess.READ)
    @no_type_check
    def maximumRate(self) -> DbusType.DOUBLE:
        return self._adapter.getMaximumRate()

    @dbusProperty(name=MprisPlayerProperty.RATE)
    @no_type_check
    def rate(self) -> DbusType.DOUBLE:
        return self._adapter.getRate()

    @rate.setter  # type: ignore
    @no_type_check
    def rate(self, value: DbusType.DOUBLE) -> None:
        self._adapter.setRate(value=value)

    @dbusProperty(name=MprisPlayerProperty.VOLUME)
    @no_type_check
    def volume(self) -> DbusType.DOUBLE:
        return self._adapter.getVolume()

    @volume.setter  # type: ignore
    @no_type_check
    def volume(self, value: DbusType.DOUBLE) -> None:
        self._adapter.setVolume(value=value)

    @dbusProperty(name=MprisPlayerProperty.METADATA, access=PropertyAccess.READ)
    @no_type_check
    def metadata(self) -> DbusType.VARIANT_DICT:
        metaData = self._adapter.getMetadata().toVariantDict()
        if metaData[MprisMetaDataField.TRACK_ID] == MprisConstant.NO_TRACK_PATH:
            raise MprisInvalidTrackException(f'Interface cannot return metadata with reserved track ID! trackId="{MprisConstant.NO_TRACK_PATH}"')

        return metaData

    @dbusProperty(name=MprisPlayerProperty.PLAYBACK_STATUS, access=PropertyAccess.READ)
    @no_type_check
    def playbackStatus(self) -> DbusType.STRING:
        return self._adapter.getPlaybackStatus().value

    @dbusProperty(name=MprisPlayerProperty.POSITION, access=PropertyAccess.READ)
    @no_type_check
    def position(self) -> DbusType.INT64:
        return int(self._adapter.getPosition())

    @dbusProperty(name=MprisPlayerProperty.LOOP_STATUS)
    @no_type_check
    def loopStatus(self) -> DbusType.STRING:
        return self._adapter.getLoopStatus().value

    @loopStatus.setter  # type: ignore
    @no_type_check
    def loopStatus(self, value: DbusType.STRING) -> None:
        self._adapter.setLoopStatus(value=MprisLoopStatus(value=value))

    @dbusProperty(name=MprisPlayerProperty.SHUFFLE)
    @no_type_check
    def shuffle(self) -> DbusType.BOOL:
        return self._adapter.isShuffle()

    @shuffle.setter  # type: ignore
    @no_type_check
    def shuffle(self, value: DbusType.BOOL) -> None:
        self._adapter.setShuffle(value=value)

    @dbusMethod(name=MprisPlayerMethod.STOP)
    @no_type_check
    def stop(self) -> None:
        self._adapter.stop()

    @dbusMethod(name=MprisPlayerMethod.PLAY)
    @no_type_check
    def play(self) -> None:
        self._adapter.play()

    @dbusMethod(name=MprisPlayerMethod.PAUSE)
    @no_type_check
    def pause(self) -> None:
        self._adapter.pause()

    @dbusMethod(name=MprisPlayerMethod.PLAY_PAUSE)
    @no_type_check
    def playPause(self) -> None:
        playbackStatus = self._adapter.getPlaybackStatus()
        if playbackStatus == MprisPlaybackStatus.PLAYING:
            self._adapter.pause()
        else:
            self._adapter.play()

    @dbusMethod(name=MprisPlayerMethod.NEXT)
    @no_type_check
    def next(self) -> None:
        self._adapter.next()

    @dbusMethod(name=MprisPlayerMethod.PREVIOUS)
    @no_type_check
    def previous(self) -> None:
        self._adapter.previous()

    @dbusMethod(name=MprisPlayerMethod.SEEK)
    @no_type_check
    def seek(self, offset: DbusType.INT64) -> None:
        position = self._adapter.getPosition() + offset
        self._adapter.seek(position=position)

    @dbusMethod(name=MprisPlayerMethod.SET_POSITION)
    @no_type_check
    def setPosition(self, trackId: DbusType.OBJECT, position: DbusType.INT64) -> None:
        DbusObjectSpec.assertValid(dbusObj=trackId)
        self._adapter.seek(position=Microseconds(position), trackId=trackId)

    @dbusMethod(name=MprisPlayerMethod.OPEN_URI)
    @no_type_check
    def openUri(self, uri: DbusType.STRING) -> None:
        self._adapter.openUri(uri=uri)

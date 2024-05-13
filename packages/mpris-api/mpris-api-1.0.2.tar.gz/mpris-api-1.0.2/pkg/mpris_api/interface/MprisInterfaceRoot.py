#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path
from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant


class MprisRootProperty:
    CAN_QUIT: str = 'CanQuit'
    CAN_RAISE: str = 'CanRaise'
    CAN_SET_FULL_SCREEN: str = 'CanSetFullscreen'
    HAS_TRACK_LIST: str = 'HasTrackList'
    FULL_SCREEN: str = 'Fullscreen'
    IDENTITY: str = 'Identity'
    DESKTOP_ENTRY: str = 'DesktopEntry'
    SUPPORTED_URI_SCHEMES: str = 'SupportedUriSchemes'
    SUPPORTED_MIME_TYPES: str = 'SupportedMimeTypes'


class MprisRootMethod:
    QUIT: str = 'Quit'
    RAISE: str = 'Raise'


class MprisInterfaceRoot(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterRoot) -> None:
        super().__init__(MprisConstant.NAME)
        self._adapter: IMprisAdapterRoot = adapter

    @dbusProperty(name=MprisRootProperty.CAN_QUIT, access=PropertyAccess.READ)
    @no_type_check
    def canQuit(self) -> DbusType.BOOL:
        return self._adapter.canQuit()

    @dbusProperty(name=MprisRootProperty.CAN_RAISE, access=PropertyAccess.READ)
    @no_type_check
    def canRaise(self) -> DbusType.BOOL:
        return self._adapter.canRaise()

    @dbusProperty(name=MprisRootProperty.CAN_SET_FULL_SCREEN, access=PropertyAccess.READ)
    @no_type_check
    def canSetFullscreen(self) -> DbusType.BOOL:
        return self._adapter.canSetFullscreen()

    @dbusProperty(name=MprisRootProperty.IDENTITY, access=PropertyAccess.READ)
    @no_type_check
    def identity(self) -> DbusType.STRING:
        return self._adapter.getIdentity()

    @dbusProperty(name=MprisRootProperty.DESKTOP_ENTRY, access=PropertyAccess.READ)
    @no_type_check
    def desktopEntry(self) -> DbusType.STRING:
        desktopEntry = self._adapter.getDesktopEntry()
        return '' if desktopEntry is None\
            else str(Path(desktopEntry).with_suffix(''))

    @dbusProperty(name=MprisRootProperty.SUPPORTED_URI_SCHEMES, access=PropertyAccess.READ)
    @no_type_check
    def supportedUriSchemes(self) -> DbusType.STRING_ARRAY:
        return self._adapter.getSupportedUriSchemes()

    @dbusProperty(name=MprisRootProperty.SUPPORTED_MIME_TYPES, access=PropertyAccess.READ)
    @no_type_check
    def supportedMimeTypes(self) -> DbusType.STRING_ARRAY:
        return self._adapter.getSupportedMimeTypes()

    @dbusProperty(name=MprisRootProperty.HAS_TRACK_LIST, access=PropertyAccess.READ)
    @no_type_check
    def hasTracklist(self) -> DbusType.BOOL:
        return self._adapter.hasTracklist()

    @dbusProperty(name=MprisRootProperty.FULL_SCREEN)
    @no_type_check
    def fullScreen(self) -> DbusType.BOOL:
        return self._adapter.isFullScreen()

    @fullScreen.setter  # type: ignore
    @no_type_check
    def fullScreen(self, value: DbusType.BOOL) -> None:
        self._adapter.setFullScreen(value=value)

    @dbusMethod(name=MprisRootMethod.QUIT)
    @no_type_check
    def quitApp(self) -> None:
        self._adapter.quitApp()

    @dbusMethod(name=MprisRootMethod.RAISE)
    @no_type_check
    def raiseApp(self) -> None:
        self._adapter.raiseApp()

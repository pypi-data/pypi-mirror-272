#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, cast

from dbus_next.service import (ServiceInterface as DbusServiceInterface)

T = TypeVar('T')


class IDbusProperty(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def __get__(self, instance: T, owner: Type[T]) -> Any: ...


class MprisInterfaceBase(DbusServiceInterface):

    def emitAll(self) -> None:
        self.emitFields()

    def emitFields(self, names: Optional[List[str]] = None) -> None:
        self._emitFields(fieldDict=self._getProperties(names=names))

    def _emitFields(self, fieldDict: Dict[str, Any]) -> None:
        self.emit_properties_changed(
            changed_properties=fieldDict,
            invalidated_properties=[]
        )

    def _getProperties(self, names: Optional[List[str]]) -> Dict[str, Any]:
        properties = cast(List[IDbusProperty], DbusServiceInterface._get_properties(self))
        return {
            prop.name: prop.__get__(self, self.__class__)
            for prop in properties
            if self._shouldGetProperty(prop=prop, names=names)
        }

    @staticmethod
    def _shouldGetProperty(prop: IDbusProperty, names: Optional[List[str]]) -> bool:
        return (
            names is None
            or prop.name in names
        )

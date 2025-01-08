# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Utility functionality.
"""
from typing import Generic, List, TypeVar

import cattrs
from arrow import Arrow
from arrow import get as arrow_get
from attrs import define, field

ISO_TIME_FORMAT = "HH:mm:ss"
ISO_TIMESTAMP_FORMAT = "YYYY-MM-DD[T]HH:mm:ssZZ"
_SERIALIZATION_FORMAT = "YYYY-MM-DD[T]HH:mm:ss.SSSSSSZZ"


class CattrConverter(cattrs.GenConverter):
    """
    Cattr converter that knows how to correctly serialize/deserialize DateTime to an ISO 8601 timestamp.
    """

    # Note: we need to use GenConverter and not Converter because we use PEP563 (postponed) annotations
    # See: https://stackoverflow.com/a/72539298/2907667 and https://github.com/python-attrs/cattrs/issues/41

    def __init__(self) -> None:
        super().__init__()
        self.register_unstructure_hook(Arrow, lambda datetime: datetime.format(_SERIALIZATION_FORMAT) if datetime else None)
        self.register_structure_hook(Arrow, lambda string, _: arrow_get(string, _SERIALIZATION_FORMAT) if string else None)


T = TypeVar("T")
"""Generic type"""


@define(slots=False)
class CircularQueue(Generic[T]):
    """A circular queue that keeps returning the original entries repeatedly, in order."""

    entries: List[T] = field()
    first: T = field()
    _working: List[T] = field()

    @first.default
    def _default_first(self) -> T:
        if not self.entries:
            raise ValueError("Entries must not be empty")
        return self.entries[0]

    # noinspection PyUnresolvedReferences
    @_working.default
    def _default_working(self) -> List[T]:
        if self.first not in self.entries:
            raise ValueError("First entry not found")
        temp = self.entries[:]
        popped = temp.pop(0)
        while popped != self.first:
            popped = temp.pop(0)
        temp.insert(0, popped)
        return temp

    def next(self) -> T:
        """Get the next entry from the queue."""
        if len(self._working) == 0:
            self._working.extend(self.entries)
        return self._working.pop(0)

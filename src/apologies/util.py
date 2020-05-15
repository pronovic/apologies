# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Utility functionality.
"""

from typing import Any, Generic, List, TypeVar

import attr
import cattr
from pendulum.datetime import DateTime
from pendulum.parser import parse


class CattrConverter(cattr.Converter):  # type: ignore
    """
    Cattr converter that knows how to correctly serialize/deserialize DateTime to an ISO 8601 timestamp.
    """

    def __init__(self) -> None:
        super().__init__()
        self.register_unstructure_hook(DateTime, lambda datetime: datetime.isoformat() if datetime else None)
        self.register_structure_hook(DateTime, lambda string, _: parse(string) if string else None)


T = TypeVar("T")  # pylint: disable=invalid-name
"""Generic type"""


@attr.s
class CircularQueue(Generic[T]):
    """A circular queue that keeps returning the original entries repeatedly, in order."""

    entries = attr.ib(type=List[T])
    first = attr.ib(type=Any)
    _working = attr.ib(type=List[T])

    @first.default
    def _default_first(self) -> Any:
        return None if not self.entries else self.entries[0]

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

    @entries.validator
    def _check_entries(self, _attribute: str, value: int) -> None:
        if not value:
            raise ValueError("Entries must not be empty")

    def next(self) -> T:
        """Get the next entry from the queue."""
        if len(self._working) == 0:
            self._working.extend(self.entries)
        return self._working.pop(0)

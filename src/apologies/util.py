# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Utility functionality.
"""

from typing import Generic, List, TypeVar

import attr

Type = TypeVar("Type")


@attr.s
class CircularQueue(Generic[Type]):
    """A circular queue, that keeps returning the original entries repeatedly, in order."""

    entries = attr.ib(type=List[Type])
    _working = attr.ib(type=List[Type])

    @_working.default
    def _init_working(self) -> List[Type]:
        return self.entries[:]

    @entries.validator
    def _check_entries(self, attribute: str, value: int) -> None:
        if not value:
            raise ValueError("Entries must not be empty")

    def next(self) -> Type:
        """Get the next entry from the queue."""
        if len(self._working) == 0:
            self._working.extend(self.entries)
        return self._working.pop(0)

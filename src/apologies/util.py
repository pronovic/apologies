# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Utility functionality.
"""

from typing import List, Any
import attr


@attr.s
class CircularQueue:
    """A circular queue, that keeps returnin the original entries repeatedly, in order."""

    _entries = attr.ib(type=List[Any])
    _working = attr.ib(init=False, default=None, type=List[Any])

    @_entries.validator
    def _check_entries(self, attribute: str, value: int) -> None:
        if not value:
            raise ValueError("Entries must not be empty")

    def next(self) -> Any:
        """Get the next entry from the queue."""
        if not self._working:
            self._working = self._entries[:]
        return self._working.pop(0)

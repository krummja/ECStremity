from __future__ import annotations
from typing import Any, Dict, Optional


class EntityEvent:

    def __init__(self, name: str, data: Optional[Dict[str, Any]] = None):
        self.name = name
        if data is None:
            self.data = {}
        else:
            self.data = data

        self._prevented: bool = False
        self._handled: bool = False

    @property
    def prevented(self) -> bool:
        """`prevented` property"""
        return self._prevented

    @property
    def handled(self) -> bool:
        """`handled` property"""
        return self._handled

    def handle(self) -> None:
        """Callback for `_handled` and `_prevented` attributes."""
        self._handled = True
        self._prevented = True

    def prevent(self) -> None:
        """Callback for `_prevented` attribute."""
        self._prevented = True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EntityEvent):
            return self.name == other.name

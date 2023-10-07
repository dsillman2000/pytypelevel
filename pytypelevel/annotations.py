import inspect
from typing import Any, Protocol, Self, runtime_checkable


@runtime_checkable
class SupportsEq(Protocol):
    def __eq__(self, __other: Self) -> bool:
        ...
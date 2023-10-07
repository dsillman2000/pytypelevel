from typing import Protocol, Self


class SupportsEq(Protocol):
    def __eq__(self, __other: Self) -> bool:
        ...
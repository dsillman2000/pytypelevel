from typing import Callable, Generic, Iterable, Optional, TypeVar

from pytypelevel.kernel.order import Order
from pytypelevel.kernel.partial_order import PartialOrder

T = TypeVar('T')


class PartialNext(Generic[T]):

    _partial_order: PartialOrder[T]
    _partial_next: Callable[[T], Optional[T]]

    def __init__(
        self, 
        __partial_next: Callable[[T], Optional[T]], 
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        self._partial_order = __partial_order
        self._partial_next = __partial_next

    def partial_order(self) -> PartialOrder[T]:
        return self._partial_order
    
    def partial_next(self, __t: T) -> Optional[T]:
        return self._partial_next(__t)
    

class Next(Generic[T], PartialNext[T]):

    _next: Callable[[T], T]

    def __init__(
        self,
        __next: Callable[[T], T],
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        super().__init__(__next, __partial_order)
        self._next = __next

    def next(self, __t: T) -> T:
        return self._next(__t)


class PartialPrevious(Generic[T]):

    _partial_order: PartialOrder[T]
    _partial_previous: Callable[[T], Optional[T]]

    def __init__(
        self,
        __partial_previous: Callable[[T], Optional[T]],
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        self._partial_order = __partial_order
        self._partial_previous = __partial_previous

    def partial_order(self) -> PartialOrder[T]:
        return self._partial_order
    
    def partial_previous(self, __t: T) -> Optional[T]:
        return self._partial_previous(__t)

class Previous(Generic[T], PartialPrevious[T]):

    _previous: Callable[[T], T]

    def __init__(
        self,
        __previous: Callable[[T], T],
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        super().__init__(__previous, __partial_order)
        self._previous = __previous

    def previous(self, __t: T) -> T:
        return self._previous(__t)
    
class UnboundedEnumerable(Generic[T], Next[T], Previous[T]):
    
    _order: Order[T]

    def __init__(
        self,
        __next: Callable[[T], T],
        __previous: Callable[[T], T],
        __order: Order[T] = Order[T](),
    ):
        self._partial_next = self._next = __next
        self._partial_previous = self._previous = __previous
        self._order = __order
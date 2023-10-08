from typing import Callable, Generator, Generic, Iterable, Optional, TypeVar

from pytypelevel.kernel.order import Order
from pytypelevel.kernel.partial_order import PartialOrder

T = TypeVar('T')

class LowerBounded(Generic[T]):

    _partial_order: PartialOrder[T]
    _min_bound: T

    def __init__(self, __min_bound: T, __partial_order: PartialOrder[T] = PartialOrder[T]()):
        self._min_bound = __min_bound
        self._partial_order = __partial_order

    def min_bound(self) -> T:
        return self._min_bound
    
    def partial_order(self) -> PartialOrder[T]:
        return self._partial_order

class UpperBounded(Generic[T]):

    _partial_order: PartialOrder[T]
    _max_bound: T

    def __init__(self, __max_bound: T, __partial_order: PartialOrder[T] = PartialOrder[T]()):
        self._max_bound = __max_bound
        self._partial_order = __partial_order

    def max_bound(self) -> T:
        return self._max_bound
    
    def partial_order(self) -> PartialOrder[T]:
        return self._partial_order


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
    
class PartialNextLowerBounded(Generic[T], PartialNext[T], LowerBounded[T]):

    def __init__(
        self, 
        __partial_next: Callable[[T], Optional[T]],
        __min_bound: T, 
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        PartialNext.__init__(self, __partial_next, __partial_order)
        LowerBounded.__init__(self, __min_bound, __partial_order)

    def members_ascending(self) -> Generator[T, None, None]:

        nxt = self.min_bound()

        while nxt is not None:
            yield nxt
            nxt = self.partial_next(nxt)
            

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
    
class PartialPreviousUpperBounded(Generic[T], PartialPrevious[T], UpperBounded[T]):

    def __init__(
        self, 
        __partial_previous: Callable[[T], Optional[T]],
        __max_bound: T, 
        __partial_order: PartialOrder[T] = PartialOrder[T](),
    ):
        PartialPrevious.__init__(self, __partial_previous, __partial_order)
        UpperBounded.__init__(self, __max_bound, __partial_order)

    def members_descending(self) -> Generator[T, None, None]:

        prv = self.max_bound()

        while prv is not None:
            yield prv
            prv = self.partial_previous(prv)


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

class BoundedEnumerable(Generic[T], PartialNextLowerBounded[T], PartialPreviousUpperBounded[T]):

    def __init__(
        self,
        __partial_next: Callable[[T], Optional[T]],
        __partial_previous: Callable[[T], Optional[T]],
        __min_bound: T,
        __max_bound: T,
        __order: Order[T] = Order[T](),
    ):
        PartialNextLowerBounded.__init__(self, __partial_next, __min_bound, __order)
        PartialPreviousUpperBounded.__init__(self, __partial_previous, __max_bound, __order)

    def cycle_next(self, __t: T) -> T:
        nxt: Optional[T] = self.partial_next(__t)
        return self.min_bound() if nxt is None else nxt

    def cycle_previous(self, __t: T) -> T:
        prv: Optional[T] = self.partial_previous(__t)
        return self.max_bound() if prv is None else prv
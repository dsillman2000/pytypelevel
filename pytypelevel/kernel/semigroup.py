import abc
import types
from functools import reduce
from itertools import repeat
from typing import (
    Annotated,
    Callable,
    Generic,
    Iterable,
    Optional,
    Protocol,
    SupportsInt,
    Type,
    TypeVar,
)

from annotated_types import Gt

from pytypelevel.typeclasses import TypeclassMeta

T = TypeVar('T')

class Semigroup(Generic[T], TypeclassMeta):

    @classmethod
    @abc.abstractmethod
    def combine(cls, a: T, b: T) -> T:
        ...

    @classmethod
    def combine_n(cls, a: T, n: Annotated[int, Gt(0)]) -> T:
        return reduce(cls.combine, repeat(a, (n - 1)), a)
    
    @classmethod
    def combine_all_option(cls, a_values: Iterable[T]) -> Optional[T]:
        try:
            return reduce(cls.combine, a_values)
        except TypeError:
            return None
        
    @classmethod
    def reverse(cls) -> "Type[Semigroup[T]]":
        __combine = cls.combine
        return Semigroup[T].instance(combine = lambda a, b: __combine(b, a))

def semigroup(__combine: Callable[[T, T], T]) -> Type[Semigroup[T]]:
    
    return Semigroup[T].instance(combine = __combine)

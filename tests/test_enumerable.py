from pytypelevel import BoundedEnumerable, UnboundedEnumerable
from pytypelevel.kernel.enumerable import (
    LowerBounded,
    Next,
    PartialNext,
    PartialNextLowerBounded,
    PartialPrevious,
    PartialPreviousUpperBounded,
    Previous,
    UpperBounded,
)


def test_semi_bounded_instances__sgnint():
    
    posint = LowerBounded[int](0)
    assert posint.min_bound() == 0 and posint.partial_order().lt(1, 2)
    del posint
    posint = PartialNextLowerBounded[int](lambda u: u + 1 if u < 10 else None, 0)
    assert posint.partial_next(8) == 9 and posint.partial_next(10) is None
    assert list(posint.members_ascending()) == list(range(0, 11, 1))

    negint = UpperBounded[int](0)
    assert negint.max_bound() == 0 and negint.partial_order().lt(-2, -1)
    del negint
    negint = PartialPreviousUpperBounded[int](lambda u: u - 1 if u > -10 else None, 0)
    assert negint.partial_previous(-8) == -9 and negint.partial_previous(-10) is None
    assert list(negint.members_descending()) == list(range(0, -11, -1))


def test_next_instances__int():

    ascint = PartialNext[int](lambda u: u + 1)
    assert ascint.partial_next(2) == 3
    
    decint = Next[int](lambda u: u - 1)
    assert decint.partial_next(0) == decint.next(0) == -1

def test_prev_instances__int():

    ascint = PartialPrevious[int](lambda u: u - 1)
    assert ascint.partial_previous(7) == 6

    decint = Previous[int](lambda u: u + 1)
    assert decint.partial_previous(0) == decint.previous(0) == 1

def test_enumerable_instances__int():

    ascint = UnboundedEnumerable[int](lambda u: u + 1, lambda v: v - 1)

    for i in range(10):
        assert ascint.next(i) == ascint.partial_next(i) == i + 1
        assert ascint.previous(i) == ascint.partial_previous(i) == i - 1

    digits = BoundedEnumerable[int](
        lambda u: u + 1 if u < 9 else None, 
        lambda v: v - 1 if v > 0 else None,
        0, 9
    )

    assert ''.join(map(str, digits.members_ascending())) == '0123456789'
    assert ''.join(map(str, digits.members_descending())) == '9876543210'

    assert digits.cycle_next(8) == 9 and digits.cycle_next(9) == 0
    assert digits.cycle_previous(1) == 0 and digits.cycle_previous(0) == 9
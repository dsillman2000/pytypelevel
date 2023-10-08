from pytypelevel import UnboundedEnumerable
from pytypelevel.kernel.enumerable import Next, PartialNext, PartialPrevious, Previous


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
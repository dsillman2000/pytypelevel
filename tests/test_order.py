import operator

from pytypelevel import Order

from .conftest import Pair


def test_order_instances__intord():

    intord = Order[int]()

    assert intord.compare(2, 3) == intord.partial_compare(2, 3) == -1 \
           and intord.compare(4, 4) == intord.partial_compare(4, 4) == 0 \
           and intord.compare(-7, -14) == intord.partial_compare(-7, -14) == 1
    assert intord.min(2, 9) == 2
    assert intord.max(2, 8) == intord.pmax(2, 8) == 8
    assert intord.eqv(7, 7) and intord.neqv(-7, 7)
    assert intord.lt(-1, 1) and intord.lteqv(-1, 1)
    assert intord.gt(1, -1) and intord.gteqv(1, -1)

def test_order_instances__tupsize():

    tupsize: Order[tuple[int, ...]] = Order[int]().by(len)

    assert tupsize.eqv((3, 3, 3), (12, 2, 4))
    assert tupsize.gt((7, 2), (1,)) and tupsize.lt((1,), (7, 2))

    rev_tupsize = tupsize.reverse()

    assert rev_tupsize.lt((7, 2), (1,)) and rev_tupsize.gt((1,), (7, 2))

def test_order_instances__pairs():

    fstord: Order[Pair] = Order[Pair]().by(operator.itemgetter(0))
    sndord: Order[Pair] = Order[Pair]().by(operator.itemgetter(1))
    lexord = Order[Pair].when_equal(fstord, sndord)

    assert lexord.lt((1, 2), (2, 2)) and lexord.lt((1, 2), (1, 3))

    lexord2 = Order[Pair].from_le(operator.le)
    assert lexord2.lt((1, 2), (2, 2)) and lexord2.lt((1, 2), (1, 12))


def test_order_instances__bindigits():

    bin_le = lambda s1, s2: s1.lstrip('0') <= s2.lstrip('0')
    bin_len = lambda s1, s2: len(s1.lstrip('0')) <= len(s2.lstrip('0'))
    bin_num1 = lambda s1, s2: s1.count('1') <= s2.count('1')

    bin_ord = Order[str] \
        .when_equal_monoid() \
        .combine_all([
            Order[str].from_le(bin_num1), 
            Order[str].from_le(bin_len), 
            Order[str].from_le(bin_le)
        ])

    assert bin_ord.eqv('1', '001') and bin_ord.lt('101', '1101')
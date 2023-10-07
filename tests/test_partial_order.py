import math
import operator

from pytypelevel import PartialOrder


def test_partial_order_instances__strord():

    strord = PartialOrder[str]()

    assert strord.partial_compare('a', 'b') == -1.0
    assert strord.partial_compare('z', 'a') == 1.0
    assert strord.eqv('a', 'a') and strord.partial_compare('a', 'a') == 0.0
    assert strord.neqv('u', 'v') and strord.partial_compare('u', 'v') == -1.0
    assert strord.try_compare('u', 'v') == -1 and \
           strord.try_compare('v', 'u') == 1
    
    assert strord.pmin('abc', 'def') == 'abc'
    assert strord.pmin('uuu', 'uuu') is None
    assert strord.pmax('abc', 'def') == 'def'
    assert strord.pmax('vvv', 'vvv') is None

    last_letter = PartialOrder[str]().by(operator.itemgetter(-1))
    assert last_letter.pmin('abc', 'def') == 'abc'
    assert last_letter.pmax('abz', 'def') == 'abz'

    assert strord.reverse().pmin('a', 'z') == 'z'

def test_partial_order_instances__str_elementwise():

    def _str_elementwise(str1: str, str2: str) -> float:
        if len(str1) != len(str2):
            return float('nan')
        for c1, c2 in zip(reversed(str1), reversed(str2)):
            if c1 > c2:
                return 1.0
            elif c1 < c2:
                return -1.0
        return 0.0

    str_elementwise = PartialOrder[str](_str_elementwise)

    assert str_elementwise.partial_compare('uvi', 'uvi') == 0.0 \
           and str_elementwise.partial_compare('uvi', 'uvw') == -1.0 \
           and math.isnan(str_elementwise.partial_compare('u', 'uvw'))
    assert str_elementwise.eqv('uni', 'uni') and \
           str_elementwise.neqv('uni', 'unv') and \
           str_elementwise.neqv('uni', 'u')
    assert str_elementwise.try_compare('uni', 'uni') == 0 and \
           str_elementwise.try_compare('u', 'uv') is None
    
    assert str_elementwise.pmin('uva', 'uvb') == 'uva'
    assert str_elementwise.pmin('uv', 'uva') is None

    assert str_elementwise.reverse().pmax('abc', 'abe') == 'abc'
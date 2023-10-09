import operator

from pytypelevel import Band


def test_band_instances__dictmerge():

    dictmerge = Band[dict](operator.ior)

    assert dictmerge.combine({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
    assert dictmerge.combine({'a': 0}, {'a': 0}) == {'a': 0}

    assert dictmerge.combine_n({'x': 3}, int(1e27)) == {'x': 3}


def test_band_instances__maxagg():

    maxagg = Band[int](max)

    assert maxagg.combine(2, 4) == maxagg.combine(4, 4) == 4
    assert maxagg.combine_n(20, int(1e27)) == 20
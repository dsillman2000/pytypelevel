from pytypelevel import Group


def test_group_instances__strdigits():

    strdigits = Group[str](
        lambda s1, s2: str((int(s1) + int(s2)) % 10),
        '0', lambda s: str(10 - int(s))
    )

    assert strdigits.combine('3', '7') == strdigits.empty
    assert strdigits.combine('4', '5') == strdigits.remove('0', '1')
    assert strdigits.inverse('5') == '5'
    assert strdigits.combine_n('3', 78) == '4'
    assert strdigits.combine_n('3', -78) == '6'
    assert strdigits.combine_n('9', 0) == '0'

def test_group_instances__charset():

    charset = Group[str](
        lambda a, b: ''.join([ i for i in (a + b) if (i in a) ^ (i in b) ]),
        '', lambda c: c
    )

    assert charset.combine('abc', 'cde') == 'abde'
    assert charset.combine_n('uv', 2) == charset.empty and \
           charset.combine_n('uv', 3) == 'uv'
    assert charset.combine_all(['lit', 'uzi', 'vert']) == 'luzver'

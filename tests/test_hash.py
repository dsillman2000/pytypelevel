from pytypelevel import Hash


def test_hash_instances__str():
    
    h = Hash[str]()

    assert h.eqv('complex string', 'complex string')
    assert h.neqv('cimplex string', 'complex string')
    
    permutation: Hash[str] = Hash[str]().by(lambda s: ''.join(sorted(s)))

    assert permutation.neqv('ample', 'good')
    assert permutation.eqv('sample', 'maples')

def test_hash_instances__sqint():

    sqint = Hash[int](lambda u: u * u)

    assert sqint.eqv(32, -32)
    assert sqint.neqv(31, 32)
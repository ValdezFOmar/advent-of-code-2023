from .challenge import ilen


def test_output():
    iterable = (i for i in range(10))
    assert ilen(iterable) == 10

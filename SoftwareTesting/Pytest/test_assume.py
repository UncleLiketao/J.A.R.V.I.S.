import pytest

@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_assume(x, y):
    pytest.assume(x == y)
    pytest.assume(3 == 4)
    pytest.assume(5 == 9)

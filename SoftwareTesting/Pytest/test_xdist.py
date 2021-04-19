import pytest
import time

@pytest.mark.parametrize('x',list(range(10)))
def test_somethins(x):
    time.sleep(1)

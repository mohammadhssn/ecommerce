import pytest


@pytest.mark.core
def test_hello_world3(test_fixture1):
    print('hello 333333333333')
    assert test_fixture1 == 1

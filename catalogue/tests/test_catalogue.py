import pytest


def test_hello_world(test_fixture1):
    print('hello world')
    assert test_fixture1 == 1


def test_hello_world2(test_fixture1):
    print('hello world 222222')
    assert test_fixture1 == 1

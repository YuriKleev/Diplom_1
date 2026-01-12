import pytest

from praktikum.burger import Burger


@pytest.fixture(scope='function')
def burger():
    burger = Burger()
    return burger

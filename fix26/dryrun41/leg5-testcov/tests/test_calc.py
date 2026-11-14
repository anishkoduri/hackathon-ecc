from src.calc import add, sub, div, clamp

def test_add():
    assert add(2, 3) == 5

def test_sub():
    assert sub(5, 3) == 2

def test_div():
    assert div(6, 3) == 2

def test_div_zero():
    import pytest
    with pytest.raises(ValueError):
        div(1, 0)

def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0

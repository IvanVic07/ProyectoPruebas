# test_main.py
import pytest
from src.main import sumar, restar

def test_sumar():
    """Prueba para la función de sumar."""
    assert sumar(3, 5) == 8
    assert sumar(-2, 3) == 1
    assert sumar(0, 0) == 0

def test_restar():
    """Prueba para la función de restar."""
    assert restar(10, 5) == 5
    assert restar(0, 0) == 0
    assert restar(-2, 3) == -5


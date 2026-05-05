import pytest
from src.sport import Sport


def test_init():
    s = Sport("football")
    assert s.nom == "football"


def test_str():
    s = Sport("basketball")
    assert str(s) == "basketball"


def test_type_invalide_leve_type_error():
    with pytest.raises(TypeError):
        Sport(42)


def test_type_invalide_liste():
    with pytest.raises(TypeError):
        Sport(["football"])

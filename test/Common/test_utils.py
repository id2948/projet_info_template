from src.Common.utils import parse_boolean


def test_lowercase_string_is_properly_inferred():
    assert parse_boolean("true")
    assert not parse_boolean("false")


def test_vrai_est_reconnu():
    assert parse_boolean("vrai")


def test_bool_directement():
    assert parse_boolean(True)
    assert not parse_boolean(False)

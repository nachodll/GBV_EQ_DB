from utils.normalization import normalize_month, normalize_provincia


def test_normalize_month_basic():
    assert normalize_month("Enero") == 1


def test_normalize_month_spaces():
    assert normalize_month("  Abril ") == 4


def test_normalize_month_case():
    assert normalize_month("octubre") == 10


def test_normalize_month_invalid():
    assert normalize_month("Foo") is None


def test_normalize_provincia_basic():
    assert normalize_provincia("Burgos") == 9


def test_normalize_provincia_accent_and_case():
    assert normalize_provincia("alava") == 1


def test_normalize_provincia_spaces_case():
    assert normalize_provincia(" LAS PALMAS ") == 35


def test_normalize_provincia_invalid():
    assert normalize_provincia("Unknown") is None

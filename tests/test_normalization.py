from utils.normalization import normalize_age_group, normalize_month, normalize_provincia


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


def test_normalize_age_group_basic_range():
    assert normalize_age_group("21-30 años") == "21-30"
    assert normalize_age_group("71-84 años") == "71-84"


def test_normalize_age_group_with_spaces_and_case():
    assert normalize_age_group("  41-50 AÑOS ") == "41-50"
    assert normalize_age_group("51 - 60 años") == "51-60"


def test_normalize_age_group_no_consta():
    assert normalize_age_group("No consta") is None
    assert normalize_age_group(" no CONSTA ") is None


def test_normalize_age_group_less_than():
    assert normalize_age_group("<16 años") == "<16"


def test_normalize_age_group_greater_than():
    assert normalize_age_group(">84 años") == ">84"


def test_normalize_age_group_short_range():
    assert normalize_age_group("16-17 años") == "16-17"
    assert normalize_age_group("18-20 años") == "18-20"


def test_normalize_age_group_invalid_format():
    assert normalize_age_group("edad desconocida") is None
    assert normalize_age_group("") is None

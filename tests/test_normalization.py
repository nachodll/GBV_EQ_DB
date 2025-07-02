import pandas as pd
import pytest

from utils.normalization import (
    NormalizationStatus,
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_comunidad_autonoma,
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_quarter,
    normalize_year,
)


# ---------------------- provincia normalization ----------------------
def test_normalize_provincia_basic():
    result = normalize_provincia("Burgos")
    assert result.value == 9
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_accent_and_case():
    result = normalize_provincia("alAvá")
    assert result.value == 1
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_spaces_case():
    result = normalize_provincia(" LAS PALMAS ")
    assert result.value == 35
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_unknown():
    result = normalize_provincia("Desconocida")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_provincia_invalid():
    result = normalize_provincia("Atlantis")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- comunidad autonoma normalization ----------------------
def test_normalize_comunidad_autonoma_basic():
    result = normalize_comunidad_autonoma("Andalucía")
    assert result.value == 1
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_accent_and_case():
    result = normalize_comunidad_autonoma("mAdríd")
    assert result.value == 13
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_spaces_case():
    result = normalize_comunidad_autonoma(" PRINCIPADO DE  ASTURIAS ")
    assert result.value == 3
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_unknown():
    result = normalize_comunidad_autonoma("Desconocida")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_comunidad_autonoma_invalid():
    result = normalize_comunidad_autonoma("Gibraltar")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- month normalization ----------------------
def test_normalize_month_basic():
    result = normalize_month("Enero")
    assert result.value == 1
    assert result.status is NormalizationStatus.VALID


def test_normalize_month_spaces():
    result = normalize_month("  Febrero  ")
    assert result.value == 2
    assert result.status is NormalizationStatus.VALID


def test_normalize_month_case():
    result = normalize_month("mArzo")
    assert result.value == 3
    assert result.status is NormalizationStatus.VALID


def test_normalize_month_unknown():
    result = normalize_month("no consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_month_invalid():
    result = normalize_month("Foo")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- quarter normalization ----------------------
def test_normalize_quarter_basic():
    r1 = normalize_quarter("Primero")
    r2 = normalize_quarter(1)
    r3 = normalize_quarter("1")
    assert r1.value == 1 and r2.value == 1 and r3.value == 1
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def test_normalize_quarter_out_of_bound():
    r1 = normalize_quarter("Quinto")
    r2 = normalize_quarter(5)
    r3 = normalize_quarter("5")
    assert r1.value is None and r2.value is None and r3.value is None
    assert r1.status is r2.status is r3.status is NormalizationStatus.INVALID


def normalize_quarter_unknown():
    result = normalize_quarter("No consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_quarter_invalid():
    result = normalize_quarter("Foo")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- year normalization ----------------------
def test_normalize_year_basic_and_string():
    r1 = normalize_year(2021)
    r2 = normalize_year("2022")
    assert r1.value == 2021 and r2.value == 2022
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_year_with_text():
    r1 = normalize_year("Año 2020")
    r2 = normalize_year("2020 año")
    r3 = normalize_year("2020 a")
    assert r1.value == 2020 and r2.value == 2020 and r3.value == 2020
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def test_normalize_year_unknown():
    result = normalize_year("No consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_year_out_of_bound():
    r1 = normalize_year(1800)
    r2 = normalize_year(2200)
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.INVALID


def test_normalize_year_invalid():
    result = normalize_year("202a3")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- age group normalization ----------------------
def test_normalize_age_group_basic_range():
    r1 = normalize_age_group("21-30 años")
    r2 = normalize_age_group("71-84 años")
    assert r1.value == "21-30"
    assert r2.value == "71-84"
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_age_group_spaces_case():
    r1 = normalize_age_group("  41-50 AÑOS ")
    r2 = normalize_age_group("51 - 60 años")
    assert r1.value == "41-50"
    assert r2.value == "51-60"
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_age_group_less_than_greater_than():
    r1 = normalize_age_group("<16 años")
    r2 = normalize_age_group(">84 años")
    assert r1.value == "<16"
    assert r2.value == ">84"
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_age_group_unknown():
    r1 = normalize_age_group("No consta")
    r2 = normalize_age_group(" no CONSTA ")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.UNKNOWN


def test_normalize_age_group_invalid():
    result = normalize_age_group("edad")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- positive integer normalization ----------------------
def test_normalize_positive_integer_basic():
    r1 = normalize_positive_integer(42)
    r2 = normalize_positive_integer(" 12 ")
    assert r1.value == 42 and r2.value == 12
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_positive_integer_unknown():
    r1 = normalize_positive_integer("n/c")
    r2 = normalize_positive_integer(" no CONSTA ")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.UNKNOWN


def test_normalize_positive_integer_invalid():
    r1 = normalize_positive_integer(-5)
    r2 = normalize_positive_integer("foo")
    r3 = normalize_positive_integer("12.34")
    assert r1.status is NormalizationStatus.INVALID
    assert r2.status is NormalizationStatus.INVALID
    assert r3.status is NormalizationStatus.INVALID


# ---------------------- apply_and_check helpers ----------------------
def test_apply_and_check_basic():
    serie = pd.Series(["Enero", "Febrero"])
    result = apply_and_check(serie, normalize_month)  # type: ignore
    assert list(result) == [1, 2]  # type: ignore


def test_apply_and_check_invalid():
    serie = pd.Series(["Enero", "Foo"])
    with pytest.raises(ValueError):
        apply_and_check(serie, normalize_month)


def test_apply_and_check_dict_basic():
    serie = pd.Series(["2021", "2022"])
    result = apply_and_check(serie, normalize_year)  # type: ignore
    assert list(result) == [2021, 2022]  # type: ignore


def test_apply_and_check_dict_invalid():
    ser = pd.Series(["a", "b", "c"])
    mapping = {"a": 1, "b": 2}
    with pytest.raises(ValueError):
        apply_and_check_dict(ser, mapping)

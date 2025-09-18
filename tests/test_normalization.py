import pandas as pd
import pytest

from utils.normalization import (
    NormalizationStatus,
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_json_string,
    normalize_month,
    normalize_municipio,
    normalize_municipio_id,
    normalize_nationality,
    normalize_plain_text,
    normalize_positive_float,
    normalize_positive_integer,
    normalize_provincia,
    normalize_quarter,
    normalize_year,
)


# ---------------------- municipio normalization ----------------------
def test_normalize_municipio_basic():
    r1 = normalize_municipio(("Asparrena", "Álava"))
    r2 = normalize_municipio(("Portaje", 10))
    assert r1.value == 1009 and r2.value == 10150
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_municipio_accent_and_case():
    result = normalize_municipio(("aRmiñon", "alAva"))
    assert result.value == 1006
    assert result.status is NormalizationStatus.VALID


def test_normalize_municipio_spaces_case():
    result = normalize_municipio(("  ChinchiLLa   de Monte-Aragón", "Albacete"))
    assert result.value == 2029
    assert result.status is NormalizationStatus.VALID


def test_normalize_municipio_commma():
    r1 = normalize_municipio(("Gineta, La", "Albacete"))
    r2 = normalize_municipio(("Gineta", "Albacete"))
    r3 = normalize_municipio(("Gineta (La)", "Albacete"))
    expeted_value = 2035
    assert r1.value == expeted_value and r2.value == expeted_value and r3.value == expeted_value
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


def test_normalize_municipio_slash():
    r1 = normalize_municipio(("Elx/Elche", "Alicante"))
    r2 = normalize_municipio(("Elx", "Alicante"))
    r3 = normalize_municipio(("Elche", "Alicante"))
    expected_value = 3065
    assert r1.value == expected_value and r2.value == expected_value and r3.value == expected_value
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


def test_normalize_municipio_slash_and_commma():
    r1 = normalize_municipio(("Alqueries, les/Alquerías del Niño Perdido", "Castellón"))
    r2 = normalize_municipio(("Alqueries, les", "Castellón"))
    r3 = normalize_municipio(("Alquerías del Niño Perdido", "Castellón"))
    expected_value = 12901
    assert r1.value == expected_value and r2.value == expected_value and r3.value == expected_value
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


def test_normalize_municipio_same_name_different_province():
    r1 = normalize_municipio(("Rebollar", "Cáceres"))
    r2 = normalize_municipio(("Rebollar", "Soria"))
    assert r1.value == 10154 and r2.value == 42151
    assert r1.status is NormalizationStatus.VALID and r2.status is NormalizationStatus.VALID


def test_normalize_municipio_unknown():
    result = normalize_municipio(("Desconocida", "Alava"))
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_municipio_invalid():
    r1 = normalize_municipio(("Andromeda", "Málaga"))
    r2 = normalize_municipio(("Famorca", "Venus"))
    assert r1.value is r2.value is None
    assert r1.status is r2.status is NormalizationStatus.INVALID


def test_normalize_municipio_id_basic():
    r1 = normalize_municipio_id("41009")
    r2 = normalize_municipio_id(10150)
    assert r1.value == 41009 and r2.value == 10150
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_municipio_id_invalid():
    r1 = normalize_municipio_id("100")
    r2 = normalize_municipio_id(123456)
    r3 = normalize_municipio_id(36080)  # This is a valid id but is does not exist
    assert r1.value is None and r2.value is None and r3.value is None
    assert r1.status is r2.status is r3.status is NormalizationStatus.INVALID


# ---------------------- provincia normalization ----------------------
def test_normalize_provincia_basic():
    result = normalize_provincia("Burgos")
    assert result.value == 9
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_with_number():
    result = normalize_provincia("01 Álava")
    assert result.value == 1
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_accent_and_case():
    result = normalize_provincia("alAvá")
    assert result.value == 1
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_spaces_case():
    result = normalize_provincia(" LAS PALMAS ")
    assert result.value == 35
    assert result.status is NormalizationStatus.VALID


def test_normalize_provincia_commma():
    r1 = normalize_provincia("Balears, Illes")
    r2 = normalize_provincia("Balears")
    r3 = normalize_provincia("Balears (Illes)")
    assert r1.value == 7 and r2.value == 7 and r3.value == 7
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


def test_normalize_provincia_slash():
    r1 = normalize_provincia("Araba/Álava")
    r2 = normalize_provincia("Álava")
    r3 = normalize_provincia("Araba")
    assert r1.value == 1 and r2.value == 1 and r3.value == 1
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


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


def test_normalize_comunidad_autonoma_with_number():
    result = normalize_comunidad_autonoma("03 Asturias")
    assert result.value == 3
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_accent_and_case():
    result = normalize_comunidad_autonoma("mAdríd")
    assert result.value == 13
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_spaces_case():
    result = normalize_comunidad_autonoma(" PRINCIPADO DE  ASTURIAS ")
    assert result.value == 3
    assert result.status is NormalizationStatus.VALID


def test_normalize_comunidad_autonoma_commma():
    r1 = normalize_comunidad_autonoma("Navarra, Comunidad Foral de")
    r2 = normalize_comunidad_autonoma("Navarra")
    r3 = normalize_comunidad_autonoma("Navarra (Comunidad Foral de)")
    assert r1.value == 15 and r2.value == 15 and r3.value == 15
    assert (
        r1.status is NormalizationStatus.VALID
        and r2.status is NormalizationStatus.VALID
        and r3.status is NormalizationStatus.VALID
    )


def test_normalize_comunidad_autonoma_unknown():
    result = normalize_comunidad_autonoma("Desconocida")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_comunidad_autonoma_invalid():
    result = normalize_comunidad_autonoma("Gibraltar")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


# ---------------------- nationality normalization ----------------------
def test_normalize_nationality_basic():
    r1 = normalize_nationality("Alemania")
    r2 = normalize_nationality("Aleman")
    r3 = normalize_nationality("Alemana")
    assert r1.value == "Alemania" and r2.value == "Alemania" and r3.value == "Alemania"
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def tesst_normalize_nationality_spaces_case():
    r1 = normalize_nationality("  aRgentina  ")
    r2 = normalize_nationality("  braSileña  ")
    assert r1.value == "Argentina" and r2.value == "Brasil"
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_nationality_accent():
    r1 = normalize_nationality("México")
    r2 = normalize_nationality("méxicana")
    assert r1.value == "México" and r2.value == "México"
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_nationality_plural():
    r1 = normalize_nationality("irlandeses")
    r2 = normalize_nationality("extranjeros")
    r3 = normalize_nationality("españoles")
    assert r1.value == "Irlanda" and r2.value == "Otros" and r3.value == "España"
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def test_normalize_nationality_unknown():
    result = normalize_nationality("No consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_nationality_invalid():
    r1 = normalize_nationality("Gibraltar")
    r2 = normalize_nationality("Foo")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.INVALID


# ---------------------- date normalization ----------------------
def test_normalize_date_basic():
    r1 = normalize_date("01/01/2020")
    r2 = normalize_date("2020-01-01")
    r3 = normalize_date("01-01-2020")
    assert (
        r1.value == pd.Timestamp("2020-01-01")
        and r2.value == pd.Timestamp("2020-01-01")
        and r3.value == pd.Timestamp("2020-01-01")
    )
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def normalize_date_unknown():
    result = normalize_date("No consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_date_invalid():
    r1 = normalize_date("01/01/20a0")
    r2 = normalize_date("2020-13-01")
    r3 = normalize_date("2020-01-32")
    assert r1.value is None and r2.value is None and r3.value is None
    assert r1.status is r2.status is r3.status is NormalizationStatus.INVALID


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


def test_normalize_age_group_single_age():
    r1 = normalize_age_group("19 años")
    r2 = normalize_age_group("  0  años ")
    assert r1.value == "19"
    assert r2.value == "0"
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


def test_normalize_age_group_special_cases():
    r1 = normalize_age_group("De 0 a 15 años")
    r2 = normalize_age_group("De 16 a 64 años")
    r3 = normalize_age_group("De 65 y más años")
    assert r1.value == "<15" and r2.value == "16-64" and r3.value == ">65"
    assert r1.status is r2.status is r3.status is NormalizationStatus.VALID


def test_normalize_greater_than_special_cases():
    r1 = normalize_age_group("100 años y más")
    assert r1.value == ">100"
    assert r1.status is NormalizationStatus.VALID


def test_normalize_age_group_unknown():
    r1 = normalize_age_group("No consta")
    r2 = normalize_age_group(" no CONSTA ")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.UNKNOWN


def test_normalize_age_group_invalid_range():
    r1 = normalize_age_group("30-21 años")
    r2 = normalize_age_group("De 16 a 15 años")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.INVALID


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
    assert r1.value is None and r2.value is None and r3.value is None
    assert r1.status is NormalizationStatus.INVALID
    assert r2.status is NormalizationStatus.INVALID
    assert r3.status is NormalizationStatus.INVALID


# ------------------------ positive float normalization ----------------------
def test_normalize_positive_float_basic():
    r1 = normalize_positive_float(3.14)
    r2 = normalize_positive_float(" 2.71 ")
    assert r1.value == 3.14 and r2.value == 2.71
    assert r1.status is r2.status is NormalizationStatus.VALID


def test_normalize_positive_float_unknown():
    r1 = normalize_positive_float("n/c")
    r2 = normalize_positive_float(" no CONSTA ")
    assert r1.value is None and r2.value is None
    assert r1.status is r2.status is NormalizationStatus.UNKNOWN


def test_normalize_positive_float_invalid():
    r1 = normalize_positive_float(-1.0)
    r2 = normalize_positive_float("foo")
    r3 = normalize_positive_float("12,34")  # Comma instead of dot
    assert r1.value is None and r2.value is None and r3.value is None
    assert r1.status is NormalizationStatus.INVALID
    assert r2.status is NormalizationStatus.INVALID
    assert r3.status is NormalizationStatus.INVALID


# ---------------------- normalize plain text ----------------------
def test_normalize_plain_text_basic():
    result = normalize_plain_text("  Hello World!  ")
    assert result.value == "Hello World!"
    assert result.status is NormalizationStatus.VALID


def test_normalize_plain_unknown():
    result = normalize_plain_text("No consta")
    assert result.value is None
    assert result.status is NormalizationStatus.UNKNOWN


def test_normalize_plain_text_invalid():
    result = normalize_plain_text("adf\x00")
    assert result.value is None
    assert result.status is NormalizationStatus.INVALID


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


def test_normalize_json_string_valid():
    result = normalize_json_string('{"a": 1, "b": "foo"}')
    assert result.status is NormalizationStatus.VALID
    assert result.value == '{"a": 1, "b": "foo"}'


def test_normalize_json_string_valid_with_spaces():
    result = normalize_json_string('  { "x": [1,2,3], "y": null }  ')
    assert result.status is NormalizationStatus.VALID
    assert result.value == '{"x": [1, 2, 3], "y": null}'


def test_normalize_json_string_invalid():
    result = normalize_json_string("{a: 1, b: 2}")  # keys not quoted
    assert result.status is NormalizationStatus.INVALID
    assert result.value is None


def test_normalize_json_string_empty():
    result = normalize_json_string("")
    assert result.status is NormalizationStatus.UNKNOWN
    assert result.value is None


def test_normalize_json_string_unknown():
    result = normalize_json_string("No consta")
    assert result.status is NormalizationStatus.UNKNOWN
    assert result.value is None


def test_normalize_json_string_none():
    result = normalize_json_string(None)  # type: ignore
    assert result.status is NormalizationStatus.UNKNOWN
    assert result.value is None

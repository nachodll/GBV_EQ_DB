import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Optional, Union

import pandas as pd

"""Utility functions for normalizing various types of data.

Each normalizer returns a :class:`NormalizationResult` describing the normalized
value and whether the original input was valid, unknown or invalid."""


class NormalizationStatus(Enum):
    """Possible outcomes of a normalization attempt."""

    VALID = auto()
    UNKNOWN = auto()
    INVALID = auto()


@dataclass
class NormalizationResult:
    """Container for a normalization result."""

    value: Optional[Any]
    status: NormalizationStatus
    raw: str


UNKNOWN_STRINGS = {"", "unknown", "n/c", "no consta", "noconsta", "desconocida"}


def _is_unknown(value: str) -> bool:
    """Return True if the cleaned value represents an explicit unknown."""

    return value.strip().lower() in UNKNOWN_STRINGS


def _strip_accents(text: str) -> str:
    """
    Remove accents from a string.
    """
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def _normalize_region_name(name: str, normalization_dict: dict[str, int]) -> int | None:
    """
    Generic normalization function for names using a provided normalization dictionary.
    Ignores case, accents, and any spaces (leading, trailing, or in the middle).
    Returns the normalized name, or None if not found.
    """
    cleaned = name.strip()
    # Try direct match first
    if cleaned in normalization_dict:
        return normalization_dict[cleaned]
    # Try case-insensitive match
    for key in normalization_dict:
        if cleaned.lower() == key.lower():
            return normalization_dict[key]
    # Try accent-insensitive and case-insensitive match
    cleaned_no_accents = _strip_accents(cleaned).lower()
    for key in normalization_dict:
        if _strip_accents(key).lower() == cleaned_no_accents:
            return normalization_dict[key]

    # Try accent-insensitive, case-insensitive, and space-insensitive match
    def normalize_spaces(s: str):
        return _strip_accents(s).replace(" ", "").lower()

    cleaned_no_spaces = normalize_spaces(cleaned)
    for key in normalization_dict:
        if normalize_spaces(key) == cleaned_no_spaces:
            return normalization_dict[key]
    return None


DICT_PROVINCIAS = {
    "Araba/Álava": 1,
    "Araba-Álava": 1,
    "Álava": 1,
    "Araba": 1,
    "Albacete": 2,
    "Alicante/Alacant": 3,
    "Alicante": 3,
    "Alacant": 3,
    "Almería": 4,
    "Ávila": 5,
    "Badajoz": 6,
    "Balears (Illes)": 7,
    "Illes Balears": 7,
    "Baleares": 7,
    "Barcelona": 8,
    "Burgos": 9,
    "Cáceres": 10,
    "Cádiz": 11,
    "Castellón/Castelló": 12,
    "Castellón de la Plana": 12,
    "Castelló": 12,
    "Castellón": 12,
    "Ciudad Real": 13,
    "Córdoba": 14,
    "A Coruña": 15,
    "Coruña (A)": 15,
    "Cuenca": 16,
    "Girona": 17,
    "Gerona": 17,
    "Granada": 18,
    "Guadalajara": 19,
    "Gipuzkoa": 20,
    "Huelva": 21,
    "Huesca": 22,
    "Jaén": 23,
    "León": 24,
    "Lleida": 25,
    "Lérida": 25,
    "Rioja (La)": 26,
    "La Rioja": 26,
    "Lugo": 27,
    "Madrid": 28,
    "Málaga": 29,
    "Murcia": 30,
    "Navarra": 31,
    "Ourense": 32,
    "Asturias": 33,
    "Asturias/Asturies": 33,
    "Asturies": 33,
    "Palencia": 34,
    "Palmas (Las)": 35,
    "Las Palmas": 35,
    "Pontevedra": 36,
    "Salamanca": 37,
    "Santa Cruz de Tenerife": 38,
    "Tenerife": 38,
    "Cantabria": 39,
    "Segovia": 40,
    "Sevilla": 41,
    "Soria": 42,
    "Tarragona": 43,
    "Teruel": 44,
    "Toledo": 45,
    "Valencia/València": 46,
    "Valencia": 46,
    "València": 46,
    "Valladolid": 47,
    "Bizkaia": 48,
    "Zamora": 49,
    "Zaragoza": 50,
    "Ceuta": 51,
    "Melilla": 52,
}


def normalize_provincia(name: str) -> NormalizationResult:
    """Normalize a province name using the dict_provincia dictionary."""

    if _is_unknown(name.strip()):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)
    normalized = _normalize_region_name(name, DICT_PROVINCIAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


DICT_COMUNIDADES_AUTOMAS = {
    "Andalucía": 1,
    "Aragón": 2,
    "Asturias": 3,
    "Principado de Asturias": 3,
    "Asturias, Principado de": 3,
    "Asturias (Principado de)": 3,
    "Islas Baleares": 4,
    "Illes Balears": 4,
    "Canarias": 5,
    "Cantabria": 6,
    "Castilla y León": 7,
    "Castilla-La Mancha": 8,
    "Cataluña": 9,
    "Comunitat Valenciana": 10,
    "Comunidad Valenciana": 10,
    "Extremadura": 11,
    "Galicia": 12,
    "Comunidad de Madrid": 13,
    "Madrid": 13,
    "Madrid (Comunidad de)": 13,
    "Madrid, Comunidad de": 13,
    "Región de Murcia": 14,
    "Murcia, Región de": 14,
    "Murcia (Región de)": 14,
    "Murcia": 14,
    "Comunidad Foral de Navarra": 15,
    "Navarra": 15,
    "Navarra (Comunidad Foral de)": 15,
    "Navarra, Comunidad Foral de": 15,
    "País Vasco": 16,
    "Euskadi": 16,
    "País Vasco/Euskadi": 16,
    "Euskadi/País Vasco": 16,
    "País Vasco (Euskadi)": 16,
    "Euskadi (País Vasco)": 16,
    "La Rioja": 17,
    "Rioja (La)": 17,
    "Rioja, La": 17,
    "Rioja": 17,
    "Ceuta": 18,
    "Melilla": 19,
    # "España": 0,
    # "España (Total)": 0,
    # "Total España": 0,
    # "Total": 0,
    # "Total Nacional": 0,
    # "Nacional": 0,
}


def normalize_comunidad_autonoma(name: str) -> NormalizationResult:
    """Normalize a comunidad autónoma name using the dict_comunidad_autonoma dictionary."""

    if _is_unknown(name.strip()):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)

    normalized = _normalize_region_name(name, DICT_COMUNIDADES_AUTOMAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


DICT_MONTHS = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12,
}


def normalize_month(month: str) -> NormalizationResult:
    """Normalize a month name to its corresponding number."""

    if _is_unknown(month):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, month)

    for key in DICT_MONTHS:
        if key.lower() == month.strip().lower():
            return NormalizationResult(DICT_MONTHS[key], NormalizationStatus.VALID, month)

    return NormalizationResult(None, NormalizationStatus.INVALID, month)


def normalize_year(year: Union[str, int, float]) -> NormalizationResult:
    """Normalize a year string, int or float to an integer."""

    raw_str = str(year)
    if isinstance(year, str) and _is_unknown(year):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)

    try:
        if isinstance(year, str):
            match = re.search(r"\b(19\d{2}|20\d{2})\b", year)
            if match:
                year_int = int(match.group(1))
            else:
                year_int = int(year.strip())
        else:
            year_int = int(year)

        if 1900 <= year_int <= datetime.now().year:
            return NormalizationResult(year_int, NormalizationStatus.VALID, raw_str)

        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)

    except (ValueError, TypeError):
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


DICT_QUARTER = {
    "primero": 1,
    "segundo": 2,
    "tercero": 3,
    "cuarto": 4,
}


def normalize_quarter(quarter: Union[str, int]) -> NormalizationResult:
    """Normalize a quarter string or int to an integer between 1 and 4."""

    raw_str = str(quarter)
    if isinstance(quarter, str) and _is_unknown(quarter):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)

    if isinstance(quarter, str):
        quarter = quarter.strip()
        if quarter.isdigit():
            # "1", "2", etc
            q = int(quarter)
            if 1 <= q <= 4:
                return NormalizationResult(q, NormalizationStatus.VALID, raw_str)
            return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)

        else:
            # "primero", "segundo", etc
            quarter = quarter.lower()
            if quarter in DICT_QUARTER:
                return NormalizationResult(DICT_QUARTER[quarter], NormalizationStatus.VALID, raw_str)
            return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)
    else:
        q = int(quarter)
        if 1 <= q <= 4:
            return NormalizationResult(q, NormalizationStatus.VALID, raw_str)
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


def normalize_age_group(raw: str) -> NormalizationResult:
    """Normalizes a raw age group string to the format '<min>-<max>'."""

    clean = raw.strip().lower().replace("años", "").replace(" ", "")

    if _is_unknown(clean) or clean == "noconsta":
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw)

    # Handle formats like 18-24
    match_range = re.match(r"(\d+)-(\d+)", clean)
    if match_range:
        normalized = f"{match_range.group(1)}-{match_range.group(2)}"
        return NormalizationResult(normalized, NormalizationStatus.VALID, raw)

    # Handle formats like <16 or +16
    match_less = re.match(r"[<+](\d+)", clean)
    if match_less:
        normalized = f"<{int(match_less.group(1))}"
        return NormalizationResult(normalized, NormalizationStatus.VALID, raw)

    # Handle formats like >84 or +84
    match_greater = re.match(r"[>+](\d+)", clean)
    if match_greater:
        normalized = f">{int(match_greater.group(1))}"
        return NormalizationResult(normalized, NormalizationStatus.VALID, raw)

    return NormalizationResult(None, NormalizationStatus.INVALID, raw)


def normalize_positive_integer(value: Union[str, int, float]) -> NormalizationResult:
    """Normalize a string, int or float to a positive integer."""
    raw_str = str(value)
    if isinstance(value, str) and _is_unknown(value):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)
    try:
        if isinstance(value, str):
            num = int(value.strip())
        else:
            num = int(value)
        if num >= 0:
            return NormalizationResult(num, NormalizationStatus.VALID, raw_str)
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)
    except ValueError:
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


def apply_and_check(series: pd.Series, func: Callable[[Any], NormalizationResult]):  # type: ignore
    """Apply a normalization function and fail on invalid results."""

    results = series.apply(func)  # type: ignore
    invalid = [r.raw for r in results if r.status is NormalizationStatus.INVALID]  # type: ignore
    if invalid:
        raise ValueError(f"Invalid values in column '{series.name}: {invalid}'")
    return results.map(lambda r: r.value)  # type: ignore


def apply_and_check_dict(series: pd.Series, mapping: dict[str, Any]):  # type: ignore
    """Normalize a string using a custom mapping dictionary."""

    def mapping_func(value: str) -> NormalizationResult:
        if _is_unknown(value):
            return NormalizationResult(None, NormalizationStatus.UNKNOWN, value)
        if value in mapping:
            return NormalizationResult(mapping[value], NormalizationStatus.VALID, value)
        return NormalizationResult(None, NormalizationStatus.INVALID, value)

    return apply_and_check(series, mapping_func)  # type: ignore

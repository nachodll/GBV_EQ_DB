import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Optional, Union

import pandas as pd

from utils.normalization_dicts import (
    DICT_COMUNIDADES_AUTOMAS,
    DICT_MONTHS,
    DICT_MUNICIPIOS,
    DICT_NATIONALITIES,
    DICT_PROVINCIAS,
    DICT_QUARTER,
    DICT_UNKNOWN_STRINGS,
)

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


def _is_unknown(value: Optional[str]) -> bool:
    """Return True if the cleaned value represents an explicit unknown."""
    if value is None or pd.isna(value):  # type: ignore
        return True
    return value.strip().lower() in DICT_UNKNOWN_STRINGS


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
    cleaned = re.sub(r"\b\d{1,2}\b", "", name).strip()

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


def normalize_provincia(name: str) -> NormalizationResult:
    """Normalize a province name using the dict_provincia dictionary."""

    if _is_unknown(name):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)
    normalized = _normalize_region_name(name, DICT_PROVINCIAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


def normalize_comunidad_autonoma(name: str) -> NormalizationResult:
    """Normalize a comunidad autónoma name using the dict_comunidad_autonoma dictionary."""

    if _is_unknown(name):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)

    normalized = _normalize_region_name(name, DICT_COMUNIDADES_AUTOMAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


def normalize_municipio_id(municipio_id: Union[str, int]) -> NormalizationResult:
    """Normalize a municipio ID, ensuring it is a 5-digit integer present in the municipios dictionary."""

    raw_str = str(municipio_id)
    if isinstance(municipio_id, str) and _is_unknown(municipio_id):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)

    try:
        normalized_id = int(municipio_id)
        if 1001 <= normalized_id <= 99999:
            # Check if the ID exists in the municipios dictionary
            found = any(normalized_id in prov_dict.values() for prov_dict in DICT_MUNICIPIOS.values())
            if found:
                return NormalizationResult(normalized_id, NormalizationStatus.VALID, raw_str)
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)
    except (ValueError, TypeError):
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


def normalize_municipio(args: tuple[str, Union[str, int]]) -> NormalizationResult:
    """Normalize a municipio name within a given province."""

    name, provincia = args

    if _is_unknown(name):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)

    # Normalize provincia
    if isinstance(provincia, str):
        prov_result = normalize_provincia(provincia)
        if prov_result.status is not NormalizationStatus.VALID:
            return NormalizationResult(None, NormalizationStatus.INVALID, name)
        provincia_id = int(prov_result.value)  # type: ignore
    else:
        provincia_id = int(provincia)

    prov_dict = DICT_MUNICIPIOS.get(provincia_id)
    if prov_dict is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)

    normalized = normalized = _normalize_region_name(name, prov_dict)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


def normalize_nationality(name: str) -> NormalizationResult:
    """Normalize a given nationality to the corresponding country name."""

    if _is_unknown(name):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)

    cleaned = name.strip()
    # Direct match
    if cleaned in DICT_NATIONALITIES:
        return NormalizationResult(DICT_NATIONALITIES[cleaned], NormalizationStatus.VALID, name)
    # Case-insensitive match
    for key in DICT_NATIONALITIES:
        if cleaned.lower() == key.lower():
            return NormalizationResult(DICT_NATIONALITIES[key], NormalizationStatus.VALID, name)
    # Accent-insensitive, case-insensitive match
    cleaned_no_accents = _strip_accents(cleaned).lower()
    for key in DICT_NATIONALITIES:
        if _strip_accents(key).lower() == cleaned_no_accents:
            return NormalizationResult(DICT_NATIONALITIES[key], NormalizationStatus.VALID, name)
    # Match with plural forms (+s or +es)
    if cleaned_no_accents.endswith("es"):
        singular = cleaned_no_accents[:-2]
    elif cleaned_no_accents.endswith("s"):
        singular = cleaned_no_accents[:-1]
    else:
        singular = cleaned_no_accents
    for key in DICT_NATIONALITIES:
        if _strip_accents(key).lower() == singular:
            return NormalizationResult(DICT_NATIONALITIES[key], NormalizationStatus.VALID, name)
    return NormalizationResult(None, NormalizationStatus.INVALID, name)


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


def normalize_date(date_str: str) -> NormalizationResult:
    """Normalize a date string to a datetime object."""

    raw_str = date_str.strip()
    if _is_unknown(raw_str):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)

    try:
        # Try parsing the date in various formats
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                date_obj = datetime.strptime(raw_str, fmt)
                return NormalizationResult(date_obj, NormalizationStatus.VALID, raw_str)
            except ValueError:
                continue
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)

    except Exception:
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


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


def normalize_age_group(raw: Optional[str]) -> NormalizationResult:
    """Normalizes a raw age group string to the format '<min>-<max>'."""

    if raw is None:
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, "")

    clean = raw.strip().lower().replace("años", "").replace(" ", "")

    if _is_unknown(clean):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw)

    # Special case: "19 años"
    match_single = re.match(r"^(\d+)$", clean)
    if match_single:
        age = int(match_single.group(1))
        if age < 0:
            return NormalizationResult(None, NormalizationStatus.INVALID, raw)
        return NormalizationResult(f"{age}", NormalizationStatus.VALID, raw)

    # Special cases: "De 0 a 15 años", "De 16 a 64 años"
    match_de_range = re.match(r"de(\d+)a(\d+)", clean)
    if match_de_range:
        min_age = int(match_de_range.group(1))
        max_age = int(match_de_range.group(2))
        if min_age == 0:
            normalized = f"<{max_age}"
        else:
            if min_age >= max_age:
                return NormalizationResult(None, NormalizationStatus.INVALID, raw)
            normalized = f"{min_age}-{max_age}"
        return NormalizationResult(normalized, NormalizationStatus.VALID, raw)

    # Handle formats like 18-24
    match_range = re.match(r"(\d+)-(\d+)", clean)
    if match_range:
        min_age = int(match_range.group(1))
        max_age = int(match_range.group(2))
        if min_age >= max_age:
            return NormalizationResult(None, NormalizationStatus.INVALID, raw)
        normalized = f"{min_age}-{max_age}"
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

    # Handle formats like '65añosymás' or '65años y más' or 'de 65 años y más años'
    match_and_more = re.match(r"(?:de)?(\d+)(?:años)?y?más(?:años)?", raw.strip().replace(" ", "").lower())
    if match_and_more:
        normalized = f">{int(match_and_more.group(1))}"
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


def normalize_positive_float(value: Union[str, int, float]) -> NormalizationResult:
    """Normalize a string, int or float to a positive float."""
    raw_str = str(value)
    if isinstance(value, str) and _is_unknown(value):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, raw_str)
    try:
        if isinstance(value, str):
            num = float(value.strip())
        else:
            num = float(value)
        if num >= 0:
            return NormalizationResult(num, NormalizationStatus.VALID, raw_str)
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)
    except ValueError:
        return NormalizationResult(None, NormalizationStatus.INVALID, raw_str)


def normalize_plain_text(text: str) -> NormalizationResult:
    """Normalize a plain text string by stripping whitespaces"""
    clean_str = text.strip()
    if _is_unknown(clean_str):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, clean_str)

    # Check for forbidden characters: null bytes, control characters
    forbidden_pattern = r"[\x00-\x1F\x7F]"
    if re.search(forbidden_pattern, clean_str):
        return NormalizationResult(None, NormalizationStatus.INVALID, clean_str)

    return NormalizationResult(clean_str, NormalizationStatus.VALID, clean_str)


def apply_and_check(series: pd.Series, func: Callable[[Any], NormalizationResult]):  # type: ignore
    """Apply a normalization function and fail on invalid results."""
    results = series.apply(func)  # type: ignore

    invalid = [r.raw for r in results if r.status is NormalizationStatus.INVALID]  # type: ignore
    if invalid:
        raise ValueError(f"Invalid values ({len(invalid)}) in column '{series.name}: {set(invalid)}")  # type: ignore
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

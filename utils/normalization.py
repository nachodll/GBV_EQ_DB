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


def _is_unknown(value: str) -> bool:
    """Return True if the cleaned value represents an explicit unknown."""

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


def normalize_provincia(name: str) -> NormalizationResult:
    """Normalize a province name using the dict_provincia dictionary."""

    if _is_unknown(name.strip()):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)
    normalized = _normalize_region_name(name, DICT_PROVINCIAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


def normalize_comunidad_autonoma(name: str) -> NormalizationResult:
    """Normalize a comunidad autónoma name using the dict_comunidad_autonoma dictionary."""

    if _is_unknown(name.strip()):
        return NormalizationResult(None, NormalizationStatus.UNKNOWN, name)

    normalized = _normalize_region_name(name, DICT_COMUNIDADES_AUTOMAS)
    if normalized is None:
        return NormalizationResult(None, NormalizationStatus.INVALID, name)
    return NormalizationResult(normalized, NormalizationStatus.VALID, name)


def normalize_municipio(args: tuple[str, Union[str, int]]) -> NormalizationResult:
    """Normalize a municipio name within a given province."""

    name, provincia = args

    if _is_unknown(name.strip()):
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

    # Handle formats like '65añosymás' or '65años y más'
    match_and_more = re.match(r"(\d+)años?y?más", raw.strip().replace(" ", "").lower())
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

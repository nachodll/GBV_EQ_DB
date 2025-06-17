import unicodedata

dict_provincia = {
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

dict_comunidad_autonoma = {
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
    "España": "España",
    "España (Total)": "España",
    "Total España": "España",
    "Total": "España",
    "Total Nacional": "España",
    "Nacional": "España",
}


def strip_accents(text: str) -> str:
    """
    Remove accents from a string.
    """
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def normalize_name(name: str, normalization_dict: dict) -> str | None:
    """
    Generic normalization function for names using a provided normalization dictionary.
    Ignores case, accents, and any spaces (leading, trailing, or in the middle).
    Returns the normalized name, or None if not found.
    """
    if not isinstance(name, str):
        return None
    cleaned = name.strip()
    # Try direct match first
    if cleaned in normalization_dict:
        return normalization_dict[cleaned]
    # Try case-insensitive match
    for key in normalization_dict:
        if cleaned.lower() == key.lower():
            return normalization_dict[key]
    # Try accent-insensitive and case-insensitive match
    cleaned_no_accents = strip_accents(cleaned).lower()
    for key in normalization_dict:
        if strip_accents(key).lower() == cleaned_no_accents:
            return normalization_dict[key]

    # Try accent-insensitive, case-insensitive, and space-insensitive match
    def normalize_spaces(s):
        return strip_accents(s).replace(" ", "").lower()

    cleaned_no_spaces = normalize_spaces(cleaned)
    for key in normalization_dict:
        if normalize_spaces(key) == cleaned_no_spaces:
            return normalization_dict[key]
    return None


def normalize_provincia(name: str) -> str | None:
    """
    Normalize a province name using the dict_provincia dictionary.
    """
    return normalize_name(name, dict_provincia)


def normalize_comunidad_autonoma(name: str) -> str | None:
    """
    Normalize a comunidad autónoma name using the dict_comunidad_autonoma dictionary.
    """
    return normalize_name(name, dict_comunidad_autonoma)


def normalize_month(month: str) -> int | None:
    """
    Normalize a month name to its corresponding number.
    """
    months = {
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
    return months.get(month.strip(), None)

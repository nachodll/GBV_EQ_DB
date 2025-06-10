import unicodedata

dict_provincia = {
    "A Coruña": "A Coruña",
    "Coruña (A)": "A Coruña",
    "Albacete": "Albacete",
    "Alicante/Alacant": "Alicante/Alacant",
    "Alicante": "Alicante/Alacant",
    "Alacant": "Alicante/Alacant",
    "Almería": "Almería",
    "Araba/Álava": "Araba/Álava",
    "Araba-Álava": "Araba/Álava",
    "Álava": "Araba/Álava",
    "Araba": "Araba/Álava",
    "Asturias": "Asturias",
    "Asturias/Asturies": "Asturias",
    "Asturies": "Asturias",
    "Badajoz": "Badajoz",
    "Barcelona": "Barcelona",
    "Bizkaia": "Bizkaia",
    "Burgos": "Burgos",
    "Cantabria": "Cantabria",
    "Castellón/Castelló": "Castellón/Castelló",
    "Castellón de la Plana": "Castellón/Castelló",
    "Castelló": "Castellón/Castelló",
    "Castellón": "Castellón/Castelló",
    "Ceuta": "Ceuta",
    "Ciudad Real": "Ciudad Real",
    "Cuenca": "Cuenca",
    "Cáceres": "Cáceres",
    "Cádiz": "Cádiz",
    "Córdoba": "Córdoba",
    "Gipuzkoa": "Gipuzkoa",
    "Girona": "Girona",
    "Gerona": "Girona",
    "Granada": "Granada",
    "Guadalajara": "Guadalajara",
    "Huelva": "Huelva",
    "Huesca": "Huesca",
    "Balears (Illes)": "Illes Balears",
    "Illes Balears": "Illes Balears",
    "Baleares": "Illes Balears",
    "Jaén": "Jaén",
    "Rioja (La)": "La Rioja",
    "La Rioja": "La Rioja",
    "Palmas (Las)": "Las Palmas",
    "Las Palmas": "Las Palmas",
    "León": "León",
    "Lleida": "Lleida",
    "Lérida": "Lleida",
    "Lugo": "Lugo",
    "Madrid": "Madrid",
    "Melilla": "Melilla",
    "Murcia": "Murcia",
    "Málaga": "Málaga",
    "Navarra": "Navarra",
    "Ourense": "Ourense",
    "Palencia": "Palencia",
    "Pontevedra": "Pontevedra",
    "Salamanca": "Salamanca",
    "Santa Cruz de Tenerife": "Santa Cruz de Tenerife",
    "Tenerife": "Santa Cruz de Tenerife",
    "Segovia": "Segovia",
    "Sevilla": "Sevilla",
    "Soria": "Soria",
    "Tarragona": "Tarragona",
    "Teruel": "Teruel",
    "Toledo": "Toledo",
    "Valencia/València": "Valencia/València",
    "Valencia": "Valencia/València",
    "València": "Valencia/València",
    "Valladolid": "Valladolid",
    "Zamora": "Zamora",
    "Zaragoza": "Zaragoza",
    "Ávila": "Ávila",
}

dict_comunidad_autonoma = {
    "Andalucía": "Andalucía",
    "Aragón": "Aragón",
    "Canarias": "Canarias",
    "Cantabria": "Cantabria",
    "Castilla-La Mancha": "Castilla-La Mancha",
    "Castilla y León": "Castilla y León",
    "Cataluña": "Cataluña",
    "Comunidad Foral de Navarra": "Comunidad Foral de Navarra",
    "Navarra": "Comunidad Foral de Navarra",
    "Navarra (Comunidad Foral de)": "Comunidad Foral de Navarra",
    "Navarra, Comunidad Foral de": "Comunidad Foral de Navarra",
    "Comunidad de Madrid": "Comunidad de Madrid",
    "Madrid": "Comunidad de Madrid",
    "Madrid (Comunidad de)": "Comunidad de Madrid",
    "Madrid, Comunidad de": "Comunidad de Madrid",
    "Comunitat Valenciana": "Comunitat Valenciana",
    "Comunidad Valenciana": "Comunitat Valenciana",
    "Extremadura": "Extremadura",
    "Galicia": "Galicia",
    "Islas Baleares": "Illes Balears",
    "Illes Balears": "Illes Balears",
    "La Rioja": "La Rioja",
    "Rioja (La)": "La Rioja",
    "Rioja, La": "La Rioja",
    "Rioja": "La Rioja",
    "País Vasco": "País Vasco",
    "Euskadi": "País Vasco",
    "País Vasco/Euskadi": "País Vasco",
    "Euskadi/País Vasco": "País Vasco",
    "País Vasco (Euskadi)": "País Vasco",
    "Euskadi (País Vasco)": "País Vasco",
    "Asturias": "Principado de Asturias",
    "Principado de Asturias": "Principado de Asturias",
    "Asturias, Principado de": "Principado de Asturias",
    "Asturias (Principado de)": "Principado de Asturias",
    "Región de Murcia": "Región de Murcia",
    "Murcia, Región de": "Región de Murcia",
    "Murcia (Región de)": "Región de Murcia",
    "Murcia": "Región de Murcia",
    "Ceuta": "Ceuta",
    "Melilla": "Melilla",
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


def normalize_name_provincia(name: str) -> str | None:
    """
    Normalize a province name using the dict_provincia dictionary.
    """
    return normalize_name(name, dict_provincia)


def normalize_name_comunidad_autonoma(name: str) -> str | None:
    """
    Normalize a comunidad autónoma name using the dict_comunidad_autonoma dictionary.
    """
    return normalize_name(name, dict_comunidad_autonoma)

import csv
from pathlib import Path

MUNICIPIOS_PATH = Path("data") / "static" / "municipios.csv"


def _load_municipios_dict() -> dict[int, dict[str, int]]:
    """Load municipios data keyed by provincia id"""
    municipios_dict: dict[int, dict[str, int]] = {}
    with open(MUNICIPIOS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")  # type: ignore
        for row in reader:  # type: ignore
            provincia_id = int(row["provincia_id"])  # type: ignore
            municipio_name = row["nombre"].strip()  # type: ignore
            municipio_id = int(row["municipio_id"])  # type: ignore
            prov_dict = municipios_dict.setdefault(provincia_id, {})
            prov_dict.setdefault(municipio_name, municipio_id)  # type: ignore

            # Special case "/" (Arrasate/Mondragón)
            slash_variants = [part.strip() for part in municipio_name.split("/")]
            for variant in slash_variants:
                prov_dict.setdefault(variant, municipio_id)
                # Nested special case "/" and "," (Alqueries, les/Alquerías del Niño Perdido)
                if "," in variant:
                    base, article = [s.strip() for s in variant.split(",", 1)]
                    prov_dict.setdefault(base, municipio_id)
                    prov_dict.setdefault(f"{base} ({article})", municipio_id)

            # Special case "," (Jonquera, La)
            if "," in municipio_name and len(slash_variants) == 1:
                base, article = [s.strip() for s in municipio_name.split(",", 1)]
                prov_dict.setdefault(base, municipio_id)
                prov_dict.setdefault(f"{base} ({article})", municipio_id)
    return municipios_dict


DICT_MUNICIPIOS: dict[int, dict[str, int]] = _load_municipios_dict()

DICT_UNKNOWN_STRINGS = {
    "",
    "unknown",
    "n/c",
    "no consta",
    "noconsta",
    "desconocida",
}

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

DICT_QUARTER = {
    "primero": 1,
    "segundo": 2,
    "tercero": 3,
    "cuarto": 4,
}

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
    "Balears, Illes": 7,
    "Balears (Illes)": 7,
    "Illes Balears": 7,
    "Baleares": 7,
    "Balears": 7,
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
    "Rioja": 26,
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
    "Palmas": 35,
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

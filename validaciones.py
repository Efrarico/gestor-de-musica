from typing import Optional
from config import GENRES, YEAR_MIN, YEAR_MAX

def validar_nombre(texto: str) -> bool:
    return isinstance(texto, str) and texto.strip() != ""

def validar_duracion(duracion: str) -> bool:
    """Formato mm:ss, segundos entre 0 y 59, minutos >= 0."""
    try:
        partes = duracion.strip().split(":")
        if len(partes) != 2:
            return False
        minutos, segundos = int(partes[0]), int(partes[1])
        return minutos >= 0 and 0 <= segundos < 60
    except Exception:
        return False

def validar_anio(anio: str) -> bool:
    if not isinstance(anio, (str, int)):
        return False
    try:
        val = int(anio)
    except Exception:
        return False
    return YEAR_MIN <= val <= YEAR_MAX

def normalizar_anio(anio: Optional[str]) -> Optional[int]:
    if anio is None or str(anio).strip() == "":
        return None
    return int(anio)

def validar_genero(genero: str) -> bool:
    return genero in GENRES

def validar_opcional_no_vacio(valor: Optional[str]) -> bool:
    return valor is None or str(valor).strip() != ""

import swisseph as swe
from datetime import datetime
import pandas as pd
import pytz

# Configurar path de efemerides (opcional si se usan las integradas, 
# pero swisseph suele venir con efemerides basicas que cubren nuestro rango temporal)
swe.set_ephe_path('')

CARTAS_NATALES = {
    "BTC":  {"fecha": "2009-01-03", "hora": "18:15", "tz": "UTC", "signo": "Capricornio"},
    "ETH":  {"fecha": "2015-07-30", "hora": "03:26", "tz": "UTC", "signo": "Leo"},
    "SOL":  {"fecha": "2020-03-16", "hora": "00:00", "tz": "UTC", "signo": "Piscis"},
    "XRP":  {"fecha": "2012-06-02", "hora": "00:00", "tz": "UTC", "signo": "Geminis"},
    "BNB":  {"fecha": "2017-07-25", "hora": "00:00", "tz": "UTC", "signo": "Leo"},
    "NEAR": {"fecha": "2020-10-13", "hora": "00:00", "tz": "UTC", "signo": "Libra"},
}

PLANETAS = {
    "Sol": swe.SUN,
    "Luna": swe.MOON,
    "Mercurio": swe.MERCURY,
    "Venus": swe.VENUS,
    "Marte": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturno": swe.SATURN,
    "Urano": swe.URANUS,
    "Neptuno": swe.NEPTUNE,
    "Pluton": swe.PLUTO
}

SIGNOS = ["Aries", "Tauro", "Geminis", "Cancer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]

def _get_julian_day(fecha_dt: datetime) -> float:
    # Convertir fecha_dt a UTC si no lo esta
    if fecha_dt.tzinfo is None:
        fecha_dt = pytz.utc.localize(fecha_dt)
    else:
        fecha_dt = fecha_dt.astimezone(pytz.utc)
    
    y, m, d = fecha_dt.year, fecha_dt.month, fecha_dt.day
    h = fecha_dt.hour + fecha_dt.minute/60.0 + fecha_dt.second/3600.0
    return swe.julday(y, m, d, h)

def get_posicion_planeta(planeta_nombre: str, fecha_dt: datetime) -> dict:
    """Retorna la posicion del planeta en grados (0-360) y su signo."""
    if planeta_nombre not in PLANETAS:
        raise ValueError(f"Planeta {planeta_nombre} no soportado.")
    
    jd = _get_julian_day(fecha_dt)
    res, ret = swe.calc_ut(jd, PLANETAS[planeta_nombre], swe.FLG_SWIEPH)
    longitud = res[0] # grados 0-360
    
    idx_signo = int(longitud / 30)
    grados_en_signo = longitud % 30
    
    return {
        "planeta": planeta_nombre,
        "longitud_total": longitud,
        "signo": SIGNOS[idx_signo],
        "grados_signo": grados_en_signo
    }

def _calcular_aspecto(grados1: float, grados2: float) -> dict:
    # Calcula el aspecto entre dos posiciones (con orbe de 5 grados)
    orbe = 5.0
    diff = abs(grados1 - grados2)
    if diff > 180:
        diff = 360 - diff
        
    aspectos = [
        {"nombre": "Conjuncion", "angulo": 0},
        {"nombre": "Sextil", "angulo": 60},
        {"nombre": "Cuadratura", "angulo": 90},
        {"nombre": "Trigono", "angulo": 120},
        {"nombre": "Oposicion", "angulo": 180}
    ]
    
    for asp in aspectos:
        if abs(diff - asp["angulo"]) <= orbe:
            return {"aspecto": asp["nombre"], "orbe": abs(diff - asp["angulo"]), "angulo_exacto": asp["angulo"]}
    return None

def get_carta_natal_activo(activo: str) -> dict:
    if activo not in CARTAS_NATALES:
        raise ValueError(f"Activo {activo} no tiene carta natal configurada.")
    
    datos = CARTAS_NATALES[activo]
    fecha_str = f"{datos['fecha']} {datos['hora']}"
    dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
    dt = pytz.utc.localize(dt)
    
    posiciones = {}
    for p in PLANETAS.keys():
        posiciones[p] = get_posicion_planeta(p, dt)
    return posiciones

def get_transitos_hoy(activo: str, fecha_hoy: datetime = None) -> list:
    """Calcula aspectos activos hoy entre los planetas en transito y la carta natal del activo."""
    if fecha_hoy is None:
        fecha_hoy = datetime.now(pytz.utc)
        
    carta_natal = get_carta_natal_activo(activo)
    transitos_activos = []
    
    for p_transito in PLANETAS.keys():
        pos_hoy = get_posicion_planeta(p_transito, fecha_hoy)
        
        for p_natal, pos_natal in carta_natal.items():
            aspecto = _calcular_aspecto(pos_hoy["longitud_total"], pos_natal["longitud_total"])
            if aspecto:
                transitos_activos.append({
                    "planeta_transito": p_transito,
                    "planeta_natal": p_natal,
                    "aspecto": aspecto["aspecto"],
                    "orbe": aspecto["orbe"],
                    "descripcion": f"{aspecto['aspecto']} {p_transito} sobre {p_natal} natal"
                })
                
    return transitos_activos

def get_sinastria_par(activo_a: str, activo_b: str) -> list:
    """Calcula aspectos entre las cartas natales de dos activos (ej BTC vs ETH)."""
    carta_a = get_carta_natal_activo(activo_a)
    carta_b = get_carta_natal_activo(activo_b)
    
    sinastria = []
    for p_a, pos_a in carta_a.items():
        for p_b, pos_b in carta_b.items():
            aspecto = _calcular_aspecto(pos_a["longitud_total"], pos_b["longitud_total"])
            if aspecto:
                sinastria.append({
                    "planeta_a": p_a,
                    "planeta_b": p_b,
                    "aspecto": aspecto["aspecto"],
                    "descripcion": f"{aspecto['aspecto']} {p_a} ({activo_a}) con {p_b} ({activo_b})"
                })
    return sinastria

def get_comparacion_historica(transito_descripcion: str, activo: str, df_ohlcv: pd.DataFrame) -> dict:
    """
    Busca cuando se dio este transito en el pasado y calcula el retorno %.
    PENDIENTE: Requiere calcular historico de transitos y cruzar con dataframe.
    Por ahora retorna un dummy para la arquitectura.
    """
    return {
        "fechas_similares": [],
        "retorno_promedio_30d": 0.0,
        "mensaje": "Funcionalidad de comparacion historica en desarrollo"
    }

if __name__ == "__main__":
    # Prueba rapida
    print(f"--- Transitos para BTC hoy ---")
    transitos_btc = get_transitos_hoy("BTC")
    for t in transitos_btc:
        print(t["descripcion"])
        
    print(f"\n--- Sinastria BTC vs ETH ---")
    sin_btc_eth = get_sinastria_par("BTC", "ETH")
    for s in sin_btc_eth:
        print(s["descripcion"])

import sys
import os
from datetime import datetime

# Anadir el directorio root (aqde-cerebro) al path para importaciones absolutas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motores.astro_engine import get_transitos_hoy, get_sinastria_par
from scrapers.scraper_astro import get_reddit_sentiment

def calcular_score_astral(activo: str) -> dict:
    """Calcula el score final para un activo, sumando factores."""
    # 1. Transitos y Aspectos (40%)
    transitos = get_transitos_hoy(activo)
    
    score_aspectos = 0
    aspectos_relevantes = []
    
    # Pesos (simplificados de la tabla)
    for t in transitos:
        p_transito = t["planeta_transito"]
        p_natal = t["planeta_natal"]
        aspecto = t["aspecto"]
        
        if p_transito == "Jupiter" and aspecto == "Trigono" and p_natal == "Sol":
            score_aspectos += 25
            aspectos_relevantes.append(t["descripcion"])
        elif p_transito == "Venus" and aspecto == "Conjuncion" and p_natal == "Sol":
            score_aspectos += 15
            aspectos_relevantes.append(t["descripcion"])
        elif p_transito == "Mercurio" and aspecto == "Sextil" and p_natal == "Sol":
            score_aspectos += 10
            aspectos_relevantes.append(t["descripcion"])
        elif p_transito == "Saturno" and aspecto == "Cuadratura":
            score_aspectos -= 20
            aspectos_relevantes.append(t["descripcion"])
        elif p_transito == "Marte" and aspecto == "Oposicion":
            score_aspectos -= 15
            aspectos_relevantes.append(t["descripcion"])
        elif p_transito == "Pluton" and aspecto == "Cuadratura":
            score_aspectos -= 12
            aspectos_relevantes.append(t["descripcion"])
            
    # Normalizamos el score de aspectos base 50
    score_aspectos_normalizado = max(0, min(100, 50 + score_aspectos))
    
    # 2. Sentimiento Reddit (30%)
    reddit_data = get_reddit_sentiment()
    score_reddit = reddit_data["score_general"]
    
    # 3. Comparacion Historica (30%)
    # Placeholder: En produccion usaremos el engine completo
    score_historico = 50 
    
    # Calculo Final
    score_final = (score_aspectos_normalizado * 0.40) + (score_reddit * 0.30) + (score_historico * 0.30)
    
    # Determinar Bias
    if score_final >= 70:
        bias = "LONG"
        confianza = "ALTA"
    elif score_final <= 30:
        bias = "SHORT / EXIT"
        confianza = "ALTA"
    else:
        bias = "NEUTRO"
        confianza = "BAJA"
        
    return {
        "asset": activo,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "score": round(score_final, 2),
        "bias": bias,
        "confianza": confianza,
        "transitos_activos": aspectos_relevantes if aspectos_relevantes else ["Ninguno mayor"],
        "fase_lunar": "Implementacion pendiente",
        "sinastria_btc_eth": "Implementacion pendiente",
        "comparacion_historica": "Implementacion pendiente",
        "nota_estratega": f"Sesgo {bias} con score {round(score_final, 2)}. Transitos: {len(transitos)} detectados."
    }

if __name__ == "__main__":
    print(calcular_score_astral("BTC"))

import pandas as pd
import os
from datetime import datetime
import sys

# Asegurar que podemos importar desde motores
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motores.astro_engine import get_transitos_hoy
# Nota: score_engine.py tiene dependencias de scrapers (Reddit), 
# para el backtest solo usaremos el factor ASTRAL (40% del score real o escalado a 100%)

def generate_historical_scores(filename):
    print(f"Procesando {filename}...")
    df = pd.read_csv(filename)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    activo = os.path.basename(filename).split('_')[0]
    
    transits_data = {
        "jupiter_trine": [],
        "saturn_square": [],
        "mars_opp": [],
        "venus_conj": [],
        "mercurio_sextil": []
    }
    scores = []

    
    total = len(df)
    for i, row in df.iterrows():
        if i % 1000 == 0:
            print(f"  Progress: {i}/{total}...")
            
        transitos = get_transitos_hoy(activo, row['datetime'])
        
        # Inicializar valores para esta fila
        row_transits = {k: 0 for k in transits_data.keys()}
        
        score_astral = 0
        for t in transitos:
            p_transito = t["planeta_transito"]
            p_natal = t["planeta_natal"]
            aspecto = t["aspecto"]
            
            # Tracking individual (para Hyperopt futuro)
            if p_transito == "Jupiter" and aspecto == "Trigono" and p_natal == "Sol": 
                score_astral += 25
                row_transits["jupiter_trine"] = 1
            elif p_transito == "Venus" and aspecto == "Conjuncion" and p_natal == "Sol": 
                score_astral += 15
                row_transits["venus_conj"] = 1
            elif p_transito == "Mercurio" and aspecto == "Sextil" and p_natal == "Sol": 
                score_astral += 10
                row_transits["mercurio_sextil"] = 1
            elif p_transito == "Saturno" and aspecto == "Cuadratura" and p_natal == "Sol": 
                score_astral -= 20
                row_transits["saturn_square"] = 1
            elif p_transito == "Marte" and aspecto == "Oposicion" and p_natal == "Sol": 
                score_astral -= 15
                row_transits["mars_opp"] = 1
            elif p_transito == "Pluton" and aspecto == "Cuadratura": 
                score_astral -= 12
        
        scores.append(max(0, min(100, 50 + score_astral)))
        for k in transits_data.keys():
            transits_data[k].append(row_transits[k])
        
    df['astro_score'] = scores
    for k, v in transits_data.items():
        df[k] = v
    
    output_filename = filename.replace('.csv', '_with_scores.csv')
    df.to_csv(output_filename, index=False)
    print(f"Finalizado: {output_filename}")

if __name__ == "__main__":
    # Asegúrate de tener pyswisseph instalado localmente: pip install pyswisseph
    folder = "datos"
    for file in os.listdir(folder):
        if file.endswith('.csv') and not file.endswith('_with_scores.csv'):
            generate_historical_scores(os.path.join(folder, file))

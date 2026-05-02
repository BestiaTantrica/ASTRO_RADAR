from flask import Flask, render_template, jsonify
import os
import json
import pandas as pd
from datetime import datetime
from motores.astro_engine import get_transitos_hoy

app = Flask(__name__)

# Configuración
DATOS_DIR = "datos"
FEATURE_IMPORTANCE_FILE = os.path.join(DATOS_DIR, "feature_importance_results.json")

def load_astro_data():
    if os.path.exists(FEATURE_IMPORTANCE_FILE):
        with open(FEATURE_IMPORTANCE_FILE, 'r') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    # Cargar importancia de planetas
    data = load_astro_data()
    
    # Obtener tránsitos generales de hoy (usando BTC como referencia global)
    transitos = get_transitos_hoy("BTC", datetime.now())
    
    return render_template('index.html', 
                           monedas=data, 
                           transitos=transitos,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "engine": "AQDE Astro-Quantum",
        "last_update": datetime.now().isoformat()
    })

@app.route('/moneda/<symbol>')
def detail(symbol):
    data = load_astro_data()
    moneda_data = data.get(symbol.upper(), {})
    
    if not moneda_data:
        return "Moneda no encontrada", 404
        
    return render_template('detail.html', 
                           symbol=symbol.upper(), 
                           data=moneda_data)

if __name__ == '__main__':
    # En producción usaremos Gunicorn, pero para desarrollo:
    app.run(host='0.0.0.0', port=5000, debug=True)

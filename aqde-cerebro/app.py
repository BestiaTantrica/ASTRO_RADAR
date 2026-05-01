from flask import Flask, request, jsonify
import sys
import os

# Asegurar importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motores.score_engine import calcular_score_astral
from motores.astro_engine import CARTAS_NATALES

app = Flask(__name__)

@app.route('/api/senal', methods=['GET'])
def get_senal():
    asset = request.args.get('asset', 'BTC').upper()
    
    if asset not in CARTAS_NATALES:
        return jsonify({"error": f"Activo {asset} no soportado. Soportados: {list(CARTAS_NATALES.keys())}"}), 400
        
    try:
        resultado = calcular_score_astral(asset)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e), "score": 50, "bias": "NEUTRO"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "AQDE Cerebro Astral"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

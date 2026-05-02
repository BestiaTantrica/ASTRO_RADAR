"""
============================================================
AQDE - FEATURE IMPORTANCE CON FRACDIFF + XGBOOST + CPCV
============================================================
Implementa las recomendaciones del experto externo:
  1. FracDiff  → Target Binario con "memoria" de largo plazo
  2. XGBoost   → Rankea planetas por poder predictivo real
  3. CPCV      → Validación robusta sin desperdiciar datos
  
Basado en: "Advances in Financial Machine Learning" - M. López de Prado
"""
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PASO 1: FRACTAL DIFFERENTIATION (FracDiff)
# Permite que el target sea estacionario pero mantenga la
# "memoria" de los ciclos planetarios de largo plazo.
# ============================================================

def get_weights_ffd(d, size):
    """Calcula los pesos para la diferenciación fraccional (FFD)."""
    w, k = [1.0], 1
    while True:
        w_ = -w[-1] / k * (d - k + 1)
        if abs(w_) < 1e-5:
            break
        w.append(w_)
        k += 1
    w = np.array(w[::-1])
    # Limitar al tamaño de ventana
    if len(w) > size:
        w = w[-size:]
    return w

def frac_diff_ffd(series, d=0.3, thres=1e-5):
    """
    Aplica diferenciación fraccional de ventana fija (FFD).
    d=0.3 es un buen punto de partida: suficientemente estacionario
    pero conservando la "memoria" de los ciclos planetarios.
    """
    w = get_weights_ffd(d, size=100)
    width = len(w) - 1
    df = pd.Series(index=series.index, dtype=float)
    
    for iloc in range(width, len(series)):
        loc0 = series.index[iloc - width]
        loc1 = series.index[iloc]
        if not np.isfinite(series.loc[loc0:loc1]).all():
            continue
        df.loc[loc1] = np.dot(w, series.loc[loc0:loc1].values)
    
    return df.dropna()

# ============================================================
# PASO 2: PREPARACIÓN DEL DATASET
# ============================================================

def prepare_dataset(csv_path, symbol, lookahead_hours=24):
    """
    Prepara el dataset con:
    - Features: tránsitos crudos (jupiter_trine, saturn_square, etc.)
    - Target: Clasificación Binaria con FracDiff (Sube/Baja en N horas)
    """
    print(f"\n{'='*50}")
    print(f"Preparando dataset para {symbol}...")
    
    df = pd.read_csv(csv_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime').sort_index()
    
    # --- Features Planetarios ---
    feature_cols = ['jupiter_trine', 'saturn_square', 'mars_opp', 
                    'venus_conj', 'mercurio_sextil', 'astro_score']
    
    # Verificar que existen las columnas
    available = [c for c in feature_cols if c in df.columns]
    if not available:
        print(f"  ERROR: No se encontraron columnas de tránsitos en {csv_path}")
        return None, None
    
    X = df[available].copy()
    
    # --- Target Binario con FracDiff ---
    # FracDiff del precio de cierre para crear un target con "memoria"
    print(f"  Aplicando FracDiff (d=0.3) al precio de cierre...")
    fd_close = frac_diff_ffd(df['close'].fillna(method='ffill'), d=0.3)
    
    # Target: 1 si el precio FracDiff sube en las próximas N horas, 0 si baja
    future_fd = fd_close.shift(-lookahead_hours)
    target = (future_fd > fd_close).astype(int)
    target.name = 'target'
    
    # Alinear índices
    common_idx = X.index.intersection(fd_close.index).intersection(target.index)
    X = X.loc[common_idx].fillna(0)
    y = target.loc[common_idx]
    
    # Eliminar filas sin target (últimas N horas)
    valid = y.notna()
    X = X[valid]
    y = y[valid]
    
    print(f"  Dataset listo: {len(X)} muestras | {y.mean():.1%} son Alcistas")
    return X, y

# ============================================================
# PASO 3: CPCV - VALIDACIÓN CRUZADA TEMPORAL ROBUSTA
# ============================================================

def run_cpcv_xgboost(X, y, symbol, n_splits=5):
    """
    Combinatorial Purged Cross-Validation simplificado.
    Usa TimeSeriesSplit de sklearn (no usa datos futuros para entrenar).
    Embargo: descarta N filas entre train y test para evitar "data leakage".
    """
    print(f"\nEntrenando XGBoost con CPCV ({n_splits} splits)...")
    
    tscv = TimeSeriesSplit(n_splits=n_splits, gap=24)  # gap=24h para evitar leakage
    
    model = XGBClassifier(
        n_estimators=200,
        max_depth=3,          # Poco profundo para evitar overfitting
        learning_rate=0.05,
        subsample=0.8,        # Usa 80% de los datos por árbol
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42,
        n_jobs=1              # Siguiendo recomendación del experto (1 job)
    )
    
    auc_scores = []
    acc_scores = []
    
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        model.fit(X_train, y_train, verbose=False)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)
        
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, y_pred)
        auc_scores.append(auc)
        acc_scores.append(acc)
        print(f"  Fold {fold+1}: AUC={auc:.3f} | Accuracy={acc:.1%}")
    
    print(f"\n  → AUC Promedio: {np.mean(auc_scores):.3f} ± {np.std(auc_scores):.3f}")
    print(f"  → Accuracy Promedio: {np.mean(acc_scores):.1%}")
    
    # Reentrenar con todos los datos para obtener importancias finales
    model.fit(X, y, verbose=False)
    
    return model, np.mean(auc_scores)

# ============================================================
# PASO 4: ANÁLISIS DE IMPORTANCIA PLANETARIA
# ============================================================

def analyze_feature_importance(model, feature_names, symbol):
    """Analiza y rankea qué planetas son realmente predictivos."""
    importances = model.feature_importances_
    
    ranking = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    
    print(f"\n🌠 ADN ASTROLÓGICO DE {symbol} (Feature Importance XGBoost):")
    print("-" * 45)
    
    emojis = {
        'jupiter_trine': '♃ Júpiter Trígono',
        'saturn_square': '♄ Saturno Cuadratura',
        'mars_opp':      '♂ Marte Oposición',
        'venus_conj':    '♀ Venus Conjunción',
        'mercurio_sextil': '☿ Mercurio Sextil',
        'astro_score':   '⭐ Score Astral Total'
    }
    
    results = {}
    for feature, importance in ranking:
        nombre = emojis.get(feature, feature)
        barra = '█' * int(importance * 50)
        print(f"  {nombre:<25} {barra} {importance:.3f}")
        results[feature] = importance
    
    return results

# ============================================================
# MAIN: Procesar todas las monedas
# ============================================================

if __name__ == "__main__":
    import os
    import json
    
    datos_dir = "datos"
    monedas = ['BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'NEAR']
    resultados_totales = {}
    
    for symbol in monedas:
        csv_path = os.path.join(datos_dir, f"{symbol}_USDT_1h_with_scores.csv")
        
        if not os.path.exists(csv_path):
            print(f"\n⚠️  No se encontró {csv_path}, saltando...")
            continue
        
        X, y = prepare_dataset(csv_path, symbol, lookahead_hours=24)
        
        if X is None or len(X) < 200:
            print(f"  Datos insuficientes para {symbol}")
            continue
        
        model, auc_mean = run_cpcv_xgboost(X, y, symbol)
        importancias = analyze_feature_importance(model, X.columns.tolist(), symbol)
        
        resultados_totales[symbol] = {
            "auc_promedio": round(auc_mean, 4),
            "importancias": {k: round(v, 4) for k, v in importancias.items()}
        }
    
    # Guardar resultados en JSON para usar en la estrategia
    output_path = "datos/feature_importance_results.json"
    with open(output_path, 'w') as f:
        json.dump(resultados_totales, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ Análisis completo. Resultados guardados en {output_path}")
    print(f"\n📊 RESUMEN COMPARATIVO:")
    for symbol, data in resultados_totales.items():
        print(f"\n  {symbol} (AUC: {data['auc_promedio']:.3f})")
        top_planeta = max(data['importancias'], key=data['importancias'].get)
        print(f"    → Planeta dominante: {top_planeta} ({data['importancias'][top_planeta]:.3f})")

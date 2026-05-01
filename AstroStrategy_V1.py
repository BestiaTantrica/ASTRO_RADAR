import pandas as pd
import numpy as np
from datetime import datetime
from freqtrade.strategy import IStrategy
import os

class AstroStrategy_V1(IStrategy):
    """
    ========================================================
             ASTRO-QUANTUM DATA ENGINE - V1 (Simple)
    ========================================================
    Estrategia impulsada por Tránsitos Astrológicos (Astro Score).
    
    Lógica de Entrada:
    - Long: Score Astral >= 70
    - (Opcional futuro) + Confirmación Técnica (Ej: RSI < 50)
    
    Lógica de Salida:
    - Exit: Score Astral <= 30
    
    Nota Técnica para Backtesting:
    Como `pyswisseph` (el motor de efemérides) requiere compilador en Windows,
    esta estrategia carga los scores pre-calculados desde archivos CSV ubicados en 
    `C:/SCRAP/ASTRO_RADAR/aqde-cerebro/datos/`.
    """
    
    INTERFACE_VERSION = 3
    timeframe = '1h'
    can_short = False
    
    # Manejo de ROI y Stoploss estándar por ahora
    minimal_roi = {
        "0": 0.10,   # 10% de ganancia
        "120": 0.05, # 5% después de 2 horas
        "240": 0     # Salir sin pérdida si tarda más de 4 horas
    }
    stoploss = -0.05 # 5% de stop loss

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        pair = metadata.get('pair', '')
        symbol = pair.split('/')[0] # Ej: 'BTC'
        
        # Ruta donde guardamos los CSV con scores precalculados (en Oracle B)
        csv_path = f"/home/ubuntu/CHACAL_LATERAL_AWS/user_data/data/binance/{symbol}_USDT_1h_with_scores.csv"
        
        if os.path.exists(csv_path):
            try:
                # Leer los scores precalculados
                df_scores = pd.read_csv(csv_path)
                df_scores['date'] = pd.to_datetime(df_scores['datetime']).dt.tz_localize('UTC')
                
                # Seleccionar solo fecha y score
                df_scores = df_scores[['date', 'astro_score']]
                
                # Merge con el dataframe actual de freqtrade
                dataframe['date'] = pd.to_datetime(dataframe['date'])
                dataframe = pd.merge(dataframe, df_scores, on='date', how='left')
                
                # Llenar huecos con 50 (Neutral) si falta algún dato
                dataframe['astro_score'] = dataframe['astro_score'].fillna(50)
                
            except Exception as e:
                print(f"Error cargando scores para {symbol}: {e}")
                dataframe['astro_score'] = 50
        else:
            print(f"ATENCIÓN: No se encontró CSV de scores para {symbol}. Usando Neutral (50).")
            dataframe['astro_score'] = 50

        # Opcional: Agregar indicadores técnicos clásicos para combinar luego
        import talib.abstract as ta
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['enter_long'] = 0
        
        # Condición Mixta: Comprar si el cosmos es ultra favorable (>70) Y el activo está barato (RSI < 40)
        dataframe.loc[
            (
                (dataframe['astro_score'] >= 70) &
                (dataframe['rsi'] < 40) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['exit_long'] = 0
        
        # Salida Astral: Vender si el cosmos se vuelve desfavorable (<30)
        dataframe.loc[
            (
                (dataframe['astro_score'] <= 30)
            ),
            'exit_long'] = 1

        return dataframe

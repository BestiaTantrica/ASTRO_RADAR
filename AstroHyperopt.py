import pandas as pd
import numpy as np
from datetime import datetime
from freqtrade.strategy import IStrategy, IntParameter
import os

class AstroHyperopt(IStrategy):
    """
    ========================================================
             ASTRO-QUANTUM DATA ENGINE - HYPEROPT V1
    ========================================================
    Estrategia de Machine Learning para descubrir el peso real 
    de cada tránsito astrológico sobre cada moneda individual.
    """
    
    INTERFACE_VERSION = 3
    timeframe = '1h'
    can_short = False
    
    minimal_roi = {
        "0": 0.10,
        "120": 0.05,
        "240": 0
    }
    stoploss = -0.05

    # ====================================================
    # ESPACIO DE BÚSQUEDA HYPEROPT (LA MAGIA)
    # La IA probará millones de combinaciones de estos pesos
    # ====================================================
    
    # Pesos planetarios (¿Qué tanto afecta un tránsito?)
    # Rango de -50 (Super Bearish) a +50 (Super Bullish)
    w_jupiter = IntParameter(-50, 50, default=25, space="buy", optimize=True)
    w_saturn = IntParameter(-50, 50, default=-20, space="buy", optimize=True)
    w_mars = IntParameter(-50, 50, default=-15, space="buy", optimize=True)
    w_venus = IntParameter(-50, 50, default=15, space="buy", optimize=True)
    w_mercury = IntParameter(-50, 50, default=10, space="buy", optimize=True)
    
    # Umbral mínimo para comprar
    buy_threshold = IntParameter(10, 100, default=70, space="buy", optimize=True)
    
    # Filtro Técnico (Gatillo)
    buy_rsi = IntParameter(20, 60, default=40, space="buy", optimize=True)

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        pair = metadata.get('pair', '')
        symbol = pair.split('/')[0]
        
        # Cargar los CSVs actualizados con los tránsitos crudos
        csv_path = f"/home/ubuntu/CHACAL_LATERAL_AWS/user_data/data/binance/{symbol}_USDT_1h_with_scores.csv"
        
        if os.path.exists(csv_path):
            try:
                df_scores = pd.read_csv(csv_path)
                df_scores['date'] = pd.to_datetime(df_scores['datetime']).dt.tz_localize('UTC')
                
                # Nos traemos TODAS las columnas de tránsitos
                columnas = ['date', 'jupiter_trine', 'saturn_square', 'mars_opp', 'venus_conj', 'mercurio_sextil']
                df_scores = df_scores[columnas]
                
                dataframe['date'] = pd.to_datetime(dataframe['date'])
                dataframe = pd.merge(dataframe, df_scores, on='date', how='left')
                
                # Rellenar con 0 donde no hay tránsito
                for col in columnas[1:]:
                    dataframe[col] = dataframe[col].fillna(0)
                    
            except Exception as e:
                print(f"Error cargando transitos para {symbol}: {e}")
                for col in ['jupiter_trine', 'saturn_square', 'mars_opp', 'venus_conj', 'mercurio_sextil']:
                    dataframe[col] = 0
        else:
            print(f"ATENCIÓN: No se encontró CSV para {symbol}.")
            for col in ['jupiter_trine', 'saturn_square', 'mars_opp', 'venus_conj', 'mercurio_sextil']:
                dataframe[col] = 0

        # Indicador Técnico
        import talib.abstract as ta
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['enter_long'] = 0
        
        # Calcular el Score Dinámico basado en los parámetros del Hyperopt actual
        # Base 50 + (Tránsito * Peso de Hyperopt)
        score_dinamico = 50 + (
            (dataframe['jupiter_trine'] * self.w_jupiter.value) +
            (dataframe['saturn_square'] * self.w_saturn.value) +
            (dataframe['mars_opp'] * self.w_mars.value) +
            (dataframe['venus_conj'] * self.w_venus.value) +
            (dataframe['mercurio_sextil'] * self.w_mercury.value)
        )
        
        # Comprar si el score dinámico supera el umbral y el RSI está en zona de gatillo
        dataframe.loc[
            (
                (score_dinamico >= self.buy_threshold.value) &
                (dataframe['rsi'] < self.buy_rsi.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['exit_long'] = 0
        
        # Para el hyperopt, la salida la dejamos fija por ROI o StopLoss por ahora,
        # para que la IA se concentre 100% en optimizar la ENTRADA planetaria.
        return dataframe

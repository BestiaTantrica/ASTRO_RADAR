import ccxt
import pandas as pd
import os
from datetime import datetime, timedelta
import time

def download_ohlcv(symbol, timeframe='1h', years=3):
    # Configurar CCXT para usar el proxy SOCKS5 de Oracle B
    exchange = ccxt.binance({
        'proxies': {
            'http': 'socks5h://127.0.0.1:1080',
            'https': 'socks5h://127.0.0.1:1080',
        },
    })
    
    since = exchange.parse8601((datetime.now() - timedelta(days=365 * years)).isoformat())
    all_ohlcv = []
    
    print(f"Descargando {symbol}...")
    
    symbol_path = symbol.replace('/', '_')
    filename = f"datos/{symbol_path}_{timeframe}.csv"
    os.makedirs('datos', exist_ok=True)
    
    while since < exchange.milliseconds():
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
            if not ohlcv:
                break
            since = ohlcv[-1][0] + 1
            all_ohlcv += ohlcv
            print(f"  {symbol}: {len(all_ohlcv)} velas descargadas...")
            
            if len(all_ohlcv) % 5000 == 0:
                df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df.to_csv(filename, index=False)
                
            time.sleep(exchange.rateLimit / 1000)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv(filename, index=False)
    print(f"Finalizado {symbol}. Guardado en {filename}")

if __name__ == "__main__":
    pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'BNB/USDT', 'NEAR/USDT']
    for p in pairs:
        download_ohlcv(p)

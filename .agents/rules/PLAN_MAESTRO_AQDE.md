# PLAN MAESTRO DEFINITIVO: ASTRO-QUANTUM DATA ENGINE (AQDE) v2.0

> Proyecto: AQDE — Motor de Inteligencia Astro-Cripto
> Infraestructura: Oracle A + Oracle B + PC local/WSL
> AWS Chacal (Brazil): INTOCABLE — opera independiente con baja latencia
> Ultima actualizacion: 2026-04-30

---

## MAPA CONCEPTUAL

```
+------------------------------------------------------------------+
|                    ECOSISTEMA AQDE                               |
|                                                                  |
|  [PC LOCAL / WSL]                                                |
|   Backtesting, Hyperopt, Desarrollo, CapCut (videos manual)      |
|                                                                  |
|  [ORACLE A: CEREBRO 129.213.77.194]                              |
|   +-- Swiss Ephemeris (pyswisseph)                               |
|   +-- Scraper: AstroSeek + CoinDesk + Reddit                     |
|   +-- Motor de Score Astral (JSON cada 4h)                       |
|   +-- Generador Horoscopo Poetico (Groq)                         |
|   +-- Bot Social IG/TikTok/YouTube (anti-ban)                    |
|   +-- API Flask puerto 5000 (/api/senal)                         |
|           |                                                      |
|           v  senales JSON cada 4h                                |
|  [ORACLE B: MUSCULO 129.80.104.116]                              |
|   +-- FreqTrade (sin Docker, ARM)                                |
|   +-- AstroStrategy.py                                           |
|   +-- Binance API (dry-run -> real)                              |
|   +-- UI puerto 8080                                             |
|           |                                                      |
|           v                                                      |
|   [REDES SOCIALES] IG + TikTok + YouTube + Facebook              |
|   X = manual por ahora (API paga)                                |
|                                                                  |
|  [AWS CHACAL - BRAZIL] --- NO SE TOCA ---                        |
|   Chacal Bear/Bull estrategia de precision baja latencia         |
+------------------------------------------------------------------+
```

---

## REGLAS DE ORO (toda IA que tome este proyecto las sigue sin excepcion)

1. AMBOS servidores son Oracle Cloud. AWS es SOLO para Chacal Brazil.
2. NO inventar data. Si el scraper falla: registrar el error, esperar, no rellenar con basura.
3. NO tocar AWS Chacal. Nunca.
4. Siempre verificar rutas con `ls` antes de reiniciar servicios en el servidor.
5. Siempre leer logs: `journalctl -u nombre-servicio -n 30` despues de cada deploy.
6. Cada modulo tiene su propio venv, su propio .env y su carpeta limpia.
7. Backtest y Hyperopt SIEMPRE en PC local con WSL. Nunca en instancias Oracle.
8. Dry-run obligatorio minimo 2 semanas antes de capital real en Binance.
9. X (Twitter) API queda manual (requiere pago). Solo automatizar lo gratuito.
10. Cada modulo funciona de forma independiente. Sin dependencias circulares.
11. Antes de terminar cada sesion, actualizar ESTADO_SISTEMA.md con lo hecho y lo pendiente.

---

## INFRAESTRUCTURA

### Oracle A — IP: 129.213.77.194 — CEREBRO ASTRAL

```
RAM: 1 GB + 2 GB SWAP (activa)
CPU: 1 OCPU ARM Ampere
OS: Ubuntu 20.04
Carpeta principal: /home/ubuntu/aqde-cerebro/
Estructura:
  aqde-cerebro/
    venv/                  <- entorno Python aislado
    scrapers/              <- scraper_astro.py
    motores/               <- astro_engine.py, score_engine.py, horoscopo_engine.py
    contenido/             <- cola de publicacion por red social
    datos/                 <- OHLCV historico, efemerides descargadas
    logs/                  <- logs de cada proceso
    resultados/            <- senales JSON generadas
    app.py                 <- Flask API puerto 5000
    .env                   <- tokens (Groq, Reddit, IG, Binance)
    astro-cerebro.service  <- systemd
SSH: ssh -i C:\fractal-mind\ssh-key-2026-02-16.key ubuntu@129.213.77.194
Estado actual (2026-04-30): Limpio. Estructura creada. Venv listo. Instalando paquetes.
```

### Oracle B — IP: 129.80.104.116 — MOTOR OPERATIVO

```
RAM: 1 GB + 2 GB SWAP (pendiente activar)
CPU: 1 OCPU AMD E2 Micro
OS: Ubuntu 20.04
Carpeta principal: /home/ubuntu/aqde-trading/
Estructura:
  aqde-trading/
    ft_userdata/           <- FreqTrade userdir
      strategies/          <- AstroStrategy.py
      data/                <- OHLCV para backtest
    venv/
    .env                   <- Binance API Key
    freqtrade.service      <- systemd
UI: http://129.80.104.116:8080
SSH: PENDIENTE (clave actual da Permission denied, necesita la clave correcta)
Estado actual (2026-04-30): PENDIENTE ACCESO
```

### PC Local — Windows + WSL Ubuntu

```
Uso: Backtesting pesado, Hyperopt, desarrollo, CapCut para videos manuales
FreqTrade instalado en WSL para backtests locales
Carpeta local: C:\SCRAP\ASTRO_RADAR\
```

### Script Setup Base (ejecutar en AMBAS instancias Oracle una sola vez)

```bash
# SWAP 2GB (si no esta activa)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo "vm.swappiness=60" | sudo tee -a /etc/sysctl.conf

# Proteccion anti-apagado
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# Verificar
free -h && swapon --show
```

---

## MODULO 1: CEREBRO ASTRAL (Oracle A) — PRIORIDAD MAXIMA

Todo lo demas depende de este modulo. Sin datos astrologicos cruzados, no hay horoscopo ni senal de trading.

### 1.1 astro_engine.py — Motor de Efemerides

Libreria: pyswisseph (Swiss Ephemeris, estandar de la industria astrologica)
Nota: pyswisseph requiere compilacion en ARM. Alternativa si falla: ephem o astropy.

Cartas Natales Hardcodeadas (son fijas, nunca cambian):

```python
CARTAS_NATALES = {
    "BTC":  {"fecha": "2009-01-03", "hora": "18:15", "tz": "UTC", "signo": "Capricornio"},
    "ETH":  {"fecha": "2015-07-30", "hora": "03:26", "tz": "UTC", "signo": "Leo"},
    "SOL":  {"fecha": "2020-03-16", "hora": "00:00", "tz": "UTC", "signo": "Piscis"},
    "XRP":  {"fecha": "2012-06-02", "hora": "00:00", "tz": "UTC", "signo": "Geminis"},
    "BNB":  {"fecha": "2017-07-25", "hora": "00:00", "tz": "UTC", "signo": "Leo"},
    "NEAR": {"fecha": "2020-10-13", "hora": "00:00", "tz": "UTC", "signo": "Libra"},
}
```

Funciones a implementar:
- get_posicion_planeta(planeta, fecha_dt) -> dict con grados y signo
- get_transitos_hoy(carta_natal) -> lista de aspectos activos hoy
- get_sinastria_par(activo_a, activo_b) -> aspectos entre dos cartas natales
- get_comparacion_historica(transito_descripcion, activo, df_ohlcv) -> fechas similares + retorno %

Aspectos a calcular (umbral de orbe 5 grados):
- Conjuncion (0 grados): fusion de energias
- Sextil (60 grados): armonia, oportunidad
- Cuadratura (90 grados): tension, volatilidad
- Trigono (120 grados): fluidez, tendencia sostenida
- Oposicion (180 grados): polaridad, punto de inflexion

### 1.2 scraper_astro.py — Fuentes de Datos

| Fuente | Extrae | Metodo | Frecuencia |
|--------|--------|--------|------------|
| AstroSeek.com | Transitos del dia, aspectos activos | Playwright headless, sin imagenes ni CSS | 06:00 UTC diario |
| CoinDesk.com | Headlines cripto del dia | requests + BeautifulSoup | Cada 4h |
| Reddit r/CryptoCurrency | Top 10 posts, sentimiento (score PRAW) | PRAW API (gratuita) | Cada 4h |
| Binance via CCXT | OHLCV 1h ultimos 3 anios BTC/ETH/SOL/XRP/BNB | ccxt.binance() | Una sola vez + incremental diario |
| Lunar API gratuita | Fase lunar actual, signo de la luna | requests JSON (varios endpoints gratuitos) | Diario |

Nota sobre Playwright: usar modo stealth, bloquear imagenes/fuentes/CSS para ahorrar RAM.
Nota sobre X: API paga, omitir. El usuario publicara manualmente en X.

### 1.3 score_engine.py — Score Astral 0-100

Formula:
```
Score = (Aspectos_Favorables_Hoy * 0.40)
      + (Sentimiento_Reddit_Noticias * 0.30)
      + (Comparacion_Historica_Precio * 0.30)
```

Pesos de aspectos planetarios:
| Aspecto | Tipo | Puntos |
|---------|------|--------|
| Trigono Jupiter sobre Sol natal | Armonico | +25 |
| Conjuncion Venus sobre Sol natal | Armonico | +15 |
| Sextil Mercurio sobre Sol natal | Armonico | +10 |
| Luna Nueva en signo natal | Oportunidad | +10 |
| Luna Llena en signo natal | Emocion/pico | +8 |
| Cuadratura Saturno | Tenso | -20 |
| Oposicion Marte | Tenso | -15 |
| Cuadratura Pluton | Tenso | -12 |
| Eclipse Solar/Lunar | Volatilidad extrema | +-30 |
| Mercurio Retrogrado | Confusion/errores | -10 |

Sinastria de Pares (para operar pares como BTC/ETH):
- Cruzar cartas natales de los dos activos del par
- Trigono o Sextil entre ellas = alta correlacion esperada = par se mueve junto
- Cuadratura u Oposicion = divergencia esperada = par se mueve en sentidos opuestos
- Esto sirve para hedging o para operar el ratio del par

Carta Personal del Usuario (producto premium):
- El usuario ingresa fecha, hora y ciudad de nacimiento
- El sistema calcula su carta natal con pyswisseph
- Cruza su carta con los transitos del dia
- Genera recomendacion personalizada: "Tu Marte esta siendo activado hoy. Momento de accion. Confianza media-alta."
- Esto es un servicio vendible a otros usuarios tambien

JSON de senal (publicado en /api/senal cada 4h):
```json
{
  "asset": "BTC",
  "timestamp": "2026-04-30T12:00:00Z",
  "score": 78,
  "bias": "LONG",
  "confianza": "ALTA",
  "transito_activo": "Jupiter trigono Sol natal BTC",
  "fase_lunar": "Luna Creciente en Tauro",
  "sinastria_btc_eth": "Trigono activo — correlacion alta esperada",
  "comparacion_historica": "Nov 2021: transito similar → BTC +180% en 4 meses",
  "nota_estratega": "Sesgo alcista moderado. Esperar confirmacion tecnica para entrar."
}
```

### 1.4 horoscopo_engine.py — Generador de Contenido

FILOSOFIA DEL CONTENIDO (definida por el usuario, no negociable):
- Tono: poetico, emotivo, resonante. No cursi, no agresivo, no criminal.
- Arquetipico: cada signo tiene su imagen arquetipica. Capricornio = el estratega. Leo = el rey. Escorpio = la transformacion. Etc.
- Basado en datos reales del dia: el texto lo genera Groq usando el JSON de transitos del dia.
- Cripto-consciente: menciona las energias del mercado de forma simbolica, sin ser explicitamente financiero (evita bans de plataformas).
- Referencia de estilo y tono: tiktok.com/@portaltarotmistico

Motor de generacion:
```python
transitos = astro_engine.get_transitos_hoy()
sentimiento = scraper.get_sentimiento_reddit()
prompt = f"""
Eres un astrologo poetico y estratega. Con base en estos transitos: {transitos}
y este sentimiento del mercado: {sentimiento},
escribe el horoscopo de {signo} para hoy.
Tono: poetico, arquetipico, emotivo pero no cursi. Maximo 150 palabras.
Incluye una frase sobre como la energia cosmica se manifiesta en las decisiones de hoy.
"""
texto = groq_client.chat(prompt)
```

Tipos de contenido generado automaticamente:
1. Horoscopo Diario por Signo: 12 posts por dia, uno por signo (formato para IG y TikTok)
2. Energia del Dia: 1 post general sobre el transito planetario mas importante del dia
3. Sinastria Cripto: analisis del par del dia (ej: "BTC y ETH forman un trigono hoy...")
4. Alerta de Transito Mayor: cuando hay eclipses, Mercurio retrogrado, Saturno cuadratura, etc.
5. Comparacion Historica Viral: "La ultima vez que Marte estuvo aqui, esto paso..." (formato enganche)

Videos: el usuario los hace en CapCut con el texto generado. El bot solo sube y programa.
Si en el futuro se tiene suscripcion a generador de imagenes/video, se automatiza la creacion tambien.

---

## MODULO 2: BOT SOCIAL (Oracle A) — bot_social.py

Objetivo: no solo publicar. Responder, interactuar y viralizar de forma estrategica sin ban.

Reglas anti-ban (NO NEGOCIABLES):
- Maximo 30 acciones por hora en IG (likes + comentarios + respuestas combinados)
- Delays aleatorios entre 45 segundos y 3 minutos entre cada accion
- Nunca repetir el mismo texto de comentario dos veces seguidas
- Nunca seguir o dejar de seguir en masa (maximo 5 por hora)
- Nunca usar palabras en lista negra de cada plataforma

Estrategia de viralizacion:
1. Responder comentarios con contenido de valor + pregunta de engagement al final
2. Comentar en cuentas grandes de astrologia con respuestas que sumen valor
3. Stories con encuestas: "Tu signo es compatible con BTC?", "Cual es tu cripto segun tu signo?"
4. Likes en posts relacionados de cuentas con alta actividad (no de competidores directos)

Plataformas:
| Red | Metodo de publicacion | Metodo de interaccion | Costo |
|-----|----------------------|-----------------------|-------|
| Instagram | Graph API (Meta for Dev) | Graph API comments/likes | Gratis |
| TikTok | Playwright headless (no oficial) | Playwright headless | Gratis |
| YouTube Shorts | YouTube Data API v3 | YouTube API comentarios | Gratis |
| Facebook | Auto por integracion con IG | Auto | Gratis |
| X Twitter | MANUAL por ahora | MANUAL | API = pago |

---

## MODULO 3: BOT DE TRADING (Oracle B) — FreqTrade + AstroStrategy

### Instalacion FreqTrade en Oracle B (ARM, sin Docker)

```bash
sudo apt-get install -y python3-pip python3-venv python3-dev build-essential
mkdir ~/aqde-trading && cd ~/aqde-trading
python3 -m venv venv && source venv/bin/activate
pip install freqtrade
freqtrade create-userdir --userdir ft_userdata
```

### AstroStrategy.py — Logica de Entrada

```python
import requests
from freqtrade.strategy import IStrategy
import talib.abstract as ta

class AstroStrategy(IStrategy):
    minimal_roi = {"0": 0.05}
    stoploss = -0.03
    timeframe = '1h'

    def get_senal_astral(self, asset: str) -> dict:
        try:
            r = requests.get(f"http://129.213.77.194:5000/api/senal?asset={asset}", timeout=5)
            return r.json()
        except:
            return {"score": 50, "bias": "NEUTRO"}

    def populate_entry_trend(self, df, metadata):
        senal = self.get_senal_astral(metadata['pair'].split('/')[0])
        score = senal.get('score', 50)
        bias = senal.get('bias', 'NEUTRO')

        df['rsi'] = ta.RSI(df, timeperiod=14)
        df['ema_fast'] = ta.EMA(df, timeperiod=9)
        df['ema_slow'] = ta.EMA(df, timeperiod=21)
        confirmacion = (df['rsi'] < 40) | (df['ema_fast'] > df['ema_slow'])

        df.loc[(score >= 70) & (bias == 'LONG') & confirmacion, 'enter_long'] = 1
        return df

    def populate_exit_trend(self, df, metadata):
        senal = self.get_senal_astral(metadata['pair'].split('/')[0])
        score = senal.get('score', 50)
        df.loc[score <= 30, 'exit_long'] = 1
        return df
```

Regla de entrada resumida:
- LONG: Score >= 70 AND bias LONG AND (RSI < 40 OR cruce EMA bullish)
- EXIT: Score <= 30 (el cosmos dice que es momento de salir)
- NEUTRO 31-69: no entrar, solo gestionar posicion existente

Pares operados: BTC/USDT, ETH/USDT, SOL/USDT (los que tienen carta natal definida)
Timeframe: 1h (compatible con actualizacion de senal cada 4h)

### Flujo de Desarrollo Obligatorio

1. Backtest en PC/WSL con OHLCV historico 3 anios
2. Reconstruir scores astrales historicos con pyswisseph para esos 3 anios
3. Hyperopt en WSL para encontrar el umbral de score optimo (60? 65? 70?)
4. Deploy AstroStrategy en Oracle B modo dry-run
5. Minimo 2 semanas dry-run antes de capital real
6. Capital real: monto minimo para validar, escalar gradualmente

---

## PROTOCOLO DE MEMORIA MULTI-IA

OBLIGATORIO. Cualquier IA que trabaje en este proyecto debe:

1. ANTES de empezar: leer C:\SCRAP\ASTRO_RADAR\ESTADO_SISTEMA.md y PENDIENTES.md
2. DURANTE el trabajo: actualizar PENDIENTES.md cuando complete tareas
3. AL TERMINAR: actualizar ESTADO_SISTEMA.md con la sesion actual:
   - Que se hizo
   - Que quedo pendiente
   - Que NO funciona y por que
   - Proximo paso exacto para la siguiente IA

Archivos de seguimiento:
- C:\SCRAP\ASTRO_RADAR\ESTADO_SISTEMA.md
- C:\SCRAP\ASTRO_RADAR\PENDIENTES.md
- C:\SCRAP\ASTRO_RADAR\PLAN_MAESTRO_AQDE.md (este archivo)

---

## ROADMAP EJECUTABLE POR FASES

### FASE 0 — Limpieza y Setup (COMPLETADA PARCIALMENTE 2026-04-30)

- [x] IP Oracle B confirmada: 129.80.104.116
- [x] Servicios radar-web y radar-autonomo detenidos en Oracle A
- [x] Estructura /home/ubuntu/aqde-cerebro/ creada en Oracle A
- [x] Venv Python creado en Oracle A
- [ ] Instalar pyswisseph en Oracle A (necesita compilacion)
- [ ] Resolver acceso SSH a Oracle B (clave actual da Permission denied)
- [ ] Activar SWAP en Oracle B
- [ ] Crear estructura /home/ubuntu/aqde-trading/ en Oracle B

### FASE 1 — Motor Astral + Datos (Semana 1) [Oracle A]

- [ ] Instalar todas las dependencias (ver lista mas abajo)
- [ ] Implementar astro_engine.py completo
- [ ] Implementar scraper_astro.py (AstroSeek + CoinDesk + Reddit)
- [ ] Descargar historico OHLCV 3 anios BTC/ETH/SOL desde Binance via CCXT
- [ ] Implementar score_engine.py
- [ ] Publicar /api/senal en Flask puerto 5000
- [ ] Test: curl http://129.213.77.194:5000/api/senal?asset=BTC

### FASE 2 — Backtesting Astral (Semana 1-2) [PC LOCAL / WSL]

- [ ] Instalar FreqTrade en WSL
- [ ] Reconstruir scores astrales historicos 3 anios con pyswisseph
- [ ] Backtest AstroStrategy con datos historicos
- [ ] Hyperopt para afinar umbral de score
- [ ] Documentar resultados en C:\SCRAP\ASTRO_RADAR\resultados_backtest\

### FASE 3 — Horoscopo + Redes (Semana 2) [Oracle A]

- [ ] Usuario consigue Groq API Key en console.groq.com
- [ ] Implementar horoscopo_engine.py
- [ ] Usuario configura Instagram Graph API en Meta for Developers
- [ ] Usuario configura YouTube Data API v3 en Google Cloud Console
- [ ] Implementar bot_social.py con reglas anti-ban
- [ ] Cron para publicacion diaria automatica 09:00 UTC

### FASE 4 — FreqTrade en Oracle B (Semana 3) [Oracle B]

- [ ] Resolver acceso SSH Oracle B
- [ ] Activar SWAP y proteccion anti-apagado en Oracle B
- [ ] Instalar FreqTrade
- [ ] Subir AstroStrategy.py
- [ ] Configurar Binance API sin permiso de retiro
- [ ] Dry-run 2 semanas

### FASE 5 — Monetizacion (Mes 2+)

- [ ] Canal VIP Telegram con senales premium
- [ ] PDF Sinastria Cripto personalizada por encargo
- [ ] Carta personal del usuario servicio de consulta paga
- [ ] Suscripciones via Mercado Pago (token ya disponible en .env viejo)

---

## TOKENS Y CREDENCIALES

| Servicio | Estado | Como obtener |
|----------|--------|--------------|
| Groq API Key | PENDIENTE USUARIO | console.groq.com — gratis |
| Instagram Graph API | PENDIENTE USUARIO | developers.facebook.com |
| YouTube Data API v3 | PENDIENTE USUARIO | console.cloud.google.com |
| Reddit PRAW | PENDIENTE IA | reddit.com/prefs/apps — gratis |
| Binance API Key | PENDIENTE USUARIO | binance.com/api-management — SIN retiro |
| X API | OMITIR | Pago — manual por ahora |
| Mercado Pago | ACTIVO | Ya en .env del proyecto inmobiliario |
| Telegram Bot | ACTIVO | Ya en .env de Chacal |

---

## DEPENDENCIAS A INSTALAR EN ORACLE A

```bash
cd ~/aqde-cerebro && source venv/bin/activate

# Base
pip install flask requests pandas ccxt groq praw beautifulsoup4 python-dotenv

# Astrologia (probar en orden, usar la primera que compile en ARM)
pip install pyswisseph  # Primera opcion, puede fallar en ARM
pip install ephem       # Segunda opcion, mas liviana
pip install astropy     # Tercera opcion si las anteriores fallan

# Playwright para scraping stealth
pip install playwright
playwright install chromium --with-deps

# APScheduler para tareas periodicas
pip install apscheduler
```

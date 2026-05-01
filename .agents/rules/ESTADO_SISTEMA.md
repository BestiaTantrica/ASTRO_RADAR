# ESTADO DEL SISTEMA AQDE

## Infraestructura

| Servidor | IP | Rol | Estado |
|---|---|---|---|
| Oracle A | 129.213.77.194 | Cerebro Astral | LIMPIO Y CONFIGURADO |
| Oracle B | 129.80.104.116 | Motor FreqTrade | LIMPIO Y CONFIGURADO |
| AWS Chacal | - | Chacal Bear/Bull Brazil | INTOCABLE |
| PC Local | - | Backtest/Hyperopt/WSL | DISPONIBLE |

## Estado de Modulos

| Modulo | Archivo | Estado |
|---|---|---|
| Motor Astral | astro_engine.py | COMPLETADO |
| Scraper Fuentes | scraper_astro.py | COMPLETADO |
| Score Engine | score_engine.py | COMPLETADO |
| Horoscopo Engine | horoscopo_engine.py | COMPLETADO |
| Bot Social | bot_social.py | PENDIENTE |
| AstroStrategy FreqTrade | AstroStrategy.py | PENDIENTE |
| API Flask senal | app.py | COMPLETADO (puerto 5000) |

## Sesion 2026-04-30 (Cont.)

### Hecho:
- **Resuelto bloqueo de Binance**: Se descargaron los 3 años de datos OHLCV usando el proxy de Oracle B -> AWS Brazil.
- **Datos Sincronizados**: Los CSVs de BTC, ETH, SOL, XRP, BNB y NEAR ya están en Oracle A y PC Local.
- **Groq API Key**: Integrada en `.env` de Oracle A.
- **Motor de Horóscopo**: `horoscopo_engine.py` operativo con Llama 3.3 70B (Groq). Genera contenido poético y cripto-consciente.
- **Fase 1 FINALIZADA**: Todo el Cerebro Astral tiene sus motores base listos.
- **Auditoría de Documentación**: Se limpiaron `MACRO_STANDARDS.md` y `PROMPT_RULES_GLOBAL.md` eliminando rastros de proyectos viejos (Inmobiliaria) y enfocando todo el ecosistema en AQDE.
- **Configuración WSL**: Iniciada la instalación de FreqTrade y sincronización de CSVs en el entorno local.

### Pendiente:
- Configurar Bot Social (IG/TikTok/YouTube).
- FASE 2: Iniciar reconstrucción de scores históricos para backtesting local (WSL).

### Proximo paso exacto:
1. Configurar FreqTrade en WSL local y mover los datos para el backtest.



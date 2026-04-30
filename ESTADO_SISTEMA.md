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
| Motor Astral | astro_engine.py | PENDIENTE |
| Scraper Fuentes | scraper_astro.py | PENDIENTE |
| Score Engine | score_engine.py | PENDIENTE |
| Horoscopo Engine | horoscopo_engine.py | PENDIENTE |
| Bot Social | bot_social.py | PENDIENTE |
| AstroStrategy FreqTrade | AstroStrategy.py | PENDIENTE |

## Sesion 2026-04-30

### Hecho:
- Plan Maestro AQDE v2 redactado.
- Oracle A limpio y con dependencias listas.
- Oracle B limpio y conexión SSH exitosa con llave-sao-paulo.pem.
- Git inicializado.

### Pendiente:
- Conseguir clave SSH correcta para Oracle B (o generar nueva desde consola Oracle)
- Bajar servicios radar-web y radar-autonomo en Oracle A
- Limpiar carpeta radar-inmobiliario en Oracle A
- Crear estructura /home/ubuntu/aqde-cerebro/ en Oracle A
- Instalar dependencias AQDE en Oracle A

### Proximo paso exacto:
1. Usuario verifica que clave para Oracle B es distinta a C:\fractal-mind\ssh-key-2026-02-16.key
2. Arrancar limpieza Oracle A mientras tanto

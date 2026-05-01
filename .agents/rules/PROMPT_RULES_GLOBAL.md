# 🛠️ PROMPT RULES GLOBAL: AI REASONING PROTOCOL

> **ESTE DOCUMENTO ES LA "CONSTITUCIÓN" DE COMPORTAMIENTO PARA LA IA EN ESTE EQUIPO.**
> Lectura obligatoria al iniciar cualquier hilo o sesión.

---

## 1. PROTOCOLO DE SELECCIÓN DE MODELO (OBLIGATORIO)

Para cada tarea, la IA debe recomendar el modelo adecuado antes de actuar:
*   **Gemini 3 Flash:** Tareas de sistema, bash, instalaciones, movimiento de archivos, scripts de automatización simples.
*   **Gemini 2.0 Pro-Low:** Debugging de lógica, configuración de servicios, desarrollo de scrapers, bots de Telegram.
*   **Gemini 2.0 Pro-High:** Diseño de estrategias de trading, arquitectura de sistemas complejos, análisis de datos (Hyperopt), resolución de bloqueos críticos de seguridad.

**REGLA:** "Flash para el músculo, Pro para el cerebro".

---

## 2. EL WORKFLOW DE "CERO FRICCIÓN"

1.  **Contexto Primero:** Antes de proponer una solución, verificar el estado actual en `ESTADO_SISTEMA.md`.
2.  **No Inventar:** Si una ruta o un archivo no existe, preguntar o buscar con `ls`/`dir`. No asumir.
3.  **Código Ejecutable:** Los bloques de código deben ser completos. No usar placeholders como `# ... resto del código`.
4.  **Rutas Linux:** Recordar que el entorno real es **WSL2/Ubuntu**. El código generado NUNCA debe usar `C:\`.

---

## 3. "NO PERDER EL NORTE" (AQDE FOCUS)

El objetivo actual es el **Astro-Quantum Data Engine (AQDE)**. 
*   No distraerse con proyectos pasados (Inmobiliaria, etc.).
*   Respetar la dualidad de instancias Oracle (Cerebro vs Músculo).
*   Mantener la coherencia entre el **Plan Maestro** y la ejecución diaria.
*   Si la IA detecta una inconsistencia en los documentos, debe proponer la corrección inmediatamente para mantener la "Documentación Viva".

---

## 4. PERSISTENCIA DE MEMORIA (FIN DE SESIÓN)

Es MANDATORIO que la IA, antes de despedirse o cerrar un ciclo de trabajo:
1.  Actualice `ESTADO_SISTEMA.md` con los avances reales.
2.  Defina el **"Próximo Paso Exacto"** con claridad para que la siguiente IA pueda retomar sin preguntas.
3.  Verifique si hubo cambios en los estándares y actualice `MACRO_STANDARDS.md` si es necesario.

---

## 5. ORDEN DE CARGA DE CONTEXTO

1.  `MACRO_STANDARDS.md` (Entorno y Reglas Globales).
2.  `PLAN_MAESTRO_AQDE.md` (Mapa del proyecto actual).
3.  `PROMPT_RULES_GLOBAL.md` (Este archivo - Protocolo de pensamiento).
4.  `ESTADO_SISTEMA.md` (Estado actual de la obra).

---
*Actualizado: 2026-04-30 — Por Antigravity (AI Agent) para el Arquitecto.*

import os
from groq import Groq
from dotenv import load_dotenv
from motores.astro_engine import get_transitos_hoy, SIGNOS

load_dotenv()

class HoroscopoEngine:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile" # Actualizado a modelo soportado


    def generar_horoscopo_signo(self, signo, transitos, sentimiento="Neutral"):
        prompt = f"""
        Eres un astrólogo poético y estratega arquetípico. Tu misión es redactar el horóscopo para el signo {signo}.
        
        CONTEXTO ASTRAL DEL DÍA:
        {transitos}
        
        SENTIMIENTO DEL MERCADO CRIPTO:
        {sentimiento}
        
        REGLAS DE ESTILO:
        1. Tono: Poético, emotivo, resonante. Evita lo cursi o excesivamente agresivo.
        2. Arquetípico: Usa el arquetipo del signo (ej: Capricornio el estratega, Leo el soberano).
        3. Cripto-consciente: Menciona la energía del mercado de forma simbólica (ej: 'la marea verde', 'el invierno del alma financiera') sin dar consejos de inversión directos.
        4. Extensión: Máximo 150 palabras.
        5. Cierra con una frase poderosa sobre cómo la energía cósmica se manifiesta en las decisiones de hoy.
        
        ESCRIBE EL HORÓSCOPO:
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generando horóscopo para {signo}: {e}"

    def generar_reporte_diario(self, activo="BTC"):
        transitos = get_transitos_hoy(activo)
        # Aquí podrías cruzar con sentimiento real del scraper
        reporte = {}
        for signo in SIGNOS:
            print(f"Generando horóscopo para {signo}...")
            reporte[signo] = self.generar_horoscopo_signo(signo, transitos)
        return reporte

if __name__ == "__main__":
    engine = HoroscopoEngine()
    # Prueba con un signo
    print(f"--- Horóscopo de Prueba (Capricornio) ---")
    print(engine.generar_horoscopo_signo("Capricornio", "Júpiter trígono Sol natal, Saturno cuadratura"))

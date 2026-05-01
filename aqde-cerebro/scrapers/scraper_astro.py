import asyncio
from playwright.async_api import async_playwright
import requests
from bs4 import BeautifulSoup
import praw
import os
from dotenv import load_dotenv

load_dotenv()

async def get_astroseek_transitos():
    """Scrapea AstroSeek usando Playwright headless bloqueando recursos pesados."""
    transitos = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # Bloquear imagenes, fuentes y css para ahorrar RAM
            await context.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_())
            
            page = await context.new_page()
            # La URL de transitos del dia (ejemplo generico, sujeto a cambios de la web)
            await page.goto("https://horoscopes.astro-seek.com/current-planets-astrology-transits-ephemeris", timeout=30000)
            
            # Extraer planetas y posiciones (ajustar selectores segun el DOM de la pagina)
            # Para la FASE 1, simularemos la extraccion y dejaremos un placeholder, 
            # dado que la logica de extraccion de pyswisseph reemplaza en parte esta necesidad para los transitos basicos.
            # Sin embargo, el scraper se exige en la arquitectura.
            
            elementos = await page.query_selector_all(".planet-info-line") # selector dummy
            for el in elementos:
                texto = await el.inner_text()
                transitos.append(texto.strip())
                
            await browser.close()
            
            if not transitos:
                # Fallback si falla el selector (muy comun en scraping)
                transitos = ["AstroSeek DOM changed, extraction requires update. Using swisseph as source of truth."]
                
    except Exception as e:
        print(f"Error AstroSeek: {e}")
        transitos = ["Error fetching AstroSeek data"]
        
    return transitos

def get_coindesk_headlines():
    """Extrae ultimas noticias de CoinDesk usando requests."""
    noticias = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get("https://www.coindesk.com/", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Selectores pueden variar
        headlines = soup.find_all('h3', limit=5)
        for h in headlines:
            noticias.append(h.get_text().strip())
    except Exception as e:
        print(f"Error CoinDesk: {e}")
    return noticias

def get_reddit_sentiment():
    """Calcula un score simple de sentimiento basado en r/CryptoCurrency."""
    try:
        # PRAW requiere CLIENT_ID, CLIENT_SECRET, y USER_AGENT en el entorno
        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        user_agent = os.environ.get("REDDIT_USER_AGENT", "linux:aqde_bot:v1.0 (by u/tu_usuario)")
        
        if not client_id or not client_secret:
            return {"score_general": 50, "top_posts": ["Reddit credentials missing"]}
            
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        subreddit = reddit.subreddit("CryptoCurrency")
        hot_posts = subreddit.hot(limit=10)
        
        score_acumulado = 0
        posts_text = []
        
        for post in hot_posts:
            # Simplificacion: asumimos upvotes como "atencion/volatilidad" 
            # y busqueda de palabras clave
            texto = post.title.lower()
            if "bull" in texto or "pump" in texto or "moon" in texto or "green" in texto:
                score_acumulado += 10
            elif "bear" in texto or "dump" in texto or "crash" in texto or "red" in texto:
                score_acumulado -= 10
                
            posts_text.append(post.title)
            
        # Normalizar score base 50 (max 100, min 0)
        score_final = max(0, min(100, 50 + score_acumulado))
        
        return {
            "score_general": score_final,
            "top_posts": posts_text
        }
        
    except Exception as e:
        print(f"Error Reddit: {e}")
        return {"score_general": 50, "top_posts": [f"Error: {str(e)}"]}

if __name__ == "__main__":
    print("Prueba CoinDesk:")
    print(get_coindesk_headlines())
    print("\nPrueba Reddit Sentiment:")
    print(get_reddit_sentiment())
    print("\nPrueba AstroSeek (async):")
    print(asyncio.run(get_astroseek_transitos()))

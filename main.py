from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Conectar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carpeta de templates
templates = Jinja2Templates(directory="templates")

# Estado del juego en memoria
juego = {
    "palabra": "",
    "letras_usadas": [],
    "intentos": 6
}

def obtener_palabra():
    """
    Selecciona una palabra aleatoria desde la base de datos SQLite.

    Returns:
        str: Palabra seleccionada en mayúsculas.
    """
    conn = sqlite3.connect("palabras.db")
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM palabras ORDER BY RANDOM() LIMIT 1")
    palabra = cursor.fetchone()[0]
    conn.close()
    return palabra

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Página de inicio del juego.

    Args:
        request (Request): Objeto de solicitud HTTP.

    Returns:
        HTMLResponse: Renderiza la plantilla index.html
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/nuevo_juego")
async def nuevo_juego():
    """
    Inicia una nueva partida:
    - Selecciona una palabra aleatoria de la base de datos.
    - Reinicia las letras usadas y los intentos.

    Returns:
        RedirectResponse: Redirige a la página de juego.
    """
    juego["palabra"] = obtener_palabra()
    juego["letras_usadas"] = []
    juego["intentos"] = 6
    return RedirectResponse(url="/jugar", status_code=303)

@app.get("/jugar", response_class=HTMLResponse)
async def jugar(request: Request):
    """
    Renderiza la página principal del juego mostrando:
    - Palabra parcial (letras adivinadas y guiones bajos).
    - Intentos restantes.
    - Letras ya usadas.

    Args:
        request (Request): Objeto de solicitud HTTP.

    Returns:
        HTMLResponse: Renderiza la plantilla game.html con datos del juego.
    """
    palabra_mostrada = " ".join([letra if letra in juego["letras_usadas"] else "_" for letra in juego["palabra"]])
    fin = juego["intentos"] <= 0 or set(juego["palabra"]).issubset(set(juego["letras_usadas"]))
    return templates.TemplateResponse("game.html", {
        "request": request,
        "palabra": palabra_mostrada,
        "intentos": juego["intentos"],
        "letras_usadas": ", ".join(juego["letras_usadas"]),
        "fin": fin,
        "palabra_real": juego["palabra"] if fin else None
    })

@app.post("/intento")
async def intento(letra: str = Form(...)):
    """
    Procesa un intento del jugador:
    - Valida la letra ingresada.
    - Agrega la letra a la lista de usadas.
    - Resta un intento si la letra no pertenece a la palabra.

    Args:
        letra (str): Letra ingresada por el usuario.

    Returns:
        RedirectResponse: Redirige nuevamente a la página del juego.
    """
    letra = letra.upper()
    if letra not in juego["letras_usadas"]:
        juego["letras_usadas"].append(letra)
        if letra not in juego["palabra"]:
            juego["intentos"] -= 1
    return RedirectResponse(url="/jugar", status_code=303)

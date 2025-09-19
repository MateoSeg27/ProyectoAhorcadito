import sqlite3

def crear_tabla():
    """
    Crea la tabla 'palabras' en la base de datos SQLite si no existe.
    
    La tabla contiene un único campo:
        - palabra (TEXT): palabra utilizada en el juego del ahorcado.

    Returns:
        None
    """
    conn = sqlite3.connect("palabras.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palabras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertar_palabras():
    """
    Inserta una lista inicial de palabras en la tabla 'palabras'.

    Nota:
        - Se pueden modificar o ampliar las palabras según el tema del juego.
        - Si ya existen las palabras, no se duplicarán porque se inserta manualmente.

    Returns:
        None
    """
    conn = sqlite3.connect("palabras.db")
    cursor = conn.cursor()

    palabras = [
        "PYTHON", "FASTAPI", "CODIGO", "AHORCADO", "SERVIDOR",
        "JUEGO", "PROYECTO", "HTML", "CSS", "SQLITE"
    ]

    for palabra in palabras:
        cursor.execute("INSERT INTO palabras (palabra) VALUES (?)", (palabra,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    """
    Punto de entrada del script.
    - Crea la tabla si no existe.
    - Inserta las palabras iniciales.
    """
    crear_tabla()
    insertar_palabras()
    print("Base de datos creada y palabras insertadas.")

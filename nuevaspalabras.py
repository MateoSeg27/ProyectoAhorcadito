import sqlite3

def agregar_palabras(nuevas_palabras):
    """
    Inserta una lista de nuevas palabras en la base de datos.

    Args:
        nuevas_palabras (list): Lista de palabras en mayúsculas.
    
    Returns:
        None
    """
    conn = sqlite3.connect("palabras.db")
    cursor = conn.cursor()

    for palabra in nuevas_palabras:
        cursor.execute("INSERT INTO palabras (palabra) VALUES (?)", (palabra.upper(),))

    conn.commit()
    conn.close()
    print(f"{len(nuevas_palabras)} palabras nuevas fueron agregadas con éxito.")

if __name__ == "__main__":
    # 🔹 Acá escribís las palabras nuevas que quieras agregar
    nuevas = ["PROYECTO", "IITA", "SOFTWARE"]
    agregar_palabras(nuevas)

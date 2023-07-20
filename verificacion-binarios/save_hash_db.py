import os
import psycopg2
from get_hash import get_hashf
PASSWD_DIR = "/etc/passwd"
SHADOW_DIR = "/etc/shadow"
DIRS = [PASSWD_DIR, SHADOW_DIR]

def clear_table(conn):
    """Borra el contenido de la tabla 'file_hashes' en la base de datos."""
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM file_hashes")
        conn.commit()
    print("Contenido de la tabla 'file_hashes' borrado correctamente.")

def insert_hash():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="db_hashes",
            user="chris",
            password="12345")
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print("Error al conectarse a la base de datos:", e)
        return

    clear_table(conn)
    for file_path in DIRS:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_hash = get_hashf(file_path)

            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO file_hashes (file_path, file_hash) VALUES (%s, %s)",
                    (file_path, file_hash)
                )
                conn.commit()
                print(f"Hash del archivo {file_path} almacenado en la base de datos.")
        else:
            print(f"El archivo {file_path} no existe o no es un archivo regular.")

    # Cerrar la conexión a la base de datos
    conn.close()

insert_hash()

import psycopg2
from get_hash import get_hashf


# Archivos a verificar
PASSWD_DIR = "/etc/passwd"
SHADOW_DIR = "/etc/shadow"

def compare_hashes():
    # Conexión a la base de datos PostgreSQL
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

    # Obtener los hashes almacenados en la base de datos
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT file_path, file_hash FROM file_hashes WHERE file_path IN (%s, %s)",
            (PASSWD_DIR, SHADOW_DIR)
        )
        db_hashes = {file_path: file_hash for file_path, file_hash in cursor.fetchall()}

    # Obtener los hashes actuales de los archivos
    current_hashes = {
        PASSWD_DIR: get_hashf(PASSWD_DIR),
        SHADOW_DIR: get_hashf(SHADOW_DIR)
    }

    # Comparar los hashes
    for file_path, file_hash in current_hashes.items():
        if file_path in db_hashes:
            if file_hash == db_hashes[file_path]:
                print(f"El archivo {file_path} no ha sido modificado.")
            else:
                print(f"El archivo {file_path} ha sido modificado.")
        else:
            print(f"El archivo {file_path} no ha sido previamente registrado en la base de datos.")

    # Cerrar la conexión a la base de datos
    conn.close()
compare_hashes()
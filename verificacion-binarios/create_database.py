import psycopg2


def create_database():
    # Conexión a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="db_hashes",
            user="chris",
            password="12345"
        )
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print("Error al conectarse a la base de datos:", e)
        return

    # Crear la tabla 'file_hashes' en la base de datos si no existe
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS file_hashes (
                id SERIAL PRIMARY KEY,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL
            )
            """
        )
        conn.commit()
create_database()
import psycopg2
import subprocess
import sys
import os
# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# directorio controlar_logs
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import send_csv_logs
# Archivos a verificar
PASSWD_DIR = "/etc/passwd"
SHADOW_DIR = "/etc/shadow"

def compare_hashes():
    # Conexión a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="hips",
            user="hips",
            password="12345")
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print("Error al conectarse a la base de datos:", e)
        return

    # Obtener los hashes almacenados en la base de datos
    cursor=conn.cursor()
    cursor.execute("SELECT file_hash FROM file_hashes WHERE file_path = %s;", (PASSWD_DIR,))
    hash_original_passwd = cursor.fetchone()
    
    cursor=conn.cursor()
    cursor.execute("SELECT file_hash FROM file_hashes WHERE file_path = %s;", (SHADOW_DIR,))
    hash_original_shadow = cursor.fetchone()
        

    # Obtener los hashes actuales de los archivos
    hash_passwd_actual=subprocess.run(["sudo", "sha256sum", PASSWD_DIR], check=True, capture_output=True).stdout.decode().strip().split()[0]                                  
    hash_shadow_actual=subprocess.run(["sudo", "sha256sum", SHADOW_DIR], check=True, capture_output=True).stdout.decode().strip().split()[0]
    print(hash_original_passwd,hash_passwd_actual)
    print(hash_original_shadow,hash_shadow_actual)
    

    # Comparar los hashes

    if hash_passwd_actual == hash_original_passwd[0]:
        print("El archivo /etc/passwd no ha sido modificado.")
        send_csv_logs.write_csv('verificacion-firma', 'verify_binaries', "/etc/passwd no ha sido modificado")

    else:
        print(f"El archivo /etc/passwd ha sido modificado.")
        cursor.execute("UPDATE file_hashes SET file_hash = %s WHERE file_path = %s;", (hash_passwd_actual, PASSWD_DIR,))
        send_csv_logs.write_csv('verificacion-firma', 'verify_binaries', "/etc/passwd ha sido modificado")

    if hash_shadow_actual == hash_original_shadow[0]:
        print("El archivo /etc/shadow no ha sido modificado.")
        send_csv_logs.write_csv('verificacion-firma', 'verify_binaries', "/etc/shadow no ha sido modificado")
    else:
        print(f"El archivo /etc/shadow ha sido modificado.")
        cursor.execute("UPDATE file_hashes SET file_hash = %s WHERE file_path = %s;", (hash_passwd_actual, PASSWD_DIR,))
        send_csv_logs.write_csv('verificacion-firma', 'verify_binaries', "/etc/shadow ha sido modificado")
    
    # Cerrar la conexión a la base de datos
    conn.commit()
    conn.close()
    cursor.close()
compare_hashes()
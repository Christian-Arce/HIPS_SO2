import subprocess

def block_email(email):
    try:
        # Agregamos el email a la lista negra
        with open("/etc/postfix/sender_access", "a") as blacklist_file:
            blacklist_file.write(f"{email} REJECT\n")

        # Creamos la base de datos con el comando postmap
        subprocess.run(["sudo", "postmap", blacklist_file])
        
        print(f"El correo {email} ha sido bloqueado.")
    except Exception as e:
        print(f"Hubo un problema al cargar el email en la lista negra: {e}")





def check_maillogg():
   
    command = "sudo cat /var/log/maillog | grep -i 'authid' " #filtro por authid
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Verificar si hubo errores en la ejecución del comando
    if process.returncode == 0:
    # Dividir la salida en líneas y eliminar el último elemento (línea vacía)
        file = process.stdout.split("\n")[:-1]
        print(file)
    else:
    # Si hubo un error, imprimir el mensaje de error
        print("Error al ejecutar el comando:")
        print(process.stderr)
    
    contador_email ={}

    #analizar linea por linea del contenido obtenido en file
    for email in file:
        email = [word for word in email.split() if 'authid=' in word][0]
        email = email.split("=")[-1][:-1] # Sacamos el 'authid=' y la ',' al final. Finalmente obtenemos el email.
        if email in contador_email:
            contador_email[email] = contador_email[email] + 1
            if contador_email == 30:
                block_email(email)

        else:
            contador_email[email] = 1
            print("1")



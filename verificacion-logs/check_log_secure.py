import subprocess
import random
import string 

#Genera una contrasena random
def random_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = random.sample(password_characters, 8)
    password = "".join(password)
    return password

def check_secure():
   
    command = "sudo cat /var/log/secure | grep -i 'smtp:auth' | grep -i 'authentication failure'" #filtro por esas strings
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
    
    contador_user ={}

    #analizar linea por linea del contenido obtenido en file
    for user in file:
        user = user.split('=')[-1]
        if user in contador_user:
            contador_user[user] = contador_user[user] + 1
            if contador_user == 30:
                new_passwd = random_password()
                command_new_passwd = f"echo '{user}:{new_passwd}' | sudo chpasswd"
                subprocess.run(command_new_passwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        else:
            contador_user[user] = 1
            print("1")



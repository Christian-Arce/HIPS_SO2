import subprocess
import random
import string 

#Genera una contrasena random
def random_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = random.sample(password_characters, 8)
    password = "".join(password)
    return password

def check_messages():
    
    command = "cat /var/log/messages | grep -i 'service=smtp' | grep -i 'auth failure'" #esta seria en una version vieja de centos?
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
    for line in file:
        # Se obtiene el usuario entre corchetes [user=username]
        user = [word for word in line.split() if 'user=' in word][0]
         # Se borran los corchetes
        user = user.split('=')[-1][1:][:-1]    
        if contador_user == 30:
            new_passwd = random_password()
            command_new_passwd = f"echo '{user}:{new_passwd}' | sudo chpasswd"
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        else:
            contador_user[user] = 1
            print("1")



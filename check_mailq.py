import subprocess

def get_mail_queue_size():
    try:
        output = subprocess.check_output("mailq | tail -n 1", shell=True).decode('utf-8')
        queue_size_line = output.strip() #elimina espacios vacios de la cadena
        if queue_size_line.split()[1] == "queue" :
            queue_size = 0
            return queue_size
        else:
            queue_size = int(queue_size_line.split()[1])#separa el output para poder agarrar el numero de colas y lo pasa a int
            return queue_size
    except:
        print("Error al obtener el tamaño de la cola.")
        return -1

if __name__ == "__main__":
    queue_size = get_mail_queue_size() #trae el valor de la cola de mails
    if queue_size > 50: #verifica la cantidad
        print(f"¡Hay más de 50 mensajes en cola! ({queue_size} mensajes)")
    else:
        print(f"El tamaño de la cola es de {queue_size} mensajes.")
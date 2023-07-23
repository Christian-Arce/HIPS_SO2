
import subprocess

def block_ip(ip_address):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])
        print(f"La dirección IP {ip_address} ha sido bloqueada.")
    except:
        print("Error al bloquear la dirección IP.")

def access_log():
    #ejemplo output Jul 23 05:06:19 localhost su[17554]: FAILED SU (to prueba) chris on pts/2
    command = "cat /var/log/httpd/access_log | grep -i 'HTTP' | grep -i '404'" #esta seria en una version vieja de centos?
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Verificar si hubo errores en la ejecución del comando
    if process.returncode == 0:
    # Dividir la salida en líneas y eliminar el último elemento (línea vacía)
        file = process.stdout.split("\n")[:-1]
    else:
    # Si hubo un error, imprimir el mensaje de error
        print("Error al ejecutar el comando:")
    
    contador_ip ={}

    #analizar linea por linea del contenido obtenido en file
    for line in file:
        ip = line.split()[1]
        if ip in contador_ip: #se verifica cuantas veces aparece la ip haciendo un request del access_log
            contador_ip[ip] = contador_ip[ip] + 1
            if contador_ip == 10:
                block_ip(ip)
        else:
            contador_ip[ip] = 1
            print("1")

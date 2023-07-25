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
import block_ip




def block_ip(ip_address):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])
        print(f"La dirección IP {ip_address} ha sido bloqueada.")
    except:
        print("Error al bloquear la dirección IP.")

def check_ddos():
    
    command = "sudo cat /var/log/dns-tcpdump/ataque" 
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Verificar si hubo errores en la ejecución del comando
    if process.returncode == 0:
    # Dividir la salida en líneas y eliminar el último elemento (línea vacía)
        file = process.stdout.split("\n")[:-1]
    else:
        send_csv_logs.write_csv('verificacion-ddos','check_log_ddos', f"Mensaje: Todo correcto, no hay ataques ddos desde una ip")
    
    contador_ip ={}


    #analizar linea por linea del contenido obtenido en file
    if process.returncode == 0:
        for line in file:
            ip_o = line.split()[2]
            ip_d = line.split()[4][:-1]
            if (ip_o , ip_d) in contador_ip: #se verifica cuantas veces aparece la ip_o ataca a ip_d
                contador_ip[(ip_o , ip_d)] = contador_ip[(ip_o , ip_d)] + 1
            else:
                contador_ip[(ip_o , ip_d)] = 1

        for (ip_o,ip_d), ocurrencia in contador_ip.items():
            if ocurrencia == 5:
                print(ocurrencia)
                #block_ip.block(ip_o)
                send_csv_logs.write_csv('verificacion-ddos','check_log_ddos', f"Mensaje: Prevencion, ip bloqueada por ataque ddos, ip:{ip_o}")
                send_csv_logs.write_log('prevencion', 'Prevencion: bloquear', 'Razon: Cola alta de emails',f'ip bloqueada por ataque ddos, ip:{ip_o}' )
            else:
                #print(ips, ocurrencia)
                send_csv_logs.write_csv('verificacion-ddos','check_log_ddos', f"Mensaje: Todo correcto, no hay suficientes ataques ddos desde una ip")
            
check_ddos()

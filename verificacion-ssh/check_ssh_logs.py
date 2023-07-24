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


def verificar_ssh_logs():
    command = "sudo cat /var/log/secure | grep -i 'sshd' | grep -i 'Failed password'"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        ssh_passwdf = result.stdout.split('\n')[:-1]  # Eliminamos el ultimo elemento vacio
    except:
        print("error")

    ip_contador = {} #diccionario que se utilizara como contador para las ips

    for element_line in ssh_passwdf:
        ip_origen = element_line.split()[-4] #En esa posicion se encuentra la ip luego de hacer el split
        if ip_origen in ip_contador:
            ip_contador[ip_origen]= ip_contador[ip_origen] + 1
        
        else:
            ip_contador[ip_origen]=1
        for ips, ocurrencia in ip_contador.items():  #se separan en (ip_origen ip_contador, valor )
            if ocurrencia == 7:
                send_csv_logs.write_csv('verificacion-ssh','check_ssh_logs', f"Mensaje: Alarma, intento de conexion remota (ssh)")
                send_csv_logs.write_log('alarmas', 'Alerta: Intento de conexion remota', 'Razon: Varios intentos de acceso al sistema')
            else:
                send_csv_logs.write_csv('verificacion-ssh','check_ssh_logs', f"Mensaje: Todo correcto, no hay intentos de acceso al sistema")

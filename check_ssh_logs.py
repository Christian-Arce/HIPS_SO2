import subprocess

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
            if ip_contador[ip_origen] > 5:
                print("avisar de muchos intentos")
        
        else:
            ip_contador[ip_origen]=1

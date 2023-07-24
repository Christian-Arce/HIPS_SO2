import subprocess

def check_sniffers_promiscuos():
    #Se verifica si actualmente esta activo el dispositivo en modo promiscuo
    command = "sudo ip a show enp0s3 | grep -i 'promis'"
    file = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(file)
    if file.returncode == 0:
        print("Hay dispositivos en modo promiscuo")
    else:
        print("No hay dispositivos en modo promiscuo")
    #Se verifica en /var/log/messages si se entro y salio del modo promiscuo en algun momento
    command1 = "sudo cat /var/log/messages |grep -i entered | grep -i promis"
    command2 = "sudo cat /var/log/messages |grep -i left | grep -i promis"
    file_entered = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    file_left = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    dic1 = {"Mensaje": "Entro en modo promiscuo"}
    dic2 = {"Mensaje": "Salio de modo promiscuo"}
    if file_entered.returncode == 0:
        file_entered = file_entered.stdout.split('\n')[:-1]
        for line1 in file_entered:
            line1 = line1.split()
            dic1["Mes"] = line1[0]
            dic1["Dia"] = line1[1]
            dic1["Hora"] = line1[2]
            
 
        print(dic1)

        
    else:
        print("No se entro en modo promiscuo")
    if file_left.returncode == 0:
        file_left = file_left.stdout.split('\n')[:-1]
        for line2 in file_left:
            line2 = line2.split()
            dic2["Mes"] = line2[0]
            dic2["Dia"] = line2[1]
            dic2["Hora"] = line2[2]
        print(dic2)


    


check_sniffers_promiscuos()
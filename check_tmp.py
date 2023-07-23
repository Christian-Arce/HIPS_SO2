import subprocess

def check_tmpf():
    command = "sudo find /tmp -type f 2>/dev/null"
    file_tmp = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
    #subprocess.run() se almacena en un objeto CompletedProcess, que tiene un atributo stdout que contiene la salida del comando ejecutado. 
    files_list = file_tmp.stdout.splitlines()

    archivos_cuarentena = []

    for file_list in files_list:
        cuarentena = {}

        # verificamos estos tipos de archivos
        if any(file in file_list for file in [".cpp", ".c", ".py", ".sh", ".php"]):
            cuarentena['ruta del archivo'] = file_list
            cuarentena['archivo a mover'] = "/quarentine/tmp_scripts" + file_list.replace("/","-")
            cuarentena['razon'] = "Archivo sospechoso"
            archivos_cuarentena.append(cuarentena)
        else: # Si no, busca si el archivo tiene un #! en la primera linea, lo cual significa que es un archivo script
            try:     
                with open(f"{file_list}", "r") as f:
                    primera_linea = f.readline() # Leemos la primera linea del archivo
                    if "#!" in primera_linea:
                        cuarentena['ruta_del_archivo'] = file_list
                        cuarentena['destino_cuarentena'] = "/quarentine/tmp_scripts" + file_list.replace("/","-")
                        cuarentena['razon'] = "Archivo sospechoso de tipo #!"
                        archivos_cuarentena.append(cuarentena)
            except Exception:
                print("El archivo esta codeado en bytes")
        
    for archivo in archivos_cuarentena:
        try:
            command = f"sudo mv {archivo['ruta_del_archivo']} {archivo['destino_cuarentena']}"
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except:
            print(f"No se pudo mover a cuarentena el archivo: {archivo}.")




        
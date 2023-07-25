import subprocess
import os
import sys
# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# directorio controlar_logs
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import send_csv_logs
import kill_ps

def get_highest_process(mem_or_cpu=""):
    if mem_or_cpu == "mem" or mem_or_cpu == "cpu":
        high_consume = f"ps -eo pid,%mem,%cpu --sort=-%{mem_or_cpu} | head -n 20"
        process_c = subprocess.run(high_consume, shell=True, capture_output=True, text=True)
        process_lines = process_c.stdout.split("\n")
        process_lines.pop(-1)
        process_lines.pop(0)
        process_list = []

        for process_line in process_lines:
            proc = process_line.split()
            #Diccionario para guardar la informacion del proceso
            process = {
                "PID": int(proc[0]),
                "%MEM": float(proc[1]),
                "%CPU": float(proc[2])
            }

            execution_time_c = f"ps -p {process['PID']} -o etime" #Tiempo de ejecucion del proceso
            
            #Tiempo de ejecucion del proceso y separar por horas,minutos,segundos
            execution_time = subprocess.run(execution_time_c, shell=True, capture_output=True, text=True)
            execution_time = execution_time.stdout.strip().split(":")
            #Se obtiene el tiempo en minutos
            if len(execution_time) == 3: # si tiene hora, minutos y segundos.
                execution_time = float(execution_time[0]) * 60 + float(execution_time[1]) + float(execution_time[2])/60.0 
            else:
                execution_time = float(execution_time[0]) + float(execution_time[1])/60.0 
                
            
             #Se agrega el tiempo de ejecucion a la lista de procesos de alto consumo
            process["Tiempo de Ejecucion"] = execution_time
            process_list.append(process)
            

        return process_list
    
#Se verifica los procesos que consumen mucha memoria y cpu, en el caso de que cumplan los
#requisitos se mataran esos procesos

def verificar_procesos_cpu_ram():
    highest_mem = get_highest_process("mem")
    highest_cpu = get_highest_process("cpu")
    kill_list = []

    for process in highest_mem:
        #Si se usa mas del 80% de la memoria ram
        if process["%MEM"] > 50.0:    
            process["motivo"] = "usa mucha memoria"
            kill_list.append(process)
            send_csv_logs.write_csv('verificacion-consumo','check_uso_alto', f"Prevencion, el proceso: {process['PID']} consume mucha memoria")
            send_csv_logs.write_log('alarmas', 'Alarma: Sistema saturado', f"Razon: Uso de mucha mememoria de {process['PID']}") 
            send_csv_logs.write_log('prevencion', f'Prevencion: Matar proceso {process["PID"]}', 'Razon: Uso de mucha memoria')       
   
    for process in highest_cpu:
        #Si se usa mas del 80% del cpu
        if process["%CPU"] > 50.0:
            process["motivo"] = "usa mucha cpu"
            send_csv_logs.write_csv('verificacion-consumo','check_uso_alto', f"Prevencion, el proceso: {process['PID']} consume mucha cpu")
            send_csv_logs.write_log('alarmas', 'Alarma: Sistema saturado', f"Razon: Uso de mucha cpu de {process['PID']}") 
            send_csv_logs.write_log('prevencion', f'Prevencion: Matar proceso {process["PID"]}', 'Razon: Uso de mucha cpu') 
            kill_list.append(process)

    #Procedemos a matar los procesos que abusaron de los recursos
    '''for process in kill_list:
        kill_ps.kill_processf(process["PID"])'''

verificar_procesos_cpu_ram()
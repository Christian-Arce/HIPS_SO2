import subprocess
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
        if process["%MEM"] > 80.0:    
            process["motivo"] = "usa mucha memoria"
            kill_list.append(process)       
   
    for process in highest_cpu:
        #Si se usa mas del 80% del cpu
        if process["%CPU"] > 80.0:
            process["motivo"] = "usa mucha cpu"
            kill_list.append(process)

    #Procedemos a matar los procesos que abusaron de los recursos
    for process in kill_list:
        kill_ps.kill_processf(process["PID"])
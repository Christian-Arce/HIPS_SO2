import os
import pwd
from crontab import CronTab

def listar_tareas_cron():
    usuarios = pwd.getpwall() #trae todo el contenido de /etc/passwd

    print("Tareas cron de todos los usuarios:\n")
    #print(usuarios)
    for usuario in usuarios:
        usuario_actual = usuario.pw_name #filtra los usuarios obtenidos de /etc/passwd
        #print(usuario_actual)
        archivo_cron = f"/var/spool/cron/{usuario_actual}"
        
        if not os.path.isfile(archivo_cron):
            # Si el usuario no tiene un archivo cron, pasamos al siguiente.
            continue
        
        cron = CronTab(user=usuario_actual)

        print(f"Usuario: {usuario_actual}")
        for tarea in cron:
            print(f"Comando: {tarea.command}")
            print(f"Frecuencia: {tarea.frequency_per_hour()} veces por hora.")
            print()

listar_tareas_cron()
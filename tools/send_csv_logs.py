import csv
from datetime import datetime
import os
import datetime


# Escribe un registro de una alerta o prevencion
# En /var/log/hips/alarmas.log o /var/log/hips/prevencion.log
# Formato fecha_hora :: tipo_alarma :: ip_email   motivo

def write_log(alarms_or_alert, tipo_alarma, reason, ip_or_email = ''):
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'{date} :: {tipo_alarma} :: {ip_or_email} \t{reason}'

    if alarms_or_alert == 'alarmas' or alarms_or_alert == 'prevencion':
        os.system(f"sudo echo '{text}' >> /var/log/hips/{alarms_or_alert}.log")
    else:
        print("Error input")



def write_csv(file, file_name, message):
    try:
        date=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(f"/var/log/hips/output/{file}/{file_name}.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, message])
        print("Guardado exitoso en .csv")
    except:
        print("Error al guardar .csv")


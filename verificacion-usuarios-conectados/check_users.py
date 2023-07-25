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

import subprocess
connected_users = subprocess.check_output("who -H | awk '{print $1, $5}'", shell=True).decode('utf-8')
send_csv_logs.write_csv('verificacion-usuarios-conectados','check_users', f"Mensaje: Usuario conectados y origen: {connected_users}")
send_csv_logs.write_log('alarma', f'Alarama: Usuarios conectados y origen{connected_users}', f'Razon: Checkeo')
print(connected_users)
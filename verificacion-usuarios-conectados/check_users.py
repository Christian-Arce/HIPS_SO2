import subprocess
connected_users = subprocess.check_output("who -H | awk '{print $1, $5}'", shell=True).decode('utf-8')
print(connected_users)
import paramiko

host = "192.168.121.232"
username = "msfadmin"
password = "msfadmin"

# Setting up ssh client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

# executing some commands for testing
res = client.exec_command("ls")
output = res[1].read().decode().strip()
print("shutting down the target")
client.close()
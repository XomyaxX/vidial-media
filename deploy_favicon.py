import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

sftp = client.open_sftp()
sftp.put("favicon.ico", "/var/www/vidial-media/favicon.ico")
sftp.close()

stdin, stdout, stderr = client.exec_command("chown www-data:www-data /var/www/vidial-media/favicon.ico && chmod 644 /var/www/vidial-media/favicon.ico && ls -la /var/www/vidial-media/favicon.ico")
print(stdout.read().decode('utf-8', errors='replace').strip())

client.close()

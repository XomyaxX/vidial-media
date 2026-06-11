import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("Full file listing", "find /var/www/vidial-media -type f | sort"),
    ("Assets subdirs", "find /var/www/vidial-media/assets -type d | sort"),
    ("Count files", "find /var/www/vidial-media -type f | wc -l"),
]

for title, cmd in commands:
    print(f"=== {title} ===")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out)
    if err:
        print(f"STDERR: {err}")
    print()

client.close()

import paramiko
import sys

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("docker-compose.yml contents", "cat /var/www/superglazka/docker-compose.yml"),
    ("Docker inspect superglaze-app mounts", "docker inspect superglaze-app --format='{{json .HostConfig.Binds}}' 2>/dev/null || echo 'cannot inspect'"),
    ("Docker inspect superglazka-backend mounts", "docker inspect superglazka-backend --format='{{json .HostConfig.Binds}}' 2>/dev/null || echo 'cannot inspect'"),
    ("superglazka.com DNS/dig", "dig +short superglazka.com 2>/dev/null || nslookup superglazka.com 2>/dev/null | head -10 || echo 'no dig/nslookup'"),
    ("nginx -T test", "nginx -T 2>&1 | grep -E 'server_name|root' | head -30"),
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

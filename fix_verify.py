import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("List backup files", "ls -la /etc/nginx/conf.d/*.bak* 2>/dev/null || ls -la /etc/nginx/conf.d/ | grep bak || echo 'No backups found'"),
    ("Current config md5", "md5sum /etc/nginx/conf.d/vidial-media.ru.conf"),
    ("HTTPS check vidial-media.ru", "curl -s -k -o /dev/null -w 'HTTP %{http_code}' -H 'Host: vidial-media.ru' https://localhost/ 2>/dev/null"),
    ("HTTPS title check", "curl -s -k -H 'Host: vidial-media.ru' https://localhost/ | grep -o '<title>.*</title>' | head -1"),
    ("superglazka.ru HTTPS check", "curl -s -k -o /dev/null -w 'HTTP %{http_code}' -H 'Host: superglazka.ru' https://localhost/ 2>/dev/null || curl -s -o /dev/null -w 'HTTP %{http_code}' http://superglazka.ru/ 2>/dev/null"),
    ("nginx running", "ps aux | grep 'nginx' | grep -v grep | head -3"),
    ("superglazka dir md5", "md5sum /var/www/superglazka/index.html /var/www/superglazka/docker-compose.yml 2>/dev/null"),
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

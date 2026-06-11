import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("Backup file exists", "ls -la /etc/nginx/conf.d/vidial-media.ru.conf.bak.* 2>/dev/null || echo 'NO BACKUP FOUND'"),
    ("Nginx config content", "cat /etc/nginx/conf.d/vidial-media.ru.conf"),
    ("superglazka.ru HTTP status", "curl -s -o /dev/null -w '%{http_code}' -H 'Host: superglazka.ru' http://localhost/ 2>/dev/null || echo 'check failed'"),
    ("vidial-media.ru local HTTP status", "curl -s -o /dev/null -w '%{http_code}' -H 'Host: vidial-media.ru' http://localhost/ 2>/dev/null || echo 'check failed'"),
    ("vidial-media.ru page title", "curl -s -H 'Host: vidial-media.ru' http://localhost/ | grep -o '<title>.*</title>' | head -1"),
    ("Check no superglazka files in vidial dir", "ls /var/www/vidial-media/ | grep -i superglazka || echo 'No superglazka files found - good'"),
    ("Check superglazka dir untouched", "ls /var/www/superglazka/index.html /var/www/superglazka/docker-compose.yml 2>/dev/null | head -5"),
    ("Nginx error log recent", "tail -5 /var/log/nginx/error.log"),
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

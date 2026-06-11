import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("superglazka.com nginx grep", "grep -r 'superglazka.com' /etc/nginx/ 2>/dev/null"),
    ("superglazka.com apache grep", "grep -r 'superglazka.com' /etc/apache2/ 2>/dev/null"),
    ("Contents of /var/www/superglazka", "ls -la /var/www/superglazka/ 2>/dev/null || echo 'cannot list'"),
    ("Top level files in /var/www/superglazka", "find /var/www/superglazka -maxdepth 2 -type f 2>/dev/null | head -50"),
    ("What's running on port 20010", "ss -tlnp | grep 20010 || netstat -tlnp | grep 20010 || echo 'nothing on 20010'"),
    ("What's running on port 3000", "ss -tlnp | grep 3000 || netstat -tlnp | grep 3000 || echo 'nothing on 3000'"),
    ("Docker containers", "docker ps 2>/dev/null || echo 'docker not running or not installed'"),
    ("PM2 processes", "pm2 list 2>/dev/null || echo 'pm2 not found'"),
    ("Systemd services with superglazka", "systemctl list-units --type=service | grep -i superglazka || echo 'no superglazka services'"),
    ("Systemd services with vidial", "systemctl list-units --type=service | grep -i vidial || echo 'no vidial services'"),
    ("Current index.html in superglazka dir", "head -20 /var/www/superglazka/index.html 2>/dev/null || echo 'no index.html'"),
]

for title, cmd in commands:
    print(f"=== {title} ===")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out)
    if err and "not found" not in err.lower() and "no such" not in err.lower():
        print(f"STDERR: {err}")
    print()

client.close()

import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("vidial-media.ru full fetch", "curl -s -k https://vidial-media.ru/ | head -20"),
    ("vidial-media.ru body check", "curl -s -k https://vidial-media.ru/ | grep -o 'Видеаль Медиа' | head -1 || echo 'Title text not found in response'"),
    ("superglazka.ru external check", "curl -s -o /dev/null -w 'HTTP %{http_code}' https://superglazka.ru/ 2>/dev/null || echo 'HTTPS check failed'"),
    ("superglazka.ru title check", "curl -s -k https://superglazka.ru/ | grep -o '<title>.*</title>' | head -1 || echo 'No title found'"),
    ("nginx config test again", "nginx -t 2>&1"),
    ("Verify vidial-media directory structure", "find /var/www/vidial-media -maxdepth 2 -type f | sort"),
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

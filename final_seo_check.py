import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

commands = [
    ("superglazka.ru status", "curl -s -o /dev/null -w 'HTTP %{http_code}' https://superglazka.ru/ 2>/dev/null || echo 'failed'"),
    ("vidial-media.ru Schema.org check", "curl -s -k https://vidial-media.ru/ | grep -c 'schema.org'"),
    ("vidial-media.ru H1 text check", "curl -s -k https://vidial-media.ru/ | grep -o 'visually-hidden.*>.*</span>' | head -1"),
    ("vidial-media.ru canonical check", "curl -s -k https://vidial-media.ru/ | grep -o 'rel=\"canonical\".*>'"),
    ("vidial-media.ru robots meta check", "curl -s -k https://vidial-media.ru/ | grep -o 'name=\"robots\".*>'"),
    ("vidial-media.ru lazy loading check", "curl -s -k https://vidial-media.ru/ | grep -c 'loading=\"lazy\"'"),
    ("vidial-media.ru og:image check", "curl -s -k https://vidial-media.ru/ | grep -o 'og:image.*content=\"[^\"]*\"'"),
    ("nginx error log recent", "tail -3 /var/log/nginx/error.log"),
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

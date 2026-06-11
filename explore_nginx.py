import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

# Find all nginx config files and show their contents related to vidial-media
commands = [
    ("Find all nginx conf files", "find /etc/nginx -type f -name '*.conf' 2>/dev/null | sort"),
    ("Nginx conf.d listing", "ls -la /etc/nginx/conf.d/ 2>/dev/null || echo 'no conf.d'"),
    ("Full nginx configs grep", "grep -rl 'vidial-media' /etc/nginx/ 2>/dev/null"),
    ("Full superglazka configs grep", "grep -rl 'superglazka' /etc/nginx/ 2>/dev/null"),
]

for title, cmd in commands:
    print(f"--- {title} ---")
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode('utf-8', errors='replace').strip())
    print()

# Read specific config files if found
stdin, stdout, stderr = client.exec_command("grep -rl 'vidial-media' /etc/nginx/ 2>/dev/null")
vidial_files = stdout.read().decode('utf-8', errors='replace').strip().split('\n')
vidial_files = [f.strip() for f in vidial_files if f.strip()]

stdin, stdout, stderr = client.exec_command("grep -rl 'superglazka' /etc/nginx/ 2>/dev/null")
super_files = stdout.read().decode('utf-8', errors='replace').strip().split('\n')
super_files = [f.strip() for f in super_files if f.strip()]

print("=== Files containing vidial-media ===")
for f in vidial_files:
    print(f"\n--- Content of {f} ---")
    stdin, stdout, stderr = client.exec_command(f"cat '{f}'")
    print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Files containing superglazka ===")
for f in super_files:
    print(f"\n--- Content of {f} ---")
    stdin, stdout, stderr = client.exec_command(f"cat '{f}'")
    print(stdout.read().decode('utf-8', errors='replace').strip())

client.close()

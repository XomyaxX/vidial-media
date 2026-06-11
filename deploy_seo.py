import paramiko
import os

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

files_to_deploy = [
    "index.html",
    "style.css",
    "main.js",
    "robots.txt",
    "sitemap.xml",
    "privacy.html",
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

sftp = client.open_sftp()
remote_dir = "/var/www/vidial-media"

for item in files_to_deploy:
    local_path = os.path.join(".", item)
    remote_path = remote_dir + "/" + item
    if os.path.isfile(local_path):
        print(f"Uploading {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
    else:
        print(f"WARNING: {local_path} not found")

sftp.close()

print("\n=== Setting permissions ===")
stdin, stdout, stderr = client.exec_command(f"chown -R www-data:www-data {remote_dir} && chmod -R 755 {remote_dir} && echo 'OK'")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Test nginx config ===")
stdin, stdout, stderr = client.exec_command("nginx -t")
print(stdout.read().decode('utf-8', errors='replace').strip())
print(stderr.read().decode('utf-8', errors='replace').strip())

print("\n=== Reload nginx ===")
stdin, stdout, stderr = client.exec_command("nginx -s reload")
out = stdout.read().decode('utf-8', errors='replace').strip()
err = stderr.read().decode('utf-8', errors='replace').strip()
if out: print(out)
if err: print(err)

print("\n=== Verify files on server ===")
stdin, stdout, stderr = client.exec_command(f"ls -la {remote_dir}/")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Quick HTTP checks ===")
stdin, stdout, stderr = client.exec_command("curl -s -k -o /dev/null -w 'vidial-media.ru: %{http_code}\n' https://vidial-media.ru/ && curl -s -k -o /dev/null -w 'privacy.html: %{http_code}\n' https://vidial-media.ru/privacy.html && curl -s -k -o /dev/null -w 'robots.txt: %{http_code}\n' https://vidial-media.ru/robots.txt && curl -s -k -o /dev/null -w 'sitemap.xml: %{http_code}\n' https://vidial-media.ru/sitemap.xml")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Verify H1 and OG tags ===")
stdin, stdout, stderr = client.exec_command("curl -s -k https://vidial-media.ru/ | grep -oE '<title>.*</title>|<meta property=\"og:title\".*>|<h1.*>.*</h1>' | head -5")
print(stdout.read().decode('utf-8', errors='replace').strip())

client.close()
print("\n=== SEO deployment complete ===")

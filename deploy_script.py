import paramiko
import os
import tarfile
import io

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

# Local files to deploy
local_root = "."
files_to_deploy = [
    "index.html",
    "style.css",
    "main.js",
    "assets"
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

sftp = client.open_sftp()

remote_dir = "/var/www/vidial-media"
nginx_conf = "/etc/nginx/conf.d/vidial-media.ru.conf"
nginx_conf_backup = "/etc/nginx/conf.d/vidial-media.ru.conf.bak." + os.popen('date +%Y%m%d%H%M%S').read().strip()

print("=== Step 1: Create remote directory ===")
stdin, stdout, stderr = client.exec_command(f"mkdir -p {remote_dir} && ls -ld {remote_dir}")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Step 2: Backup current nginx config ===")
stdin, stdout, stderr = client.exec_command(f"cp {nginx_conf} {nginx_conf_backup} && echo 'Backup created at {nginx_conf_backup}'")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Step 3: Upload files via SFTP ===")

def upload_dir(local_path, remote_path):
    try:
        sftp.mkdir(remote_path)
    except IOError:
        pass  # already exists
    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        remote_item = remote_path + "/" + item
        if os.path.isfile(local_item):
            print(f"  Uploading {local_item} -> {remote_item}")
            sftp.put(local_item, remote_item)
        elif os.path.isdir(local_item):
            upload_dir(local_item, remote_item)

for item in files_to_deploy:
    local_path = os.path.join(local_root, item)
    remote_path = remote_dir + "/" + item
    if os.path.isfile(local_path):
        print(f"  Uploading {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
    elif os.path.isdir(local_path):
        upload_dir(local_path, remote_path)

print("\n=== Step 4: Set permissions ===")
stdin, stdout, stderr = client.exec_command(f"chown -R www-data:www-data {remote_dir} && chmod -R 755 {remote_dir} && echo 'Permissions set'")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Step 5: Update nginx config ===")
new_nginx_conf = '''server {
    listen 80;
    server_name vidial-media.ru www.vidial-media.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    client_max_body_size 50M;
    server_name vidial-media.ru www.vidial-media.ru;

    ssl_certificate /opt/superglazka/certbot-data/live/vidial-media.ru/fullchain.pem;
    ssl_certificate_key /opt/superglazka/certbot-data/live/vidial-media.ru/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    root /var/www/vidial-media;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # JS/CSS — short cache
    location ~* \.(js|css)$ {
        expires 1h;
        access_log off;
        add_header Cache-Control "public, must-revalidate";
    }

    # Images, fonts, media — long cache
    location ~* \.(png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|mp4|webm|mp3|ogg|wav|webp)$ {
        expires 6M;
        access_log off;
        add_header Cache-Control "public, immutable";
    }

    # Main app
    location / {
        try_files $uri $uri/ /index.html;
    }
}
'''

# Write new config via SFTP
with sftp.file(nginx_conf, 'w') as f:
    f.write(new_nginx_conf)

print("Nginx config updated.")

print("\n=== Step 6: Test nginx config ===")
stdin, stdout, stderr = client.exec_command("nginx -t")
out = stdout.read().decode('utf-8', errors='replace').strip()
err = stderr.read().decode('utf-8', errors='replace').strip()
print(out)
if err:
    print(f"STDERR: {err}")
    if "failed" in err.lower() or "failed" in out.lower():
        print("\n!!! NGINX TEST FAILED - RESTORING BACKUP !!!")
        client.exec_command(f"cp {nginx_conf_backup} {nginx_conf}")
        sftp.close()
        client.close()
        exit(1)

print("\n=== Step 7: Reload nginx ===")
stdin, stdout, stderr = client.exec_command("nginx -s reload")
out = stdout.read().decode('utf-8', errors='replace').strip()
err = stderr.read().decode('utf-8', errors='replace').strip()
if out:
    print(out)
if err:
    print(f"STDERR: {err}")

print("\n=== Step 8: Verify deployed files ===")
stdin, stdout, stderr = client.exec_command(f"ls -la {remote_dir}/ && echo '---' && head -5 {remote_dir}/index.html")
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Step 9: Quick HTTP check ===")
stdin, stdout, stderr = client.exec_command("curl -s -o /dev/null -w '%{http_code}' https://vidial-media.ru/")
print("HTTP Status:", stdout.read().decode('utf-8', errors='replace').strip())

sftp.close()
client.close()
print("\n=== Deployment complete ===")

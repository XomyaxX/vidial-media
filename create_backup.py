import paramiko

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

old_config = '''server {
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

    root /var/www/superglazka;
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

    # Uploads — serve directly from filesystem
    location ^~ /uploads/ {
        alias /opt/superglazka/server/uploads/;
        expires 6M;
        access_log off;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:3000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 60s;
    }

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

    # Service worker (no cache)
    location = /service-worker.js {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        expires off;
    }
}
'''

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, timeout=15)

sftp = client.open_sftp()
backup_path = "/etc/nginx/conf.d/vidial-media.ru.conf.bak.pre-deploy"

with sftp.file(backup_path, 'w') as f:
    f.write(old_config)

stdin, stdout, stderr = client.exec_command(f"ls -la {backup_path}")
print(stdout.read().decode('utf-8', errors='replace').strip())

sftp.close()
client.close()
print("Backup of old config created.")

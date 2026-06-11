import paramiko
import sys

host = "83.217.203.41"
user = "root"
password = "rA3US@@R5Kg4e6"

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, timeout=15)
    
    print("=== Connected to server ===\n")
    
    # Check web server
    commands = [
        ("Web server version", "nginx -v 2>&1 || apachectl -v 2>&1 || httpd -v 2>&1 || echo 'not found'"),
        ("Nginx sites-enabled", "ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo 'no nginx sites-enabled'"),
        ("Apache sites-enabled", "ls -la /etc/apache2/sites-enabled/ 2>/dev/null || ls -la /etc/httpd/conf.d/ 2>/dev/null || echo 'no apache sites'"),
        ("All document roots from nginx", "grep -rh 'root' /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ 2>/dev/null | grep -v '^#' || echo 'no nginx roots found'"),
        ("All document roots from apache", "grep -rh 'DocumentRoot' /etc/apache2/sites-enabled/ /etc/httpd/conf.d/ 2>/dev/null | grep -v '^#' || echo 'no apache roots found'"),
        ("Server name grep nginx", "grep -rh 'server_name' /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ 2>/dev/null | grep -v '^#' || echo 'no nginx server_names'"),
        ("Server name grep apache", "grep -rh 'ServerName\|ServerAlias' /etc/apache2/sites-enabled/ /etc/httpd/conf.d/ 2>/dev/null | grep -v '^#' || echo 'no apache server_names'"),
        ("WWW directories", "ls -la /var/www/ 2>/dev/null || ls -la /home/ 2>/dev/null || echo 'no typical www dirs'"),
        ("Current vidial-media.ru dir", "find /var/www -maxdepth 3 -type d -iname '*vidial*' 2>/dev/null || find /home -maxdepth 3 -type d -iname '*vidial*' 2>/dev/null || echo 'no vidial dirs found'"),
        ("Current superglazka dirs", "find /var/www -maxdepth 3 -type d -iname '*superglazka*' 2>/dev/null || find /home -maxdepth 3 -type d -iname '*superglazka*' 2>/dev/null || echo 'no superglazka dirs found'"),
    ]
    
    for title, cmd in commands:
        print(f"--- {title} ---")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='replace').strip()
        err = stderr.read().decode('utf-8', errors='replace').strip()
        if out:
            print(out)
        if err and "not found" not in err.lower():
            print(f"STDERR: {err}")
        print()
    
    client.close()
    print("=== Exploration complete ===")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

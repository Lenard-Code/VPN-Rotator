import os

base = "rotating-vpn-proxy"
dirs = [
    f"{base}/vpn-proxy",
    f"{base}/frontend-rotator",
    f"{base}/vpn-configs",
    f"{base}/vpn-auth/nordvpn",
    f"{base}/vpn-auth/pia",
    f"{base}/vpn-auth/hma",
    f"{base}/vpn-auth/expressvpn",
]
files = {
    f"{base}/docker-compose.yml": """version: '3.8'
services:
  vpn-proxy-1:
    build: ./vpn-proxy
    environment:
      - VPN_CONFIG=/vpn/nordvpn.ovpn
    volumes:
      - ./vpn-configs/nordvpn.ovpn:/vpn/nordvpn.ovpn:ro
      - ./vpn-auth/nordvpn:/vpn/auth:ro
    ports:
      - "10001:10000"
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
  vpn-proxy-2:
    build: ./vpn-proxy
    environment:
      - VPN_CONFIG=/vpn/pia.ovpn
    volumes:
      - ./vpn-configs/pia.ovpn:/vpn/pia.ovpn:ro
      - ./vpn-auth/pia:/vpn/auth:ro
    ports:
      - "10002:10000"
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
  vpn-proxy-3:
    build: ./vpn-proxy
    environment:
      - VPN_CONFIG=/vpn/hma.ovpn
    volumes:
      - ./vpn-configs/hma.ovpn:/vpn/hma.ovpn:ro
      - ./vpn-auth/hma:/vpn/auth:ro
    ports:
      - "10003:10000"
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
  vpn-proxy-4:
    build: ./vpn-proxy
    environment:
      - VPN_CONFIG=/vpn/expressvpn.ovpn
    volumes:
      - ./vpn-configs/expressvpn.ovpn:/vpn/expressvpn.ovpn:ro
      - ./vpn-auth/expressvpn:/vpn/auth:ro
    ports:
      - "10004:10000"
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
  frontend-rotator:
    build: ./frontend-rotator
    ports:
      - "9000:9000"
    depends_on:
      - vpn-proxy-1
      - vpn-proxy-2
      - vpn-proxy-3
      - vpn-proxy-4
    restart: unless-stopped
""",
    f"{base}/vpn-proxy/Dockerfile": """FROM alpine:latest
RUN apk add --no-cache openvpn socat
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
""",
    f"{base}/vpn-proxy/entrypoint.sh": """#!/bin/sh
openvpn --config "$VPN_CONFIG" --daemon
sleep 5
socat TCP-LISTEN:10000,fork,reuseaddr TCP4-CONNECT:$1:$2
""",
    f"{base}/frontend-rotator/Dockerfile": """FROM python:3-alpine
COPY rotator.py /rotator.py
ENTRYPOINT ["python3", "/rotator.py"]
""",
    f"{base}/frontend-rotator/rotator.py": """import socket
import threading

PROXIES = [("vpn-proxy-1", 10000), ("vpn-proxy-2", 10000), ("vpn-proxy-3", 10000), ("vpn-proxy-4", 10000)]
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 9000

counter = 0
lock = threading.Lock()

def relay(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    finally:
        src.close()
        dst.close()

def handle_client(client_sock):
    global counter
    with lock:
        proxy_host, proxy_port = PROXIES[counter % len(PROXIES)]
        counter += 1
    remote = socket.create_connection((proxy_host, proxy_port))
    t1 = threading.Thread(target=relay, args=(client_sock, remote))
    t2 = threading.Thread(target=relay, args=(remote, client_sock))
    t1.start(); t2.start()
    t1.join(); t2.join()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((LISTEN_HOST, LISTEN_PORT))
    s.listen(100)
    while True:
        client_sock, _ = s.accept()
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    main()
""",
    f"{base}/vpn-configs/nordvpn.ovpn": "",
    f"{base}/vpn-configs/pia.ovpn": "",
    f"{base}/vpn-configs/hma.ovpn": "",
    f"{base}/vpn-configs/expressvpn.ovpn": "",
    f"{base}/vpn-auth/nordvpn/auth.txt": "",
    f"{base}/vpn-auth/pia/auth.txt": "",
    f"{base}/vpn-auth/hma/auth.txt": "",
    f"{base}/vpn-auth/expressvpn/auth.txt": "",
}

for d in dirs:
    os.makedirs(d, exist_ok=True)

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

os.chmod(f"{base}/vpn-proxy/entrypoint.sh", 0o755)
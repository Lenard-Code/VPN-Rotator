import socket
import threading

PROXIES = [
    ("vpn-proxy-1", 10001),
    ("vpn-proxy-2", 10002),
    ("vpn-proxy-3", 10003),
    ("vpn-proxy-4", 10004),
    ("vpn-proxy-5", 10005),
    ("vpn-proxy-6", 10006)
]
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
    except Exception:
        pass
    finally:
        try: src.shutdown(socket.SHUT_RDWR)
        except: pass
        try: dst.shutdown(socket.SHUT_RDWR)
        except: pass
        src.close()
        dst.close()

def handle_client(client_sock):
    global counter
    try:
        req = b""
        while b"\r\n\r\n" not in req:
            chunk = client_sock.recv(4096)
            if not chunk:
                client_sock.close()
                return
            req += chunk
        first_line = req.split(b"\r\n", 1)[0].decode(errors="ignore")
        method, target, _ = first_line.split(" ")

        with lock:
            proxy_host, proxy_port = PROXIES[counter % len(PROXIES)]
            counter += 1

        proxy_sock = socket.create_connection((proxy_host, proxy_port))

        if method.upper() == "CONNECT":
            proxy_sock.sendall(req)
            response = b""
            while b"\r\n\r\n" not in response:
                chunk = proxy_sock.recv(4096)
                if not chunk:
                    client_sock.close()
                    proxy_sock.close()
                    return
                response += chunk
            client_sock.sendall(response)
        else:
            proxy_sock.sendall(req)

        t1 = threading.Thread(target=relay, args=(client_sock, proxy_sock))
        t2 = threading.Thread(target=relay, args=(proxy_sock, client_sock))
        t1.start(); t2.start()
        t1.join(); t2.join()
    except Exception:
        client_sock.close()

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
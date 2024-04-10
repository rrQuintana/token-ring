import socket
import threading
import sys

def iniciar_servidor(host, port, siguiente_host, siguiente_port):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(1)
    print(f"Servidor esperando conexiones en {host}:{port}...")

    conn, addr = servidor.accept()
    with conn:
        print(f"Conectado por {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Token recibido: {data.decode()}")
            enviar_token(siguiente_host, siguiente_port, data.decode())

def enviar_token(host, port, token):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f"Enviando token a {host}:{port}")
        sock.sendall(token.encode())

if __name__ == "__main__":
    # Configuración de la "computadora" actual y la siguiente en el anillo
    mi_host = "127.0.0.1"
    mi_puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    siguiente_host = "127.0.0.1"
    siguiente_puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 5001

    # Inicia el servidor en un hilo separado
    threading.Thread(target=iniciar_servidor, args=(mi_host, mi_puerto, siguiente_host, siguiente_puerto), daemon=True).start()

    input("Presiona Enter después de iniciar todas las instancias para enviar el token...")

    # El primer token se envía manualmente para iniciar el ciclo
    enviar_token(siguiente_host, siguiente_puerto, "TOKEN_INICIAL")

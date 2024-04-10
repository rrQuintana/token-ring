import os
import socket
import threading
import time

# Dirección IP del host actual
my_host = '175.1.58.24'

# Lista de direcciones IP de los otros hosts en el anillo
hostList = ["175.1.57.71", "175.1.61.58"]


# Puerto para la comunicación
port = 12345

# Función para recibir conexiones de los hosts en el anillo
def receive_connections(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        # Se puede hacer algo con la conexión, pero en este caso no se hace nada.
        conn.close()

# Función para enviar el token al siguiente host en el anillo
def send_token(host, port, token):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(token.encode('utf-8'))  # Envía el token al siguiente host
    print(f"Token enviado a {host}")

    client_socket.close()

# Función para manejar la simulación
def start_simulation():
    print("Simulación iniciada.")
    while True:
        for next_host in hostList:
            send_token(next_host, port, "TOKEN")
            time.sleep(1)  # Espera 1 segundo antes de enviar el token al siguiente host

if __name__ == "__main__":
    # Iniciar subproceso para recibir conexiones de los hosts
    connection_thread = threading.Thread(target=receive_connections, args=(my_host, port))
    connection_thread.start()

    input("Presione Enter para iniciar la simulación con todos los hosts conectados.")

    # Iniciar simulación
    start_simulation()

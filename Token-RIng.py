import os
import socket
import threading
import time

Roberto = '175.1.58.24'
Oliver = '175.1.57.71'
Jose = '175.1.61.58'

# Dirección IP del host actual
my_host = Roberto

# Lista de direcciones IP de los otros hosts en el anillo
hostList = [Oliver, Jose]

# Puerto para la comunicación
port = 12345

# Variable para indicar si el host tiene el token o no
has_token = False

# Función para recibir conexiones de los hosts en el anillo
def receive_connections(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        global has_token
        # Imprimir "token recibido"
        print("Token recibido")
        if not has_token:
            execute_task()
            has_token = True
        conn.close()

# Función para enviar el token al siguiente host en el anillo
def send_token(host, port, token):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(token.encode('utf-8'))  # Envía el token al siguiente host
    print(f"Token enviado a {host}")

    client_socket.close()

# Función para simular la ejecución de una tarea
def execute_task():
    print("Simulando ejecución de tarea...")
    time.sleep(2)  # Simulamos una tarea que tarda 2 segundos en ejecutarse
    print("Tarea completada.")

# Función para manejar la simulación
def start_simulation():
    print("Simulación iniciada.")
    while True:
        if has_token:
            for next_host in hostList:
                send_token(next_host, port, "TOKEN")  # Envía el token al siguiente host
            has_token = False
        time.sleep(1)

if __name__ == "__main__":
    # Iniciar subproceso para recibir conexiones de los hosts
    connection_thread = threading.Thread(target=receive_connections, args=(my_host, port))
    connection_thread.start()

    input("Presione Enter para iniciar la simulación con todos los hosts conectados.")

    # Iniciar simulación
    start_simulation()

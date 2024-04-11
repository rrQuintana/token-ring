import socket
import threading
import time

# Direcciones IP de los hosts en el anillo
hosts = {
    'Roberto': '175.1.58.24',
    'Oliver': '175.1.57.71',
    'Uziel': '175.1.60.131',
    'Jose': '175.1.61.58',
}

# Configuración del host actual
my_name = 'Oliver'  
my_host = hosts[my_name]

# Encuentra el siguiente host en el anillo
next_name = list(hosts.keys())[(list(hosts.keys()).index(my_name) + 1) % len(hosts)]
next_host = hosts[next_name]

# Puerto para la comunicación
port = 12345

# Función para recibir el token
def receive_token():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((my_host, port))
        server_socket.listen()
        print(f"Esperando token en {my_host}:{port}")
        conn, _ = server_socket.accept()
        with conn:
            print("Token recibido")
            # Simula la ejecución de una tarea
            time.sleep(2)
            print("Tarea completada.")

# Función para enviar el token al siguiente host en el anillo
def send_token():
    time.sleep(5)  # Espera inicial antes de enviar el token por primera vez
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((next_host, port))
        print(f"Enviando token a {next_name} ({next_host})")
        client_socket.send(b"TOKEN")

if __name__ == "__main__":
    # Iniciar hilo para recibir el token
    threading.Thread(target=receive_token, daemon=True).start()

    # Enviar el token al siguiente host después de una espera inicial
    send_token()

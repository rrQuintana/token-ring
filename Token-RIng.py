import socket
import threading

# Puerto para la comunicación
PUERTO = 5000

# Lista de nodos en el anillo
NODOS = ["175.1.58.24", "175.1.57.71", "175.1.61.58"]

# Variable para almacenar el token
token = False

# Función para enviar el token al siguiente nodo
def enviar_token(nodo):
    global token

    # Crear un socket para enviar el token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((nodo, PUERTO))

    # Enviar el token al siguiente nodo
    sock.sendall(b"TOKEN")
    sock.close()

    # Indicar que ya no se tiene el token
    token = False

# Función para escuchar mensajes del anillo
def escuchar_mensajes():
    global token

    # Crear un socket para escuchar mensajes
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PUERTO))
    sock.listen(1)

    while True:
        # Recibir una conexión
        conn, addr = sock.accept()

        # Recibir el mensaje
        mensaje = conn.recv(1024).decode()

        # Si el mensaje es el token, procesarlo
        if mensaje == "TOKEN":
            # Indicar que se tiene el token
            token = True

            # Si hay un siguiente nodo, enviarle el token
            if NODOS.index(addr[0]) < len(NODOS) - 1:
                siguiente_nodo = NODOS[NODOS.index(addr[0]) + 1]
                enviar_token(siguiente_nodo)

        # Cerrar la conexión
        conn.close()

# Iniciar el hilo para escuchar mensajes
hilo_escucha = threading.Thread(target=escuchar_mensajes)
hilo_escucha.start()

# Enviar el token al primer nodo
enviar_token(NODOS[0])

# Bucle principal para esperar a que el usuario quiera salir
while True:
    # Si el usuario tiene el token, puede realizar alguna acción
    if token:
        print("¡Tienes el token!")
        # ...

    # Esperar a que el usuario presione una tecla para salir
    input("Presiona enter para salir...")
    break

# Detener el hilo para escuchar mensajes
hilo_escucha.join()

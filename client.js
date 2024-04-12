const readline = require('readline');
const io = require('socket.io-client');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Dirección IP del servidor
const serverIP = '127.0.0.1'; // Cambia esto con la IP de tu servidor

// Conectar al servidor
const socket = io.connect(`http://${serverIP}`);

socket.on('connect', () => {
    console.log('Conectado al servidor.');
    // Enviar mensaje al servidor indicando que el cliente se ha conectado
    socket.emit('message', 'Cliente conectado');
});

// Escuchar mensajes del servidor
socket.on('message', (data) => {
    console.log('Mensaje del servidor:', data);
});

// Leer entrada del usuario desde la consola y enviarla al servidor
rl.on('line', (input) => {
    // Enviar mensaje al servidor
    socket.emit('message', input);
});

// Manejar desconexión del servidor
socket.on('disconnect', () => {
    console.log('Desconectado del servidor.');
    rl.close();
});

// Cerrar la interfaz de lectura cuando se desconecta el servidor
rl.on('close', () => {
    process.exit(0);
});

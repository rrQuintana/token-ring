const http = require('http');
const socketio = require('socket.io');

const server = http.createServer((req, res) => {
    // Código para manejar solicitudes HTTP si es necesario
});

const io = socketio(server);

io.on('connection', (socket) => {
    console.log('Cliente conectado.');

    // Enviar mensaje de bienvenida al cliente conectado
    socket.emit('message', '¡Hola! Bienvenido al servidor.');

    // Escuchando mensajes del cliente
    socket.on('message', (data) => {
        console.log('Mensaje recibido del cliente:', data);

        // Puedes hacer algo con el mensaje recibido, como registrar en un archivo de log
        // O ejecutar alguna acción en base a ese mensaje

        // Enviar una respuesta al cliente
        socket.emit('message', 'Mensaje recibido por el servidor.');
    });

    // Escuchando eventos de desconexión
    socket.on('disconnect', () => {
        console.log('Cliente desconectado.');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor escuchando en el puerto ${PORT}`);
});

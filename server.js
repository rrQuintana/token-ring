const http = require('http');
const socketio = require('socket.io');

const server = http.createServer((req, res) => {
    res.end('Token Ring Server');
});

const io = socketio(server);
const clients = [];
const clientStrengths = {};

io.on('connection', (socket) => {
    console.log(`Cliente conectado: ${socket.id}`);
    const strength = Math.random();
    clients.push(socket);
    clientStrengths[socket.id] = strength;

    // Informar a todos los clientes sobre la nueva conexión
    io.emit('message', `Nuevo cliente conectado: ${socket.id}, fuerza: ${strength}`);

    socket.on('disconnect', () => {
        console.log(`Cliente desconectado: ${socket.id}`);
        const index = clients.indexOf(socket);
        if (index > -1) {
            clients.splice(index, 1);
            delete clientStrengths[socket.id];
            io.emit('message', `Cliente ${socket.id} ha caído. Reorganizando...`);
            performLeaderElection();
        }
    });

    socket.on('token', (msg) => {
        console.log(`Token recibido de ${socket.id}: ${msg}`);
        passToken(socket);
    });
});

function passToken(socket) {
    const index = clients.indexOf(socket);
    const nextIndex = (index + 1) % clients.length;
    if (clients[nextIndex]) {
        console.log(`Pasando token al cliente ${clients[nextIndex].id}`);
        clients[nextIndex].emit('token', 'Tienes el token');
    }
}

function performLeaderElection() {
    const strongest = Object.keys(clientStrengths).reduce((a, b) => clientStrengths[a] > clientStrengths[b] ? a : b);
    io.emit('message', `Nuevo líder elegido: ${strongest}`);
    clients.forEach(client => {
        if (client.id === strongest) {
            client.emit('token', 'Eres el nuevo líder y tienes el token');
        }
    });
}

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Servidor escuchando en el puerto ${PORT}`);
});

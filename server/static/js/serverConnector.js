
connected = false;
queue = [];
onmessage = function(e) {
    var message = e.data;
    if (message == "CONNECT") connect();
    else if (!connected) {
        queue.push(message);
    }
    else {
        socket.send(message);
    }
}

function connect() {
    socket = new WebSocket("ws://localhost:31666");

    socket.onopen = function(event){
        console.log("Connection established.");
        connected = true;
        queue.forEach(msg => {
            socket.send(msg);
        });
    };

    socket.onmessage = function(event){handleSignal(event.data)};
    socket.onclose = function(event){
        console.log("Connection closed.");handleSignal("CLOSED")
        connected = false;
    };
    socket.onerror = function(error){console.log(`Error: ${error.message}`)};
}

function handleSignal(signal) {
    postMessage(signal);
}
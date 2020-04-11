onmessage = function(e) {
    message = e.data;
    if (message == "CONNECT") connect();
    else {
        socket.send(message);
    }
}

function connect() {
    socket = new WebSocket("wss://localhost:31666");

    socket.onopen = function(event){console.log("Connection established.")};

    socket.onmessage = function(event){handleSignal(event.data)};
    socket.onclose = function(event){console.log("Connection closed.");handleSignal("CLOSED")};
    socket.onerror = function(error){console.log(`Error: ${error.message}`)};
}

function handleSignal(signal) {
    postMessage(signal);
}
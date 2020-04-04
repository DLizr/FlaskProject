// var canvas = document.querySelector("canvas");

// var c = canvas.getContext("2d");

socket = new WebSocket("wss://localhost:31666");

socket.onopen = function(event){console.log("Connection established."); let 
send=function(){socket.send("Test")};;send();};

socket.onmessage = function(event){console.log(event.data)};
socket.onclose = function(event){console.log("Connection closed.")};
socket.onerror = function(error){console.log(`Error: ${error.message}`)};

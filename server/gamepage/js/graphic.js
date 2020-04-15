var canvas = document.querySelector("canvas");
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

var c = canvas.getContext("2d");
c.font = (window.innerWidth + window.innerHeight) / 60 + "pt Neucha"


var serverConnector = new Worker("js/serverConnector.js");
serverConnector.postMessage("CONNECT");
serverConnector.onmessage = (e) => SCREEN.handleMessage(e.data);


var confirmationMenu = document.getElementById("loadingConfirmationScreen");
confirmationMenu.style.display = "none";

confirmationMenu.getElementsByClassName("acceptButton").item(0).addEventListener("click", function() {
    serverConnector.postMessage("READY");
    loading.ready = true;
});


window.addEventListener("resize", function() {
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    SCREEN.resize();
});


loading = {
    radius: (window.innerHeight + window.innerHeight) / 15,
    speed: 0.04,
    dg: 0,
    dR: 0,
    dDR: 0.4,
    color: "#EEEEEE",
    betweenWallsWidth: 0,

    waiting: true,
    confirming: false,
    speedingUp: false,
    ready: false,

    textX: window.innerWidth/2 - c.measureText("Ожидание противника...").width/2,
    textY: window.innerHeight * 0.3,

    update() {
        if (this.waiting) {
            this.renderWaitingAnimation();
            if (this.confirming) 
                this.renderConfirmationButton();
            if (this.speedingUp)
                this.speedUp();
        } else {
            this.renderOpeningAnimation();
        }
    },

    resize() {
        if (this.waiting) this.radius = (window.innerHeight + window.innerHeight) / 15;
        let f = (window.innerWidth + window.innerHeight) / 60;
        c.font = f + "pt Neucha";
        this.textX = window.innerWidth/2 - c.measureText("Ожидание противника...").width/2;
        this.textY = window.innerHeight * 0.3;
        this.dR = 0;
        this.startRendering();
    },

    renderWaitingAnimation() {
        let x = window.innerWidth / 2; let y = window.innerHeight / 2;
        c.beginPath();

        let r2 = this.radius / 1.5 + this.dR;
        c.fillStyle = "#1300B1";
        c.arc(x, y, this.radius / 1.05, 0, 7);
        c.fill();

        c.fillStyle = this.color;
        c.beginPath();
        c.moveTo(x + r2 * Math.cos(this.dg + Math.PI * 3 / 4),
                 y + r2 * Math.sin(this.dg + Math.PI * 3 / 4));
        c.lineTo(x + r2 * Math.cos(this.dg + Math.PI / 4),
                 y + r2 * Math.sin(this.dg + Math.PI / 4));
        c.lineTo(x + r2 * Math.cos(this.dg - Math.PI / 4),
                 y + r2 * Math.sin(this.dg - Math.PI / 4));
        c.lineTo(x + r2 * Math.cos(this.dg - Math.PI * 3 / 4),
                 y + r2 * Math.sin(this.dg - Math.PI * 3 / 4));
        c.fill()
        
        c.beginPath();
        c.fillStyle="#1300B1";
        c.arc(x, y, r2 / 1.3, 0, 7);
        c.fill();
        c.arc(x, y, r2 / 1.3, 0, 7);
        c.stroke();

        if (r2 > this.radius) this.dDR = -0.4; else if (r2 < this.radius / 3) this.dDR = 0.4;

        this.dg += this.speed;
        this.dR += this.dDR;
        
    },
    
    startRendering() {
        c.fillStyle = "#1300B1";
        c.fillRect(0, 0, window.innerWidth, window.innerHeight);
        c.fillStyle = "#EEEEEE";
        c.arc(window.innerWidth / 2, window.innerHeight / 2, this.radius, 0, 7);
        c.fill();
        c.fillText("Ожидание противника...", this.textX, this.textY);
        c.strokeStyle=this.color;
        c.lineWidth = 5;
    },

    renderConfirmationButton() {
        let o = parseFloat(confirmationMenu.style.opacity)
        if (o != 1) {
            confirmationMenu.style.opacity = o + 0.02;
        }
    },

    speedUp() {
        loading.speed += 0.004;
        loading.radius *= 1.02;
    },

    startSpeedingUp() {
        c.fillRect(0, 0, window.innerWidth, window.innerHeight);
        this.speedingUp = true;
        setInterval(() => this.waiting = false, 2500);
    },

    renderOpeningAnimation() {
        if (this.betweenWallsWidth*2 <= window.innerWidth) {
            this.betweenWallsWidth += 10;
            c.fillStyle = "#DDDDDD";
            c.fillRect(window.innerWidth/2-this.betweenWallsWidth, 0, 2*this.betweenWallsWidth, window.innerHeight);
        }
        else {
            SCREEN = phase1;
            SCREEN.start();
        }
    },

    handleMessage(message) {
        switch (message) {
            case "READY_CHECK":
                confirmationMenu.style.opacity = 0;
                confirmationMenu.style.display = "block";
                loading.confirming = true;
                break;
            
            case "PHASE_1":
                confirmationMenu.style.display = "none";
                loading.startSpeedingUp();
                serverConnector.postMessage("OK");
                break;
            
            case "CLOSED":
                this.speed = 0.04;
                this.dR = 0;
                this.waiting = true;
                this.confirming = false;
                this.speedingUp = false;
                this.ready = false;

                confirmationMenu.style.display = "none";

                setTimeout(() => serverConnector.postMessage("CONNECT"), 5000);
                break;
            
            case "KICKED:AFK":
                window.location.assign("http://google.com"); // TODO
                break;
            
            case "KICKED:NO_RESPONSE":
                window.location.assign("http://google.com"); // TODO
                break
            
            default:
                console.error("Undefined message: " + message);
        }
    }
}


phase1 = {
    startRendering() {
        window.addEventListener("click", this.onclick);
        grid.create();
    },
    
    handleMessage(msg) {

    },

    update() {

    }
}

grid = {
    x: 50,
    y: 50,
    hTiles: 5,
    vTiles: 5,
    tileWidth: 100,
    tileHeight: 100,

    draw() {
        
    },

    create() {
        var field = document.getElementById("phase1field")
        field.style.width = `${this.hTiles * (this.tileWidth + 4)}px`;
        field.style.height = `${this.vTiles * (this.tileHeight + 4)}px`;
        field.style.left = `${this.x}px`;
        field.style.top = `${this.y}px`;

        for (let i=0; i<this.hTiles * this.vTiles; i++) {
            let cell = document.createElement("div");
            cell.className = "cell";
            cell.style.width = `${this.tileWidth}px`;
            cell.style.height = `${this.tileHeight}px`;
            field.appendChild(cell);
        }
    }
}


var SCREEN = phase1;
SCREEN.startRendering();
render = function() {
    try {
        SCREEN.update();
    } catch {/* Display is being resized, waiting. */}
    window.requestAnimationFrame(render);
}


render();

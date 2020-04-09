var canvas = document.querySelector("canvas");
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

var c = canvas.getContext("2d");
c.font = (window.innerWidth + window.innerHeight) / 60 + "pt Neucha"


var serverConnector = new Worker("js/serverConnector.js");
serverConnector.postMessage("CONNECT");
serverConnector.onmessage = function(e) {
    let msg = e.data;
    switch (msg) {
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
    }
};


var confirmationMenu = document.getElementById("loadingConfirmationScreen");
confirmationMenu.style.display = "none";

confirmationMenu.getElementsByClassName("acceptButton").item(0).addEventListener("click", function() {
    serverConnector.postMessage("READY");
});


window.addEventListener("resize", function() {
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    if (loading.waiting) loading.radius = (window.innerHeight + window.innerHeight) / 15;
    let f = (window.innerWidth + window.innerHeight) / 60;
    c.font = f + "pt Neucha";
    loading.textX = window.innerWidth/2 - c.measureText("Ожидание противника...").width/2;
    loading.textY = window.innerHeight * 0.3;
    loading.startRendering();
});


loading = new function() {
    this.radius = (window.innerHeight + window.innerHeight) / 15;
    this.speed = 0.04;
    this.dg = 0;
    this.dR = 0;
    this.dDR = 0.4;
    this.color = "#EEEEEE";
    this.betweenWallsWidth = 0;

    this.waiting = true;
    this.confirming = false;
    this.speedingUp = false;

    this.render = function() {
        if (this.waiting) {
            this.renderWaitingAnimation();
            if (this.confirming) 
                this.renderConfirmationButton();
            if (this.speedingUp)
                this.speedUp();
        } else {
            this.renderOpeningAnimation();
        }
    }

    this.renderWaitingAnimation = function() {
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
        
    };
    
    this.startRendering = function() {
        c.fillStyle = "#1300B1";
        c.fillRect(0, 0, window.innerWidth, window.innerHeight);
        c.fillStyle = "#EEEEEE";
        c.arc(window.innerWidth / 2, window.innerHeight / 2, this.radius, 0, 7);
        c.fill();
        c.fillText("Ожидание противника...", this.textX, this.textY);
        c.strokeStyle=this.color;
        c.lineWidth = 5;
    }

    this.textX = window.innerWidth/2 - c.measureText("Ожидание противника...").width/2;
    this.textY = window.innerHeight * 0.3;

    this.renderConfirmationButton = function() {
        let o = parseFloat(confirmationMenu.style.opacity)
        if (o != 1) {
            confirmationMenu.style.opacity = o + 0.02;
        }
    };

    this.speedUp = function() {
        loading.speed += 0.004;
        loading.radius *= 1.02;
    };

    this.startSpeedingUp = function() {
        c.fillRect(0, 0, window.innerWidth, window.innerHeight);
        this.speedingUp = true;
        setInterval(() => this.waiting = false, 2500);
    }

    this.renderOpeningAnimation = function() {
        if (this.betweenWallsWidth <= window.innerWidth) this.betweenWallsWidth += 10;
        c.fillStyle = "#DDDDDD";
        c.fillRect(window.innerWidth/2-this.betweenWallsWidth, 0, 2*this.betweenWallsWidth, window.innerHeight);
    };
}


render = function() {
    loading.render();
    window.requestAnimationFrame(render);
}


loading.startRendering();
render();

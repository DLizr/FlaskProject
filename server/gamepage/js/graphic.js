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
            this.betweenWallsWidth += window.innerWidth / 120;
            c.fillStyle = "#DDDDDD";
            c.fillRect(window.innerWidth/2-this.betweenWallsWidth, 0, 2*this.betweenWallsWidth, window.innerHeight);
        }
        else {
            SCREEN = phase1;
            SCREEN.startRendering();
            serverConnector.postMessage("OK");
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


Buildings = {
    _sources: ["./img/core.svg", "./img/wall.svg", "./img/mortar.svg"],
    _shortcuts: ["0", "C", "W", "M"],
    EMPTY: -1,
    CORE: 0,
    WALL: 1,
    MORTAR: 2
}

AttackBuildings = {
    _sources: ["./img/cannon.svg", "./img/crossbow.svg"],
    _shortcuts: ["0", "A", "R"],
    EMPTY: -1,
    CANNON: 0,
    CROSSBOW: 1
}

AllBuildings = {
    _sources: ["./img/core.svg", "./img/wall.svg", "./img/mortar.svg", "./img/cannon.svg", "./img/crossbow.svg"],
    _shortcuts: ["0", "C", "W", "M", "A", "R"],
    EMPTY: -1,
    CORE: 0,
    WALL: 1,
    MORTAR: 2,
    CANNON: 3,
    CROSSBOW: 4
}

currentBuildings = Buildings;


gameScreen = {
    selected: -1,

    mouseX: 0,
    mouseY: 0,
    mouseDown: false,
    mouseMoved: false,
    readOnly: false,

    timer: document.getElementById("timer"),

    tooltips: [
        document.getElementById("phase1wallTooltip"),
        document.getElementById("phase1coreTooltip"),
        document.getElementById("phase1mortarTooltip")
    ],

    startListening() {
        window.addEventListener("mousemove", this.onmove);
        window.addEventListener("mousedown", this.ondown);
        window.addEventListener("mouseup", this.onup);
        window.addEventListener("wheel", this.onwheel);
    },

    stopListening() {
        window.removeEventListener("mousedown", this.ondown);
        window.removeEventListener("mousemove", this.onmove);
        window.removeEventListener("mouseup", this.onup);
        window.removeEventListener("wheel", this.onwheel);
    },

    onup(e) {
        gameScreen.mouseDown = false;

        let x = e.clientX;
        let y = e.clientY;

        for (let i=0; i<gameScreen.menu.children.length; i++) {
            let rect = gameScreen.menu.children[i].getBoundingClientRect();
            if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
                if (i == gameScreen.selected) {
                    gameScreen.selected = -1;
                    gameScreen.menu.children[i].style.backgroundColor = "#00566B";
                } else {
                    gameScreen.selected = i;
                    gameScreen.menu.children[i].style.backgroundColor = "#4096AB";
                }
                   
                return;
            }
        }

        if (!gameScreen.mouseMoved && !gameScreen.readOnly)
            grid.onclick(x, y);
        gameScreen.mouseMoved = false;
    },

    onmove(e) {
        let x = e.clientX;
        let y = e.clientY;

        for (let i=0; i<gameScreen.menu.children.length; i++) {
            let rect = gameScreen.menu.children[i].getBoundingClientRect();
            if ((x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom)) {
                gameScreen.tooltips[i].style.display = "block";
                gameScreen.menu.children[i].style.backgroundColor = "#4096AB";
            } else {
                gameScreen.tooltips[i].style.display = "none";
                if (gameScreen.selected != i)
                    gameScreen.menu.children[i].style.backgroundColor = "#00566B";
            }
        }

        if (gameScreen.mouseDown) {
            grid.move(x - gameScreen.mouseX, y - gameScreen.mouseY);
            gameScreen.mouseX = x;
            gameScreen.mouseY = y;
            gameScreen.mouseMoved = true;
        }

        grid.onhover(x, y);
        
    },

    ondown(e) {
        gameScreen.mouseX = e.clientX;
        gameScreen.mouseY = e.clientY;
        gameScreen.mouseDown = true;
    },

    onwheel(e) {
        if (e.deltaY == -3) {
            grid.zoomIn();
        } else {
            grid.zoomOut();
        }
    },
}


phase1 = {
    selected: -1,
    buildingIndex: 0,

    startRendering() {
        this.prototype = gameScreen;
        this.prototype.menu = document.getElementById("phase1").getElementsByClassName("towerMenu")[0]
        this.prototype.startListening();

        let p = document.getElementById("phase1");
        p.style.display = "block";
        timer.style.display = "block";

        grid.create();
        this.resize();
    },
    
    handleMessage(msg) {
        switch (msg) {
            case "TIME:0":
                gameScreen.timer.innerHTML = "00:00";
                gameScreen.timer.style.color = "#FF0000";
                phase1.onTimeEnd();
                break;
            case "GET_BASE":
                serverConnector.postMessage("OK");
                phase1.onPhaseEnd();
                break;
            case "PHASE_2":
                serverConnector.postMessage("OK")
                document.getElementById("phase1").style.display = "none";
                SCREEN = phase2;
                SCREEN.startRendering();
        }
        if (msg.startsWith("TIME:")) {
            let time = parseInt(msg.split(":")[1]);
            let m = Math.floor(time / 60).toString();
            let s = (time % 60).toString()
            if (m.length == 1) m = "0" + m;
            if (s.length == 1) s = "0" + s;
            gameScreen.timer.innerHTML = `${m}:${s}`
        }
    },

    update() {

    },

    resize() {
        
    },

    onTimeEnd() {
        document.getElementById("phase1").style.opacity = 0.2;
        document.getElementById("dataExchange").style.display = "block";
        this.prototype.stopListening();
    },

    onPhaseEnd() {
        var cell = grid.field[phase1.buildingIndex];
        if (!cell.isLocked) {
            let c = Buildings._shortcuts[cell.building + 1];
            serverConnector.postMessage(c); 
        }
        phase1.buildingIndex++;
        if (phase1.buildingIndex < 49) {
            setTimeout(phase1.onPhaseEnd);
        }
    },

}

class Cell {

    isLocked = false;
    building = -1;
    preview = -1;
    hp = 0;
    cell;

    constructor(cell) {
        this.cell = cell;
    }

    lock() {
        this.isLocked = true;
        this.cell.style.border = "2px solid red";
        this.cell.style.backgroundColor = "#FFBBBB";
    }

    setBuilding(building) {
        if (this.isLocked) return;
        try {
            this.cell.removeChild(this.cell.lastChild);
            this.hp = 0;
        }
        catch (TypeError) {/* No building */}

        if (building != -1) {
            let img = document.createElement("img");
            img.src = currentBuildings._sources[building];
            img.ondragstart = () => {return false};
            this.cell.appendChild(img);
        }
        this.building = building;
        this.hp = Hitpoints.get(building);
    }

    previewBuilding(building) {
        if (this.building != -1 || this.isLocked) return;
        try {
            this.cell.removeChild(this.cell.lastChild);
        } catch (TypeError) {/* No building */}
        if (building != -1) {
            let img = document.createElement("img");
            img.src = currentBuildings._sources[building];
            img.style.opacity = "0.8";
            img.ondragstart = () => {return false};
            this.cell.appendChild(img);
        }
        this.preview = building;
        
    }
}


grid = {
    x: 50,
    y: 50,
    hTiles: 7,
    vTiles: 7,
    tileWidth: 100,
    tileHeight: 100,
    borderedWidth: 104,
    borderedHeight: 104,
    field: [],
    fieldObjects: [],
    grid: document.getElementById("field"),

    hovered: new Cell(),
    border: 4,
    tileBorder: 2,

    draw() {
        
    },

    create() {
        this.borderedWidth = this.tileWidth + 4;
        this.borderedHeight = this.tileHeight + 4;
        this.grid.style.width = `${this.hTiles * this.borderedWidth}px`;
        this.grid.style.height = `${this.vTiles * this.borderedHeight}px`;
        this.grid.style.left = `${this.x}px`;
        this.grid.style.top = `${this.y}px`;

        this.grid.style.display = "block";
        
        for (let i=0; i<this.hTiles * this.vTiles; i++) {
            let cell = document.createElement("div");
            cell.className = "cell";
            cell.style.width = `${this.tileWidth}px`;
            cell.style.height = `${this.tileHeight}px`;
            this.field.push(new Cell(cell));
            this.grid.appendChild(cell);
        }
        this.hovered = this.field[0];
    },

    resize() {
        for (let i=0; i<this.hTiles * this.vTiles; i++) {
            let cell = this.field[i];
            cell.cell.style.width = `${this.tileWidth}px`;
            cell.cell.style.height = `${this.tileHeight}px`;
            cell.cell.style.border = `${this.tileBorder}px solid gray`;
        }
        this.grid.style.width = `${this.hTiles * this.borderedWidth}px`;
        this.grid.style.height = `${this.vTiles * this.borderedHeight}px`;
        this.grid.style.border = `${this.border}px solid black`;
    },

    move(dx, dy) {
        this.x += dx;
        this.y += dy;

        this.grid.style.left = `${this.x}px`;
        this.grid.style.top = `${this.y}px`;

        this.fieldObjects.forEach(obj => {
            let x = parseFloat(obj.style.left);
            let y = parseFloat(obj.style.top);
            obj.style.left = `${x + dx}px`;
            obj.style.top = `${y + dy}px`;
        });
    },

    zoomIn() {
        this.tileWidth *= 2;
        this.borderedWidth = this.borderedWidth * 2 - 4;
        this.tileHeight *= 2;
        this.borderedHeight = this.borderedHeight * 2 - 4;
        
        this.resize();
    },

    zoomOut() {
        if (this.tileWidth > 50) {
            this.tileWidth /= 2;
            this.borderedWidth = this.borderedWidth / 2 + 2;
            this.tileHeight /= 2;
            this.borderedHeight = this.borderedHeight / 2 + 2;
            
            this.resize();
        }
    },

    setBuilding(n, building) {
        let cell = this.field[n];
        if (cell == undefined) return;

        cell.setBuilding(building);
        if (currentBuildings._shortcuts[building + 1] == "R") {
            if (n % this.hTiles < 2) cell.cell.firstChild.style.transform = "rotate(270deg)";
            else if (n % this.hTiles > 8) cell.cell.firstChild.style.transform = "rotate(90deg)";
            else if (n / this.vTiles > 8) cell.cell.firstChild.style.transform = "rotate(180deg)";
        }
    },

    setBuildingByAbsolute(x, y, building) {
        let rX = this.getRelativeX(x);
        let rY = this.getRelativeY(y);

        let n = rY * this.hTiles + rX;
        this.setBuilding(n, building);
    },

    clear() {
        this.field.clear();
        while (this.grid.firstChild) this.grid.removeChild(this.grid.lastChild);
    },

    getAbsoluteX(x) {
        return this.x + this.borderedWidth * (x + 0.5) + this.border - this.tileBorder;
    },

    getAbsoluteY(y) {
        return this.y + this.borderedHeight * (y + 0.5) + this.border - this.tileBorder;
    },

    getRelativeX(x) {
        return Math.floor((x - this.x - this.border) / this.borderedWidth);
    },

    getRelativeY(y) {
        return Math.floor((y - this.y - this.border) / this.borderedHeight);
    },

    onclick(x, y) {
        this.setBuildingByAbsolute(x, y, gameScreen.selected);
            
    },

    onhover(x, y) {
        let cell = this.getCellByAbsoluteCoords(x, y);
        if (cell == undefined) return;
        if (cell != this.hovered) {
            this.hovered.previewBuilding(-1);
            this.hovered.cell.style.opacity = "1";
            cell.previewBuilding(gameScreen.selected);
            cell.cell.style.opacity = "0.5";
            this.hovered = cell;
        }
    
    },

    getCellByAbsoluteCoords(x, y) {
        x -= this.x;
        y -= this.y;
        if (0 < x && x < this.borderedWidth * this.hTiles &&
            0 < y && y < this.borderedHeight * this.vTiles) {
                x = Math.floor(x / this.borderedWidth);
                y = Math.floor(y / this.borderedHeight);
                let cell = grid.field[y * this.hTiles + x];
                return cell;
            }
    }
}


phase2 = {

    gettingBase: false,
    currentIndex: 24,

    tooltips: [
        document.getElementById("phase2cannonTooltip"),
        document.getElementById("phase2crossbowTooltip")
    ],

    startRendering() {
        this.prototype = gameScreen;
        this.prototype.tooltips = this.tooltips;

        let p = document.getElementById("phase2");
        this.prototype.menu = p.getElementsByClassName("towerMenu")[0];
        p.style.display = "block";

        grid.field = [];
        while (grid.grid.firstChild) grid.grid.removeChild(grid.grid.lastChild);
        grid.hTiles += 4;
        grid.vTiles += 4;
        grid.create();
        gameScreen.selected = -1;
    },

    handleMessage(msg) {
        if (phase2.gettingBase) {
            let building = Buildings._shortcuts.indexOf(msg);
            grid.field[phase2.currentIndex].setBuilding(building - 1);
            grid.field[phase2.currentIndex].lock()
            phase2.currentIndex++;
            
            if (phase2.currentIndex == 97) {
                this.onPhaseBeginning();
            }
            // Each row has 11 elements, 1st and 2nd rows are untouched, therefore 22 + (11 * 7) = 99 is the beggining of nondefending row.
            // 99 - 2 is the first nondefending column.

            if ((phase2.currentIndex + 2) % 11 == 0) phase2.currentIndex += 4;
            // Reached the right corner.

            return;
        }

        switch (msg) {
            case "SEND_BASE":
                serverConnector.postMessage("OK");
                phase2.gettingBase = true;
                gameScreen.timer.style.color = "#000000";
                break;
            
            case "GET_BASE":
                serverConnector.postMessage("OK");
                phase2.onPhaseEnd();
                break;
            
            case "TIME:0":
                gameScreen.timer.innerHTML = "00:00";
                gameScreen.timer.style.color = "#FF0000";
                phase2.onTimeEnd();
                break;
            
            case "PHASE_3":
                serverConnector.postMessage("OK");
                document.getElementById("phase2").style.display = "none";
                SCREEN = phase3;
                SCREEN.startRendering();
        }

        if (msg.startsWith("TIME:")) {
            let time = parseInt(msg.split(":")[1]);
            let m = Math.floor(time / 60).toString();
            let s = (time % 60).toString()
            if (m.length == 1) m = "0" + m;
            if (s.length == 1) s = "0" + s;
            gameScreen.timer.innerHTML = `${m}:${s}`
        }
    },

    resize() {

    },

    update() {

    },

    onPhaseBeginning() {
        document.getElementById("dataExchange").style.display = "none";
        this.prototype.startListening();
        currentBuildings = AttackBuildings;

        phase2.gettingBase = false;
    },

    onTimeEnd() {
        document.getElementById("phase2").style.opacity = 0.2;
        document.getElementById("dataExchange").style.display = "block";
        this.prototype.stopListening();
    },

    onPhaseEnd() {
        grid.field.forEach(cell => {
            if (!cell.isLocked) {
                let c = AttackBuildings._shortcuts[cell.building + 1];
                serverConnector.postMessage(c);
            }
        });
    }
}

BulletSpeeds = new Map([  // In tiles/second.
    [AllBuildings.CANNON, 0.8],
    [AllBuildings.MORTAR, 0.5],
    [AllBuildings.CROSSBOW, 1.6]
]);

Hitpoints = new Map([
    [AllBuildings.CORE, 15],
    [AllBuildings.WALL, 20],
    [AllBuildings.MORTAR, 15],
    [AllBuildings.CANNON, 10],
    [AllBuildings.CROSSBOW, 10]
]);

Damages = new Map([
    [AllBuildings.CANNON, 5],
    [AllBuildings.MORTAR, 10],
    [AllBuildings.CROSSBOW, 2]
]);


phase3 = {

    gettingBase: false,
    currentIndex: 0,
    wins: 0,
    loses: 0,

    bullets: [],
    phaseElement: document.getElementById("phase3"),

    startRendering() {
        this.prototype = gameScreen;

        this.prototype.menu = this.phaseElement.getElementsByClassName("towerMenu")[0];
        this.prototype.readOnly = true;
        this.prototype.startListening();

        window.addEventListener("wheel", this.onwheel);

        currentBuildings = AllBuildings;

        grid.field = [];
        while (grid.grid.firstChild) grid.grid.removeChild(grid.grid.lastChild);
        grid.create();
        gameScreen.selected = -1;
    },

    handleMessage(msg) {
        if (phase3.gettingBase) {
            let building = AllBuildings._shortcuts.indexOf(msg);
            grid.setBuilding(phase3.currentIndex, building-1);
            phase3.currentIndex++;
            
            if (phase3.currentIndex == 121) {
                this.gettingBase = false;
                document.getElementById("dataExchange").style.display = "none";
            }
            return;
        }

        switch (msg) {
            case "SEND_BASE":
                serverConnector.postMessage("OK");
                phase3.gettingBase = true;
                phase3.currentIndex = 0;
                while (phase3.bullets.length > 0) {
                    phase3.phaseElement.removeChild(phase3.bullets.pop()[0]);
                }
                gameScreen.timer.style.color = "#000000";
                break;
            
            case "TIME:0":
                gameScreen.timer.innerHTML = "00:00";
                gameScreen.timer.style.color = "#FF0000";
                phase3.onTimeEnd();
        }

        if (msg.startsWith("TIME:")) {
            let time = parseInt(msg.split(":")[1]);
            let m = Math.floor(time / 60).toString();
            let s = (time % 60).toString();
            if (m.length == 1) m = "0" + m;
            if (s.length == 1) s = "0" + s;
            gameScreen.timer.innerHTML = `${m}:${s}`;
        }
        else if (msg.startsWith("S:")) {
            let args = msg.split(":");
            let xFrom = parseInt(args[1]);
            let yFrom = parseInt(args[2]);
            let xTo = parseInt(args[3]);
            let yTo = parseInt(args[4]);

            phase3.shoot(xFrom, yFrom, xTo, yTo);
        }
        else if (msg.startsWith("L:")) {
            let time = parseInt(msg.split(":")[1]);
            let s = (time % 60).toString();
            let m = Math.floor(time/60).toString();
            if (s.length == 1) s = "0" + s;
            if (m.length == 1) m = "0" + m;

            phase3.loses++;
            let strTime = `${m}:${s}`;
            let message = `Счёт: ${phase3.wins}:${phase3.loses} <br/> Время: ${strTime}`;
            
            let mos = document.getElementById("messageOnScreen");
            mos.innerHTML = message;
            mos.style.display = "block";
            let game = document.getElementById("game")
            game.style.opacity = 0.5;
            phase3.phaseElement.style.opacity = 0.4;

            setTimeout(function() {
                mos.style.display = "none";
                phase3.phaseElement.style.opacity = 1;
                game.style.opacity = 1;
            } , 4000);
            
        }
        else if (msg.startsWith("W:")) {
            let time = parseInt(msg.split(":")[1]);
            let s = (time % 60).toString();
            let m = Math.floor(time/60).toString();
            if (s.length == 1) s = "0" + s;
            if (m.length == 1) m = "0" + m;

            phase3.wins++;
            let strTime = `${m}:${s}`;
            let message = `Счёт: ${phase3.wins}:${phase3.loses} <br/> Время: ${strTime}`;
            
            let mos = document.getElementById("messageOnScreen");
            mos.innerHTML = message;
            mos.style.display = "block";
            let game = document.getElementById("game")
            game.style.opacity = 0.4;
            phase3.phaseElement.style.opacity = 0.4;

            setTimeout(function() {
                mos.style.display = "none";
                phase3.phaseElement.style.opacity = 1;
                game.style.opacity = 1;
            } , 4000);

            
        }
        else if (msg.startsWith("R:")) {
            let args = msg.split(":");

            let time = parseInt(args[2]);
            let s = (time % 60).toString();
            let m = Math.floor(time/60).toString();
            if (s.length == 1) s = "0" + s;
            if (m.length == 1) m = "0" + m;

            let defTime = `${m}:${s}`;

            time = parseInt(args[4]);
            s = (time % 60).toString();
            m = Math.floor(time/60).toString();
            if (s.length == 1) s = "0" + s;
            if (m.length == 1) m = "0" + m;

            let atkTime = `${m}:${s}`;

            let gos = document.getElementById("gameOverScreen");
            document.getElementById("whiteBackground").style.display = "block";
            let rounds = document.getElementById("gameStats");

            let message = "Защита: ";
            message += defTime;

            if (args[1] == "L") {
                message += " — Поражение";
            } else message += " — Победа";

            message += "<br/>";

            message += `Атака: ${atkTime}`;
            if (args[3] == "L") {
                message += " — Поражение";
            } else message += " — Победа";

            rounds.innerHTML = message;
            gos.style.display = "block";
        }
    },

    shoot(xFrom, yFrom, xTo, yTo) {
        let shooter = grid.field[xFrom + yFrom * 11].building;
        if (shooter == -1) return;

        let target = grid.field[xTo + yTo * 11].building
        if (target == -1) return;

        let damage = Damages.get(shooter);
        let bullet = document.createElement("div");

        let bulletWidth = grid.tileWidth / 4;
        let bulletHeight = grid.tileHeight / 4;
        bullet.style.width = `${bulletWidth}px`;
        bullet.style.height = `${bulletHeight}px`;

        let absoluteXFrom = grid.getAbsoluteX(xFrom) - bulletWidth/2;
        let absoluteYFrom = grid.getAbsoluteY(yFrom) - bulletWidth/2;
        bullet.style.left = `${absoluteXFrom}px`;
        bullet.style.top = `${absoluteYFrom}px`;

        bullet.classList.add("cannonBullet");
        phase3.phaseElement.appendChild(bullet);
        grid.fieldObjects.push(bullet);

        let time = Math.sqrt((xTo - xFrom) ** 2 + (yTo - yFrom) ** 2) // distance
                   / BulletSpeeds.get(shooter) // time
                   * 60; // time in frames with 60 fps
        
        let dX = (xTo - xFrom) * grid.borderedWidth / time;
        let dY = (yTo - yFrom) * grid.borderedWidth / time;

        phase3.bullets.push([bullet, dX, dY, 0 /* Time passed */, time /* Total time */, damage]);
    },

    resize() {

    },

    update() {
        for (let i=0; i < phase3.bullets.length; i++) {
            let element = phase3.bullets[i];
            if (element == undefined) break; // 
            let bullet = phase3.bullets[i][0];
            let x = parseFloat(bullet.style.left);
            let y = parseFloat(bullet.style.top);
            bullet.style.left = `${x + phase3.bullets[i][1]}px`;
            bullet.style.top = `${y + phase3.bullets[i][2]}px`;

            phase3.bullets[i][3]++;
            if (phase3.bullets[i][3] >= phase3.bullets[i][4]) {
                this.hitBuilding(bullet, phase3.bullets[i][5]);
                phase3.bullets.splice(i, 1);
                this.phaseElement.removeChild(bullet);
                grid.fieldObjects.splice(grid.fieldObjects.indexOf(bullet), 1);
                i--;
            }
        }
    },

    hitBuilding(bullet, damage) {
        let x = parseFloat(bullet.style.left);
        let y = parseFloat(bullet.style.top);
        let cell = grid.getCellByAbsoluteCoords(x, y);
        if (cell.building == -1) return;

        cell.hp -= damage;
        cell.cell.style.opacity = 0.5;
        if (cell.hp > 0) {
            setTimeout(() => cell.cell.style.opacity = 1, 120);
        } else {
            setTimeout(function() {
                cell.setBuilding(-1);
                cell.cell.style.opacity = 1;
            }, 120);
        }
    },

    onwheel(event) {
        if (event.deltaY == -3) {
            phase3.bullets.forEach(element => {
                let cell = element[0];
                let x = parseFloat(cell.style.left);
                let y = parseFloat(cell.style.top);
                cell.style.top = `${grid.y + (y - grid.y) * 2}px`;
                cell.style.left = `${grid.x + (x - grid.x) * 2}px`;
                cell.style.width = `${grid.tileWidth / 4}px`;
                cell.style.height = `${grid.tileHeight / 4}px`;
                
                element[1] *= 2;
                element[2] *= 2;
            });
        } else {
            phase3.bullets.forEach(element => {
                let cell = element[0];
                if (parseFloat(cell.style.width) == 12.5) return;
                let x = parseFloat(cell.style.left);
                let y = parseFloat(cell.style.top);
                cell.style.top = `${grid.y + (y - grid.y) / 2}px`;
                cell.style.left = `${grid.x + (x - grid.x) / 2}px`;
                cell.style.width = `${grid.tileWidth / 4}px`;
                cell.style.height = `${grid.tileHeight / 4}px`;

                element[1] /= 2;
                element[2] /= 2;
            });
        }
        
    }
}


var SCREEN = loading;
SCREEN.startRendering();
render = function() {
    try {
        SCREEN.update();
    } catch {/* Display is being resized, waiting. */}
    window.requestAnimationFrame(render);
}


render();

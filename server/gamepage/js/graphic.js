var canvas = document.querySelector("canvas");
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

var c = canvas.getContext("2d");
c.font = (window.innerWidth + window.innerHeight) / 60 + "pt Neucha"


var s = false;
var s1 = false;
var w = 0;
var textWidth = c.measureText("Ожидание противника...").width/2;
var textHeight = window.innerHeight / 5;


window.addEventListener("resize", function() {
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    if (!s) loading.radius = (window.innerHeight + window.innerHeight) / 15;
    let f = (window.innerWidth + window.innerHeight) / 60;
    c.font = f + "pt Neucha";
    textWidth = c.measureText("Ожидание противника...").width/2;
    textHeight = window.innerHeight / 5;
});


loading = new function() {
    this.radius = (window.innerHeight + window.innerHeight) / 15;
    this.speed = 0.04;
    this.dg = 0;
    this.dR = 0;
    this.dDR = 0.4;
    this.color = "#EEEEEE";

    this.render = function() {
        x = window.innerWidth / 2; y = window.innerHeight / 2;
        c.beginPath();
        c.fillStyle=this.color;
        c.strokeStyle=this.color;
        c.lineWidth = 5;
        c.arc(x, y, this.radius, 0, 7);
        c.stroke();

        let r2 = this.radius / 1.5 + this.dR;
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
        c.beginPath();
        c.arc(x, y, r2 / 1.3, 0, 7);
        c.stroke();

        if (r2 > this.radius) this.dDR = -0.4; else if (r2 < this.radius / 3) this.dDR = 0.4;

        this.dg += this.speed;
        this.dR += this.dDR;
        
    };
}


renderall = function() {
    c.fillStyle = "#1300B1";
    c.fillRect(0, 0, window.innerWidth, window.innerHeight);
    if (s1) {
        if (w <= window.innerWidth) w += 10;
        c.fillStyle = "#DDDDDD";
        c.fillRect(window.innerWidth/2-w, 0, 2*w, window.innerHeight);
    } else {
        loading.render();
        if (s) {
            loading.speed += 0.004;
            loading.radius *= 1.02;
        } else {
            c.fillStyle = "#EEEEEE";
            c.fillText("Ожидание противника...", x - textWidth, y - textHeight);
        }
    }
    
    window.requestAnimationFrame(renderall);
};

renderall();
setTimeout(function() {
    s = true;
    setTimeout(() => s1 = true, 2500);
}, 6000);

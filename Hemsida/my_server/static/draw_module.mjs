//draw ---

//Position class for objects
class Position {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    getX() {
        return this.x;
    }
    getY() {
        return this.y;
    }
    setX(x) {
        this.x = x;
    }
    setY(y) {
        this.y = y;
    }
}

//Player
function drawPlayer(playerX, playerY, playerWidth, playerHeight, ctx) {
    ctx.beginPath();
    ctx.rect(playerX, playerY, playerWidth, playerHeight);
    ctx.fillStyle = "#046cd4";
    ctx.fill();
    ctx.closePath();
}

//Wall
function drawWall(wallX, wallY, wallWidth, wallHeight, ctx) {
    ctx.beginPath();
    ctx.rect(wallX, wallY, wallWidth, wallHeight);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

//Monster
function drawMonster(monsterX, monsterY, monsterWidth, monsterHeight, ctx) {
    ctx.beginPath();
    ctx.rect(monsterX, monsterY, monsterWidth, monsterHeight);
    ctx.fillStyle = "#04d49d";
    ctx.fill();
    ctx.closePath();
}

//Grid
function drawGrid(canvasWidth, canvasHeight, tileSize, ctx) {
    ctx.strokeStyle = '#cccccc';
    ctx.stroke();
    for (var i = 0; i <= canvasWidth; i += tileSize) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvasHeight);
        ctx.stroke();
        ctx.closePath();
    }

    for (var i = 0; i <= canvasHeight; i += tileSize) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvasWidth, i);
        ctx.stroke();
    }
}

export {Position, drawPlayer, drawMonster, drawWall, drawGrid}
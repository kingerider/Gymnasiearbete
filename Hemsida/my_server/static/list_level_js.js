function initializeCanvas(htmlId, levelId) {
   console.log("hello")
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

    //Canvas
    var canvas = document.getElementById(htmlId);
    var ctx = canvas.getContext("2d");
    var tileSize = canvas.height/20
    var canvasHeight = canvas.height / tileSize
    var canvasWidth = canvas.width / tileSize

    //Player
    var playerHeight = tileSize;
    var playerWidth = tileSize;
    var playerArray = [];
    console.log(canvasWidth)
    playerArray.push(new Position(parseInt(canvasWidth) / 8, parseInt(canvasHeight) / 2));
    playerArray.push(new Position(parseInt(canvasWidth) - parseInt(canvasWidth) / 8, parseInt(canvasHeight) / 2));

    //Wall
    var wallHeight = tileSize;
    var wallWidth = tileSize;
    var wallArray = [];

    //Monster
    var monsterHeight = tileSize;
    var monsterWidth = tileSize;
    var monsterArray = [];

    const dataLevel = {
        level_id: levelId
    }
    //console.log(data)
    $.ajax({
        method: 'POST',
        url: "/ajax-get-data-level",
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify(dataLevel),
        dataType: "json",
        success: (data) => {
            if (data.success) {
                console.log("success");
                console.log(data);
                setVariables(data);

            }
            //alert(JSON.stringify(data))
        }
    });

    function setVariables(data){
        for (let index = 0; index < data['wallX'].length; index++) {
            wallArray.push(new Position(data['wallX'][index], data['wallY'][index]));
        }
        for (let index = 0; index < data['monsterX'].length; index++) {
            monsterArray.push(new Position(data['monsterX'][index], data['monsterY'][index]));
        }
        $("#edit_title").val(data['title'])
        $("#edit_description").val(data['description'])

    }

    //Player
    function drawPlayer(playerX, playerY) {
        ctx.beginPath();
        ctx.rect(playerX, playerY, playerWidth, playerHeight);
        ctx.fillStyle = "#046cd4";
        ctx.fill();
        ctx.closePath();
    }

    //Wall
    function drawWall(wallX, wallY) {
        ctx.beginPath();
        ctx.rect(wallX, wallY, wallWidth, wallHeight,);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    //Monster
    function drawMonster(monsterX, monsterY) {
        ctx.beginPath();
        ctx.rect(monsterX, monsterY, monsterWidth, monsterHeight);
        ctx.fillStyle = "#04d49d";
        ctx.fill();
        ctx.closePath();
    }

    //Grid
    function drawGrid() {
        ctx.strokeStyle = '#cccccc';
        ctx.stroke();
        for (var i = 0; i <= canvas.width; i += tileSize) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, canvas.height);
            ctx.stroke();
            ctx.closePath();
        }

        for (var i = 0; i <= canvas.height; i += tileSize) {
            ctx.beginPath();
            ctx.moveTo(0, i);
            ctx.lineTo(canvas.width, i);
            ctx.stroke();
        }

    }

    //Draw objects
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();
        console.log("Hellooo")
        console.log(wallArray)
        console.log(wallArray.length)
        for (let i = 0; i < wallArray.length; i++) {
            drawWall(wallArray[i].getX() * tileSize, wallArray[i].getY() * tileSize);
        }
        for (let i = 0; i < monsterArray.length; i++) {
            drawMonster(monsterArray[i].getX() * tileSize, monsterArray[i].getY() * tileSize);
        }
        for (let i = 0; i < playerArray.length; i++) {
            drawPlayer(playerArray[i].getX() * tileSize, playerArray[i].getY() * tileSize);
        }
    }
    let updateInterval = setInterval(draw, 100);
    setTimeout(function( ) { clearInterval(updateInterval); }, 2000); //Kill interval for efficent server resources

}


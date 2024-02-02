let player = {
    username: null,
    room: null
}

socket = io()

function joinGame(data) {
    console.log(data)
    player.username = $("#playerName").val()
    player.room = data

    socket.emit('join', {
        username: player.username,
        room: player.room,
        role: 'join'
    })
    console.log(`Du är inne på ${player.room}`)
}

function createGame(data) {
    console.log(data)
    player.username = $("#playerName").val()
    player.room = data

    socket.emit('join', {
        username: player.username,
        room: player.room,
        role: 'create'
    })
    console.log(`Du är inne på ${player.room}`)
}

$(document).ready(() => {
    
    //game code -------------
    console.log(window.location.pathname)
    console.log(player.room)
    console.log(window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1))

        //Load game
    if ( window.location.pathname == `/play_game/join/${window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)}`) {
        //code for index page
        console.log("In index")
        startGame()
    } else if ( window.location.pathname == `/play_game/create/${window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)}`) {
        console.log("In index")
        startGame()
    } else if (window.location.pathname == '/build_game'){
        console.log("In index build")
        buildGame()
    } else{
        console.log("Not in index")
    }
    //end game code -----------

    //Socket code ---------

    socket.on('navigate_to', (path) => {
        window.location.href = path
    })

    /*$('#button-joingame-test').click(() => { 
        player.username = $("#username").val()
        player.room = $("#input_room").val()
        
        console.log(`Dobro pozhalovat ${player.username} to room ${player.room}`)
        
        socket.emit('join', {
            username: player.username,
            room: player.room
        })
    })

    $('#button-leavegame-test').click(() => { 
        console.log("Ty ostavil menya")
        socket.emit('leave', {
            username: player.username,
            room: player.room
        })
        $("#the_text").text("");
    })

    $('#button_send_message').click(() => {
        console.log($('#input_the_text').val())
        socket.emit('send_message_to_room', {
            heading: player.username,
            message: $('#input_the_text').val(),
            room: player.room
        });
        $('#input_the_text').val("")
    })

    socket.on('message_from_server', (data) => {
        $("#the_text").append(
            create_new_message(
                data["heading"],
                data["message"]
            )
        )
    })

    socket.on('connect', () => {
        $("#the_text").append("Du är inne på servern")

    });

    const create_new_message = (heading, msg) => {
        return `
            <div class="ms-2 me-auto">
              <div class="fw-bold">${heading}</div>
              ${msg}
            </div>`
    }*/

    //End scoket code ---------

   
});

$.ajax({
    method: 'POST',
    url: "/path",
    data: "data",
    dataType: "json",
    success: (response) => {
        
    }
});

//Game Code ==>
//https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Create_the_Canvas_and_draw_on_it

function startGame() {
    console.log("Here");

    //Canvas
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var x = canvas.width/2;
    var y = canvas.height-30;
    var tileSize = 10;

    //Position class for objects
    class position{
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
    
    //Ball
    var ballRadius = tileSize;
    var dx = 1;
    var dy = -1;

    //Wall
    var wallHeight = tileSize;
    var wallWidth = tileSize;
    var wallArray = [];
    for (let index = 0; index < 1000; index++) {
        wallArray.push(new position((Math.floor(Math.random() * canvas.width/tileSize) * tileSize), (Math.floor(Math.random() * canvas.height/tileSize) * tileSize)));
    }
    console.log("Wall x pos");
    console.log(wallArray.length)
    console.log(wallArray[1].getX());

    //Monster
    var monsterHeight = tileSize;
    var monsterWidth = tileSize;
    var monsterArray = [];
    for (let index = 0; index < 100; index++) {
        monsterArray.push(new position((Math.floor(Math.random() * canvas.width/tileSize) * tileSize), (Math.floor(Math.random() * canvas.height/tileSize) * tileSize)));
    }
    
    //Player
    var playerHeight = tileSize;
    var playerWidth = tileSize;
    var playerX = 0;
    var playerY = 0;
    

    //Keys
    var rightPressed = false;
    var leftPressed = false;
    var upPressed = false;
    var downPressed = false;

    document.addEventListener("keydown", keyDownHandler, false);
    document.addEventListener("keyup", keyUpHandler, false);


    function keyDownHandler(e) {
        if(e.key == "Right" || e.key == "ArrowRight") {
            rightPressed = true;
        }
        else if(e.key == "Left" || e.key == "ArrowLeft") {
            leftPressed = true;
        }
        if(e.key == "Up" || e.key == "ArrowUp") {
            upPressed = true;
        }
        else if(e.key == "Down" || e.key == "ArrowDown") {
            downPressed = true;
        }
    }

    function keyUpHandler(e) {
        if(e.key == "Right" || e.key == "ArrowRight") {
            rightPressed = false;
        }
        else if(e.key == "Left" || e.key == "ArrowLeft") {
            leftPressed = false;
        }
        if(e.key == "Up" || e.key == "ArrowUp") {
            upPressed = false;
        }
        else if(e.key == "Down" || e.key == "ArrowDown") {
            downPressed = false;
        }
    }

    //Grid
    function drawGrid() {
        ctx.strokeStyle = '#eeeeee';
        ctx.stroke();
        for (var i = 0; i <= canvas.width; i += tileSize) {
            ctx.beginPath(); 
            ctx.moveTo(i, 0); 
            ctx.lineTo(i, canvas.height); 
            ctx.stroke();
        }
    
        for (var i = 0; i <= canvas.height; i += tileSize) {
            ctx.beginPath(); 
            ctx.moveTo(0, i); 
            ctx.lineTo(canvas.width, i); 
            ctx.stroke();
        }
        
    }

    //Ball
    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI*2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    //Wall
    function drawWall(wallX, wallY) {
        ctx.beginPath();
        ctx.rect(wallX, wallY, wallWidth, wallHeight, );
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


    //Player
    function drawPlayer() {
        ctx.beginPath();
        ctx.rect(playerX, playerY, playerWidth, playerHeight);
        ctx.fillStyle = "#046cd4";
        ctx.fill();
        ctx.closePath();
    }

    //Draw objects
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();
        drawBall();
        drawPlayer();
        
        for (let i = 0; i < wallArray.length; i++) {
            drawWall(wallArray[i].getX(), wallArray[i].getY());            
        }
        for (let i = 0; i < monsterArray.length; i++) {
            drawMonster(monsterArray[i].getX(), monsterArray[i].getY());            
        }
        
        //Ball movment
        if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        if(y + dy < ballRadius) {
            dy = -dy;
        }
        else if(y + dy > canvas.height-ballRadius) {
            if(x > playerX && x < playerX + playerWidth) {
                dy = -dy;
            }
            else {
                alert("GAME OVER");
                document.location.reload();
                clearInterval(interval); // Needed for Chrome to end game
            }
        }
        x += dx;
        y += dy;
        
        //Monster movement
        for (let j = 0; j < monsterArray.length; j++) {
            //Choose what way to go
            var movementChoose = 0

            //how close is player
            if(5*tileSize > (playerX - monsterArray[j].getX()) && -5*tileSize < (playerX - monsterArray[j].getX()) && 5*tileSize > (playerY - monsterArray[j].getY()) && -5*tileSize < (playerY - monsterArray[j].getY())){
                console.log("Hello")
                movementChoose = 1;
            }else{
                movementChoose = Math.floor(Math.random() * 4);
            }

            //console.log(movementChoose);
            if(movementChoose == 0 && monsterArray[j].getX() < canvas.width-playerWidth) {
                //console.log("0m")
                //Check walls
                var checkForWalls = true
                for (let i = 0; i < wallArray.length; i++) {
                    if (monsterArray[j].getX() == (wallArray[i].getX()-tileSize) && monsterArray[j].getY() == wallArray[i].getY()) {
                        checkForWalls = false
                    }
                }
                if(checkForWalls){
                    monsterArray[j].setX(monsterArray[j].getX() + tileSize);
                }
            }
            else if(movementChoose == 1 && monsterArray[j].getX() > 0) {
                //console.log("1m");
                //console.log(movementChoose);
                //Check walls
                var checkForWalls = true
                for (let i = 0; i < wallArray.length; i++) {
                    if (monsterArray[j].getX() == (wallArray[i].getX()+tileSize) && monsterArray[j].getY() == wallArray[i].getY()) {
                        checkForWalls = false
                    }
                }
                if(checkForWalls){
                    monsterArray[j].setX(monsterArray[j].getX() - tileSize); //Must use diffrent method for arrayyyyyyyyyyyyy
                }
            }
            else if(movementChoose == 2 && monsterArray[j].getY() > 0) {
                //console.log("2m")
                var checkForWalls = true
                for (let i = 0; i < wallArray.length; i++) {
                    if (monsterArray[j].getY() == (wallArray[i].getY()+tileSize) && monsterArray[j].getX() == wallArray[i].getX()) {
                        checkForWalls = false
                    }
                }
                if(checkForWalls){
                    monsterArray[j].setY(monsterArray[j].getY() - tileSize);
                }
            }
            else if(movementChoose == 3 && monsterArray[j].getY() < canvas.height-playerHeight) {
                //console.log("3m")
                var checkForWalls = true
                for (let i = 0; i < wallArray.length; i++) {
                    if (monsterArray[j].getY() == (wallArray[i].getY()-tileSize) && monsterArray[j].getX() == wallArray[i].getX()) {
                        checkForWalls = false
                    }
                }
                if(checkForWalls){
                    monsterArray[j].setY(monsterArray[j].getY() + tileSize);
                }
            }
        }
        
        //Player movement
        if(rightPressed && playerX < canvas.width-playerWidth) {
            //Check walls
            var checkForWalls = true
            for (let i = 0; i < wallArray.length; i++) {
                if (playerX == (wallArray[i].getX()-tileSize) && playerY == wallArray[i].getY()) {
                    checkForWalls = false
                }
            }
            if(checkForWalls){
                playerX += tileSize;
            }
        }
        else if(leftPressed && playerX > 0) {
            //Check walls
            var checkForWalls = true
            for (let i = 0; i < wallArray.length; i++) {
                if (playerX == (wallArray[i].getX()+tileSize) && playerY == wallArray[i].getY()) {
                    checkForWalls = false
                }
            }
            if(checkForWalls){
                playerX -= tileSize;
            }
        }
        if(upPressed && playerY > 0) {
            var checkForWalls = true
            for (let i = 0; i < wallArray.length; i++) {
                if (playerY == (wallArray[i].getY()+tileSize) && playerX == wallArray[i].getX()) {
                    checkForWalls = false
                }
            }
            if(checkForWalls){
                playerY -= tileSize;
            }
        }
        else if(downPressed && playerY < canvas.height-playerHeight) {
            var checkForWalls = true
            for (let i = 0; i < wallArray.length; i++) {
                if (playerY == (wallArray[i].getY()-tileSize) && playerX == wallArray[i].getX()) {
                    checkForWalls = false
                }
            }
            if(checkForWalls){
                playerY += tileSize;
            }
        }
    }

    var interval = setInterval(draw, 60);

}

function buildGame() {
    console.log("Here");

    //Canvas
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var x = canvas.width/2;
    var y = canvas.height-30;
    var tileSize = 10;


    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();
    }
}

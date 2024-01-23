let player = {
    username: null,
    room: null
}

$(document).ready(() => {
    
    //game code -------------
    console.log(window.location.pathname)

        //Load game
    if ( window.location.pathname == '/play_game' ){
        //code for index page
        console.log("In index")
        startGame.addEventListener('load', startGame())
    }else{
        console.log("Not in index")
    }
    //end game code -----------

    //Scoket code ---------

    let socket = io()

    $('#button-joingame-test').click(() => { 
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
    }

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

    //Ball
    var ballRadius = tileSize;
    var dx = 2;
    var dy = -2;

    //Wall
    var wallHeight = 20
    var wallWidth = 20
    wallX = (Math.floor(Math.random() * 80) * tileSize)
    wallY = (Math.floor(Math.random() * 40) * tileSize)

    //Player
    var playerHeight = 2 * tileSize;
    var playerWidth = tileSize;
    var playerX = 10*tileSize;
    var playerY = 20*tileSize;

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

    //Ball
    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI*2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    //Wall
    function drawWall() {
        ctx.beginPath();
        ctx.rect(wallX, wallY, wallWidth, wallHeight, );
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    //Player
    function drawPlayer() {
        ctx.beginPath();
        ctx.rect(playerX, playerY, playerWidth, playerHeight);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    //Draw objects
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBall();
        drawPlayer();
        drawWall();
        
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
        
        if(rightPressed && playerX < canvas.width-playerWidth) {
            playerX += tileSize;
        }
        else if(leftPressed && playerX > 0) {
            playerX -= tileSize;
        }
        if(upPressed && playerY > 0) {
            playerY -= tileSize;
        }
        else if(downPressed && playerY < canvas.height-playerHeight) {
            playerY += tileSize;
        }
        
        x += dx;
        y += dy;
    }

    var interval = setInterval(draw, 60);
}

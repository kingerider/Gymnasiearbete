let player = {
    username: null,
    room: null,
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
        player.username = $("username").val()
        
        player.room = $("input[name='rooms']:checked").val()
        socket.emit('join', {
            username: player.username,
            room: player.room
        })
    })

    $('#button-leavegame-test').click(() => { 
        socket.emit('leave', {
            username: user.username,
            room: user.room
        })
    })

    $('#button_send_message').click(() => {
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
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var ballRadius = 10;
    var x = canvas.width/2;
    var y = canvas.height-30;
    var dx = 2;
    var dy = -2;
    var playerHeight = 15;
    var playerWidth = 10;
    var playerX = (canvas.width-playerWidth)/2;
    var playerY = (canvas.height-playerHeight)/2;
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

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI*2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }
    function drawPlayer() {
        ctx.beginPath();
        ctx.rect(playerX, playerY, playerWidth, playerHeight);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBall();
        drawPlayer();
        
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
            playerX += 7;
        }
        else if(leftPressed && playerX > 0) {
            playerX -= 7;
        }
        if(upPressed && playerY < canvas.height-playerHeight) {
            playerY -= 7;
        }
        else if(downPressed && playerY > 0) {
            playerY += 7;
        }
        
        x += dx;
        y += dy;
    }

    var interval = setInterval(draw, 20);
}

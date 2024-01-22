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
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto">
              <div class="fw-bold">${heading}</div>
              ${msg}
            </div>
          </li>`
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
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    let x = canvas.width / 2;
    let y = canvas.height - 30;
    let dx = 2;
    let dy = -2;
    const ballRadius = 10;

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
      }
      
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBall();
    
        if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        if(y + dy > canvas.height-ballRadius || y + dy < ballRadius) {
            dy = -dy;
        }
    
        x += dx;
        y += dy;
    }
    setInterval(draw, 10);
}

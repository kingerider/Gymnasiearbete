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

function startGame() {
    console.log("Here");
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.rect(20, 40, 50, 50);
    ctx.fillStyle = "#FF0000";
    ctx.fill();
    ctx.closePath();
}

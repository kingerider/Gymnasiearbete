import { Position, drawPlayer, drawMonster, drawWall, drawGrid } from './draw_module.mjs';

document.querySelector('#wall').addEventListener('click', function () {
    setWall()
});
document.querySelector('#monster').addEventListener('click', function () {
    setMonster()
});


function setWall() {
    var button = document.getElementById("wall");
    button.disabled = true;
    button = document.getElementById("monster");
    button.disabled = false;
}
function setMonster() {
    var button = document.getElementById("wall");
    button.disabled = false;
    button = document.getElementById("monster");
    button.disabled = true;
}

$(document).ready(() => {

    //Canvas
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var tileSize = 20;
    var canvasHeight = canvas.height / tileSize
    var canvasWidth = canvas.width / tileSize

    //Player
    var playerHeight = tileSize;
    var playerWidth = tileSize;
    var playerArray = [];
    console.log(canvasWidth)
    playerArray.push(new Position(parseInt(canvasWidth) / 8, parseInt(canvasHeight) / 2));
    playerArray.push(new Position(parseInt(canvasWidth) - parseInt(canvasWidth) / 8 - 1, parseInt(canvasHeight) / 2));

    //Wall
    var wallHeight = tileSize;
    var wallWidth = tileSize;
    var wallArray = [];

    //Monster
    var monsterHeight = tileSize;
    var monsterWidth = tileSize;
    var monsterArray = [];

    //Draw objects
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid(canvas.width, canvas.height, tileSize, ctx);
        for (let i = 0; i < wallArray.length; i++) {
            drawWall(wallArray[i].getX() * tileSize, wallArray[i].getY() * tileSize, wallWidth, wallHeight, ctx);
        }
        for (let i = 0; i < monsterArray.length; i++) {
            drawMonster(monsterArray[i].getX() * tileSize, monsterArray[i].getY() * tileSize, monsterWidth, monsterHeight, ctx);
        }
        for (let i = 0; i < playerArray.length; i++) {
            drawPlayer(playerArray[i].getX() * tileSize, playerArray[i].getY() * tileSize, playerWidth, playerHeight, ctx);
        }
    }
    var interval = setInterval(draw, 60);

    addEventListener("mouseup", (event) => {

        //Mouse position locator on canvas
        var rect = canvas.getBoundingClientRect();
        var x = event.clientX - rect.left + (canvas.width - parseInt(getComputedStyle(canvas).getPropertyValue("width"), 10)) / 2; //Sets origo in canvas corner
        var y = event.clientY - rect.top + (canvas.height - parseInt(getComputedStyle(canvas).getPropertyValue("height"), 10)) / 2;

        var canvasClickX = parseInt(x / tileSize)
        var canvasClickY = parseInt(y / tileSize)

        switch (event.button) {
            case 0:
                //Left click add wall or monster to canvas
                console.log("Left button clicked.");
                if (canvasClickX >= 0 && canvasClickY >= 0 && canvasClickX < canvasWidth && canvasClickY < canvasHeight) { //checks if mouse on canvas
                    let doesExist = false;
                    for (var i = 0; i < wallArray.length; i++) {
                        if (wallArray[i].getX() == canvasClickX && wallArray[i].getY() == canvasClickY) { //checks if object exists
                            console.log("Object already exists");
                            doesExist = true;
                        }
                    }
                    for (var i = 0; i < monsterArray.length; i++) {
                        if (monsterArray[i].getX() == canvasClickX && monsterArray[i].getY() == canvasClickY) { //checks if object exists
                            console.log("Object already exists")
                            doesExist = true;
                        }
                    }
                    for (var i = 0; i < playerArray.length; i++) {
                        if (playerArray[i].getX() == canvasClickX && playerArray[i].getY() == canvasClickY) { //checks if object exists
                            console.log("Object already exists")
                            doesExist = true;
                        }
                    }
                    if (!doesExist) {
                        if (document.getElementById("wall").disabled == true) {
                            wallArray.push(new Position(canvasClickX, canvasClickY));
                        } else {
                            if (monsterArray.length < 6) {
                                monsterArray.push(new Position(canvasClickX, canvasClickY));
                            } else {
                                $("#message_m").css('display', 'block')
                                $("#message_m").text('Spelet kan bara ha sex stycken monster')
                            }
                        }
                    }
                }
                break;
            case 1:
                console.log("Middle button clicked.");

                break;
            case 2:
                //Left click add wall or monster
                console.log("Right button clicked.");
                console.log(canvasClickX);
                console.log(canvasClickY)
                if (canvasClickX >= 0 && canvasClickY >= 0 && canvasClickX < canvasWidth && canvasClickY < canvasHeight) {
                    if (document.getElementById("wall").disabled == true) {
                        for (var i = 0; i < wallArray.length; i++) {
                            console.log(wallArray[i].getX()) //is not a function
                            console.log(wallArray[i].getY())
                            console.log(canvasClickX)
                            console.log(canvasClickY)
                            if (wallArray[i].getX() == canvasClickX && wallArray[i].getY() == canvasClickY) {
                                wallArray.splice(i, 1); // 2nd parameter removes only that item and not more?

                            }
                        }
                    } else {
                        for (var i = 0; i < monsterArray.length; i++) {
                            console.log(monsterArray[i].getX()) //is not a function
                            console.log(monsterArray[i].getY())
                            console.log(canvasClickX)
                            console.log(canvasClickY)
                            if (monsterArray[i].getX() == canvasClickX && monsterArray[i].getY() == canvasClickY) {
                                monsterArray.splice(i, 1); // 2nd parameter removes only that item and not more?   
                            }
                        }
                    }
                }

                break;
            default:
                log.textContent = `Unknown button code: ${e.button}`;
        }


    });
    $("#create_level").click(() => {
        if ($("#create_description").val() != "" && $("#create_title").val() != "") {
            if ($("#create_title").val().length < 26) {
                if ($("#create_description").val().length < 151) {


                    var playerXArray = []
                    var playerYArray = []
                    var monsterXArray = []
                    var monsterYArray = []
                    var wallXArray = []
                    var wallYArray = []
                    for (let index = 0; index < playerArray.length; index++) {
                        playerXArray.push(playerArray[index].getX());
                        playerYArray.push(playerArray[index].getY());
                    }
                    for (let index = 0; index < monsterArray.length; index++) {
                        monsterXArray.push(monsterArray[index].getX());
                        monsterYArray.push(monsterArray[index].getY());
                    }
                    for (let index = 0; index < wallArray.length; index++) {
                        wallXArray.push(wallArray[index].getX());
                        wallYArray.push(wallArray[index].getY());

                    }

                    const data = {
                        title: $("#create_title").val(),
                        description: $("#create_description").val(),
                        username: $("#this_user").text(),
                        hearts: $("#hearts").val(),
                        playerX_Positions: playerXArray, //is not in use
                        playerY_Positions: playerYArray, //is not in use
                        monsterX_Positions: monsterXArray,
                        monsterY_Positions: monsterYArray,
                        wallX_Positions: wallXArray,
                        wallY_Positions: wallYArray
                    }

                    //console.log(data)
                    $.ajax({
                        method: 'POST',
                        url: "/ajax-create-level",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        data: JSON.stringify(data),
                        dataType: "json",
                        success: (data) => {
                            if (data.success) {
                                var base_url = window.location.origin;
                                window.location = (base_url + "/profile")
                            } else {
                                $("#message_td").css('display', 'block')
                                $("#message_td").text('Something went wrong')
                            }

                            //alert(JSON.stringify(data))
                        }
                    });
                } else {
                    console.log("Hello")
                    $("#message_td").css('display', 'block')
                    $("#message_td").text('Description can only contian max 150 chracters')

                }
            } else {
                console.log("Hello")
                $("#message_td").css('display', 'block')
                $("#message_td").text('Title can only contain max 25 chracters')

            }
        } else {
            console.log("Hello")
            $("#message_td").css('display', 'block')
            $("#message_td").text('Title and description can not be empty')

        }
    })

});


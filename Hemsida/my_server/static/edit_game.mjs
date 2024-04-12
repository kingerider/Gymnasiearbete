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
        level_id: $("#this_level").text()
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

    function setVariables(data) {
        for (let index = 0; index < data['wallX'].length; index++) {
            wallArray.push(new Position(data['wallX'][index], data['wallY'][index]));
        }
        for (let index = 0; index < data['monsterX'].length; index++) {
            monsterArray.push(new Position(data['monsterX'][index], data['monsterY'][index]));
        }
        $("#edit_title").val(data['title'])
        $("#edit_description").val(data['description'])
        $("#hearts").val(data['hearts'])
    }

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
                            if (monsterArray.length < 5) {
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
    $("#edit_level").click(() => {
        if ($("#edit_description").val() != "" && $("#edit_title").val() != "") {
            if ($("#edit_title").val().length < 26) {
                if ($("#edit_description").val().length < 151) {

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
                        title: $("#edit_title").val(),
                        description: $("#edit_description").val(),
                        level_id: $("#this_level").text(),
                        hearts: $("#hearts").val(),
                        playerX_Positions: playerXArray, //is not in use
                        playerY_Positions: playerYArray, //is not in use
                        monsterX_Positions: monsterXArray,
                        monsterY_Positions: monsterYArray,
                        wallX_Positions: wallXArray,
                        wallY_Positions: wallYArray
                    }

                    console.log(data)
                    $.ajax({
                        method: 'POST',
                        url: "/ajax-edit-level",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        data: JSON.stringify(data),
                        dataType: "json",
                        success: (data) => {
                            if (data.success) {
                                console.log("success")
                                $("#info_message").text(data.msg)
                                $("#info_message").show(() => {
                                    setTimeout(function(){
                                        $('#info_message').fadeOut();
                                      },4000);
                                });
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


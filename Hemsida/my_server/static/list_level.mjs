import { Position, drawPlayer, drawMonster, drawWall, drawGrid } from './draw_module.mjs';

function initializeCanvas(htmlId, levelId) {

    //Canvas
    var canvas = document.getElementById(htmlId);
    var ctx = canvas.getContext("2d");
    var tileSize = canvas.height / 20
    var canvasHeight = canvas.height / tileSize
    var canvasWidth = canvas.width / tileSize

    //Player
    var playerHeight = tileSize;
    var playerWidth = tileSize;
    var playerArray = [];
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
    let updateInterval = setInterval(draw, 100);
    setTimeout(function () { clearInterval(updateInterval); }, 1000); //Kill interval for efficent server resources

}

export { initializeCanvas }
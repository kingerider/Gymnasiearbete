import { Position, drawPlayer, drawMonster, drawWall } from './draw_module.mjs';

player.room = $("#gameid").val()

$(document).ready(() => {
    console.log("bläbl")
    console.log($("#this_user").text())
    socket.connect();

    socket.emit('join', {
        room: player.room,
    })

    let room_id = player.room

    socket.on('message_from_server', (data) => {
        $("#message").text(data.message)
        if (data.game != null) {
            console.log("NU VILL NAGON STARTA SPELET")
            start(data.game);
        }
    })

    const leave = () => {
        console.log("Lämna")
        socket.emit('leave', {
            room: room_id
        })
    }
    $("#btnleave").click(() => {
        leave()
    })
    socket.on('navigate_to', (path) => {
        window.location.href = path
        socket.disconnect()
    })

    var start = (start_game) => {

        var audio = new Audio('../../static/audio/adventure.mp3');
        audio.play();

        let player1 = start_game.players[0]
        let player2 = start_game.players[1]
        let newData = null

        if (player1 == $("#this_user").text()) {
            $.ajax({
                method: 'POST',
                url: "/ajax-add-played-game",
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify({
                    player1: player1,
                    player2: player2
                }),
                dataType: "json",
                success: (data) => {
                    if (data.success) {
                        console.log(data.msg)
                    }
                }
            });
        }

        //New canvas
        let canvas = document.createElement("canvas")
        canvas.id = "myCanvas"
        $("#canvasbody").text("")
        $("#canvasbody").append(canvas)

        console.log("js document.ready")

        console.log(room_id)
        console.log("player1 :" + player1)
        console.log("player2 :" + player2)

        //Canvas
        // canvas = document.getElementById("myCanvas"); //Does not need var because it already exists
        var ctx = canvas.getContext("2d");
        var tileSize = null;

        //Wall
        var wallHeight = tileSize;
        var wallWidth = tileSize;
        var wallArray = [];

        //Monster
        var monsterHeight = tileSize;
        var monsterWidth = tileSize;
        var monsterArray = [];

        //Player
        var playerHeight = tileSize;
        var playerWidth = tileSize;
        var playerArray = [];
        
        //hearts
        var heartHeight = tileSize;
        var heartWidth = tileSize;
        var heart1object = null;
        var heart2object = null;

        //projectile
        var projectileHeight = tileSize;
        var projectileWidth = tileSize;
        var projectileArray = [];

        //Grid
        var gridHeight = canvas.height / tileSize
        var gridWdith = canvas.width / tileSize

        var wait = false;
        function waitUpdate() {
            if (wait == false) {
                wait = true;
                return true
            } else {
                return false
            }
        }
        function cancelWait() {
            wait = false;
        }


        //text
        function drawText() {
            var x = canvas.width/2
            ctx.font = `${tileSize}pt Calibri`;
            ctx.textAlign = 'center'
            ctx.fillStyle = 'black'
            ctx.fillText(`${player1} vs ${player2}`, x, (2*tileSize)/2);
        }

        //Grid
        function drawGrid() {
            ctx.strokeStyle = '#eeeeee';
            ctx.stroke();
            for (var i = 0; i <= canvas.width; i += tileSize) {
                ctx.beginPath();
                ctx.moveTo(i, 40);
                ctx.lineTo(i, canvas.height);
                ctx.stroke();
                ctx.closePath();
            }
        
            for (var i = 0; i <= canvas.height; i += tileSize) {
                ctx.beginPath();
                ctx.moveTo(0, i + 40);
                ctx.lineTo(canvas.width, i + 40);
                ctx.stroke();
                ctx.closePath();
            }
        
        }

        //hearts
        function drawHearts() {
            for (var i = 0; i < heart1object.health; i++) {
                ctx.beginPath()
                ctx.rect(i*(heartWidth + 5), (2*tileSize)/2, heartWidth, heartHeight)
                ctx.fillStyle = "#ff0000";
                ctx.fill()
                ctx.closePath()
            }
            for (var i = 1; i <= heart2object.health; i++) {
                ctx.beginPath()
                if (i == 1) {
                    ctx.rect(canvas.width - i*(heartWidth), (2*tileSize)/2, heartWidth, heartHeight)
                } else {
                    ctx.rect(canvas.width - (i*heartWidth) - 5, (2*tileSize)/2, heartWidth, heartHeight)
                }
                ctx.fillStyle = "#ff0000";
                ctx.fill()
                ctx.closePath()
            }
        }

        //Projectile
        function drawProjectile(projectileX, projectileY) {
            ctx.beginPath();
            ctx.rect(projectileX, projectileY, projectileWidth, projectileHeight);
            ctx.fillStyle = "#383e42";
            ctx.fill();
            ctx.closePath();
        }

        function youWin(){
            clearInterval(updateInterval);
            console.log("YouWin")
            ctx.beginPath();
            var image = new Image();
            image.onload = function () {
                var imgW = 300, imgH = 90;
                var x = canvas.width/2 - imgW/2, y = canvas.height/2 - imgH/2;
                ctx.drawImage(image, x, y, imgW, imgH);  //aka, ctx2.drawImage(this, 0, 0);
            }
            image.src = '../../static/img/YouWinBig.png';
            ctx.closePath();
        }

        function youLose(){
            clearInterval(updateInterval);
            console.log("YouLose")
            ctx.beginPath();
            var image = new Image();
            image.onload = function () {
                var imgW = 300, imgH = 90;
                var x = canvas.width/2 - imgW/2, y = canvas.height/2 - imgH/2;
                ctx.drawImage(image, x, y, imgW, imgH);  //aka, ctx2.drawImage(this, 0, 0);
            }
            image.src = '../../static/img/YouLoseBig.png';
            ctx.closePath();
        }

        const updatePage = () => {
            socket.emit('update_canvas', {
                room: room_id
            })
        }

        //Updates variebles and gui
        socket.on('update', (data) => {
            //newData
            cancelWait();
            newData = data;
            updateEntityPosition();
            endGame();
            //canvas
            canvas = document.getElementById("myCanvas");
            ctx = canvas.getContext("2d");
            canvas.width = newData.width;
            canvas.height = newData.height;
            tileSize = newData.tile_size;

            //Wall
            wallHeight = tileSize;
            wallWidth = tileSize;
            //Monster
            monsterHeight = tileSize;
            monsterWidth = tileSize;

            //Player
            playerHeight = tileSize;
            playerWidth = tileSize;

            //Heart
            heartHeight = tileSize;
            heartWidth = tileSize;

            //Projectile
            projectileHeight = tileSize;
            projectileWidth = tileSize;

            //Grid
            gridHeight = canvas.height / tileSize;
            gridWdith = canvas.width / tileSize;

            function draw() {
                ctx.beginPath();
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.closePath();
                drawGrid();

                var countX = 0;
                for (const colum in newData.field_map) {
                    if (Object.hasOwnProperty.call(newData.field_map, colum)) {
                        const element1 = newData.field_map[colum];
                        var countY = 2;
                        for (const square in element1) {
                            if (Object.hasOwnProperty.call(element1, square)) {
                                const element2 = element1[square];
                                if (element2 != null) {
                                    if (element2["type"] == "wall") {
                                        drawWall(countX * tileSize, countY * tileSize, wallWidth, wallWidth, ctx);
                                    }
                                    if (element2["type"] == "enemy") {
                                        drawMonster(countX * tileSize, countY * tileSize, monsterWidth, monsterHeight, ctx);
                                    }
                                    if (element2["type"] == "player") {
                                        drawPlayer(countX * tileSize, countY * tileSize, playerWidth, playerHeight, ctx)
                                    }
                                    if (element2["type"] == "projectile") {
                                        drawProjectile(countX * tileSize, countY * tileSize)
                                    }
                                }
                            }
                            countY++;
                        }
                    }
                    countX++;
                }
                drawHearts();
                drawText();
            }
            draw();
        })

        function endGame(){
            let username = $("#this_user").text();
            console.log(heart1object.health)
            if (player1 == username){
                if (heart1object.health < 1) {
                    youLose();
                    $.ajax({
                        method: 'POST',
                        url: "/ajax-end-game",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        data: JSON.stringify({
                            winner: player2,
                            loser: player1
                        }),
                        dataType: "json",
                        success: (data) => {
                            if (data.success) {
                                console.log(data.msg)
                            }
                        }
                    });
                }else if (heart2object.health < 1) {
                    youWin();

                }
            }else{
                if (heart1object.health < 1) {
                    youWin();

                }else if (heart2object.health < 1) {
                    youLose();
                    $.ajax({
                        method: 'POST',
                        url: "/ajax-end-game",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        data: JSON.stringify({
                            winner: player1,
                            loser: player2
                        }),
                        dataType: "json",
                        success: (data) => {
                            if (data.success) {
                                console.log(data.msg)
                            }
                        }
                    });
                }
            }
        }

        //Adds all walls to the array;
        function updateEntityPosition() {
            wallArray = [];
            monsterArray = [];
            playerArray = [];
            var countX = 0;
            for (const colum in newData.field_map) {
                if (Object.hasOwnProperty.call(newData.field_map, colum)) {
                    const element1 = newData.field_map[colum];
                    var countY = 0;
                    for (const square in element1) {
                        if (Object.hasOwnProperty.call(element1, square)) {
                            const element2 = element1[square];
                            if (element2 != null) {
                                if (element2["type"] == "wall") {
                                    wallArray.push(new Position(countX, countY));
                                }
                                if (element2["type"] == "enemy") {
                                    monsterArray.push(new Position(countX, countY));
                                }
                                if (element2["type"] == "player") {
                                    if (element2["name"] == player1){
                                        heart1object = element2;
                                    } else {
                                        heart2object = element2;  
                                    }
                                    playerArray.push(new Position(countX, countY));
                                }
                                if (element2["type"] == "projectile") {
                                    if (element2["player_id"] == 0) {
                                        projectileArray.push(new Position(countX, countY))
                                    } else if(element2["player_id"] == 1) {
                                        projectileArray.push(new Position(countX, countY)) 
                                    }
                                }
                            }
                        }
                        countY++;
                    }
                }
                countX++;
            }
        }
        
        //Takes a position and checks if moveable
        //Direction indicates where to move (right)

        function checkForEntity(position, direction) {
            var entityNotThere = true;
            console.log(playerArray)
            console.log(wallArray)
            switch (direction) {
                case "right":
                    for (let i = 0; i < wallArray.length; i++) {
                        if (position.getX() + 1 == wallArray[i].getX() && position.getY() == wallArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < monsterArray.length; i++) {
                        if (position.getX() + 1 == monsterArray[i].getX() && position.getY() == monsterArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < playerArray.length; i++) {
                        if (position.getX() + 1 == playerArray[i].getX() && position.getY() == playerArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    break;
                case "left":
                    for (let i = 0; i < wallArray.length; i++) {
                        if (position.getX() - 1 == wallArray[i].getX() && position.getY() == wallArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < monsterArray.length; i++) {
                        if (position.getX() - 1 == monsterArray[i].getX() && position.getY() == monsterArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < playerArray.length; i++) {
                        if (position.getX() - 1 == playerArray[i].getX() && position.getY() == playerArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    break;
                case "up":
                    for (let i = 0; i < wallArray.length; i++) {
                        if (position.getX() == wallArray[i].getX() && position.getY() - 1 == wallArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < monsterArray.length; i++) {
                        if (position.getX() == monsterArray[i].getX() && position.getY() - 1 == monsterArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < playerArray.length; i++) {
                        if (position.getX() == playerArray[i].getX() && position.getY() - 1 == playerArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    break;
                case "down":
                    for (let i = 0; i < wallArray.length; i++) {
                        if (position.getX() == wallArray[i].getX() && position.getY() + 1 == wallArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < monsterArray.length; i++) {
                        if (position.getX() == monsterArray[i].getX() && position.getY() + 1 == monsterArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    for (let i = 0; i < playerArray.length; i++) {
                        if (position.getX() == playerArray[i].getX() && position.getY() + 1 == playerArray[i].getY()) {
                            entityNotThere = false;
                        }
                    }
                    break;
                default:
                    console.log("EnitityNotThere: " + entityNotThere)
            }
            return entityNotThere;
        }

        //Gives returns a instence of position with the X and Y position of player with given username
        function userPosition(username) {
            var pos = new Position(0, 0);
            var countX = 0;
            for (const colum in newData.field_map) {
                if (Object.hasOwnProperty.call(newData.field_map, colum)) {
                    const element1 = newData.field_map[colum];
                    var countY = 0;
                    for (const square in element1) {
                        if (Object.hasOwnProperty.call(element1, square)) {
                            const element2 = element1[square];
                            if (element2 != null) {
                                if (element2["name"] == username) {
                                    pos.setX(countX);
                                    pos.setY(countY);
                                }
                            }
                        }
                        countY++;
                    }
                }
                countX++;
            }
            return pos;
        }

        //player_move
        $("body").on("keypress", function (event) {
            if (waitUpdate()) {
                console.log("Handler for `keypress` called.");
                let this_player_id = null
                let username = $("#this_user").text();

                if (username == player1) {
                    this_player_id = 0
                    console.log("Spelare 1");
                }
                else if (username == player2) {
                    this_player_id = 1
                    console.log("Spelare 2")
                }
                let move = null
                let key = (event.keyCode ?
                    event.keyCode :
                    event.which);
                let character = String.fromCharCode(key)
                var usernamePosition = new Position;
                usernamePosition = userPosition(username);
                console.log(character)

                if (character == "d" && usernamePosition.getX() < gridWdith && checkForEntity(usernamePosition, "right")) {
                    move = 'right'
                    console.log("Höger")
                    console.log("Spelare: " + this_player_id)
                }
                else if (character == "a" && usernamePosition.getX() > 0 && checkForEntity(usernamePosition, "left")) {
                    move = 'left';
                    console.log("Vänster")
                    console.log("Spelare: " + this_player_id)
                }
                else if (character == "w" && usernamePosition.getY() > 0 && checkForEntity(usernamePosition, "up")) {
                    move = 'up'
                    console.log("Upp")
                    console.log("Spelare: " + this_player_id)
                }
                else if (character == "s" && usernamePosition.getY() < gridHeight && checkForEntity(usernamePosition, "down")) {
                    move = 'down'
                    console.log("Ner")
                    console.log("Spelare: " + this_player_id)
                } else {
                    console.log("Error, player going out of bounds")
                }

                console.log(usernamePosition)
                console.log("X: " + usernamePosition.getX())
                console.log("Y: " + usernamePosition.getY())
                console.log("Grid x: " + gridWdith)
                console.log("Grid y: " + gridHeight)

                socket.emit('player_move', {
                    room: room_id,
                    player_id: this_player_id,
                    move: move
                })
            }

        });

        //Shoot_projectile
        $("body").on("keypress", function (event) {
            if (event.keyCode == 32) { //spacebar
                var audio = new Audio('../../static/sound/laserSound.mp3');
                audio.play();
                console.log("Handler for `keypress` called.");
                let this_player_id = null
                let username = $("#this_user").text();
                if (username == player1) {
                    this_player_id = 0
                    console.log("Spelare 1");
                }
                else if (username == player2) {
                    this_player_id = 1
                    console.log("Spelare 2")
                }

                socket.emit('shoot_projectile', {
                    room: room_id,
                    player_id: this_player_id
                })
            }
        })

        addEventListener("mouseup", (event) => {
            switch (event.button) {
                case 0:
                    console.log("Du klickade på vänsterklick, SKJUT")
                    let this_player_id = null
                    let username = $("#this_user").text();
                    if (username == player1) {
                        this_player_id = 0
                        console.log("Spelare 1");
                    }
                    else if (username == player2) {
                        this_player_id = 1
                        console.log("Spelare 2")
                    }
                    socket.emit('shoot_projectile', {
                        room: room_id,
                        player_id: this_player_id
                    })
                    break;
                case 1:
                    console.log("okej mitten...")
                    break;
                case 2:
                    console.log("okej höger...")
                default:
                    console.log("okej hörru...")
            }
        })
        let updateInterval = setInterval(updatePage, 100)
    }
})
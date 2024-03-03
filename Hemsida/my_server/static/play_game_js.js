player.room = $("#gameid").val()



$(document).ready(() => {
    console.log("bläbl")
    console.log($("#this_user").text())
    socket.connect();

    socket.emit('join', {
        room: player.room,
    })

    //socket.on('message_from_server', (data) => {
    //    $("#message").text(data.message)
    //    $("#this_user").val() = data.username
    //})

    socket.on('message_from_server', (data) => {
        $("#message").text(data.message)
        if (data.game != null/*data.message == "start_game"*/) {
            console.log("NU VILL NAGON STARTA SPELET")
            start(data.game);
        }
    })

    var start = (start_game) => {
        //if room = 1;
        let room_id = player.room

        //let game = start_game.game
        let player1 = start_game.players[0]
        let player2 = start_game.players[1]
        let newData = null

        //Players
        let newHead1 = document.createElement("h1")
        newHead1.innerText = "Player: " + player1
        let newHead2 = document.createElement("h1")
        newHead2.innerText = "Player: " + player2
        $("body").append(newHead1)
        $("body").append(newHead2)


        //playerhearts
        let player1hearts = document.createElement("canvas")
        player1hearts.id = "player1hearts"
        let player2hearts = document.createElement("canvas")
        player2hearts.id = "player2hearts"
        //$("body").append(player1hearts)
        //$("body").append(player2hearts)

        //New canvas
        let canvas = document.createElement("canvas")
        canvas.id = "myCanvas"
        $("body").append(canvas)

        

        //Else if room = 2;
        console.log("js document.ready")

        console.log(room_id)
        console.log("player1 :" + player1)
        console.log("player2 :" + player2)
        //Console.log("username:" + $("#this_user").val())

        //Canvas
        canvas = document.getElementById("myCanvas"); //Does not need var because it already exists
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

        //Grid
        function drawGrid() {
            ctx.strokeStyle = '#eeeeee';
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
                ctx.closePath();
            }

        }

        //hearts
        function drawHearts() {
            //dimensioner: w 300 h 50
            player1hearts = document.getElementById("player1hearts")
            var ctxnew = player1hearts.getContext("2d");
            ctxnew.beginPath()
            ctxnew.moveTo(50, 12.5)

            ctxnew.stroke()
            ctxnew.closePath()
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


        //Player
        function drawPlayer(playerX, playerY) {
            ctx.beginPath();
            ctx.rect(playerX, playerY, playerWidth, playerHeight);
            ctx.fillStyle = "#046cd4";
            ctx.fill();
            ctx.closePath();
        }

        /*socket.emit("start_monster", {
            room: room_id
        })*/
        

        const updatePage = () => {

            //allowMonsterMove = true
            //do socket requests that request info
            //update the page based on the received info

            //socket.emit('clientlist', {
            //    room: room_id
            //})

            /*socket.emit('monster_move', {
                room: room_id
            })*/

            socket.emit('update_canvas', {
                room: room_id
            })
        }

        //Updates variebles and gui
        socket.on('update', (data) => {
            //console.log(data)
            //console.log(data.field_map)
            //update canvas based on the data received back from the server

            //newData
            cancelWait();
            newData = data;
            updateEntityPosition();
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
                        var countY = 0;
                        for (const square in element1) {
                            if (Object.hasOwnProperty.call(element1, square)) {
                                const element2 = element1[square];
                                if (element2 != null) {
                                    if (element2["type"] == "wall") {
                                        //This is what wall is
                                        //console.log("Wall:" + element2 + "X:" + countX + "Y:" + countY);
                                        drawWall(countX * tileSize, countY * tileSize);
                                    }
                                    if (element2["type"] == "enemy") {
                                        drawMonster(countX * tileSize, countY * tileSize);
                                    }
                                    if (element2["type"] == "player") {
                                        drawPlayer(countX * tileSize, countY * tileSize)
                                    }
                                }
                            }
                            countY++;
                        }
                    }
                    countX++;
                }
            }
            draw();
        })

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
                                    playerArray.push(new Position(countX, countY));
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
            entityNotThere = true;
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
            pos = new Position(0, 0);
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

        //Tar in input från klienten var den vill sin spelare ska röra sig
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
                usernamePosition = new Position;
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

        const leave = () => {
            console.log("Lämna")
            console.log("Lämna")
            console.log("Lämna")
            console.log("Lämna")
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
        setInterval(updatePage, 500)
    }
})
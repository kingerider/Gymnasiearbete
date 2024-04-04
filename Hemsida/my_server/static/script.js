let player = {
    username: null,
    room: null
}

socket = io({autoConnect: false})

//socket.connect()

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
    player.username = $("#playerName").val()
    player.room = data

    socket.emit('join', {
        username: player.username,
        room: player.room,
        role: 'create'
    })
    console.log(`Du är inne på ${player.room}`)
}

function leaveGame(data) {
    console.log(data)
    player.room = null
    socket.emit('leave', {
        room: data
    })
}

from my_server import socket, app


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=8080, debug=True)
from pyjano.server import create_server


if __name__ == '__main__':
    server = create_server(debug=True)
    server.run()
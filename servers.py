import socket
import threading
import time
import http.server as server

data = list()


class SocketServer(socket.socket):
    def __init__(self):
        super().__init__()
        self.bind(('192.168.1.46', 12345))
        self.users = list()
        self.messages = dict()

    def __receiveMessages(self):
        while True:
            for user in self.users:
                self._receiveUserMessage(user[0], user[1])

    def _receiveUserMessage(self, user_socket, user_address):
        global data
        message = user_socket.recv(4096).decode('utf-8')
        if message:
            self.messages[user_address] = message
        data.append(message.split())

    def _acceptConnection(self):
        while True:
            self.users.append(self.accept())
            self.users[-1][0].send('Welcome'.encode('utf-8'))

    def __requestData(self):
        while True:
            try:
                self.users[-1][0].send(
                    '1f58b9145b24d108d7ac38887338b3ea3229833b9c1e418250343f907bfd1047 '
                    'request'.encode('utf-8'))
                time.sleep(4)
            except IndexError:
                pass

    def activate(self):
        self.listen()
        thread_accept = threading.Thread(target=self._acceptConnection)
        thread_accept.start()

        thread_messages = threading.Thread(target=self.__receiveMessages)
        thread_messages.start()

        thread_request = threading.Thread(target=self.__requestData)
        thread_request.start()


class HTTPServer(server.HTTPServer):
    def __init__(self, server_address=('192.168.1.46', 8000), RequestHandlerClass=server.CGIHTTPRequestHandler):
        super().__init__(server_address, RequestHandlerClass)

    def activate(self):
        thread_HTTP = threading.Thread(target=self.serve_forever)
        thread_HTTP.start()

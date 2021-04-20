import socket
import threading
import time
import http.server as server


data = list()


class PreferencesFile:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.contain = dict()

    def getContain(self):
        if not self.contain:
            for line in self.file:
                key, value = line.split(': ')
                self.contain[key] = value[:-1] if key != 'password' else value
        return self.contain


file = PreferencesFile('preference.ini')
PREFERENCE = file.getContain()
del file


class SocketServer(socket.socket):
    def __init__(self):
        super().__init__()
        self.bind((PREFERENCE['ip'], int(PREFERENCE['tcp_port'])))
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
                    f'{PREFERENCE["password"]} '
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
    def __init__(self, server_address=(PREFERENCE['ip'], int(PREFERENCE['http_port'])),
                 RequestHandlerClass=server.CGIHTTPRequestHandler):
        super().__init__(server_address, RequestHandlerClass)

    def activate(self):
        thread_HTTP = threading.Thread(target=self.serve_forever)
        thread_HTTP.start()

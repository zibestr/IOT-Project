import dht
import machine
import socket
import network
from time import sleep


class Client(socket.socket):
    @staticmethod
    def connectWiFi():
        SSID = 'Keenetic-2772'
        password = 'uxB68yGC'
        conn = network.WLAN(network.STA_IF)
        conn.active(True)
        conn.connect(SSID, password)

    def __collectData(self):
        d = dht.DHT22(machine.Pin(5))
        sleep(3)
        d.measure()
        temp = str(d.temperature())
        humid = str(d.humidity())
        return '{} {}'.format(temp, humid)

    def __allowAccess(self, message):
        if message == '1f58b9145b24d108d7ac38887338b3ea3229833b9c1e418250343f907bfd1047':
            return True
        return False

    def active(self):
        isConnect = False
        led = machine.Pin(2, machine.Pin.OUT)
        led.on()
        self.connectWiFi()
        while not isConnect:
            try:
                self.connect(('192.168.1.46', 12345))
                isConnect = True
            except OSError:
                isConnect = False
        while True:
            data_from_server = [elem for elem in self.recv(4096).decode('utf-8').split()]
            print(data_from_server)
            if self.__allowAccess(data_from_server[0]):
                for message in data_from_server[1:]:
                    if message == 'request':
                        data_to_server = self.__collectData().encode('utf-8')
                        self.send(data_to_server)


client = Client()
client.active()

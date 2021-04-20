import servers
from panel.main import *

host = servers.SocketServer()
http_server = servers.HTTPServer()

host.activate()
http_server.activate()

iot_panel = WebSite()
iot_panel.start(servers.data)

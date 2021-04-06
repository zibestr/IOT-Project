import servers
import webpanel

host = servers.SocketServer()
http_server = servers.HTTPServer()

host.activate()
http_server.activate()

iot_panel = webpanel.WebSite()
iot_panel.start(servers.data)

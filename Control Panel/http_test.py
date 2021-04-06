import http.server as server

server_address = ('127.0.0.1', 8000)
server_http = server.HTTPServer(server_address, server.CGIHTTPRequestHandler)
server_http.serve_forever()

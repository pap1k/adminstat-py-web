from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address=('', 777)
    httpd = server_class(server_address, handler_class)
    try:
        print("SERVER STARTED")
        httpd.serve_forever()
    except Exception:
        httpd.server_close()
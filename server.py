import http.server
import socketserver

PORT = 80

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Serving at port: " + str(PORT))
    httpd.serve_forever()
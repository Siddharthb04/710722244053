from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server is working!")

print("Starting test server on port 8000...")
httpd = HTTPServer(('127.0.0.1', 8000), SimpleHandler)
httpd.serve_forever() 
import http.server
import socketserver
import json
import os
from io import BytesIO
from api.chat import application  # Import your WSGI application

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            environ = {
                'wsgi.input': BytesIO(post_data),
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'HTTP_X_API_KEY': self.headers.get('x-api-key', ''),
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'http',
                'wsgi.errors': self.wfile,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': True,
            }
            headers_sent = []

            def start_response(status, headers):
                headers_sent.extend([status, headers])
                self.send_response(int(status.split()[0]))
                for name, value in headers:
                    self.send_header(name, value)
                self.end_headers()

            result = application(environ, start_response)
            response = b''.join(result)
            self.wfile.write(response)
        else:
            super().do_POST()  # For other potential POST requests

    def do_OPTIONS(self):
        if self.path == '/api':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key')
            self.send_header('Content-Length', '0')
            self.end_headers()
        else:
            super().do_OPTIONS()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

PORT = 8000
Handler.extensions_map['.js'] = 'application/javascript'
Handler.extensions_map['.css'] = 'text/css'

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    # Set the LANGFLOW_API_KEY as an environment variable for local testing
    os.environ['LANGFLOW_API_KEY'] = "sk-2jBkPki_UoR35ofcH2aH4D52KNmlZjwExNNbv8kVhxI"
    httpd.serve_forever()
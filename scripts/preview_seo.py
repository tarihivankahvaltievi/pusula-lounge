"""Local static preview with the release's actual CSP and security headers."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from functools import partial
import json,sys
root=Path(sys.argv[1]).resolve()
headers=next(g['headers'] for g in json.loads((root/'vercel.json').read_text())['headers'] if g['source']=='/(.*)')
class Preview(SimpleHTTPRequestHandler):
    def end_headers(self):
        for header in headers:self.send_header(header['key'],header['value'])
        super().end_headers()
    def log_message(self,*args):pass
class Server(ThreadingHTTPServer):
    request_queue_size=128
Server(('127.0.0.1',int(sys.argv[2]) if len(sys.argv)>2 else 8874),partial(Preview,directory=str(root))).serve_forever()

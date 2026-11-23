"""仅公开选定交付文件，支持视频 Range 请求，不提供目录浏览。"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, mimetypes, os, re

HERE=Path(__file__).resolve().parent
SITE=HERE.parent/'output/cloudflare-share'
FILES={'/'+str(p.relative_to(SITE)):p for p in SITE.rglob('*') if p.is_file()}
FILES['/']=SITE/'index.html'

class Handler(BaseHTTPRequestHandler):
    def serve(self,head=False):
        path=FILES.get(unquote(urlsplit(self.path).path))
        if path is None:
            self.send_error(404);return
        size=path.stat().st_size;start=0;end=size-1
        part=self.headers.get('Range')
        if part:
            m=re.fullmatch(r'bytes=(\d*)-(\d*)',part)
            if not m or not any(m.groups()):
                self.send_error(416);return
            if m[1]:start=int(m[1]);end=min(int(m[2]),end) if m[2] else end
            else:start=max(0,size-int(m[2]))
            if start>=size or end<start:
                self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return
        self.send_response(206 if part else 200)
        mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
        if path.suffix=='.md':mime='text/plain; charset=utf-8'
        if path.suffix=='.html':mime='text/html; charset=utf-8'
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(end-start+1))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Cache-Control','no-cache' if path.suffix=='.html' else 'public, max-age=300')
        self.send_header('X-Content-Type-Options','nosniff')
        if part:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        if head:return
        try:
            with path.open('rb') as f:
                f.seek(start);left=end-start+1
                while left:
                    data=f.read(min(left,256*1024))
                    if not data:break
                    self.wfile.write(data);left-=len(data)
        except (BrokenPipeError,ConnectionResetError):pass
    def do_GET(self):self.serve()
    def do_HEAD(self):self.serve(True)

server=ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('SHARE_ORIGIN_PORT','0'))),Handler)
(HERE/'cloudflare-origin.json').write_text(json.dumps({'pid':os.getpid(),'port':server.server_port,'url':f'http://127.0.0.1:{server.server_port}','public_files':list(FILES)}))
server.serve_forever()

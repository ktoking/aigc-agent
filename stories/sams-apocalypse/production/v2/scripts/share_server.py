"""Serve only this delivery directory, with byte-range support for video seeking."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import argparse,re,os
class Handler(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def list_directory(self,path):self.send_error(404);return None
    def send_head(self):
        path=self.translate_path(self.path)
        if os.path.isdir(path):path=os.path.join(path,'index.html')
        if not os.path.isfile(path):self.send_error(404);return None
        f=open(path,'rb');size=os.fstat(f.fileno()).st_size
        start,end=0,size-1
        request_range=self.headers.get('Range')
        if request_range:
            m=re.fullmatch(r'bytes=(\d*)-(\d*)',request_range.strip())
            if not m:f.close();self.send_error(416);return None
            a,b=m.groups()
            if a:start=int(a);end=min(int(b),size-1) if b else size-1
            elif b:start=max(0,size-int(b))
            if start>=size or start>end:
                f.close();self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
        self.send_response(206 if request_range else 200)
        self.send_header('Content-Type',self.guess_type(path));self.send_header('Content-Length',str(end-start+1))
        self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','public, max-age=3600')
        if request_range:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers();f.seek(start);self.remaining=end-start+1;return f
    def copyfile(self,source,output):
        left=self.remaining
        try:
            while left>0:
                buf=source.read(min(256*1024,left))
                if not buf:break
                output.write(buf);left-=len(buf)
        except (BrokenPipeError,ConnectionResetError):pass
p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--port',type=int,default=5194);args=p.parse_args()
server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(args.directory.resolve())))
print(f'Serving delivery on http://127.0.0.1:{args.port}',flush=True);server.serve_forever()

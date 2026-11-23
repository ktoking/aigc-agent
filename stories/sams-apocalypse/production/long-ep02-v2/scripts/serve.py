from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from functools import partial
import re
ROOT=Path(__file__).resolve().parents[3]/'output/LONG-EP02-v2'
class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range=None
        path=Path(self.translate_path(self.path))
        requested=self.headers.get('Range','')
        if requested and path.is_file():
            m=re.fullmatch(r'bytes=(\d+)-(\d*)',requested)
            if m:
                size=path.stat().st_size;a=int(m[1]);b=min(int(m[2]) if m[2] else size-1,size-1)
                if a> b:
                    self.send_error(416);return None
                source=path.open('rb');source.seek(a);self.byte_range=(a,b)
                self.send_response(206);self.send_header('Content-type',self.guess_type(str(path)))
                self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {a}-{b}/{size}')
                self.send_header('Content-Length',str(b-a+1));self.end_headers();return source
        return super().send_head()
    def copyfile(self,source,dest):
        if self.byte_range:
            remaining=self.byte_range[1]-self.byte_range[0]+1
            while remaining:
                data=source.read(min(1024*1024,remaining))
                if not data:break
                dest.write(data);remaining-=len(data)
        else:super().copyfile(source,dest)
print('Serving generated delivery only:',ROOT,flush=True)
ThreadingHTTPServer(('127.0.0.1',5198),partial(RangeHandler,directory=str(ROOT))).serve_forever()

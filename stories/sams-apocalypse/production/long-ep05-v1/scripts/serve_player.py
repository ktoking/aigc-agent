"""Local-only player with byte ranges so MP4 seeking works."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import re, argparse
class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range=None
        path=Path(self.translate_path(self.path))
        if path.is_file() and self.headers.get('Range'):
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',self.headers['Range'])
            if match:
                size=path.stat().st_size;left,right=match.groups()
                start=int(left) if left else max(0,size-int(right));end=min(int(right),size-1) if right and left else size-1
                if start>=size or end<start:
                    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
                src=path.open('rb');src.seek(start);self.byte_range=(start,end)
                self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers();return src
        return super().send_head()
    def copyfile(self,source,outputfile):
        if self.byte_range is None:return super().copyfile(source,outputfile)
        remaining=self.byte_range[1]-self.byte_range[0]+1
        while remaining:
            block=source.read(min(1024*1024,remaining))
            if not block:break
            outputfile.write(block);remaining-=len(block)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=18886);args=parser.parse_args()
    root=Path(__file__).resolve().parents[3]/'output/LONG-EP05-v1'
    ThreadingHTTPServer(('127.0.0.1',args.port),lambda *a,**kw:Handler(*a,directory=str(root),**kw)).serve_forever()

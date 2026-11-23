"""仅绑定本机的文件预览；支持HTML视频拖动所需的HTTP字节范围。"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse, os, re

ROOT=Path(__file__).resolve().parents[1]

class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT),**kw)
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes');super().end_headers()
 def send_head(self):
  self.byte_range=None;path=self.translate_path(self.path);header=self.headers.get('Range')
  if not header or not os.path.isfile(path):return super().send_head()
  match=re.fullmatch(r'bytes=(\d*)-(\d*)',header.strip())
  if not match:return super().send_head()
  f=open(path,'rb');size=os.fstat(f.fileno()).st_size;lo,hi=match.groups()
  if not lo:
   count=int(hi or 0);start=max(0,size-count);end=size-1
  else:start=int(lo);end=min(size-1,int(hi)) if hi else size-1
  if start>=size or start<0 or end<start:
   f.close();self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
  self.byte_range=(start,end);f.seek(start);self.send_response(206)
  self.send_header('Content-Type',self.guess_type(path));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.send_header('Last-Modified',self.date_time_string(os.fstat(f.fileno()).st_mtime));self.end_headers();return f
 def copyfile(self,source,out):
  if self.byte_range is None:return super().copyfile(source,out)
  remaining=self.byte_range[1]-self.byte_range[0]+1
  try:
   while remaining:
    block=source.read(min(1024*1024,remaining))
    if not block:break
    out.write(block);remaining-=len(block)
  except (BrokenPipeError,ConnectionResetError):pass

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8790);a=p.parse_args();server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);print(f'http://127.0.0.1:{a.port}/production/user-script-v2/release-speed1p3/',flush=True);server.serve_forever()

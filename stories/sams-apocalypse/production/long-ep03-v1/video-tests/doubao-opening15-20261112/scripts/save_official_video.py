#!/usr/bin/env python3
"""Save an official MP4 already exported by this account-pool task; no third-party parser."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import urllib.error
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--request-id', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    db = Path.home() / 'Library/Application Support/doubao-account-manager/doubao-manager.sqlite3'
    with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as conn:
        row = conn.execute('SELECT doubao_thread_url,status FROM api_requests WHERE request_id=?', (args.request_id,)).fetchone()
    if not row or not row[0]:
        raise SystemExit('该任务尚无分享导出记录；不重新生成')
    share_url = row[0]
    share = urllib.parse.urlsplit(share_url)
    if share.scheme != 'https' or share.hostname not in ['www.doubao.com', 'doubao.com'] or not share.path.startswith(('/thread/', '/share/')):
        raise SystemExit('该任务尚无官方视频分享页；不重新生成')
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.doubao.com/'}
    # Never forward the local API Bearer key or account cookies to any remote URL.
    with urllib.request.urlopen(urllib.request.Request(share_url, headers=headers), timeout=20) as response:
        page = response.read(16 * 1024 * 1024).decode('utf-8', errors='replace')
    payloads = [html.unescape(page)]
    for _ in range(3):
        payloads.append(payloads[-1].replace('\\"', '"').replace('\\/', '/').replace('\\u002F', '/').replace('\\u002f', '/').replace('\\u0026', '&'))
    candidates = []
    for payload in payloads:
        for match in re.finditer(r'"(?:download_url|play_url|playUrl|downloadUrl)"\s*:\s*"((?:\\.|[^"\\])*)"', payload):
            try:
                value = json.loads('"' + match.group(1) + '"')
            except json.JSONDecodeError:
                continue
            url = urllib.parse.urlsplit(value)
            host = (url.hostname or '').lower()
            official = any(host == domain or host.endswith('.' + domain) for domain in ['doubao.com', 'douyin.com', 'byteoversea.com', 'ibytedtos.com', 'bytedance.com', 'bytecdn.cn', 'bytescm.com'])
            if url.scheme == 'https' and official and value not in candidates:
                candidates.append(value)
    if not candidates:
        print(json.dumps({'saved': False, 'reason': 'no_official_download_url_in_share_page', 'shareVideoMarker': bool(re.search('creation_block|video_dsz|download_url', page)), 'pageBytes': len(page)}))
        return
    output = Path(args.output).resolve()
    if output.exists():
        raise SystemExit('输出文件已存在，未覆盖')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.part')
    for candidate in candidates:
        try:
            with urllib.request.urlopen(urllib.request.Request(candidate, headers=headers), timeout=60) as response:
                prefix = response.read(64)
                if response.status != 200 or b'ftyp' not in prefix[:32]:
                    continue
                digest = hashlib.sha256()
                with temporary.open('wb') as stream:
                    stream.write(prefix)
                    digest.update(prefix)
                    while chunk := response.read(1024 * 1024):
                        stream.write(chunk)
                        digest.update(chunk)
            probe = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(temporary)],capture_output=True,text=True)
            if probe.returncode:
                temporary.unlink(missing_ok=True)
                continue
            media = json.loads(probe.stdout)
            video = next((stream for stream in media.get('streams',[]) if stream.get('codec_type') == 'video'), None)
            if not video:
                temporary.unlink(missing_ok=True)
                continue
            temporary.replace(output)
            manifest = {'saved': True, 'requestId': args.request_id, 'source': 'official Doubao exported download resource', 'output': str(output), 'bytes': output.stat().st_size, 'sha256': digest.hexdigest(), 'thirdPartyParserUsed': False, 'watermarkProcessing': 'none', 'mediaValidation': 'ffprobe video stream confirmed; full decode pending', 'durationSeconds': float(media['format']['duration']), 'width': video['width'], 'height': video['height']}
            output.with_suffix('.download.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps(manifest, ensure_ascii=False))
            return
        except (urllib.error.URLError, TimeoutError, OSError):
            temporary.unlink(missing_ok=True)
    print(json.dumps({'saved': False, 'reason': 'official_candidates_not_downloadable', 'candidateCount': len(candidates)}))


if __name__ == '__main__':
    main()

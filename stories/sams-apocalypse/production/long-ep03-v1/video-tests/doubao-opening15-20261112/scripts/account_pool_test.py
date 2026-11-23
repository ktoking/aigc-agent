#!/usr/bin/env python3
"""本次三镜测试：密钥只在内存中使用，落盘记录删除远程URL。"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEGMENT = ROOT / 'segment_01_00-15s'
SOURCE = ROOT.parents[1]
API = 'http://127.0.0.1:17888'


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def clean(value):
    if isinstance(value, dict):
        return {k: ('[URL omitted]' if ('url' in k.lower() and isinstance(v, str) and v) else clean(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, str):
        return re.sub(r'https?://[^\s<>\"]+', '[URL omitted]', value)
    return value


def settings():
    path = Path.home() / 'Library/Application Support/doubao-account-manager/doubao-manager.sqlite3'
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as conn:
        return {k: json.loads(v) for k, v in conn.execute('SELECT key,value FROM settings')}


def call(route, data=None):
    cfg = settings()
    body = None if data is None else json.dumps(data, ensure_ascii=False).encode()
    req = urllib.request.Request(API + route, data=body, headers={
        'Authorization': 'Bearer ' + cfg['apiKey'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        result = json.load(error)
        result['httpStatus'] = error.code
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['submit', 'poll'])
    parser.add_argument('shot', choices=['p001', 'p002', 'p003'])
    parser.add_argument('--attempt', type=int, default=1)
    parser.add_argument('--account-id', type=int)
    args = parser.parse_args()
    out = SEGMENT / 'output' / args.shot
    if args.attempt != 1:
        out = out / f'attempt-{args.attempt:02d}'
    out.mkdir(parents=True, exist_ok=True)
    receipt = out / 'api-submit.json'
    if args.action == 'submit':
        if receipt.exists() or (out / 'submission-intent.json').exists():
            raise SystemExit('存在提交或意图记录；禁止盲目重复生成，请先核对任务。')
        prompt = (SEGMENT / f'prompt-{args.shot}.txt').read_text()
        body = {'prompt': prompt, 'referenceImagePath': str(SOURCE / 'assets' / f'{args.shot}.png'),
                'model': 'seedance_2_0_mini', 'aspectRatio': '16:9',
                'source': f'sams-ep03-opening15-20261112-{args.shot}-a{args.attempt:02d}'}
        if args.account_id is not None:
            body['accountId'] = args.account_id
        if not Path(body['referenceImagePath']).is_file():
            raise SystemExit('参考图不存在')
        write(out / 'request-body.json', body)
        write(out / 'submission-intent.json', {'time': dt.datetime.now(dt.timezone.utc).isoformat(), 'shot': args.shot})
        result = call('/api/generate', body)
        write(receipt, clean(result))
    else:
        record = json.loads(receipt.read_text())
        request_id = record.get('requestId') or record.get('request', {}).get('requestId')
        if not request_id:
            raise SystemExit('提交响应缺少requestId，需要人工核对，不重复提交')
        result = call('/api/requests/' + request_id)
        write(out / 'api-result.json', clean(result))
    print(json.dumps(clean(result), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

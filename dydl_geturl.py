#!/usr/bin/env python3
"""Fetch a Douyin video's real CDN URL by driving Chrome over CDP.

Chrome (headed — Douyin blocks headless) loads douyin.com so Douyin's own
JS/service worker signs the detail API request (a_bogus / msToken /
x-secsdk-web-signature). We then read the best bit_rate play URL from the
response — no signature reimplementation needed. Prints JSON {url,title,gear}.
"""
import json
import re
import subprocess
import sys
import time
import urllib.request

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PROFILE = '/tmp/dydl-chrome-profile'
PORT = 9333


def cdp_targets():
    return json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json', timeout=5))


def main(video_id):
    import websockets.sync.client as wsc

    proc = subprocess.Popen([
        CHROME, f'--remote-debugging-port={PORT}', f'--user-data-dir={PROFILE}',
        '--no-first-run', '--no-default-browser-check',
        '--window-position=-2000,-2000', '--window-size=400,300',
        'https://www.douyin.com/',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        ws_url = None
        for _ in range(40):
            try:
                for t in cdp_targets():
                    if t.get('type') == 'page':
                        ws_url = t['webSocketDebuggerUrl']
                        break
                if ws_url:
                    break
            except Exception:
                pass
            time.sleep(0.5)
        if not ws_url:
            raise SystemExit('could not connect to Chrome CDP')

        with wsc.connect(ws_url, max_size=50_000_000) as ws:
            mid = [0]

            def cmd(method, params=None):
                mid[0] += 1
                ws.send(json.dumps({'id': mid[0], 'method': method, 'params': params or {}}))
                while True:
                    msg = json.loads(ws.recv())
                    if msg.get('id') == mid[0]:
                        return msg

            cmd('Page.enable')

            js = '''(async () => {
                try {
                    const r = await fetch('https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=%s',
                        {credentials:'include', headers:{'referer':'https://www.douyin.com/'}});
                    const t = await r.text();
                    if (!t) return JSON.stringify({empty:true});
                    const d = JSON.parse(t);
                    const v = d.aweme_detail && d.aweme_detail.video;
                    if (!v) return JSON.stringify({empty:true, status:d.status_code});
                    const brs = (v.bit_rate||[]).slice().sort((a,b)=>(b.bit_rate||0)-(a.bit_rate||0));
                    const pick = brs[0] && brs[0].play_addr && brs[0].play_addr.url_list[0];
                    return JSON.stringify({url: pick || (v.play_addr.url_list||[])[0],
                                           title: d.aweme_detail.desc,
                                           gear: brs[0] && brs[0].gear_name});
                } catch (e) { return JSON.stringify({empty:true, err:''+e}); }
            })()''' % video_id

            for attempt in range(5):
                time.sleep(7)
                res = cmd('Runtime.evaluate', {
                    'expression': js, 'awaitPromise': True, 'returnByValue': True})
                val = res.get('result', {}).get('result', {}).get('value')
                if val:
                    data = json.loads(val)
                    if data.get('url'):
                        return data
                cmd('Page.reload')
            raise SystemExit('could not obtain signed URL (Douyin challenge not passed)')
    finally:
        proc.terminate()


if __name__ == '__main__':
    arg = sys.argv[1]
    m = re.search(r'(\d{8,})', arg)
    vid = m.group(1) if m else arg
    print(json.dumps(main(vid), ensure_ascii=False))

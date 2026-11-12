"""Serve personal CSV data locally without copying it into the public site."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent.parent
private = root / 'private-data'
for name in ('words.csv', 'poems.csv'):
    if not (private / name).is_file():
        sys.exit(f'缺少个人数据：{private / name}')
with tempfile.TemporaryDirectory(prefix='rijiyuelei-private-') as tmp:
    tmp_root = Path(tmp)
    shutil.copytree(root / 'dist', tmp_root / 'dist', ignore=shutil.ignore_patterns('words', 'poems'))
    shutil.copytree(root / 'scripts', tmp_root / 'scripts')
    for name in ('words.csv', 'poems.csv'):
        shutil.copy2(private / name, tmp_root / 'dist' / name)
    subprocess.run([sys.executable, str(tmp_root / 'scripts' / 'build_routes.py')], check=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(tmp_root / 'dist'))
    server = ThreadingHTTPServer(('127.0.0.1', 8765), handler)
    print('个人数据预览：http://127.0.0.1:8765/ ；按 Ctrl+C 退出。', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

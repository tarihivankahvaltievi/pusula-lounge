# -*- coding: utf-8 -*-
"""Notify IndexNow of the latest commit's published HTML changes. Receipt does not prove indexing."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from datetime import datetime
from zoneinfo import ZoneInfo
import concurrent.futures,hashlib,json,subprocess,sys,argparse
parser=argparse.ArgumentParser();parser.add_argument('root',type=Path);parser.add_argument('--submit',action='store_true');parser.add_argument('--report',type=Path,required=True);args=parser.parse_args()
root=args.root.resolve();origin='https://www.pusulalounge.com'
files=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD','--','*.html'],cwd=root,text=True).splitlines()
files=[path for path in files if (root/path).is_file() and not path.startswith('__')]
assert files,'No changed HTML pages in latest commit'
paths=['/'+path[:-10] if path.endswith('index.html') else '/'+path for path in files]
key_files=[p for p in root.glob('*.txt') if p.stem==p.read_text().strip()]
assert len(key_files)==1,'Expected one existing public IndexNow verification file'
key_file=key_files[0];key=key_file.read_text().strip();urls=[origin+path for path in paths]
if not args.submit:
 print(json.dumps({'mode':'dry-run','urls':urls},indent=2));sys.exit(0)
with urlopen(origin+'/'+key_file.name,timeout=25) as response:assert response.read().decode().strip()==key,'Live public verification file mismatch'
def check(pair):
 file,url=pair
 with urlopen(url,timeout=25) as response:
  assert response.status==200 and hashlib.sha256(response.read()).digest()==hashlib.sha256((root/file).read_bytes()).digest(),'Live HTML mismatch: '+url
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(check,zip(files,urls)))
payload={'host':'www.pusulalounge.com','key':key,'keyLocation':origin+'/'+key_file.name,'urlList':urls}
request=Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8'},method='POST')
try:
 with urlopen(request,timeout=30) as response:status=response.status;message=response.read().decode()
except HTTPError as response:status=response.code;message=response.read().decode()
report={'checkedAt':datetime.now(ZoneInfo('Europe/Istanbul')).isoformat(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'status':status,'message':message,'urls':urls,'note':'200 = received; 202 = received with key validation pending. Neither confirms indexing, ranking or reservations. Google Search Console submission is separate.'}
args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':status,'submittedURLs':len(urls),'received':status in (200,202)},indent=2))
sys.exit(0 if status in (200,202) else 1)

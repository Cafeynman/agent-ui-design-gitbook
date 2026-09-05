"""Deterministic offline checks for generated pages and source JavaScript."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys
from urllib.parse import urlparse, unquote
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'_site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.labels=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'for' in a:self.labels.append(a['for'])
  for k in ('href','src'):
   if k in a:self.links.append(a[k])

def check():
 errors=[];warnings=[]
 for p in SITE.rglob('*.html'):
  parser=Page();parser.feed(p.read_text(encoding='utf-8'))
  if len(set(parser.ids))!=len(parser.ids):errors.append(f'{p.relative_to(SITE)}: duplicate ID')
  for label in parser.labels:
   if label not in parser.ids:errors.append(f'{p.relative_to(SITE)}: missing label target {label}')
  for link in parser.links:
   u=urlparse(link)
   if u.scheme or u.netloc or not u.path:continue
   path=(SITE/unquote(u.path).lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
   if path.is_dir():path=path/'index.html'
   if not path.exists():errors.append(f'{p.relative_to(SITE)}: missing {link}')
 for path in (ROOT/'assets').glob('*.js'):
  p=subprocess.run(['node','--check',str(path)],capture_output=True,text=True)
  if p.returncode:errors.append(p.stderr)
 data=json.loads((SITE/'version.json').read_text());assert data['terms']==168
 result={'errors':errors,'warnings':warnings,'html_pages':len(list(SITE.rglob('*.html'))),'source_js':len(list((ROOT/'assets').glob('*.js'))),'terms':data['terms']}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return result
if __name__=='__main__':sys.exit(bool(check()['errors']))

"""Targeted learning-UX regressions. Local fixture mode uses mock storage, explicitly labeled."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json, os, re, sys, http.server, socketserver, threading
R=Path(__file__).resolve().parents[1];results=[];page_errors=[];fixture='--fixture' in sys.argv
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(R/'_site'),**k)
 def log_message(self,*a):pass
server=None
if not fixture:
 server=socketserver.TCPServer(('127.0.0.1',0),Handler)
 threading.Thread(target=server.serve_forever,daemon=True).start()
 url=f'http://127.0.0.1:{server.server_address[1]}/'
def check(label,value):
 assert value,label
 results.append(label)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or p.chromium.executable_path,headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844});page.on('pageerror',lambda e:page_errors.append(str(e)))
 if fixture:
  markup=(R/'index.html').read_text();markup=re.sub(r'<script.*?</script>','',markup,flags=re.S)
  markup=re.sub(r'<link rel="stylesheet"[^>]+>','<style>'+(R/'assets/style.css').read_text()+'</style>',markup)
  page.set_content(markup)
  page.add_script_tag(content='const memory={};Object.defineProperty(window,"localStorage",{value:{getItem:k=>memory[k]||null,setItem:(k,v)=>memory[k]=v}});')
  for file in ['catalog.js','lessons.js','app.js']:page.add_script_tag(content=(R/'assets'/file).read_text())
 else:page.goto(url)
 def go(id):
  page.evaluate('(id)=>location.hash="lesson="+id',id)
  page.wait_for_function('(id)=>document.querySelector("#lesson-picker").value===id',arg=id)
 page.locator('#controls button').first.click()
 check('Vague hero gets vague feedback','还不知道' in page.locator('#observation').inner_text())
 page.locator('#controls button').nth(1).click()
 check('Concrete hero gets concrete feedback','上传论文' in page.locator('#observation').inner_text())
 check('First question avoids introducing another unknown term','首屏可见范围' not in page.locator('#question').inner_text())
 page.locator('#answers button').nth(1).click()
 page.locator('#next').click()
 expect(page.locator('#lesson-title')).to_be_focused()
 check('Mobile next lesson scrolls to its title',0<=page.locator('#lesson-title').bounding_box()['y']<=30)
 go('hero');check('Completed lesson stays visibly completed','本课已完成' in page.locator('#save-note').inner_text())
 go('type');page.locator('.skip').evaluate('(e)=>e.click()')
 check('Skip link does not reset the active lesson',page.locator('#lesson-picker').input_value()=='type')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':844});go('responsive')
  page.wait_for_function('Math.abs(document.querySelector("#responsive-shell").getBoundingClientRect().width-parseFloat(document.querySelector("#range-value").textContent))<2')
  for edge in ['max','min']:
   page.locator('#range').evaluate('(e,k)=>{e.value=e[k];e.dispatchEvent(new Event("input",{bubbles:true}))}',edge)
   dimensions=page.evaluate('''()=>{const s=document.querySelector('#responsive-shell'),d=document.querySelector('#demo'),b=s.getBoundingClientRect(),r=d.getBoundingClientRect();return {inside:b.left>=r.left&&b.right<=r.right,actual:b.width,shown:parseFloat(document.querySelector('#range-value').textContent),columns:getComputedStyle(document.querySelector('.responsive-grid')).gridTemplateColumns.trim().split(/\\s+/).length}}''')
   check(f'{width}px {edge}: preview not clipped',dimensions['inside'])
   check(f'{width}px {edge}: width label is real',abs(dimensions['actual']-dimensions['shown'])<2)
   check(f'{width}px {edge}: layout follows real width',dimensions['columns']==(1 if dimensions['actual']<=440 else 3))
  if not page.locator('#layout-schematic').is_visible():page.locator('#layout-compare').click()
  expect(page.locator('#layout-schematic')).to_be_visible()
  check(f'{width}px: wide/narrow explanation available',page.locator('#layout-compare').get_attribute('aria-expanded')=='true')
  check(f'{width}px: comparison fits screen',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  if width==390:page.screenshot(path=str(R/'reviews/review-mobile.png'),full_page=True)
 go('states');page.locator('#controls button').nth(2).click();page.locator('#state-action button').click()
 expect(page.locator('#demo')).to_contain_text('笔记已生成')
 check('Retry selects the actual success state',page.locator('#controls button').nth(3).get_attribute('aria-pressed')=='true')
 go('spacing');page.locator('#range').evaluate('(e)=>{e.value=0;e.dispatchEvent(new Event("input"))}')
 check('Tight spacing not described as wide','挤在一起' in page.locator('#observation').inner_text())
 # Deliberately hold file reads to verify late reads cannot replace newer picks.
 page.locator('#records').click()
 page.evaluate('''()=>{window.realFileText=File.prototype.text;window.finishSlow=null;File.prototype.text=function(){if(this.name==='slow.json')return new Promise(resolve=>window.finishSlow=resolve);return window.realFileText.call(this)}}''')
 payload=lambda name, data:{'name':name,'mimeType':'application/json','buffer':json.dumps(data).encode()}
 valid={'version':1,'completed':['hero'],'saved':[]};invalid={'version':1,'completed':['does-not-exist'],'saved':[]}
 page.locator('#import-file').set_input_files(payload('slow.json',valid));page.wait_for_function('window.finishSlow!==null')
 page.locator('#import-file').set_input_files(payload('new.json',invalid));expect(page.locator('#import-status')).to_contain_text('无法识别')
 page.evaluate('(s)=>window.finishSlow(JSON.stringify(s))',valid);page.wait_for_timeout(60)
 check('Late file read cannot override latest invalid pick',page.locator('#confirm-import').is_hidden())
 check('Latest file error stays visible','无法识别' in page.locator('#import-status').inner_text())
 page.locator('#import-file').set_input_files(payload('slow.json',valid));page.wait_for_function('window.finishSlow!==null')
 page.keyboard.press('Escape');expect(page.locator('#records-dialog')).not_to_be_visible()
 page.evaluate('(s)=>window.finishSlow(JSON.stringify(s))',valid);page.wait_for_timeout(60)
 page.locator('#records').click();check('Closing dialog discards pending import',page.locator('#confirm-import').is_hidden())
 page.keyboard.press('Escape');go('hero');page.locator('#controls button').nth(1).click()
 page.screenshot(path=str(R/'reviews/review-desktop.png'),full_page=True)
 check('No page JavaScript errors',not page_errors)
 browser.close()
if server:server.shutdown();server.server_close()
report={'independent_agent':False,'mode':'in-memory DOM / mock storage' if fixture else 'Chromium / real local HTTP','checks_passed':len(results),'checks':results,'page_errors':page_errors}
(R/'reviews/review-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))

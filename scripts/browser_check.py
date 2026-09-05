"""Real Chromium regression tests, not an independent model review."""
from pathlib import Path
import json,threading,http.server,socketserver,os,re
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1];RESULTS=ROOT/'reviews';RESULTS.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT/'_site'),**k)
 def log_message(self,*a):pass
server=socketserver.TCPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_address[1]}/'
checks=[];errors=[]
def ok(name,test):
 assert test,name
 checks.append(name)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or p.chromium.executable_path,headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1050});page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url);page.wait_for_selector('#lesson-list button');page.screenshot(path=str(RESULTS/'home-desktop.png'),full_page=True)
 lessons=page.evaluate('window.LESSONS');ok('12 lessons available',len(lessons)==12)
 for lesson in lessons:
  name=lesson['id'];page.goto(url+'#lesson='+name);page.wait_for_function('(id)=>document.querySelector("#lesson-picker").value===id',arg=name)
  if name in ['hero','cta','hierarchy','states','tabs']:page.locator('#controls button').nth(1).click()
  elif name in ['spacing','type','responsive']:page.locator('#range').focus();page.keyboard.press('ArrowLeft')
  elif name=='form':
   page.locator('#sample-email').fill('abc');page.locator('#sample-form button').click();ok('Invalid field marked',page.locator('#sample-email').get_attribute('aria-invalid')=='true');ok('Invalid field focused',page.evaluate('document.activeElement.id')=='sample-email');page.locator('#sample-email').fill('name@example.com');page.locator('#sample-form button').click();ok('Valid form feedback',page.locator('#email-error').inner_text().startswith('✓'))
  elif name=='modal':
   page.locator('#controls button').first.click();ok('Native modal open',page.locator('#demo-dialog').evaluate('(e)=>e.open'));page.keyboard.press('Escape');ok('Escape closes modal',not page.locator('#demo-dialog').evaluate('(e)=>e.open'));ok('Modal focus restored',page.locator('#controls button').first.evaluate('(e)=>e===document.activeElement'))
  elif name=='focus':page.locator('#controls button').first.click();page.keyboard.press('Tab');ok('Tab moves to next action',page.evaluate('document.activeElement.id')=='focus-second')
  elif name=='tokens':page.locator('#controls button').nth(1).click();ok('Tokens recolor all linked controls',page.locator('#token-preview').evaluate('(e)=>getComputedStyle(e).getPropertyValue("--accent").trim()')=='#7540a1')
  wrong=1-lesson['correct'];page.locator('#answers button').nth(wrong).click();ok(name+' wrong answer explains',page.locator('#feedback').inner_text().startswith('再看看'))
  page.locator('#answers button').nth(lesson['correct']).click();ok(name+' completion saved',name in page.evaluate('JSON.parse(localStorage.getItem("aui-learn-v1")).completed'))
 page.reload();ok('Progress survives reload',page.locator('#progress').get_attribute('value')=='12')
 page.goto(url+'#lesson=tabs');page.locator('#tab-summary').focus();page.keyboard.press('ArrowRight');ok('Tab arrow keyboard support',page.locator('#tab-notes').get_attribute('aria-selected')=='true')
 page.goto(url+'#lesson=states');page.locator('#controls button').nth(2).click();page.locator('#state-action button').click();page.wait_for_timeout(850);ok('Error can recover', '笔记已生成' in page.locator('#demo').inner_text())
 page.goto(url+'#dictionary');page.locator('#search').fill('首屏');ok('Chinese search works',page.locator('.term-row').count()>0);page.locator('#search').fill('shouping');ok('Common alias search works',page.locator('.term-row').count()>0)
 page.locator('.term-row').first.click();ok('Term dialog visible',page.locator('#term-dialog').evaluate('(e)=>e.open'));page.locator('#term-save').click();page.keyboard.press('Escape');expect(page.locator('.term-row').first).to_be_focused();ok('Term dialog restores focus after save',page.evaluate('document.activeElement.classList.contains("term-row")'));page.locator('#search').fill('<img src=x onerror=alert(1)>');ok('Search does not insert HTML',page.locator('#term-list img').count()==0);ok('No result state',page.locator('#empty-search').is_visible());page.locator('#clear-search').click();ok('Reset shows all 168 terms',page.locator('.term-row').count()==168)
 page.locator('#records').click();bad={'version':1,'completed':['made-up'],'saved':[]};page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});expect(page.locator('#import-status')).to_contain_text('无法识别');ok('Unknown IDs rejected','无法识别' in page.locator('#import-status').inner_text());ok('Invalid import cannot apply',page.locator('#confirm-import').is_hidden())
 saved=page.evaluate('JSON.parse(localStorage.getItem("aui-learn-v1"))');page.locator('#import-file').set_input_files({'name':'ok.json','mimeType':'application/json','buffer':json.dumps(saved).encode()});expect(page.locator('#confirm-import')).to_be_visible();ok('Import requires confirmation',page.locator('#confirm-import').is_visible());page.locator('#confirm-import').click();ok('Import merge confirmed','已合并' in page.locator('#import-status').inner_text());page.keyboard.press('Escape')
 for width in [320,390,768,1440]:
  page.set_viewport_size({'width':width,'height':950});
  for name in [l['id'] for l in lessons]:
   page.goto(url+'#lesson='+name);ok(f'No overflow {width}px {name}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  page.goto(url+'#lesson=hero')
  if width==390:page.screenshot(path=str(RESULTS/'home-mobile.png'),full_page=True)
 page.set_viewport_size({'width':1440,'height':1050});page.goto(url+'#lesson=hero');page.screenshot(path=str(RESULTS/'hero-reviewed.png'),full_page=True)
 blocked=browser.new_context();blocked.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new Error("blocked")}})');b=blocked.new_page();b.goto(url);ok('Blocked local storage does not crash',b.locator('#lesson-title').inner_text()=='开头说清楚');blocked.close()
 ok('No page JavaScript errors',len(errors)==0);browser.close()
server.shutdown()
report={'kind':'automated-browser-review','independent_agent':False,'checks_passed':len(checks),'checks':checks,'javascript_errors':errors,'viewports':[320,390,768,1440]}
(RESULTS/'browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))

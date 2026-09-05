"""Build the searchable catalog and a static reading mirror. Never writes git refs."""
from pathlib import Path
import hashlib, html, json, os, re, shutil
from markdown_it import MarkdownIt
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
BOOK = ROOT / 'book'

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    for name in ('index.html','assets','labs'):
        src, dst = ROOT/name, OUT/name
        if src.is_dir(): shutil.copytree(src,dst)
        else: shutil.copy2(src,dst)
    terms=[]
    cats={'page-structure':'页面与结构','components':'界面组件','interaction-states':'交互与状态','visual-styles':'视觉与排版','ux-design-system':'体验与设计系统'}
    for name, category in cats.items():
        p=BOOK/'glossary'/f'{name}.md'
        for line in p.read_text(encoding='utf-8').splitlines():
            cells=[x.strip() for x in line.strip().strip('|').split('|')]
            if len(cells)!=5 or cells[0] not in ('P0','P1','P2'): continue
            level,en,cn,definition,review=cells
            slug=re.sub(r'[^a-z0-9]+','-',en.lower()).strip('-')
            terms.append(dict(id=slug,en=en,cn=cn,def_=definition,review=review,level=level,category=category,chapter=f'glossary/{name}.md'))
    assert len({t['id'] for t in terms})==len(terms), 'Duplicate term IDs'
    assert len(terms)>=150,'Glossary missing: refusing an incomplete build'
    for t in terms:t['def']=t.pop('def_')
    catalog='window.CATALOG = '+json.dumps(terms,ensure_ascii=False)+';\n'
    (OUT/'assets/catalog.js').write_text(catalog,encoding='utf-8')
    (ROOT/'assets/catalog.js').write_text(catalog,encoding='utf-8')
    md=MarkdownIt('commonmark',{'html':True}).enable('table')
    guide=OUT/'guide';guide.mkdir()
    shutil.copytree(BOOK/'.gitbook',guide/'.gitbook')
    entries=re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)',(BOOK/'SUMMARY.md').read_text(encoding='utf-8'))
    missing=[href for title,href in entries if not (BOOK/href).exists()]
    assert not missing,f'Book chapters missing: {missing}'
    for p in BOOK.rglob('*.md'):
        rel=p.relative_to(BOOK);dest=guide/rel.with_suffix('.html');dest.parent.mkdir(parents=True,exist_ok=True)
        rootlink=os.path.relpath(OUT,dest.parent).replace(os.sep,'/')
        text=p.read_text(encoding='utf-8')
        text=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
        # GitBook-specific wrappers become normal text or links in this reading mirror.
        text=re.sub(r'{% embed url="([^"]+)" %}',lambda m:f'[打开示例]({m[1]})',text)
        text=re.sub(r'{% (?:tab|step) title="([^"]+)" %}',lambda m:f'\n### {m[1]}\n',text)
        text=re.sub(r'{%.*?%}','',text,flags=re.S)
        rendered=md.render(text)
        def local_links(m):
            attr,url=m[1],m[2]
            for prefix in ('https://raw.githack.com/Cafeynman/agent-ui-design-gitbook/main/','https://cafeynman.github.io/agent-ui-design-gitbook/'):
                if url.startswith(prefix):return f'{attr}="{rootlink}/{url[len(prefix):]}"'
            if not re.match(r'(?:https?:|mailto:|#)',url):url=re.sub(r'\.md(?=$|#)', '.html',url)
            return f'{attr}="{url}"'
        rendered=re.sub(r'(href|src)="([^"]+)"',local_links,rendered)
        title_match=re.search(r'^# (.+)',text,re.M);title=title_match[1] if title_match else p.stem
        nav=''.join(f'<a href="{html.escape(os.path.relpath(guide/Path(href).with_suffix(".html"),dest.parent).replace(os.sep,"/"))}">{html.escape(title)}</a>' for title,href in entries)
        note='<p class="archive-note">这是原始长篇资料，保留作参考。工具功能请以官方文档为准；先学互动课，不必一次读完。</p>'
        page=f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · 点一下，懂 UI</title><link rel="stylesheet" href="{rootlink}/assets/style.css"><body><header class="top"><a class="brand" href="{rootlink}/index.html">◧ 点一下，懂 UI</a><a href="{rootlink}/index.html#dictionary">查词</a></header><main class="guide-layout"><details class="guide-nav"><summary>展开全书目录</summary>{nav}</details><article class="guide-copy">{note}{rendered}</article></main></body></html>'
        dest.write_text(page,encoding='utf-8')
    shutil.copy2(guide/'README.html',guide/'index.html')
    # Publication marker makes it possible to verify an actual deployment, not just a 200 page.
    versions={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'index.html',ROOT/'assets/app.js',ROOT/'assets/style.css',ROOT/'assets/lessons.js']}
    release={'edition':'learn-by-doing-1','terms':len(terms),'lessons':12,'source_files':versions,'commit':os.environ.get('GITHUB_SHA','local')}
    (OUT/'version.json').write_text(json.dumps(release,indent=2),encoding='utf-8')
    (OUT/'.nojekyll').touch()
    print(json.dumps({'terms':len(terms),'book_pages':len(list(BOOK.rglob('*.md'))),'output':str(OUT)},ensure_ascii=False))

if __name__=='__main__':build()

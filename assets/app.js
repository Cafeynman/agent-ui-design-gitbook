'use strict';
(() => {
const $ = id => document.getElementById(id), lessons = window.LESSONS || [], terms = window.CATALOG || [];
const KEY = 'aui-learn-v1';
let cleanDemo = () => {}, focusLessonOnRoute = false, importRequest = 0;
let state = {version:1,completed:[],saved:[]}, storageOK=true, current=0, touched=false, solved=false, timer=0, noticeTimer=0, selectedTerm=null, pendingImport=null;
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function validState(data) {
 if(!data || data.version!==1 || !Array.isArray(data.completed) || !Array.isArray(data.saved)) throw Error('格式不符：请选择本工具导出的备份。');
 if(data.completed.length>lessons.length || data.saved.length>terms.length) throw Error('记录数量异常。');
 const ids = new Set(lessons.map(l=>l.id)), tids = new Set(terms.map(t=>t.id));
 if(data.completed.some(x=>typeof x!=='string'||!ids.has(x))||data.saved.some(x=>typeof x!=='string'||!tids.has(x))) throw Error('包含无法识别的课程或词条。');
 return {version:1,completed:[...new Set(data.completed)],saved:[...new Set(data.saved)]};
}
try {const v=localStorage.getItem(KEY);if(v) state=validState(JSON.parse(v));} catch{storageOK=false;}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch{storageOK=false;notice('浏览器未保存记录，请导出备份。');} updateProgress();}
function notice(text){clearTimeout(noticeTimer);$('notice').textContent=text;$('notice').hidden=false;noticeTimer=setTimeout(()=>$('notice').hidden=true,3500);}
function updateProgress(){
 $('progress').max=lessons.length;$('progress').value=state.completed.length;
 $('progress-label').textContent=`完成 ${state.completed.length}/${lessons.length}`;
 $('lesson-list').innerHTML=lessons.map((l,i)=>`<li><button data-lesson="${esc(l.id)}" ${i===current?'aria-current="step"':''}><span class="lesson-number ${state.completed.includes(l.id)?'done':''}">${state.completed.includes(l.id)?'✓':String(i+1).padStart(2,'0')}</span><span>${esc(l.name)}</span></button></li>`).join('');
 $('lesson-picker').value=lessons[current].id;
}
$('lesson-picker').innerHTML=lessons.map((l,i)=>`<option value="${l.id}">${i+1}. ${esc(l.name)}</option>`).join('');
function complete(){
 const id=lessons[current].id;
 if(touched&&solved&&!state.completed.includes(id)){state.completed.push(id);save();}
 $('save-note').textContent=state.completed.includes(id)
  ? (storageOK?'本课已完成。也可以再试一次。':'本课已完成；请导出备份，避免丢失。')
  : solved?'答对了！再操作一次示例，就能完成。':'操作示例并答对，才会记为完成。';
}
function observe(text){touched=true;$('observation').textContent=text||lessons[current].observe;complete();}
function button(label,run,cls='quiet'){const b=document.createElement('button');b.textContent=label;b.className=cls;b.onclick=run;return b;}
// Feedback describes the selected example, not a prewritten "good" outcome.
function controlsSwitch(labels,render){
 const messages={
  hero:['听起来很厉害，但还不知道它做什么。','现在知道了：上传论文，得到笔记。'],
  cta:['“提交”没说接下来会发生什么。','“生成笔记”说清了点击结果。'],
  hierarchy:['全都一样重，眼睛不知道先看哪里。','先看到标题，再读说明。重点出来了。'],
  states:['正在生成，结果还没出来。','还没有内容，先告诉用户怎么开始。','没成功，给一次重试的机会。','成功了，让用户看到结果。'],
  tabs:['标签页换内容，不表示先后顺序。','步骤条表示：先选择，再生成，最后完成。']
 };
 const row=$('controls');
 labels.forEach((label,i)=>{
  const b=button(label,()=>{
   [...row.children].forEach(x=>x.setAttribute('aria-pressed','false'));
   b.setAttribute('aria-pressed','true');render(i);
   observe(messages[lessons[current].id]?.[i]);
  });
  b.setAttribute('aria-pressed',String(i===0));row.append(b);
 });render(0);
}
function slider(label,min,max,value,step,onChange){
 $('controls').innerHTML=`<label for="range">${esc(label)}</label><input id="range" type="range" min="${min}" max="${max}" step="${step}" value="${value}"><output id="range-value" for="range">${value}</output>`;
 $('range').oninput=e=>{
  $('range-value').textContent=e.target.value;
  const message=onChange(Number(e.target.value));observe(message);
 };
}
function renderResponsive(){
 $('demo').innerHTML=`<div id="responsive-shell" class="responsive-shell"><div class="responsive-content"><div class="mini-nav"><strong>我的论文</strong><span class="desktop-menu">所有论文　收藏　设置</span><span class="mobile-menu">☰ 菜单示意</span></div><div class="responsive-grid"><div>论文一<br>阅读笔记</div><div>论文二<br>关键发现</div><div>论文三<br>待阅读</div></div></div></div><div id="layout-schematic" hidden><p class="small">排法示意，不是缩小真实页面。</p><div class="layout-comparison"><div><strong>宽屏：并排</strong><div class="layout-blocks wide"><span>A</span><span>B</span><span>C</span></div></div><div><strong>窄屏：向下排</strong><div class="layout-blocks narrow"><span>A</span><span>B</span><span>C</span></div></div></div></div>`;
 const host=$('demo'), shell=$('responsive-shell');
 slider('预览宽度',220,640,640,1,n=>{
  shell.style.width=n+'px';$('range-value').textContent=n+' px';
  $('range').setAttribute('aria-valuetext',n+' 像素');
  return n<=440?'现在排成一列，不把文字挤小。':'宽度够了，可以并排放三列。';
 });
 const compare=button('看宽窄对照',()=>{
  const box=$('layout-schematic');box.hidden=!box.hidden;
  compare.setAttribute('aria-expanded',String(!box.hidden));
  if(!box.hidden)observe('对照看：宽屏并排，窄屏向下排。');
 });
 compare.id='layout-compare';compare.setAttribute('aria-expanded','false');
 compare.setAttribute('aria-controls','layout-schematic');$('controls').append(compare);
 // Use real available width. A hidden overflow must not masquerade as responsiveness.
 let first=true;
 const sync=()=>{
  if(!shell.isConnected||host.closest('[hidden]'))return;
  const css=getComputedStyle(host);
  const max=Math.min(640,Math.floor(host.clientWidth-parseFloat(css.paddingLeft)-parseFloat(css.paddingRight)));
  if(max<1)return;
  const min=Math.min(220,max), input=$('range');
  const n=first?max:Math.max(min,Math.min(max,Number(input.value)));
  first=false;input.min=min;input.max=max;input.value=n;shell.style.width=n+'px';
  input.setAttribute('aria-valuetext',n+' 像素');$('range-value').textContent=n+' px';
 };
 sync();const observer=new ResizeObserver(sync);observer.observe(host);
 cleanDemo=()=>observer.disconnect();
}
const product=`<div class="mini-product" aria-label="论文笔记示意"><strong>我的第一份笔记</strong><div class="note-lines"><div class="line blue"></div><div class="line"></div><div class="line short"></div></div><div class="line short"></div></div>`;
function hero(specific){return `<div class="demo-frame"><div class="mini-nav"><strong>纸舟 · 论文笔记</strong><span>功能　帮助</span></div><div class="mini-hero"><div><h3>${specific?'把长论文，<br>变成一页笔记。':'下一代 AI 平台'}</h3><p>${specific?'上传论文，先看要点，再读原文。':'重塑未来，释放无限可能。'}</p><button class="primary" id="hero-action">${specific?'试着生成笔记':'了解更多'}</button></div>${product}</div></div>`;}
function setHero(i){$('demo').innerHTML=hero(i);$('hero-action').onclick=()=>observe('这是教学演示；真实页面还需兑现按钮承诺。');}
function stateDemo(mode){clearTimeout(timer);['loading','empty','error','success'].forEach((name,i)=>$('controls').children[i]?.setAttribute('aria-pressed',String(name===mode)));const map={loading:['◌','正在生成笔记','稍等一下，结果会出现在这里。'],empty:['＋','还没有论文','上传第一份论文，开始做笔记。'],error:['!','生成失败','模拟网络中断，可以重新生成。'],success:['✓','笔记已生成','摘要和关键段落已准备好。']};const x=map[mode];$('demo').innerHTML=`<div class="demo-frame state-box"><div class="state-symbol" aria-hidden="true">${x[0]}</div><h3>${x[1]}</h3><p class="small">${x[2]}</p><div id="state-action"></div></div>`;if(mode==='error'||mode==='empty')$('state-action').append(button(mode==='error'?'重新生成':'模拟上传',()=>{observe();stateDemo('loading');timer=setTimeout(()=>{stateDemo('success');observe('现在成功了：给结果，而不是让用户一直等。');},700);},'primary'));}
function renderLesson(){
 clearTimeout(timer);cleanDemo();cleanDemo=()=>{};touched=false;solved=false;const l=lessons[current];
 $('lesson-count').textContent=`第 ${current+1} 课 / ${lessons.length}`;$('lesson-title').textContent=l.name;$('lesson-en').textContent=l.en;$('lesson-def').textContent=l.def;$('try-instruction').textContent=l.try;$('question').textContent=l.question;$('prompt').textContent=l.prompt;$('usage').textContent=l.use;$('caution').textContent=l.avoid;$('lesson-source').href=l.source;$('feedback').textContent='';$('feedback').className='feedback';$('observation').textContent='先操作上面的示例。';$('controls').replaceChildren();$('demo').replaceChildren();$('more').open=false;
 $('next').textContent=current===lessons.length-1?'返回第一课':'下一课';
 $('answers').replaceChildren(...l.answers.map((a,i)=>button(a,()=>{const correct=i===l.correct;solved=correct;$('feedback').className='feedback '+(correct?'correct':'wrong');$('feedback').textContent=(correct?'✓ 对。':'再看看。')+l.why;complete();})));
 switch(l.id){
 case 'hero':controlsSwitch(['含糊的开场','说清用途'],setHero);break;
 case 'cta':controlsSwitch(['只写“提交”','写清结果'],i=>{$('demo').innerHTML=`<div class="demo-frame state-box"><h3>论文已选好</h3><p class="small">我的论文.pdf · 示例文件</p><button id="cta-action" class="primary">${i?'生成笔记':'提交'}</button></div>`;$('cta-action').onclick=()=>observe('✓ 笔记已生成（模拟）。按钮与结果应该说同一件事。');});break;
 case 'hierarchy':controlsSwitch(['全部一样重','分出主次'],i=>{$('demo').innerHTML=`<div class="demo-frame ${i?'':'hierarchy-bad'}"><p class="small">我的工作台</p><h3 style="font-size:30px">今天读哪一篇？</h3><p>先选一篇论文，再生成阅读笔记。</p><p class="small">支持 PDF。这里是次要说明。</p></div>`;});break;
 case 'spacing':$('demo').innerHTML='<div class="demo-frame" id="spacing-frame"><div class="group-block"><strong>账户信息</strong><p>姓名、头像、登录邮箱</p></div><div class="group-block"><strong>通知偏好</strong><p>提醒时间、通知渠道</p></div></div>';slider('组间距离',0,48,8,4,n=>{$('spacing-frame').style.setProperty('--group-gap',n+'px');return n<16?'两组挤在一起，分界不明显。':'组与组拉开了，组内仍然靠近。';});break;
 case 'type':$('demo').innerHTML='<div class="demo-frame"><p id="read-sample" class="read-sample">一份好界面，不要求你先读懂说明书。标题告诉你这是哪里，按钮告诉你接下来能做什么。文字之间留一点空间，眼睛就不必在拥挤的行间寻找下一句。先让内容好读，再考虑装饰。</p></div>';slider('行距',1,2.4,1.2,.1,n=>{$('read-sample').style.setProperty('--leading',n);return n<1.4?'行挤在一起，阅读容易串行。':n>2?'行距有些散，再往回试一点。':'比刚才舒展。试着读完一段。';});break;
 case 'responsive':renderResponsive();break;
 case 'states':controlsSwitch(['等待','空白','失败','成功'],i=>stateDemo(['loading','empty','error','success'][i]));break;
 case 'form':$('demo').innerHTML='<form id="sample-form" class="demo-frame form-sample" novalidate><label for="sample-email">收件邮箱</label><input id="sample-email" type="email" autocomplete="off" aria-describedby="email-error" placeholder="name@example.com"><p id="email-error" class="field-error" role="status"></p><button type="submit" class="primary">发送示例笔记</button></form>';$('sample-form').onsubmit=e=>{e.preventDefault();const f=$('sample-email'),valid=f.value.trim()&&f.checkValidity();f.setAttribute('aria-invalid',String(!valid));$('email-error').textContent=valid?'✓ 格式正确。已模拟发送，没有发出真实邮件。':'请输入完整邮箱，例如 name@example.com。';if(!valid)f.focus();observe();};break;
 case 'modal':$('controls').append(button('打开弹窗',()=>{$('demo-dialog').showModal();observe();}),button('打开侧边抽屉',()=>{$('drawer-example').hidden=false;observe();}));$('demo').innerHTML='<div class="demo-frame"><p>这里是你正在编辑的笔记。</p><div id="drawer-example" class="drawer-preview" hidden><strong>笔记信息</strong><p class="small">此示例不阻止背景操作。</p><button id="close-drawer">收起抽屉</button></div><button id="background-action">背景仍可操作</button></div>';$('close-drawer').onclick=()=>{$('drawer-example').hidden=true;observe();};$('background-action').onclick=()=>observe('这个抽屉没有阻止背景操作；模态弹窗会阻止。');break;
 case 'tabs':controlsSwitch(['标签页：换内容','步骤条：走流程'],i=>{if(!i){$('demo').innerHTML='<div class="demo-frame"><div role="tablist" aria-label="笔记内容" class="tablist"><button role="tab" id="tab-summary" aria-controls="tab-panel" aria-selected="true">摘要</button><button role="tab" id="tab-notes" aria-controls="tab-panel" aria-selected="false" tabindex="-1">我的笔记</button></div><div role="tabpanel" id="tab-panel" aria-labelledby="tab-summary" tabindex="0" class="tabpanel">这篇论文提出了一个新方法。</div></div>';const tabs=[...$('demo').querySelectorAll('[role=tab]')];function selectTab(n,focus){tabs.forEach((t,j)=>{t.setAttribute('aria-selected',String(n===j));t.tabIndex=n===j?0:-1;});$('tab-panel').setAttribute('aria-labelledby',tabs[n].id);$('tab-panel').textContent=n?'我的想法：先比较它与旧方法的差异。':'这篇论文提出了一个新方法。';if(focus)tabs[n].focus();observe();}tabs.forEach((t,n)=>{t.onclick=()=>selectTab(n,false);t.onkeydown=e=>{let k;if(e.key==='ArrowRight'||e.key==='ArrowLeft')k=1-n;else if(e.key==='Home')k=0;else if(e.key==='End')k=1;if(k!==undefined){e.preventDefault();selectTab(k,true);}};});}else{let step=0;$('demo').innerHTML='<div class="demo-frame"><ol class="steps"><li aria-current="step">选择</li><li>生成</li><li>完成</li></ol><p id="step-label">先选择一份论文。</p><button id="step-next" class="primary">继续</button></div>';$('step-next').onclick=()=>{step=(step+1)%3;[...$('demo').querySelectorAll('.steps li')].forEach((el,j)=>{el.removeAttribute('aria-current');if(j===step)el.setAttribute('aria-current','step');});$('step-label').textContent=['先选择一份论文。','现在生成笔记。','✓ 笔记准备好了。'][step];$('step-next').textContent=step===2?'重新体验':'继续';observe();};}});break;
 case 'focus':$('controls').append(button('开始：把焦点放进示例',()=>{$('focus-first').focus({focusVisible:true});observe();}));$('demo').innerHTML='<div class="demo-frame"><p>按 Tab，观察焦点移动。</p><div class="answers"><button id="focus-first">上传论文</button><button id="focus-second">查看笔记</button><button id="focus-third">导出笔记</button></div></div>';$('demo').onfocusin=()=>observe();break;
 case 'tokens':$('demo').innerHTML='<div class="demo-frame token-preview" id="token-preview"><h3>统一的品牌色</h3><p class="small">下面三个元素共用一个颜色设置。</p><span class="tag">已收藏</span><button id="token-action">生成笔记</button></div>';$('controls').append(button('蓝色',()=>{$('token-preview').style.setProperty('--accent','#2459c4');observe();}),button('紫色',()=>{$('token-preview').style.setProperty('--accent','#7540a1');observe();}),button('绿色',()=>{$('token-preview').style.setProperty('--accent','#17643e');observe();}));$('token-action').onclick=()=>observe('按钮、标签、标题共享颜色，但不同角色仍应各有设置。');break;
 }
 if(l.id!=='focus')$('demo').onfocusin=null;
 updateProgress();complete();
}
function lessonRoute(id){focusLessonOnRoute=true;if(location.hash==='#lesson='+id)route();else location.hash='lesson='+id;}
$('lesson-list').onclick=e=>{const b=e.target.closest('[data-lesson]');if(b)lessonRoute(b.dataset.lesson);};$('lesson-picker').onchange=e=>lessonRoute(e.target.value);$('next').onclick=()=>lessonRoute(lessons[(current+1)%lessons.length].id);
async function copy(text){try{await navigator.clipboard.writeText(text);notice('指令已复制。');}catch{notice('未能自动复制，请选中指令手动复制。');}}
$('copy').onclick=()=>copy(lessons[current].prompt);
function route(){if(location.hash==='#lesson-title'){$('lesson-title').focus();return;}clearTimeout(timer);const hash=new URLSearchParams(location.hash.slice(1));const dict=location.hash.startsWith('#dictionary')||hash.has('term');$('learning').hidden=dict;$('dictionary').hidden=!dict;$('learn-link').removeAttribute('aria-current');$('dictionary-link').removeAttribute('aria-current');$(dict?'dictionary-link':'learn-link').setAttribute('aria-current','page');if(dict){if(hash.has('q'))$('search').value=hash.get('q');renderTerms();if(hash.has('term')){const t=terms.find(x=>x.id===hash.get('term'));if(t)openTerm(t);else notice('词条不存在，请搜索。');}}else{if($('term-dialog').open)$('term-dialog').close();const i=lessons.findIndex(l=>l.id===hash.get('lesson'));current=i<0?0:i;renderLesson();if(focusLessonOnRoute){$('lesson-title').focus({preventScroll:true});$('lesson-title').scrollIntoView({block:'start'});focusLessonOnRoute=false;}}}
const aliases={'hero section':'首屏 hero page shouping','cta':'行动按钮 xingdong','skeleton':'骨架屏 gujiaping','responsive design':'响应式 xiangyingshi','modal':'弹窗 tanchuang','drawer':'抽屉 chouti','navbar':'导航 daohang'};
function norm(v){return v.normalize('NFKC').toLowerCase().trim();}
for(const c of [...new Set(terms.map(t=>t.category))]){const o=document.createElement('option');o.value=c;o.textContent=c;$('category').append(o);}
function renderTerms(){const q=norm($('search').value);const found=terms.filter(t=>(!$('category').value||t.category===$('category').value)&&(!$('only-saved').checked||state.saved.includes(t.id))&&q.split(/\s+/).every(word=>norm([t.en,t.cn,t.def,aliases[t.en.toLowerCase()]||''].join(' ')).includes(word)));$('result-count').textContent=`找到 ${found.length} / ${terms.length} 个词。点开看一句解释。`;$('empty-search').hidden=!!found.length;$('term-list').replaceChildren(...found.map(t=>{const b=button('',()=>{history.replaceState(null,'','#term='+t.id);openTerm(t);},'term-row');b.dataset.term=t.id;b.innerHTML=`<span><strong>${esc(t.cn)}${state.saved.includes(t.id)?' ☆':''}</strong><small>${esc(t.en)}</small></span><span>${esc(t.def)}</span>`;return b;}));}
$('search').oninput=()=>{renderTerms();history.replaceState(null,'','#dictionary&q='+encodeURIComponent($('search').value));};$('category').onchange=renderTerms;$('only-saved').onchange=renderTerms;$('clear-search').onclick=()=>{$('search').value='';$('category').value='';$('only-saved').checked=false;history.replaceState(null,'','#dictionary');renderTerms();$('search').focus();};
function openTerm(t){selectedTerm=t;$('term-title').textContent=t.cn+' · '+t.en;$('term-definition').textContent=t.def;$('term-review').textContent=t.review;$('term-reading').href='guide/'+t.chapter.replace(/\.md$/,'.html');$('term-save').textContent=state.saved.includes(t.id)?'取消收藏':'收藏';if(!$('term-dialog').open)$('term-dialog').showModal();$('term-title').focus();}
$('term-dialog').addEventListener('close',()=>{if(location.hash.startsWith('#term='))history.replaceState(null,'','#dictionary');const returnTo=[...$('term-list').querySelectorAll('button')].find(b=>b.dataset.term===selectedTerm?.id);if(!$('dictionary').hidden)(returnTo||$('search')).focus();});
$('term-save').onclick=()=>{if(!selectedTerm)return;const id=selectedTerm.id;state.saved=state.saved.includes(id)?state.saved.filter(x=>x!==id):[...state.saved,id];save();$('term-save').textContent=state.saved.includes(id)?'取消收藏':'收藏';renderTerms();};
$('records').onclick=()=>{$('storage-warning').textContent=storageOK?'完成记录不代表已掌握，建议回到自己的项目再试一次。':'本地存储不可用或旧记录损坏，本次进度仅在当前页面内。请导出备份。';$('records-dialog').showModal();};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='ui-learning-records.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
// Discard stale file reads if a newer file is picked or the dialog is closed.
$('import-file').onchange=async e=>{
 const request=++importRequest, input=e.target, f=input.files[0];
 pendingImport=null;$('confirm-import').hidden=true;$('import-status').textContent='';
 if(!f)return;
 try{
  if(f.size>65536)throw Error('文件太大，请选择小于 64 KB 的备份。');
  const text=await f.text();if(request!==importRequest)return;
  pendingImport=validState(JSON.parse(text));
  $('import-status').textContent=`读到 ${pendingImport.completed.length} 课和 ${pendingImport.saved.length} 个收藏。确认后再合并。`;
  $('confirm-import').hidden=false;
 }catch(err){if(request===importRequest)$('import-status').textContent=err instanceof SyntaxError?'不是有效的 JSON 备份。':err.message;}
 finally{if(request===importRequest)input.value='';}
};
$('records-dialog').addEventListener('close',()=>{importRequest++;pendingImport=null;$('confirm-import').hidden=true;$('import-status').textContent='';});
document.querySelector('.skip').onclick=e=>{e.preventDefault();const target=$('dictionary').hidden?$('lesson-title'):$('search');target.focus();target.scrollIntoView({block:'start'});};
$('confirm-import').onclick=()=>{if(!pendingImport)return;state.completed=[...new Set([...state.completed,...pendingImport.completed])];state.saved=[...new Set([...state.saved,...pendingImport.saved])];pendingImport=null;save();renderTerms();$('confirm-import').hidden=true;$('import-status').textContent='已合并。原来的记录也保留了。';};
window.addEventListener('hashchange',route);route();
})();

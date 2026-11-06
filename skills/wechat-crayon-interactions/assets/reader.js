(function(){
  'use strict';
  const $=(s,root=document)=>root.querySelector(s);
  const all=(s,root=document)=>Array.from(root.querySelectorAll(s));
  const clamp=(v,lo=0,hi=1)=>Math.max(lo,Math.min(hi,v));
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const seen=new WeakMap();
  function inMotion(el,active){
    seen.set(el,active);
    const stopped=el.dataset.paused==='yes'||(reduced.matches&&el.dataset.paused!=='no');
    for(const scene of all('.plate > svg',el)){if(active&&!stopped)scene.unpauseAnimations();else scene.pauseAnimations();}
    const b=$('[data-play]',el);if(b){b.setAttribute('aria-pressed',String(stopped));b.title=stopped?'继续动画':'暂停动画';b.innerHTML=stopped?icons.play:icons.pause;}
  }
  const observe=new IntersectionObserver(items=>items.forEach(it=>inMotion(it.target,it.isIntersecting&&!document.hidden)));
  const icons=JSON.parse(document.getElementById('ui-icons').textContent);
  function nativeKeys(el){
    for(const hit of all('rect[id][pointer-events]',el)){
      hit.setAttribute('role','button');hit.setAttribute('tabindex','0');
      const b=hit.closest('g');const labels=b?all('text',b).slice(-2).map(t=>t.textContent):[];
      hit.setAttribute('aria-label',labels.join('，')||el.querySelector('h3').textContent+'，触发');
      hit.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();hit.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
    }
  }
  function gesture(section,signal){
    const n=Number(section.dataset.n),plane=$('.pad',section),strip=$('.strip',section),value=$('[type=range]',section);
    const status=$('.feedback',section),s=String(n),suffix=k=>plane.querySelector('[id$="n'+s+'k'+k+'"]');
    const on=(node,event,fn,opts={})=>node&&node.addEventListener(event,fn,{...opts,signal});
    let frame=0,timer=0,sequence=0,down=false,held=false,x0=0,y0=0,unlocked=false,finished=false,draw=0,turn=0,spinning=false,angle=0,raf=0;
    const say=(v,message)=>{section.dataset.phase=v;if(status)status.textContent=message;};
    const frames=all('g[id*="kframe"]',plane);
    const show=i=>{frame=i;frames.forEach((node,j)=>node.setAttribute('visibility',i===j?'visible':'hidden'));section.dataset.frame=String(i);};
    const progress=v=>{
      v=clamp(v);section.dataset.progress=v.toFixed(3);if(value)value.value=String(Math.round(v*100));
      if(n===26){[0,1,2].forEach(i=>suffix('layer'+i).setAttribute('transform','translate('+((v-.5)*(i+1)*47)+' 0)'));say('drag',Math.round(v*100)+'%');}
      if(n===27){const idx=Math.min(2,Math.floor(v*3));show(idx);say('drag',['松绿工装','朱红围裙','钴蓝外套'][idx]);}
      if(n===28){suffix('wipe').setAttribute('width',String(v*480));const line=$('.split-mark',plane);line.style.left=(v*100)+'%';say('drag','套色 '+Math.round(v*100)+'%');}
      if(n===58&&!finished){unlocked=v>=.99;show(unlocked?1:0);$('.unlock',section).disabled=!unlocked;say(unlocked?'unlocked':'drag',unlocked?'签印到位':'签印 '+Math.round(v*100)+'%');}
    };
    const later=(fn,ms)=>setTimeout(fn,ms);
    const clear=()=>{clearTimeout(timer);clearInterval(sequence);timer=sequence=0;};
    const lastPage=()=>strip&&strip.scrollLeft>=strip.scrollWidth-strip.clientWidth-4;
    const fire=()=>{
      if((n===34||n===60)&&!lastPage()){say('locked','先到末页');return;}
      held=true;
      if(n===29||n===30||n===31){show(1);say('held',n===31?'松开还原':'校样已显现');}
      else if(n===32){show((frame+1)%frames.length);sequence=setInterval(()=>{show((frame+1)%frames.length);},230);say('playing','六帧试印中');}
      else if(n===33){draw=draw%3+1;show(draw);say('draw','第 '+draw+' 支编者签');}
      else if(n===34){show(2);say('revealed','校色编号 02');}
      else if(n===60){show(3);finished=true;say('complete','三步完成，终稿入册');}
    };
    const release=()=>{const wasHeld=held;clear();down=held=false;if(n===31&&wasHeld){show(0);say('restored','已还原铅稿');}if(n===32&&wasHeld)say('paused','停在第 '+(frame+1)+' 帧');};
    const arm=()=>{release();down=true;timer=later(()=>{if(down)fire();},460);};
    if([26,27,28,58].includes(n)){
      const val=ev=>{const r=plane.getBoundingClientRect();return clamp((ev.clientX-r.left)/r.width);};
      on(plane,'pointerdown',ev=>{if(ev.button!==0||finished)return;down=true;plane.setPointerCapture(ev.pointerId);progress(val(ev));});
      on(plane,'pointermove',ev=>{if(down)progress(val(ev));});on(plane,'pointerup',()=>{down=false;});on(plane,'pointercancel',()=>{down=false;});
      on(value,'input',()=>progress(value.value/100));progress(n===58?0:.5);
      if(n===58)on($('.unlock',section),'click',()=>{if(!unlocked)return;finished=true;show(2);$('.extra-sheet',section).hidden=false;$('.unlock',section).disabled=true;value.disabled=true;say('complete','终稿已展开');});
    }else if(n===54){
      const wheel=suffix('wheel'),button=$('.wheel-button',section);
      const spin=()=>{if(!spinning)return;angle=(angle+5)%360;wheel.setAttribute('transform','rotate('+angle+')');raf=requestAnimationFrame(spin);};
      on(button,'click',()=>{if(!spinning){spinning=true;button.textContent='停下';say('spinning','选色中');spin();}else{
        spinning=false;cancelAnimationFrame(raf);const stops=[0,1,2];const i=stops[turn++%3];angle=(360-(i+.5)*45)%360;wheel.setAttribute('transform','rotate('+angle+')');button.textContent='再转一次';say('stopped','停在'+['松绿','朱红','钴蓝'][i]);}});
    }else{
      if(n===34){show(1);}if(n===60)show(2);
      on(plane,'pointerdown',ev=>{if(ev.button!==0||finished)return;x0=ev.clientX;y0=ev.clientY;plane.setPointerCapture(ev.pointerId);arm();});
      on(plane,'pointermove',ev=>{if(down&&!held&&Math.hypot(ev.clientX-x0,ev.clientY-y0)>14)release();});
      for(const e of ['pointerup','pointercancel','lostpointercapture','blur'])on(plane,e,release);
      on(plane,'keydown',ev=>{if((ev.key===' '||ev.key==='Enter')&&!ev.repeat){ev.preventDefault();arm();}});on(plane,'keyup',ev=>{if(ev.key===' '||ev.key==='Enter')release();});
      on(plane,'contextmenu',ev=>ev.preventDefault());
      if(strip){for(const b of all('[data-page]',section))on(b,'click',()=>strip.scrollBy({left:Number(b.dataset.page)*strip.clientWidth,behavior:reduced.matches?'instant':'smooth'}));
        on(strip,'scroll',()=>{if(!finished&&!held)say(lastPage()?'at-end':'scroll',lastPage()?'末页':'翻页中');},{passive:true});}
      if(n===60){const open=$('.unseal',section);on(open,'click',()=>{$('.folded',section).hidden=true;$('.longfold',section).hidden=false;say('opened','封皮已揭');});}
    }
    on(window,'blur',release);on(document,'visibilitychange',()=>{if(document.hidden){release();if(spinning)buttonStop();}});
    function buttonStop(){const b=$('.wheel-button',section);if(spinning&&b)b.click();}
    signal.addEventListener('abort',()=>{release();spinning=false;cancelAnimationFrame(raf);},{once:true});
  }
  const snapshots=new Map();
  const controls=new WeakMap();
  function mount(el,fresh=false){
    const stage=$('.work',el);if(!stage)return;
    if(fresh){controls.get(el)?.abort();stage.innerHTML=snapshots.get(el);for(const k of ['phase','progress','frame','paused'])delete el.dataset[k];}else snapshots.set(el,stage.innerHTML);
    const controller=new AbortController();controls.set(el,controller);
    if(el.dataset.kind==='gesture')gesture(el,controller.signal);else nativeKeys(el);
    if(el.dataset.kind==='scroll'){
      const rail=$('[tabindex="0"]',stage);
      for(const b of all('[data-scroll]',stage))b.addEventListener('click',()=>{const dir=Number(b.dataset.scroll);rail.scrollBy(el.dataset.n==='22'?{top:dir*rail.clientHeight,behavior:'smooth'}:{left:dir*rail.clientWidth,behavior:'smooth'});},{signal:controller.signal});
    }
    if($('[data-play]',el)){observe.observe(el);inMotion(el,seen.get(el)??false);}
  }
  const items=all('.effect');for(const el of items){
    mount(el);
    $('[data-reset]',el).addEventListener('click',()=>mount(el,true));
    const play=$('[data-play]',el);play?.addEventListener('click',()=>{const state=play.getAttribute('aria-pressed')==='true';el.dataset.paused=state?'no':'yes';inMotion(el,true);});
  }
  document.addEventListener('visibilitychange',()=>{for(const el of items)if($('[data-play]',el))inMotion(el,!document.hidden&&el.getBoundingClientRect().top<innerHeight&&el.getBoundingClientRect().bottom>0);});
  reduced.addEventListener('change',()=>{for(const el of items)if($('[data-play]',el))inMotion(el,seen.get(el));});
  const chapters=all('.chapter');const navlinks=all('[data-nav]');
  function mark(){let current=chapters[0];for(const c of chapters)if(c.getBoundingClientRect().top<=145)current=c;for(const a of navlinks)a.toggleAttribute('aria-current',!!current&&a.hash==='#'+current.id);}
  let queued=false;addEventListener('scroll',()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{mark();queued=false;});},{passive:true});mark();
  const menu=$('#contents-toggle'),drawer=$('#contents-pop');
  function closeMenu(){if(drawer){drawer.hidden=true;menu.setAttribute('aria-expanded','false');}}
  menu?.addEventListener('click',()=>{drawer.hidden=!drawer.hidden;menu.setAttribute('aria-expanded',String(!drawer.hidden));});
  drawer?.addEventListener('click',ev=>{if(ev.target.closest('a'))closeMenu();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
  document.addEventListener('click',e=>{if(drawer&&!drawer.hidden&&!drawer.contains(e.target)&&!menu.contains(e.target))closeMenu();});
  // Namescope each clipboard write, including two copies of the same sample in one draft.
  function fragment(key,n){
    const temp=document.createElement('section');
    const payload=JSON.parse(document.getElementById('print-data').textContent);
    temp.innerHTML=n?payload.parts[n]:payload[key];
    const p='c'+Date.now().toString(36)+'x'+Math.random().toString(36).slice(2,9)+'x',ids=new Map();
    all('[id]',temp).forEach((el,i)=>{ids.set(el.id,p+i);el.id=p+i;});
    for(const el of all('[begin],[end]',temp))for(const attr of ['begin','end'])if(el.hasAttribute(attr))
      el.setAttribute(attr,el.getAttribute(attr).split(';').map(token=>token.replace(/^([a-zA-Z][a-zA-Z0-9]*)\.(click|begin|end)/,(_,id,event)=>(ids.get(id)||id)+'.'+event)).join(';'));
    return temp.innerHTML;
  }
  async function copy(key,n){
    const message=$('#notice');try{
      const html=fragment(key,n);await MengfeiClipboard.write(html);
      message.textContent=n?(n.startsWith('ch')?'已复制第 '+n.slice(2)+' 章':'已复制 '+n+' 号正文片段'):key==='static'?'已复制静态全文':'已复制公众号试贴全文';
    }catch{message.textContent='富文本复制失败。请用 Chrome 或 Edge 打开本页重试。';}
    message.hidden=false;clearTimeout(message._timer);message._timer=setTimeout(()=>{message.hidden=true;},5500);
  }
  for(const el of all('[data-copy]'))el.addEventListener('click',()=>copy(el.dataset.copy,el.dataset.part));
  document.documentElement.classList.add('reader-ready');
})();

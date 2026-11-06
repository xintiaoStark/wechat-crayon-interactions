"""Build an offline reader, a script-free WeChat trial, a static edition and an editable manuscript."""
import argparse
import base64
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from catalog import EFFECTS, GROUPS, GESTURES, SCROLL, group, kind
from ink import Plate, WORDS, VOCAB, AUTHOR, artframe, book, PINE, BLUE, RED
from effects import first, scrolling, motion
from choices import decisions
from gestures import gesture
from typeplate import BRAND, MUTED, COMMON, OUTER, CHAPTER, SUBHEAD, CAPTION, SOURCE, CODE, CODEBOX, SIGN, SIGNBOX, reader_rules

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets"
REPO="https://github.com/xintiaoStark/wechat-crayon-interactions"
GALLERY="https://xintiaostark.github.io/wechat-crayon-interactions/"
ICONS=json.loads((ASSETS/"icons.json").read_text(encoding="utf-8"))
ES=lambda s:escape(str(s),quote=True)
DEFAULT={
    "title":"梦飞AI · 公众号互动排版样刊","cover_lines":["纸上","有机关"],"subtitle":"60 种互动排版样张",
    "author":"梦飞AI","issue":"INTERACTION NOTES / 01","cover_alt":"蜡笔绘制的样书、印色和咖啡杯",
    "intro":["墨迹下面压着一句话。点开第一张，再看看下面那行字有没有移动。",
            "这份样刊按动作排成八章。标着正文试贴的效果会生成无脚本片段。标着网页手势的样张，在这里可以直接操作；公众号稿保留动作分镜与网页版入口。"],
    "outro":["挑一张适合当前段落的，再决定要不要用下一张。若读者没点开，也应当读得到要紧的结论。"],
    "repo_url":REPO,"gallery_url":GALLERY,
}
def para(value,style=COMMON):
    return '<p style="'+style+'"><span leaf="">'+ES(value)+'</span></p>'
def link(label,url):
    return '<p style="'+SOURCE+'"><a href="'+ES(url)+'" style="color:'+MUTED+';text-decoration:underline;"><span leaf="">'+ES(label)+'</span></a></p>'
def h(value,large=False):
    return para(value,CHAPTER if large else SUBHEAD)
def codeblock(value):
    return '<section style="'+CODEBOX+'">'+para(value,CODE)+'</section>'
def url(value):
    parts=urlsplit(value)
    if parts.scheme!='https' or not parts.netloc or parts.username or parts.password:
        raise ValueError("Use a public HTTPS URL without credentials.")
    return value
def picture(path):
    path=Path(path);data=path.read_bytes()
    mime="image/jpeg" if data.startswith(b"\xff\xd8") else "image/png" if data.startswith(b"\x89PNG\r\n\x1a\n") else None
    if mime is None or len(data)>5_000_000:raise ValueError("Cover must be a PNG/JPEG smaller than 5 MB.")
    return "data:"+mime+";base64,"+base64.b64encode(data).decode("ascii")
def core(n,ns="edition",terms=None,author="梦飞AI"):
    p=Plate(n,ns);token=WORDS.set(terms or {});terms_in_art=set();capture=VOCAB.set(terms_in_art);byline=AUTHOR.set(author)
    try:
        if n in GESTURES:live,printed=gesture(p,n)
        elif n in SCROLL:live=printed=scrolling(p,n)
        elif n<=20:live=printed=first(p,n)
        elif n<=46 or n==59:live=printed=motion(p,n)
        else:live=printed=decisions(p,n)
    finally:WORDS.reset(token);VOCAB.reset(capture);AUTHOR.reset(byline)
    if terms and set(terms)-terms_in_art:raise ValueError(f"{n:02}: unknown artwork text: {set(terms)-terms_in_art}")
    return live,printed.replace(' tabindex="0"',''),terms_in_art

def work(n,picture_html,author):
    if n in SCROLL:
        axis="上下" if n==22 else "左右"
        return '<div class="scroll-art">'+picture_html+'</div><div class="play-tools">'+''.join(f'<button type="button" class="mini" data-scroll="{v}" title="{w}" aria-label="{w}">{ICONS[icon]}</button>' for v,w,icon in [(-1,"向上滚动" if n==22 else "向前滚动","ChevronLeft"),(1,"向下滚动" if n==22 else "向后滚动","ChevronRight")])+'</div>'
    if n not in GESTURES:
        return '<div class="plate">'+picture_html+'</div>'+('<p class="normal-after">交稿标记 · '+ES(author)+'</p>' if n in (4,5,6) else '')
    isdrag=n in (26,27,28,58)
    plane='<div class="pad '+('drag' if isdrag else 'hold')+'"'+(' role="button" tabindex="0" aria-label="长按校样"' if n in (29,30,31,32,33,34,60) else '')+'>'+picture_html+('<span aria-hidden="true" class="split-mark"></span>' if n==28 else '')+'</div>'
    foot='<div class="gesture-line">'
    if isdrag:foot+='<input type="range" min="0" max="100" value="50" aria-label="手势进度">'
    if n==58:foot+='<button class="action unlock" disabled>打开终稿</button>'
    if n==54:foot+='<button class="action wheel-button">开始选色</button>'
    foot+='<span class="feedback" role="status"></span></div>'
    if n==58:foot+='<p class="extra-sheet" hidden>终稿已打开。把原任务、生成的样张和验收条件放在一起，下一位编辑才能接着改。</p>'
    if n in (34,60):
        dummy=Plate(n,"empty");pages=2 if n==34 else 3
        slides=''.join('<div class="slide">'+dummy.svg(artframe(j,["待校样纸","校色批注"][j],"横滑到末页",book([PINE,BLUE][j])))+'</div>' for j in range(pages-1))+'<div class="slide">'+plane+'</div>'
        strip='<div class="strip" tabindex="0" aria-label="分页画卷">'+slides+'</div><div class="play-tools"><button class="mini" data-page="-1" title="上一页" aria-label="上一页">'+ICONS['ChevronLeft']+'</button><button class="mini" data-page="1" title="下一页" aria-label="下一页">'+ICONS['ChevronRight']+'</button></div>'
        if n==34:return strip+foot
        return '<div class="folded">'+dummy.svg(artframe(0,"末页有一枚签印","先揭开封皮",book(RED)))+'<button class="action unseal">揭开封皮</button></div><div class="longfold" hidden>'+strip+'</div>'+foot
    return plane+foot

TIP='<set attributeName="visibility" to="hidden" begin="click" fill="freeze"/>'
LESSON=[
    "先做最小的一块。把答案写在 SVG 的底层，再在上面放一组深色笔画。文字和遮罩占的是同一块地方。",
    "把下面这一行放进遮罩的 g 组。begin 让它等点击，visibility 改这一组的可见性，freeze 让揭开后的状态留下。图不需要为这一步运行网页脚本。",
    "第 04 张换了一种做法，动的是画布高度。展开时请盯着交稿标记，跟着下移，就说明真的多出了一段版面。",
]
def lesson_web():
    return '<aside class="print-example"><h4>这层墨是怎么揭开的？</h4><p>'+ES(LESSON[0])+'</p><pre class="sample-code">'+ES(TIP)+'</pre><p>'+ES(LESSON[1])+'</p><p>'+ES(LESSON[2])+'</p></aside>'
def lesson_print():
    return h("这层墨是怎么揭开的？")+para(LESSON[0])+codeblock(TIP)+para(LESSON[1])+para(LESSON[2])
def merge_config(raw,ids):
    if not isinstance(raw,dict):raise ValueError("Config must be an object.")
    allowed=set(DEFAULT)|{"effects","sources","lesson","guide","install","opening_note"}
    if set(raw)-allowed:raise ValueError("Unknown config fields: "+str(set(raw)-allowed))
    conf={**DEFAULT,**raw};url(conf["repo_url"]);url(conf["gallery_url"])
    for key in ["title","subtitle","author","issue","cover_alt","opening_note"]:
        if key in conf and not isinstance(conf[key],str):raise ValueError(key+" must be text")
    for key in ["cover_lines","intro","outro","guide"]:
        if key in conf and (not isinstance(conf[key],list) or any(not isinstance(x,str) for x in conf[key])):raise ValueError(key+" must be a list of paragraphs")
    if len(conf["cover_lines"])!=2:raise ValueError("Use exactly two short cover lines")
    original=conf.get("effects",list(EFFECTS))
    if not isinstance(original,list) or not original:raise ValueError("Select at least one effect.")
    selected={}
    for obj in original:
        row={"id":obj} if not isinstance(obj,dict) else obj.copy()
        if set(row)-{"id","name","cue","still","terms"}:raise ValueError("Unknown effect field.")
        n=int(row.pop("id"))
        if n not in EFFECTS or n in selected:raise ValueError(f"Unknown or duplicate effect {n}")
        base=EFFECTS[n];entry={"name":base.name,"cue":base.cue,"still":base.still.replace("梦飞AI",conf["author"]),"terms":{},**row}
        if any(not isinstance(entry[k],str) or not entry[k].strip() for k in ['name','cue','still']):raise ValueError("Name, cue and still need text.")
        if not isinstance(entry["terms"],dict) or not all(isinstance(k,str) and isinstance(v,str) and v.strip() for k,v in entry["terms"].items()):raise ValueError("terms must map original text to nonempty text.")
        if entry["terms"] and not {"still","cue"}<=row.keys():raise ValueError("When changing artwork text, also supply a matching cue and static fallback.")
        selected[n]=entry
    if ids:
        missing=set(ids)-set(selected)
        if missing:raise ValueError(f"Missing IDs in this config: {missing}")
        selected={n:selected[n] for n in ids}
    return conf,dict(sorted(selected.items()))

def assemble(conf,entries,art,poster=None):
    author=conf["author"];repo=conf["repo_url"];gallery=conf["gallery_url"].split('#')[0]
    ns=sha256(json.dumps([conf["title"],list(entries)],ensure_ascii=False).encode()).hexdigest()[:10]
    chapters=sorted({group(n) for n in entries})
    first_read=conf["intro"][:1] if 1 in entries else conf["intro"]
    rest=conf["intro"][len(first_read):]
    html=[];wx=[];still=[];md=["# "+conf["title"],"",author,"",*first_read,""]
    intro=''.join('<p class="prose '+('lede' if i==0 else '')+'">'+ES(s)+'</p>' for i,s in enumerate(first_read))
    note=conf.get("opening_note","标为正文试贴的片段仍要在微信草稿中验证；网页手势的正文版是可点击的动作分镜。")
    marginal='<p class="reading-note">'+ES(note)+'</p>'
    if 1 not in entries:intro+=marginal;md.extend([note,""])
    # A real image remains in the printable edition; a rendered cover can carry type for the WeChat body.
    pic=poster or art;image='<img alt="'+ES(conf['cover_alt'])+'" src="'+pic+'" style="display:block;width:100%;max-width:100%;height:auto;margin:0 auto 24px;">'
    opening=('<section style="'+OUTER+'">'+image+para(author+" · FH-014 蜡笔社论",CAPTION)+''.join(para(s) for s in first_read)+(para(note) if 1 not in entries else ""))
    parts={};chapterparts={};web_only=sum(n in GESTURES for n in entries)
    for g in chapters:
        start,title,eng,desc,color=GROUPS[g];chapterid=f"ch{g+1}"
        copy_button=f'<button type="button" class="mini chapter-copy" data-copy="part" data-part="{chapterid}" title="复制本章" aria-label="复制本章">{ICONS["Copy"]}</button>'
        hh=f'<header class="chapter-head">{copy_button}<h2>{g+1:02}　{ES(title)}</h2><p>{ES(desc)}</p></header>'
        html.append('<section id="'+chapterid+'" class="chapter" style="--chapter:'+color+'">'+hh)
        sub=h(f'{g+1:02}　{title}',True)+para(desc);wx.append(sub);still.append(sub);cp=[sub];md+=["## "+title,"",desc,""]
        for n,entry in entries.items():
            if group(n)!=g:continue
            i=f"{n:02}";name=entry["name"];cue=entry["cue"];summary=entry["still"]
            live,printed,_=core(n,ns,entry['terms'],author)
            kind_label=("网页手势 · 正文为分镜" if n in GESTURES else "正文试贴 · 滚动" if n in SCROLL else "正文试贴 · SVG")
            html.append(f'<section id="s{i}" data-n="{n}" data-kind="{kind(n)}" class="effect"><div class="effect-head"><span class="en">{i}</span><h3>{ES(name)}</h3></div><p class="cue">{ES(cue)}</p><div class="work">'+work(n,live,author)+'</div><div class="eff-foot"><span class="channel">'+kind_label+'</span>'+('<button class="mini" data-play title="暂停动画" aria-label="暂停或继续自动动画">'+ICONS["Pause"]+'</button>' if n in range(35,40) else '')+f'<button class="mini" data-copy="part" data-part="{i}" title="复制第 {i} 项正文片段" aria-label="复制第 {i} 项正文片段">{ICONS["Copy"]}</button><button class="mini" data-reset title="从头体验" aria-label="重置第 {i} 张">{ICONS["RotateCcw"]}</button></div></section>')
            head=h(i+"　"+name)
            head+=para(cue if n not in GESTURES else "这张在正文里点播动作分镜。到完整体验页可以亲手玩。"+cue)
            content=head+'<section style="display:block;max-width:540px;margin:0 auto 24px;">'+printed+'</section>'
            if n in (4,5,6):content+=para("交稿标记 · "+author,CAPTION)
            content+=para(summary)
            if n in GESTURES:content+=link("到第 "+i+" 张操作原手势",gallery+"#s"+i)
            fallback=h(i+"　"+name)+para(cue)+para(summary)
            parts[i]='<section style="'+OUTER+'">'+content+'</section>';cp.append(content);wx.append(content);still.append(fallback)
            md+=["### "+i+" "+name,"",cue,"",summary,"",f"[体验这一张]({gallery}#s{i})",""]
            if n==1:
                html.append(''.join('<p class="prose">'+ES(s)+'</p>' for s in rest)+marginal)
                after=''.join(para(s) for s in rest)+para(note);wx.append(after);still.append(after);cp.append(after);md.extend([*rest,note,""])
            if n==1 and conf.get("lesson",True):
                html.append(lesson_web());wx.append(lesson_print());still.append(lesson_print());cp.append(lesson_print())
                md+=["#### 这层墨是怎么揭开的？","",LESSON[0],"","\x60\x60\x60xml",TIP,"\x60\x60\x60","",LESSON[1],"",LESSON[2],""]
        html.append('</section>');chapterparts[chapterid]='<section style="'+OUTER+'">'+''.join(cp)+'</section>'
    parts.update(chapterparts)
    nav=''.join(f'<a data-nav href="#ch{g+1}"><b>{g+1:02}</b> {ES(GROUPS[g][1])}</a>' for g in chapters)+'<a href="#open-source">开源与用法</a>'
    guide=conf.get("guide",["把想用的编号写进配置，分别给读者一句动作提示和一句静态结论。改第 01 张时，可以直接替换那层蜡痕下面的文字。","用下方 Skill 生成预览，复制正文到空白草稿。保存、重开，再用手机点一次。读者必须读到的信息始终留在普通段落里。"])
    ending=conf["outro"]
    sources=conf.get("sources",[])
    for item in sources:
        if set(item)!={"label","url"}:raise ValueError("Sources need a label and URL.")
        url(item["url"])
    install=conf.get("install","把仓库里的 skills/wechat-crayon-interactions 文件夹放进你的 Codex skills 目录，重新打开会话后调用 $wechat-crayon-interactions。也可以单独用 Python 运行脚本。")
    call='用 $wechat-crayon-interactions，把我的提示词对照做成第 01 张遮罩揭晓，给出能复制到公众号的版本和静态答案。'
    cmd="python scripts/press.py --config examples/reveal.json --out my-issue"
    close_head="把一张样纸带回自己的文章"
    close=f'<section class="closing" id="open-source"><div class="eyeline">COLOPHON / OPEN SOURCE</div><h2>{close_head}</h2>'+''.join('<p class="prose">'+ES(s)+'</p>' for s in guide+ending)+f'<p class="source-note"><a class="github" href="{ES(repo)}">{ICONS["Github"]} GitHub · wechat-crayon-interactions {ICONS["ArrowUpRight"]}</a></p><p class="prose">{ES(install)}</p><p class="prose">{ES(call)}</p><p class="prose">在 Skill 文件夹内运行这条命令，会得到自己的第一张样刊。</p><pre class="sample-code">{cmd}</pre><p class="source-note"><a href="{ES(gallery)}">60 项完整体验页</a></p>'+''.join(f'<p class="source-note"><a href="{ES(s["url"])}">{ES(s["label"])}</a></p>' for s in sources)+'<span class="end-mark">'+ES(author)+'</span><a class="backtop" href="#top">回到封面 ↑</a></section>'
    tail=h(close_head,True)+''.join(para(s) for s in guide+ending)+link("开源 Skill",repo)+para(repo,SOURCE)+para(install)+para(call)+para("在 Skill 文件夹内运行")+codeblock(cmd)+link("60 项完整体验页",gallery)+para(gallery,SOURCE)+''.join(link(s['label'],s['url']) for s in sources)+'<section style="'+SIGNBOX+'">'+para(author,SIGN)+'</section></section>'
    md+=["## "+close_head,"",*guide,*ending,"",f"[开源 Skill]({repo})","",install,"",call,"","\x60\x60\x60sh",cmd,"\x60\x60\x60","",f"[60 项完整体验页]({gallery})",""]+[f'[{s["label"]}]({s["url"]})' for s in sources]
    payload={'wx':opening+''.join(wx)+tail,'static':opening+''.join(still)+tail,'parts':parts}
    safe_json=lambda value:json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
    css=(ASSETS/"reader.css").read_text(encoding="utf-8")+'\n'+reader_rules();scripts=(ASSETS/"clipboard.js").read_text(encoding="utf-8")+'\n'+(ASSETS/"reader.js").read_text(encoding="utf-8")
    cover='<header class="cover" style="--art:url('+art+');"><div class="cover-type"><div class="folio">'+ES(author)+' / 手作刊 01</div><h1>'+''.join('<span>'+ES(s)+'</span>' for s in conf['cover_lines'])+'</h1><i class="inkline"></i><p class="dek">'+ES(conf['subtitle'])+'</p><span class="tiny">CRAYON EDITORIAL · FH-014</span></div></header>'
    page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \x27none\x27; img-src data:; style-src \x27unsafe-inline\x27; script-src \x27unsafe-inline\x27; base-uri \x27none\x27; form-action \x27none\x27"><title>'+ES(conf['title'])+'</title><link rel="icon" href="data:,"><style>'+css+'</style></head><body id="top">'
    page+='<header class="top"><div class="wrap bar"><a href="#top" class="imprint"><i class="swatch"></i><span>'+ES(author)+'</span><small>Crayon Editorial</small></a><div class="tools"><button class="mini" id="contents-toggle" aria-label="章节目录" aria-expanded="false" aria-controls="contents-pop" title="章节目录">'+ICONS['List']+'</button><button class="mini" data-copy="static" title="复制静态全文" aria-label="复制静态全文">'+ICONS['FileText']+'</button><button class="tool primary" data-copy="wx">'+ICONS['Copy']+'复制公众号稿</button></div></div><nav hidden class="toc-pop" id="contents-pop">'+nav+'</nav></header>'
    page+='<div class="wrap">'+cover+'<div class="issue-rule"><strong>'+ES(conf['issue'])+'</strong><span>'+str(len(entries))+' 枚样张 · 蜡笔社论</span></div><div class="layout"><aside class="rail"><h2>本期目录</h2>'+nav+'</aside><main class="story">'+intro+''.join(html)+close+'</main></div></div><div hidden id="notice" role="status" class="notice"></div>'
    page+='<script type="application/json" id="print-data">'+safe_json(payload)+'</script><script type="application/json" id="ui-icons">'+safe_json({'play':ICONS['Play'],'pause':ICONS['Pause']})+'</script><script>'+scripts+'</script></body></html>'
    license_text=(ASSETS/'lucide-LICENSE.txt').read_text(encoding='utf-8').replace('--','- -')
    page=page.replace('</head>','<!-- Lucide icon license:\n'+license_text+'\n--></head>',1)
    checklist=f"""发布清单
公众号标题栏：{conf['title']}
本稿 {len(entries)} 项。正文原手势试贴 {len(entries)-web_only} 项；网页手势 {web_only} 项在正文改为可点播的动作分镜。
未通过微信客户端验收。复制的是富文本，不能用无格式粘贴。若长稿保存失败，可逐章、逐项定位。
保存草稿并重新打开，再分别在 iOS 和 Android 微信预览。检查图像接管、点击热区、折叠后正文位置与纵横滑动。
封面如果未被接管，通过素材库手动上传封面图。外链可能被改写，建议把完整体验页填到“阅读原文”，在手机验证可达；未设置前不要宣称已设置。
阅读原文候选：{gallery}
代码和使用说明：{repo}
静态全文保留每项结论，不需要脚本，不含 SVG。未发布到公众号。
"""
    return {"index.html":page,"wechat.html":payload["wx"],"static.html":payload["static"],"article.md":'\n'.join(md).rstrip()+'\n',"publish-checklist.txt":checklist}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--list',action='store_true');ap.add_argument('--vocab',type=int);ap.add_argument('--ids',help="Comma-separated IDs");ap.add_argument('--config',type=Path);ap.add_argument('--out',type=Path);ap.add_argument('--cover',type=Path,default=ASSETS/"cover.jpg");ap.add_argument('--print-cover',type=Path);ap.add_argument('--force',action='store_true')
    a=ap.parse_args()
    try:
        if a.list:
            for n,item in EFFECTS.items():print(f"{n:02} {kind(n):8} {item.name}")
            return
        if a.vocab is not None:
            if a.vocab not in EFFECTS:raise ValueError("ID must be 1..60")
            print(json.dumps(sorted(core(a.vocab)[2]),ensure_ascii=False,indent=2));return
        if not a.out:ap.error("--out is required for a build")
        ids=[int(s) for s in a.ids.split(',')] if a.ids else []
        if len(ids)!=len(set(ids)):raise ValueError("Duplicate ID in --ids")
        raw=json.loads(a.config.read_text(encoding="utf-8-sig")) if a.config else {}
        conf,entries=merge_config(raw,ids);out=assemble(conf,entries,picture(a.cover),picture(a.print_cover) if a.print_cover else None)
        cover_file=a.print_cover or a.cover
        packed=picture(cover_file)
        cover_name="print-cover."+("jpg" if packed.startswith("data:image/jpeg;") else "png")
        for name in ("wechat.html","static.html"):
            out[name]=out[name].replace('src="'+packed+'"','src="'+cover_name+'"')
        if not a.force and any((a.out/name).exists() for name in [*out,cover_name]):raise ValueError("Output exists; choose a new folder or pass --force.")
        a.out.mkdir(parents=True,exist_ok=True)
        for name,body in out.items():(a.out/name).write_text(body,encoding="utf-8")
        (a.out/cover_name).write_bytes(cover_file.read_bytes())
        print(f"{len(entries)} effects; {len(set(entries)&GESTURES)} web gestures with print storyboards. Output: {a.out}")
    except (OSError,ValueError,KeyError,TypeError) as error:ap.exit(2,f"Build failed: {error}\n")

if __name__=="__main__":
    main()

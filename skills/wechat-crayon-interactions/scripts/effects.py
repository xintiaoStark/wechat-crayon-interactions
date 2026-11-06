"""Editable, declarative SVG and native scroll plates. No browser script in these fragments."""
from ink import *
from catalog import GESTURES, SCROLL, EFFECTS

def flow(p,n):
    heights={4:[58,187],5:[58,187],6:[58,118,202]}[n]
    opens=[p.click("o"+str(i)) for i in range(len(heights)-1)]
    close=p.click("close")
    motion=''.join(anim("height",heights[i],h,opens[i],".38s") for i,h in enumerate(heights[1:]))
    if n==5:motion+=anim("height",187,58,close,".38s")
    titles={4:["打开完整提示词","为梦飞AI画一张栏目封面。","给手机读者看，画一只蓝杯。","左侧留白，检查标题是否放得下。"],5:["展开制作笔记","原稿只有“请画个好看的封面”。","改后加了画幅和标题的位置。","收起笔记"],6:["第一折　给谁画？","第二折　构图怎么放？","验收　标题不压住杯子。"]}[n]
    body=motion+wax(7,6,220,41,PINE)+t(20,34,titles[0],18,PAPER)+p.tap("o0",5,2,240,51)
    if n==6:
        body+=group_switch(wax(7,65,234,39,BLUE)+t(17,91,titles[1],17,PAPER)+p.tap("o1",5,60,240,50),opens[0])
        body+=group_switch(t(13,153,"画面右侧放一只杯子。",17)+t(13,182,titles[2],17,RED),opens[1])
    else:
        for i,line in enumerate(titles[1:]):
            body+=t(12,86+i*38,line,17,RED if i==2 else INK)
        if n==5:body+=p.tap("close",4,140,245,44)
    return p.svg(body,heights[0],True)

def first(p,n):
    fire=p.click("go")
    if n==1:
        base=t(42,85,"先说清楚，这张图给谁看。",25,INK,bold=True)+path("M43 103q130 3 265-2","none",RED,3)
        mask=wax(26,37,424,96,PINE,101)+t(238,97,"点开这层绿蜡",27,PAPER,"middle",True)+p.tap("go",22,30,434,116)
        return p.svg(base+group_switch(mask,"",fire,True)+caption("改提示词 · 第一笔","01 / 60"))
    if n==2:
        phrase='<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.28;.7;1" dur="2.8s" begin="'+fire+'" fill="freeze"/>'+t(240,99,"给标题留出一块白。",30,RED,"middle",True)+'</g>'
        return p.svg(place(pencil(GOLD),28,44,.8)+phrase+caption("轻点纸面，读一条批注")+p.tap("go"))
    if n==3:
        body=''
        for i,(word,c) in enumerate(zip(["补上读者","选好画幅","留下标题位"],[PINE,BLUE,RED])):
            y=14+i*50
            body+=t(65,y+27,word,22,INK,bold=True)+group_switch(wax(31,y,365-24*i,38,c,15+i)+t(49,y+26,f"0{i+1}",18,PAPER),"",fire+f"+{.12+i*.34:.2f}s",True)
        return p.svg(body+caption("一次揭开三条改稿意见")+p.tap("go"))
    if n in (4,5,6):return flow(p,n)
    if n==7:
        return p.svg(choice(28,54,132,"A　看校样")+p.tap("go",24,49,140,48)+path("M171 76q42-15 65 4","none",GOLD,3)+group_switch(t(248,75,"B　编者注",24,RED,bold=True)+t(248,111,"标题左边留白。",18),fire)+caption("点左边，批注写在右边"))
    if n==8:
        body=''
        for i,(l,r,c) in enumerate(zip(["纸","笔","印章"],["先定画幅","再选线条","最后落款"],[PINE,RED,BLUE])):
            x=21+154*i;k="s"+str(i)
            body+=choice(x,42,125,l,c)+p.tap(k,x,40,125,43)+group_switch(t(x+62,125,r,20,c,"middle"),p.click(k))
        return p.svg(body+caption("每一枚热点都可以单独打开"))
    if n==9:
        base=artframe(0,"一张封面的出处","打开纸上编者注",book())+p.tap("open")
        modal=box(10,9,460,170,"#eaf1e7")+wax(31,29,165,8,RED)+t(38,80,"编者注",30,INK,bold=True)+t(38,122,"这幅校样只用三种印色。",23)+t(420,49,"关闭",18,RED,"middle")+p.tap("x",380,15,80,57)
        return p.svg(base+group_switch(modal,p.click("open"),p.click("x")))
    if n==10:
        front='<g>'+transform("translate","0 0;0 -210",fire,".8s",'restart="never"')+wax(12,11,454,165,PINE)+t(240,100,"揭开首印封皮",31,PAPER,"middle",True)+p.tap("go")+'</g>'
        return p.svg(artframe(1,"朱红校样","掀开封皮以后",proof(RED))+front)
    if n in (11,12,13):
        sequence={11:[0,2],12:[0,1,2],13:[0,1,2,1]}[n]
        frames=[]
        for i,v in enumerate(sequence):
            title=["A　铅笔稿","B　双色稿","C　套色稿"][v]
            art=artframe(v,title,["轮廓先行","补上色块","对准套印线"][v],proof([PINE,RED,BLUE][v],v))+caption(["点图换一张","翻到下一张","继续翻页"][n-11],f"{i+1:02} / {len(sequence):02}")
            edges=[] if n==12 and i==len(sequence)-1 else [(ALL,(i+1)%len(sequence))]
            frames.append((art,edges))
        return p.machine(frames)
    if n in (14,19,20):
        tabs={14:["任务","素材","交付"],19:["松绿","朱红","钴蓝"],20:["主笔","插画","校对"]}[n]
        text={14:["给手机读者看","一只杯子的线稿","横幅留出标题位"],19:["第一种印色","第二种印色","第三种印色"],20:["先写一份简报","把概念画出来","拿样张逐项核对"]}[n]
        frames=[]
        for i in range(3):
            c=PALETTE[i];motif=(proof(c) if n==19 else [book(c),pencil(c),proof(c)][i])
            body=place(motif,40,52,.98)+t(174,110,text[i],24,c,bold=True)
            edges=[]
            for j,tab in enumerate(tabs):
                x=27+j*145;body+=choice(x,10,127,tab,PALETTE[j] if i==j else "#57625a")
                edges.append(((x,7,130,45),j))
            frames.append((body,edges))
        return p.machine(frames)
    if n==15:
        sheet=box(0,0,448,167,"#e6efea")+place(book(),24,23,1.05)+t(155,69,"资料笺",30,PINE,bold=True)+t(155,103,"画一只蓝色搪瓷杯。",20)+t(155,141,"推回纸笺",17,RED)+p.tap("close",0,0,448,167)
        # The tab remains inside the canvas when the sheet is parked off to the right.
        drawer='<g transform="translate(421 8)">'+anim_transform_pair(p,"421 8","23 8","open","close")+sheet+choice(0,14,52,"拉",RED)+p.tap("open",0,10,54,48)+'</g>'
        return p.svg(artframe(1,"底稿","右端有一只纸舌",mug())+drawer)
    if n==16:
        frames=[]
        for i,(head,sub) in enumerate([("正面 · 主题","给公众号画一张题图"),("背面 · 提示词","只画一只蓝杯子")]):
            content=artframe(i,head,sub,[book(),mug(BLUE)][i])+caption("点纸签翻面")
            frames.append((wrap(transform("scale",".06 1;1 1",p.click(f"t{1-i}z0"),".35s")+content),[(ALL,1-i)]))
        return p.machine(frames)
    if n==17:
        return p.machine([(place(mug(BLUE),37,28,1.22)+t(220,95,"看杯沿细节",26)+caption("点画面放大"),[(ALL,1)]),(place(mug(BLUE),25,-32,3.0)+t(303,115,"局部 × 2.5",18,RED)+caption("再点还原"),[(ALL,0)])])
    if n==18:
        body=''
        for i,(name,c) in enumerate(zip(["纸样","线条","落款"],PALETTE)):
            x=26+151*i;k="c"+str(i)
            body+=wax(x,43,120,82,"#9ba69f")+group_switch(wax(x,43,120,82,c),p.click(k))+t(x+60,92,name,22,PAPER,"middle",True)+p.tap(k,x,40,120,90)
        return p.svg(body+caption("点哪一块，就给哪一块着色"))
    raise ValueError(n)

def anim_transform_pair(p,a,b,open_key,close_key):
    return transform("translate",a+";"+b,p.click(open_key),".5s")+transform("translate",b+";"+a,p.click(close_key),".5s")

def scrolling(p,n):
    frames=[p.svg(artframe(i,h,s,proof(PALETTE[i],i))+caption("梦飞AI · 试印",f"0{i+1} / 03")) for i,(h,s) in enumerate([("先画线稿","把对象和画幅定下来"),("再套印色","让主图更容易辨认"),("装订成册","留出题名的位置")])]
    if n==22:
        return '<section tabindex="0" style="display:block;max-height:178px;overflow-y:auto;overscroll-behavior-y:contain;">'+''.join(frames)+'</section>'
    if n in (21,23):
        w=300
        snap=";scroll-snap-type:x mandatory" if n==23 else ""
        return '<section tabindex="0" style="max-width:100%;overflow-x:auto'+snap+';"><section style="display:flex;width:900px;min-width:900px;">'+''.join('<section style="width:300px;min-width:300px;scroll-snap-align:start;">'+frame+'</section>' for frame in frames)+'</section></section>'
    if n==24:
        base=p.svg(place(mug(PINE),140,18,1.6)+caption("杯子不动，描图纸在走"))
        layers=[]
        for i in range(3):
            art=path(f"M20 92Q90 {12+22*i} 160 92T305 84","none",PALETTE[i],8)+t(34,149,f"描图纸 0{i+1}",18,PALETTE[i])
            layers.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 190" style="display:block;width:330px;min-width:330px;height:100%;">'+art+'</svg>')
        return '<section style="position:relative;">'+base+'<section tabindex="0" style="position:absolute;inset:0;overflow-x:auto;"><section style="display:flex;width:990px;min-width:990px;height:100%;">'+''.join(layers)+'</section></section></section>'
    track='<section tabindex="0" style="overflow-x:auto;"><section style="display:flex;width:900px;min-width:900px;">'+''.join('<section style="width:300px;min-width:300px;">'+a+'</section>' for a in frames)+'</section></section>'
    return '<section style="position:relative;">'+track+'<section style="position:absolute;left:14%;top:10%;width:72%;height:77%;box-sizing:border-box;border:4px solid #b8492e;pointer-events:none;"></section></section>'

def opacity_loop(i,total,seconds):
    values=['1' if j==i else '0' for j in range(total)]
    return '<animate attributeName="opacity" values="'+';'.join(values+[values[0]])+'" keyTimes="'+';'.join(f'{j/total:.4f}'.rstrip('0').rstrip('.') or '0' for j in range(total+1))+'" calcMode="discrete" dur="'+str(seconds)+'s" repeatCount="indefinite"/>'

def motion(p,n):
    go=p.click("run")
    if n==35:
        b=''.join('<g opacity="'+str(int(i==0))+'">'+opacity_loop(i,3,6)+artframe(i,["线稿版","双色版","终印版"][i],"封面轮换",proof(PALETTE[i],i))+'</g>' for i in range(3))
        return p.svg(b+caption("三张校样，每张停两秒"))
    if n==36:
        parts=[wax(50,37,340,86,"#e1eadf"),place(proof(PINE),60,22,1.2),t(218,89,"校样入册",29,RED,bold=True)]
        b=''.join('<g opacity="0">'+attrset("opacity",0,go)+anim("opacity",0,1,f"{i*.65:.2f}s;{go}+{i*.65:.2f}s",".45s")+s+'</g>' for i,s in enumerate(parts))
        return p.svg(b+caption("底色、主图、签印依次入场","轻点重播")+p.tap("run"))
    if n==37:
        b=''.join('<g visibility="hidden">'+attrset("visibility","hidden",go)+attrset("visibility","visible",f"{i*.18+.15:.2f}s;{go}+{i*.18+.15:.2f}s")+t(34+i*31,98,char,28,INK,bold=True)+'</g>' for i,char in enumerate("把提示词写给一个具体的人。"))
        return p.svg(b+caption("文字预先写好，逐字显现","轻点重播")+p.tap("run"))
    if n==38:
        lines=[("给封面留一块白。",RED,75,7),("把动词写具体。",PINE,130,9)]
        return p.svg(''.join('<g>'+transform("translate","490 0;-290 0","0s",f"{sec}s",'repeatCount="indefinite"')+t(0,y,s,26,c)+'</g>' for s,c,y,sec in lines)+caption("校对眉批 · 两条跑道"))
    if n==39:
        body=''
        for i,(typ,vals) in enumerate([("translate","-11 0;11 0;-11 0"),("rotate","-18;20;-18"),("scale",".8;1.15;.8")]):
            body+=wrap(wrap(transform(typ,vals,"0s","2.6s",'repeatCount="indefinite"')+place(pencil(PALETTE[i]),-43,-43,.88)),f"translate({82+i*154} 83)")
            body+=t(82+i*154,158,["位移","旋转","缩放"][i],18,INK,"middle")
        return p.svg(body)
    if n==40:
        b=artframe(0,"套色完成","两种揭幕",book(GOLD))
        b+='<rect x="12" y="16" width="215" height="134" fill="'+PINE+'">'+anim("height",134,0,p.click("roll"),"1s")+'</rect>'
        for i in range(5):
            b+=f'<rect x="{240+i*43}" y="16" width="43" height="134" fill="{BLUE if i%2 else PLUM}">'+anim("height",134,0,p.click("shutter")+f"+{i*.12:.2f}s",".55s")+'</rect>'
        return p.svg(b+t(119,177,"点左侧卷起",17,PINE,"middle")+t(348,177,"点右侧百叶",17,BLUE,"middle")+p.tap("roll",0,0,230,190)+p.tap("shutter",235,0,245,190))
    if n in (41,59):
        d="M38 126Q76 140 112 88T195 99Q235 128 274 67T369 79Q401 98 438 52"
        return p.svg(path(d,"none","#c6d0c8",3)+'<path d="'+d+'" fill="none" stroke="'+PINE+'" stroke-width="6" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="100">'+anim("stroke-dashoffset",100,0,go,"1.5s",'restart="always"')+'</path>'+caption("再点就从起笔重来" if n==59 else "点纸面，把路线描出来")+p.tap("run"))
    if n==42:
        b=path("M71 82q150-8 339 0","none","#b9c5ba",5)
        for i,w in enumerate(("构思","生成","校对")):
            x=77+i*163
            b+=circle(x,81,30,"#a7b6ab")+group_switch(circle(x,81,30,PALETTE[i]),go+f"+{i*.48:.2f}s")+t(x,89,i+1,24,PAPER,"middle",True)+t(x,147,w,20,INK,"middle")
        return p.svg(b+p.tap("run"))
    if n==43:
        b=''
        for i,v in enumerate([3,5,8]):
            c=PALETTE[i];x=42+i*61;y=46+i*32
            b+=f'<rect x="{x}" y="140" width="35" height="0" fill="{c}">'+anim("height",0,v*12,go)+anim("y",140,140-v*12,go)+'</rect>'+t(x+17,162,v,17,c,"middle")
            b+=f'<rect x="242" y="{y}" width="0" height="18" fill="{c}">'+anim("width",0,v*20,go)+'</rect>'+t(427,y+15,v,17,c)
        return p.svg(b+caption("点图开印 · 示意值")+p.tap("run"))
    if n==44:
        b=circle(102,86,52,"none",'stroke="#d4dccf" stroke-width="11"')+'<circle cx="102" cy="86" r="52" fill="none" stroke="'+PINE+'" stroke-width="11" pathLength="100" transform="rotate(-90 102 86)" stroke-dasharray="100 100" stroke-dashoffset="100">'+anim("stroke-dashoffset",100,25,go,"1s")+'</circle>'+t(102,94,"75%",25,PINE,"middle",True)
        b+=box(200,79,218,15,"#d4dccf")+'<rect x="200" y="79" width="0" height="15" fill="'+RED+'">'+anim("width",0,163.5,go,"1s")+'</rect>'+t(200,125,"同一份进度",18)
        return p.svg(b+caption("点纸面，两把尺同时走")+p.tap("run"))
    if n==45:
        digits=''.join(t(100,55+i*72,str(v).zfill(2),50,PAPER,"middle",True) for i,v in enumerate([0,6,12,18,24]))
        b=wax(46,44,204,75,PINE)+'<svg x="48" y="46" width="200" height="72" viewBox="0 0 200 72" overflow="hidden"><g>'+transform("translate","0 0;0 -72;0 -144;0 -216;0 -288",go,"1.2s")+digits+'</g></svg>'+t(277,95,"张校样",24,INK)
        return p.svg(b+caption("点数字表，从 00 数到 24")+p.tap("run"))
    if n==46:
        b=''
        for i,word in enumerate(["铅稿","落线","底色","套印","校色","装订"]):
            show=go+(f"+{i*.32:.2f}s" if i else "")
            off=go+f"+{(i+1)*.32:.2f}s" if i<5 else go
            b+=group_switch(box(12,14,456,144,PAPER)+artframe(i,word,f"FRAME 0{i+1}",proof(PALETTE[i%5],min(2,i//2))),show,off,initial=i==0)
        return p.svg(b+caption("轻点播放六帧试印")+p.tap("run"))
    raise ValueError(n)

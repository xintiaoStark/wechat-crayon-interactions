"""Pointer-driven plates have a clearly labelled click-to-play print counterpart."""
from ink import *
from catalog import EFFECTS

def vista(p,xshift="",moving=False):
    out=''
    layers=[("M-80 115L46 49l87 44 93-62 147 77 94-63 108 82v65H-80Z","#d2ded4"),
        ("M-90 151L43 102l85 9 97-47 152 71 82-27 116 39v45H-90Z","#93b3a8"),
        ("M-90 175l140-48 98 24 120-45 144 46 150-39v79H-90Z",PINE)]
    for i,(d,c) in enumerate(layers):
        animline=transform("translate",f"0 0;{-16*(i+1)} 0;0 0",p.click("play"),"1.6s") if moving else ""
        out+=f'<g id="{p.key("layer"+str(i))}">{animline}'+path(d,c,c,1)+'</g>'
    return out

def gesture_art(p,n):
    """Return live-layer art plus an independent declarative motion sample."""
    cue=EFFECTS[n].cue
    if n==26:
        return vista(p),vista(p,moving=True)
    if n==27:
        arts=[garment(PALETTE[i],i) for i in range(3)]
        labels=["松绿工装","朱红围裙","钴蓝外套"]
    elif n==28:
        base=place(proof(PINE,0),155,7,1.75)
        overlay=place(proof(RED,2),155,7,1.75)
        # An SVG viewport clips the coloured proof instead of covering it with a fake divider.
        def wipe(animate):
            return base+f'<svg id="{p.key("wipe")}" x="0" y="0" width="240" height="190" overflow="hidden">'+(anim("width",20,460,p.click("play"),"1.4s") if animate else "")+overlay+'</svg>'
        return wipe(False),wipe(True)
    elif n==54:
        wheel=''
        for i in range(8):
            wheel+=wrap(path("M0 0L0 -61A61 61 0 0 1 43.13 -43.13Z",PALETTE[i%5],PAPER,2),f"rotate({45*i})")
        body=wrap(f'<g id="{p.key("wheel")}">{wheel}</g>',"translate(150 90)")+path("M139 17l11 15 11-15Z",INK,INK,1)+t(255,90,"校色转盘",26,INK,bold=True)
        acted=wrap(wrap(transform("rotate","0;675",p.click("play"),"1.6s")+wheel),"translate(150 90)")+path("M139 17l11 15 11-15Z",INK,INK,1)+t(255,90,"校色转盘",26,INK,bold=True)
        return body,acted
    else:
        labels={29:["校样批注","请给标题留白"],30:["轮廓稿","双色稿"],31:["铅笔稿","彩色稿"],32:["描线","铺色","套印","校色","打样","装订"],33:["长按取签","减一行","留一块白","换一个动词"],34:["第一张","第二张","校色编号 02"],58:["签印未到位","已经解锁","终稿打开了"],60:["首印封皮","第二页","最后一页","给自己的稿留一块白。"]}[n]
        arts=[(proof(PALETTE[i%5],min(i,2)) if n in (30,31,32,34) else pencil(PALETTE[i%5]) if n==33 else book(PALETTE[i%5])) for i in range(len(labels))]
    live=''; reel=''
    for i,(art,label) in enumerate(zip(arts,labels)):
        panel=place(art,38,22,1.22)+t(190,90,label,23,INK,bold=True)
        live+=f'<g id="{p.key("frame"+str(i))}" visibility="{"visible" if i==0 else "hidden"}">{panel}</g>'
        sel=p.click("play")
        # The motion storyboard intentionally never pretends to accept a long press or drag.
        show=(sel+f"+{i*.53:.2f}s") if i else sel
        off=sel+f"+{(i+1)*.53:.2f}s" if i+1<len(labels) else sel
        if n==31 and i==0:show+=';'+sel+'+1.06s'
        if n==31 and i==1:off+=';'+sel+'+1.06s'
        reel+=f'<g visibility="{"visible" if i==0 else "hidden"}">'+attrset("visibility","visible",show)+attrset("visibility","hidden",off)+panel+'</g>'
    return live,reel

def gesture(p,n):
    live,reel=gesture_art(p,n)
    picture=p.svg(live)
    preview=p.svg(reel+caption("点纸面播放动作分镜","原手势在网页版")+p.tap("play"))
    return picture,preview

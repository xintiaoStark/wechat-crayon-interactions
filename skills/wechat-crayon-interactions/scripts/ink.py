"""Small, deterministic drawing primitives for offline, script-free article plates."""
from html import escape
from random import Random
from contextvars import ContextVar

WORDS = ContextVar("words", default={})
VOCAB = ContextVar("vocab", default=None)
AUTHOR = ContextVar("author", default="梦飞AI")

PINE, RED, BLUE, GOLD, PLUM = "#195f47", "#b8492e", "#315f98", "#ce9335", "#77608b"
INK, PAPER, GRAY = "#272b28", "#fffef9", "#69736b"
PALETTE = [PINE, RED, BLUE, GOLD, PLUM]
SERIF = "Georgia,'Songti SC','Noto Serif CJK SC',SimSun,serif"
SANS = "'PingFang SC','Microsoft YaHei',sans-serif"

def t(x,y,value,size=22,color=INK,anchor="start",bold=False):
    value=str(value)
    if VOCAB.get() is not None:
        VOCAB.get().add(value)
    value=WORDS.get().get(value,value.replace("梦飞AI",AUTHOR.get()))
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{SERIF}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(str(value))}</text>'

def path(d,fill="none",stroke=INK,width=2,extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def box(x,y,w,h,color,extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'

def circle(x,y,r,color,extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'

def wrap(body,transform=""):
    return f'<g transform="{transform}">{body}</g>' if transform else "<g>"+body+"</g>"

def wax(x,y,w,h,color,seed=0):
    """A broken edge and sparse parallel flecks give the screen ink a paper tooth."""
    rng=Random(seed+int(w)*3+int(x))
    steps=min(31,max(9,int(w/10)))
    top=[(x+i*w/steps, y+rng.uniform(-2.5,2.5)) for i in range(steps+1)]
    bottom=[(x+i*w/steps, y+h+rng.uniform(-2.5,2.5)) for i in reversed(range(steps+1))]
    right=[(x+w+rng.uniform(-4,2),y+h*i/6) for i in range(1,6)]
    left=[(x+rng.uniform(-2,4),y+h*i/6) for i in reversed(range(1,6))]
    body=f'<path d="M'+" L".join(f"{a:.0f} {b:.0f}" for a,b in top+right+bottom+left)+f' Z" fill="{color}"/>'
    strokes=[]
    for _ in range(max(5,min(210,int(w*h/84)))):
        a=x+rng.uniform(1,max(3,w-9)); b=y+rng.uniform(2,max(3,h-1))
        length=rng.choice([2,2,3,4,6,9,12]);rise=min(int(b-y),max(1,int(length*.78)))
        strokes.append(f"M{a:.0f} {b:.0f}l{length}-{rise}")
    return body+f'<path d="{"".join(strokes)}" fill="none" stroke="#fffef9" stroke-opacity=".57" stroke-width="1.15"/>'

def mug(color=PINE):
    return (path("M70 37Q99 30 94 52Q89 68 69 66","none",color,8)+
        path("M17 28Q46 22 75 29L70 76Q44 92 20 74Z",color,INK,2.8)+
        path("M18 29Q44 18 75 28Q49 38 18 29Z","#efe3c8",INK,2)+
        path("M24 42l5-4m-4 15 9-10m-6 18 11-13m-2 19 9-12m-2 15 9-12m3 8 6-9","none",PAPER,2)+
        path("M27 15q-9-9-2-14m15 11q-6-7 0-12","none",GRAY,2)+
        path("M7 90q34 6 76-2","none",INK,1.4))

def pencil(color=RED):
    return (path("M9 76L69 13l13 13-62 62-17 5Z",color,INK,2.5)+
        path("M9 76l11 12-17 5Z","#e7c797",INK,1.5)+path("M4 87l5 4-7 3Z",INK,INK,1)+
        path("M22 74l48-51m-44 56 47-50","none",PAPER,2)+
        path("M68 14l4-5q7-3 15 9l-5 8Z",GOLD,INK,2))

def book(color=BLUE):
    return (path("M6 23Q25 15 49 26Q75 12 94 17l-4 59Q72 72 50 85Q28 73 6 80Z",PAPER,INK,2.6)+
        path("M9 26Q28 20 49 29l1 49Q32 66 10 71Z",color,color,1)+
        path("M50 29Q74 17 91 20l-4 51q-18-2-37 9Z","#f1e4c2",INK,1.3)+
        path("M18 36l18-2m-19 10 22-2m-20 11 15-1m23-13 22-5m-23 14 18-4m-19 13 24-6","none",PAPER,2.2)+
        path("M61 37l18-4m-19 13 16-3m-16 13 22-5","none",INK,1.6))

def proof(color=PINE,mode=2):
    return (path("M9 6L89 9L86 91L8 88Z",PAPER,INK,2.5)+
        path("M17 20l48 1m-49 5 36 1","none",INK,1.8)+
        path("M16 66l23-31 16 21 12-14 13 25Z",color if mode else "none",color,2.5)+
        circle(70,32,5,GOLD if mode>1 else PAPER,'stroke="#897348" stroke-width="1.5"')+
        path("M18 75l56 1m-55 6 37 1","none",INK,1.5)+
        path("M26 59l8-12m0 12 6-9m8 11 4-6","none",PAPER,1.7))

def garment(color=PINE,look=0):
    body=(circle(50,16,12,"#e8c5a7",'stroke="#37362c" stroke-width="2"')+
        path("M37 14q3-20 23-9l4 9-12-5-15 6Z",INK,INK,1)+
        path("M36 32l-13 9-11 27 13 6 11-20-1 24h30l-2-23 11 20 14-7-11-29-14-8Z",color,INK,2)+
        path("M35 77l-3 25h14l5-19 4 19h15l-6-25Z","#587385",INK,2))
    return body+(path("M35 39l16 11 14-13m-23 12-3 18m13-16 5 18","none",PAPER,2) if look==0 else path("M41 37l3 15h14l2-17m-19 20h22v19H39Z",PAPER,INK,1.5) if look==1 else path("M35 45l29 2m-30 6 30 2m-29 6 29 2","none",PAPER,2))

def place(art,x,y,scale=1):
    return wrap(art,f"translate({x} {y}) scale({scale})")

def caption(left,right="",color=PINE):
    return t(25,178,left,16,color)+t(452,178,right,14,GRAY,"end")

def choice(x,y,w,label,color=PINE):
    return wax(x,y,w,37,color)+t(x+w/2,y+25,label,18,PAPER,"middle",True)

def artframe(i,title,detail="",motif=None):
    colors=[PINE,RED,BLUE,PLUM,GOLD]; c=colors[i%len(colors)]
    art=motif if motif is not None else [proof(c,i%3),book(c),mug(c),pencil(c)][i%4]
    return place(art,26,30,1.1)+t(173,75,title,27,INK,bold=True)+t(174,113,detail,18,c)

def attrset(name,to,begin):
    return f'<set attributeName="{name}" to="{to}" begin="{begin}" fill="freeze"/>'

def group_switch(body,on,off="",initial=False):
    return f'<g visibility="{"visible" if initial else "hidden"}">'+(attrset("visibility","visible",on) if on else "")+(attrset("visibility","hidden",off) if off else "")+body+'</g>'

def anim(name,start,end,begin,dur=".65s",extra=""):
    return f'<animate attributeName="{name}" from="{start}" to="{end}" begin="{begin}" dur="{dur}" fill="freeze" {extra}/>'

def transform(kind,values,begin,dur=".65s",repeat=""):
    return f'<animateTransform attributeName="transform" type="{kind}" values="{values}" begin="{begin}" dur="{dur}" fill="freeze" {repeat}/>'

class Plate:
    def __init__(self,n,namespace):
        self.n=n
        self.prefix=f"w{namespace}n{n}k"
    def key(self,key):
        return self.prefix+str(key)
    def click(self,key):
        return self.key(key)+".click"
    def tap(self,key,x=0,y=0,w=480,h=190):
        return box(x,y,w,h,"#000",f'fill-opacity="0" pointer-events="visiblePainted" id="{self.key(key)}"')
    def svg(self,body,h=190,flow=False):
        geometry=f'width="100%" height="{h}"' if flow else f'width="100%" viewBox="0 0 480 {h}"'
        marks='' if flow else path("M8 17V8h10m444 0h10v9M8 173v9h10m444 0h10v-9","none","#b6c0b4",1.2)
        return f'<svg xmlns="http://www.w3.org/2000/svg" {geometry} style="display:block;width:100%;height:auto;overflow:hidden;background:{PAPER};font-family:{SANS};">'+box(0,0,"100%","100%",PAPER)+marks+body+'</svg>'
    def machine(self,frames):
        # One visible group at a time. Hidden controls cannot intercept the active group's clicks.
        enter=[[] for _ in frames]; leave=[[] for _ in frames]; parts=[]
        for i,(_,edges) in enumerate(frames):
            for j,(region,target) in enumerate(edges):
                if target==i: continue
                trigger=self.click(f"t{i}z{j}")
                enter[target].append(trigger);leave[i].append(trigger)
        for i,(content,edges) in enumerate(frames):
            switches=(attrset("visibility","visible",";".join(enter[i])) if enter[i] else "")+(attrset("visibility","hidden",";".join(leave[i])) if leave[i] else "")
            taps=''.join(self.tap(f"t{i}z{j}",*region) for j,(region,_) in enumerate(edges))
            parts.append(f'<g visibility="{"visible" if i==0 else "hidden"}">{switches}{content}{taps}</g>')
        return self.svg(''.join(parts))

ALL = (0,0,480,190)

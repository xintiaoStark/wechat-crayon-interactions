"""Finite-state quizzes and paper toys rendered without JavaScript."""
from ink import *

def decisions(p,n):
    if n==47:
        b=''
        for i,(label,reply) in enumerate([("画得漂亮","还缺可验收的要求"),("左侧留白","能用样张核对")]):
            x=25+228*i;k="a"+str(i)
            b+=choice(x,44,201,label,PALETTE[i])+group_switch(t(x+100,128,reply,18,INK,"middle"),p.click(k))+p.tap(k,x,40,201,49)
        return p.svg(b+caption("两个选项都能看反馈"))
    if n==48:
        b=t(32,48,"哪条要求能验收？",25,INK,bold=True)+choice(29,67,196,"感觉高级",RED)+choice(251,67,196,"左侧留白",PINE)
        b+=group_switch(t(39,149,"再试一次。高级没有固定尺度。",21,RED),p.click("a"),p.click("b"))
        b+=group_switch(t(39,149,"对。把标题放上去就能核对。",21,PINE),p.click("b"),p.click("a"))
        return p.svg(b+p.tap("a",29,66,196,42)+p.tap("b",251,66,196,42))
    if n==49:
        b=t(269,63,"找双线印记",24,INK,bold=True); wrong=[]
        for i in range(9):
            x=30+(i%3)*66;y=12+(i//3)*55;k="cell"+str(i)
            b+=box(x,y,52,43,"#e3ebdf")+path(f"M{x+12} {y+32}l24-20","none",PINE,4)
            if i==5:b+=path(f"M{x+20} {y+35}l22-19","none",RED,4)
            else:wrong.append(p.click(k))
            b+=p.tap(k,x,y,52,43)
        fail=";".join(wrong);win=p.click("cell5")
        return p.svg(b+group_switch(t(269,109,"对，是这一枚。",20,PINE),win,fail)+group_switch(t(269,109,"再看一眼线数。",20,RED),fail,win))
    if n==50:
        qs=[("先写哪件事？","读者是谁","字体多大",0),("哪一句定义画幅？","很有气势","横向三比二",1),("哪一句可以核对？","标题不压主图","特别好看",0)]
        frames=[]
        for i,(question,a,b,correct) in enumerate(qs):
            for retry in (False,True):
                prompt=t(28,49,question,25,INK,bold=True)+choice(25,72,201,a,PINE)+choice(251,72,201,b,BLUE)+caption("再选一次" if retry else f"简报小测 · 第 {i+1} 题",f"0{i+1} / 03",RED if retry else PINE)
                targets=[2*(i+1) if j==correct else i*2+1 for j in (0,1)]
                frames.append((prompt,[((25,69,201,47),targets[0]),((251,69,201,47),targets[1])]))
        frames.append((artframe(2,"简报已齐","读者、画幅和验收都有了",book(PINE))+caption("三题完成"),[]))
        return p.machine(frames)
    if n==51:
        def fork(h,a,b,target):
            return (t(26,54,h,25,INK,bold=True)+choice(25,81,201,a,PINE)+choice(251,81,201,b,BLUE),[((25,77,201,49),target[0]),((251,77,201,49),target[1])])
        frames=[fork("这份稿先从哪里做起？","写文字","做图像",(1,2)),fork("文字交给谁？","新读者","老读者",(3,4)),fork("图画放哪里？","封面","内页",(5,6))]
        for i,word in enumerate(["入门短笺","进阶批注","封面校样","内页插图"]):
            frames.append((artframe(i,word,"这条路线的交付物",proof(PALETTE[i]))+caption("点纸面另选路线"),[(ALL,0)]))
        return p.machine(frames)
    if n==52:
        order=[2,4,1];frames=[]
        for i,k in enumerate(order):
            body=t(30,49,"签印次序　2 · 4 · 1",25,INK,bold=True)+t(29,161,f"已盖 {i} 枚",18,PINE)
            edges=[]
            for j in range(4):
                x=27+110*j;body+=choice(x,73,89,str(j+1),PALETTE[j])
                edges.append(((x,70,89,46),i+1 if j+1==k else 0))
            frames.append((body,edges))
        return p.machine(frames+[(artframe(2,"签发完成","顺序正确，校样可以入册",book(PINE)),[])])
    if n==53:
        words=["减一行","留一块白","换一个动词"]
        frames=[(artframe(0,"纸盒里有一支签","点盒面开封",book(RED)),[(ALL,1)])]
        for i,word in enumerate(words):
            frames.append((artframe(i,word,"编者签 · 预设次序",pencil(PALETTE[i]))+caption("点纸面再抽一支"),[(ALL,1+(i+1)%3)]))
        return p.machine(frames)
    if n==55:
        words=["补受众","定画幅","删形容词","留题位","对原稿"]
        frames=[]
        for i in range(6):
            title="五张改稿卡" if i==0 else words[i-1]
            frames.append((artframe(i,title,"抽完这一叠" if i==5 else "点纸面取下一张",book(PALETTE[i%5]))+caption(f"已抽 {i} / 5", "本轮结束" if i==5 else ""),[] if i==5 else [(ALL,i+1)]))
        return p.machine(frames)
    if n==56:
        coords=[(54,89),(145,62),(235,112),(330,67),(421,101)]
        b=path("M54 89Q99 42 145 62T235 112Q280 105 330 67T421 101","none","#c2cbbd",3)
        for i,(x,y) in enumerate(coords):
            k="mark"+str(i);b+=circle(x,y,22,"#c4cec4")+group_switch(circle(x,y,22,PALETTE[i])+path(f"M{x-9} {y}l6 7 13-15","none",PAPER,3),p.click(k))+t(x,y+43,["选题","起稿","生成","校色","交付"][i],17,INK,"middle")+p.tap(k,x-27,y-26,54,55)
        return p.svg(b+caption("五站校色地图"))
    if n==57:
        b=''
        for i,label in enumerate(["门页","信封","纸箱"]):
            x=22+i*153;k="flap"+str(i);c=PALETTE[i]
            b+=t(x+65,91,["进编辑室","给未来的稿","终稿入盒"][i],17,c,"middle")
            shape=(path(f"M{x+12} 30h93v88h-93Z",c,INK,2)+circle(x+90,78,4,PAPER) if i==0 else path(f"M{x+3} 47h117v66H{x+3}Z",c,INK,2)+path(f"M{x+3} 48l58 35 59-35","none",PAPER,2) if i==1 else path(f"M{x+5} 52l50-25 64 14-13 72H{x+12}Z",c,INK,2)+path(f"M{x+6} 53l53 17 60-28m-60 28v40","none",PAPER,3))
            b+='<g>'+transform("translate","0 0;0 -36;0 -130",p.click(k),".6s")+shape+'</g>'+t(x+62,160,label,19,c,"middle")+p.tap(k,x,20,133,111)
        return p.svg(b)
    raise ValueError(n)

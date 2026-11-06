# 梦飞AI · 公众号互动排版样刊

梦飞AI

墨迹下面压着一句话。点开第一张，再看看下面那行字有没有移动。

## 掀开这一层

给读者留出猜答案的时间。先看第 01 张和第 04 张，注意它们下面的文字有没有移动。

### 01 遮罩揭晓

点掉绿色蜡痕，看看提示词里常被漏掉的那句话。

先说清楚，这张图给谁看。遮罩消失，后面的段落留在原位。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s01)

这份样刊按动作排成八章。标着正文试贴的效果会生成无脚本片段。标着网页手势的样张，在这里可以直接操作；公众号稿保留动作分镜与网页版入口。
标为正文试贴的片段仍要在微信草稿中验证；网页手势的正文版是可点击的动作分镜。

#### 这层墨是怎么揭开的？

先做最小的一块。把答案写在 SVG 的底层，再在上面放一组深色笔画。文字和遮罩占的是同一块地方。

```xml
<set attributeName="visibility" to="hidden" begin="click" fill="freeze"/>
```

把这行代码放进遮罩的 g 组。begin 让它等点击，visibility 改这一组的可见性，freeze 让揭开后的状态留下。这一步不需要网页脚本。

第 04 张换了一种做法，动的是画布高度。展开时请盯着交稿标记，跟着下移，就说明真的多出了一段版面。

### 02 渐显与渐隐

点纸面，等这句批注浮出来，再看它慢慢淡去。

先用一句话交代用途。短暂出现的批注适合提示，不适合承载唯一的正文。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s02)

### 03 逐条揭晓

点一次封条，三条改稿意见会依次露出来。

改稿顺序依次是补受众、定画幅、留标题位。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s03)

### 04 真正增高展开

点开被折起来的提示词，看画板下面的交稿标记。

短提示词展开成三行，后面的交稿标记被实际推低。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s04)

### 05 展开后收起

点开制作笔记，再点收起，留意后文回到原位。

笔记可以双向折叠。展开能读到完整约束，收起后正文回到原来的高度。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s05)

### 06 多层递进展开

先看任务，再看约束，最后打开验收条件。

三层依次补齐任务、构图约束和验收条件。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s06)

### 07 点 A 显示 B

点左边的校样符号，右边会多一条编者注。

校样 A 对应的批注是给标题留白。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s07)

### 08 多热点独立触发

分别点纸、笔、印章。它们不会替对方作答。

纸定尺寸，笔定线条，印章定落款。每处热点各自揭晓。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s08)

### 09 画布内弹层与关闭

打开编者注，再点注页上的关闭。

注页覆盖本幅校样，关闭后仍在原处，不挡住整篇文章。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s09)

### 10 封面消失与移出

揭开首印封皮，看下面是哪一种印色。

绿色封皮向上退场，露出朱红校样。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s10)

## 给同一张图换个看法

做 AI 生图对照时，两幅画最好在同一位置换。眼睛不用来回找，笔触的差别才看得清。

### 11 A/B 两图切换

点图在草稿和套色稿之间往返。

A 版只有轮廓，B 版在相同构图上套了色。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s11)

### 12 多图逐张切换

顺着试印次序翻完三张样纸。

线稿、双色、成稿依次出现，末张停留。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s12)

### 13 往返或循环切换

反复点画面，留意第三张之后回到哪张。

顺序是第一版、第二版、第三版、第二版，然后回到第一版。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s13)

### 14 标签页切换

在任务、素材、交付三个页签之间任选一个。

任务写给谁看，素材列可用图，交付约定尺寸。页签互斥。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s14)

### 15 抽屉式卡片切换

拉出右边的纸舌，读完再推回去。

资料笺从右侧滑入，收回后重新露出底稿。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s15)

### 16 翻面与翻牌

点纸签，翻到背面的提示词，再翻回来。

正面是主题，背面写着只画一只杯子。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s16)

### 17 点击放大细节

点画上的小窗，看杯沿放大后露出的笔触。

同一只杯子的局部被放大，再点一次恢复全图。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s17)

### 18 局部点亮与着色

给三块校色样分别着色。

三枚色块可独立从铅灰变为松绿、朱红和钴蓝。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s18)

### 19 换色与换肤

点三个墨点，给同一张封面换主色。

构图保持不变，封面可换松绿、朱红或钴蓝。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s19)

### 20 角色或场景选择器

选主笔、插画或校对，看桌上的工具怎样变。

主笔拿手稿，插画用蜡笔，校对拿放大后的样张。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s20)

## 让纸从指下经过

把宽画卷进窄小的手机屏幕。横向图库只需要一个能滚动的窗口，连续擦除则要知道手指停在哪里。

### 21 横向滑动图库

横滑三张同主题校样，比较不同配色。

图库按松绿、朱红、钴蓝排列，三张都能单独阅读。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s21)

### 22 纵向长图滚动窗

在窗口里向上滑，看看下面的第二次、第三次试印。

窗口依次容纳线稿、套色与交稿三个阶段。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s22)

### 23 滑动翻页与连环画

横滑一格再松手，让连环画停在一整页。

三个画格依次是起稿、上色和装订，网页吸附到页边。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s23)

### 24 底图固定、上层滑动

移动前面的描图纸，盯住下面那只杯子。

杯子留在原地，流动的彩色笔画从它上面经过。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s24)

### 25 上层固定、底图移动

把底片滑过固定的取景框。

取景框不动，三幅底稿在它后面经过。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s25)

### 26 双层或三层视差

拖动纸带，比较远山、近坡和前景的移动距离。

三层沿同一方向移动，近景位移最远。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s26)

### 27 滑动变装

拖过三档，让纸模换上三套印色。

同一纸模依次穿松绿工装、朱红围裙和钴蓝外套。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s27)

### 28 滑动擦除与前后对照

拖动分界线，任意停在铅稿与套色稿之间。

两侧画的是同一处。分割线的位置由手指连续控制。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s28)

## 按住，再松手

短点和长按值得分开设计。尤其是松手那一下，要事先决定读者看到的画面是留住还是还原。

### 29 长按显示

按住墨点约半秒，读到藏起来的校样批注。

长按后出现批注，松手保留，短点无效。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s29)

### 30 长按换图

按住底稿，等它换成另一版。

长按后切换到双色稿，松开后新稿仍然保留。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s30)

### 31 长按换图后恢复

按住看彩稿，松开再对照铅稿。

彩稿只在按住时出现，松开还原。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s31)

### 32 长按播放序列

按住让样纸经过六步试印，松开停在当前帧。

松手暂停，再按会从停下的帧继续。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s32)

### 33 长按抽签

长按领取一张改稿签，再长按领取下一张。

三条建议按预设顺序轮换，不涉及概率或领奖。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s33)

### 34 滑动后长按查看

先滑到第二张校样，再长按校色章。

抵达第二张后，长按才露出这张的校色编号。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s34)

## 纸自己动起来

有些过程，读者不必操作也能看懂。每个循环都留一点停顿，手机读者还有正文要读。

### 35 自动轮播

让三幅封面自行轮换，看它在哪一幅停留。

三张封面依次出现，每张留有阅读时间。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s35)

### 36 分幕入场与快闪

看三张套色版按先后顺序落到纸上。

先铺底色，再落主图，末了出现签印。用缓和切换替代快速闪烁。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s36)

### 37 打字机与逐字显现

看编者的一句话逐字写出来。

把提示词写给一个具体的人。字是预先写好的，不是实时模型输出。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s37)

### 38 弹幕与文字跑马灯

看两句校对批注横穿纸面。

两条预设批注以不同速度经过，正文不依赖读者追着看。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s38)

### 39 缩放、旋转与位移

比较三支色笔的位移、旋转和缩放。

松绿笔平移，朱红笔旋转，钴蓝笔放大缩小。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s39)

### 40 卷轴与百叶窗揭幕

点纸张左半边和右半边，分别看卷起和百叶揭幕。

整片卷帘向上收，另一侧的五条百叶依次缩短。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s40)

## 把过程画给人看

介绍 AI 工作流，可以让路径先走、节点再亮。数字用的是示意值，目的是看出先后和比例。

### 41 路径逐步绘出

点铅笔线，让墨迹沿曲线走一遍。

先藏起描边，触发后把路径从起点描到终点。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s41)

### 42 流程节点依次点亮

点第一枚印记，顺着看完 AI 作图的三个环节。

构思、生成、校对依次点亮。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s42)

### 43 柱状与条形增长

点图，同时看竖柱与横条向目标值增长。

两组图显示相同示意值 3、5、8，不代表模型跑分。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s43)

### 44 环形与线性进度

点进度画面，看圆环和纸尺是否停在同一个数。

两种画法都停在示意进度 75%。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s44)

### 45 数字滚动与翻牌

点页数表，看数字轮转到最后一张校样。

计数从 00 滚到 24，是固定目标值，不连接实时数据。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s45)

### 46 序列帧过程演示

点样纸，看六帧怎样把一册小刊印出来。

六幅预画的样张从轮廓一路排到最终成稿。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s46)

## 先让读者做个选择

做提示词小测验时，把反馈写在选项旁边。这里的答案只在这一页显示，不交卷，也不记录读者身份。

### 47 选项点击反馈

分别点两条提示词，各看一句反馈。

具体描述能指定对象；含糊描述只表达偏好。两份反馈可同时保留。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s47)

### 48 单选与判断题

选出可验收的要求，选错可以改。

画面左侧留白可核对；感觉高级没有明确验收尺度。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s48)

### 49 九宫格找答案

九枚印记里，哪枚出现了两道斜线？

正确印记在中间一排最右侧。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s49)

### 50 多题闯关

用三道小题把一份创作简报补齐。

依次选读者、画幅、验收条件。答错留在本题，答对才翻页。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s50)

### 51 分支剧情与路线选择

先选文字或图像，再选一项任务，看看你的终稿。

两层分支通向四份终稿，路线不同，交付物也不同。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s51)

### 52 顺序点选解锁

按样张上的 2、4、1 三次盖印。

顺序正确才显示签发完成，点错从第一枚开始。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s52)

## 留一个小彩蛋

签文、抽牌和盖章用的是预设内容，不涉及中奖或发奖。玩完以后，仍然要让读者拿走一句有用的话。

### 53 点击抽签与盲盒

揭开纸盒，再抽一支编者签。

签文依次是减一行、留一块白、换一个动词。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s53)

### 54 转盘与跑马灯停靠

启动选色盘，再点停下，看看落在哪一格。

转盘启动后可以停靠。本例使用预设停靠次序，不用于抽奖。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s54)

### 55 连续点击抽牌

抽完五张改稿卡，留意末张的提示。

五张依次抽取，不重复，抽完停止。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s55)

### 56 点亮地图与收集徽章

在制版地图上盖齐五枚校色章。

每个地点只保留一枚彩章，重复点击不会重复获得徽章。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s56)

### 57 开门、开信封与开箱

分别打开门页、信封和小纸箱。

三种外形揭出三个不同的小提示，互不干扰。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s57)

### 58 滑动解锁后展开

把签印滑到右端，再打开终稿。

滑到底才解锁按钮，打开后正文增高。这不是安全验证。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s58)

### 59 点击重播与回到初始画面

点一下绘线，中途再点就会从头开始。

重播只重启这段描线，不会重置其他样张。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s59)

### 60 多动作互动长卷

揭封、滑到末页，再长按最后一枚签印。

三个动作按顺序完成，末页才显示梦飞AI的交稿寄语。

[体验这一张](https://xintiaostark.github.io/wechat-crayon-interactions/#s60)

## 把一张样纸带回自己的文章

把想用的编号写进配置，分别给读者一句动作提示和一句静态结论。改第 01 张时，可以直接替换那层蜡痕下面的文字。
用下方 Skill 生成预览，复制正文到空白草稿。保存、重开，再用手机点一次。读者必须读到的信息始终留在普通段落里。
挑一张适合当前段落的，再决定要不要用下一张。若读者没点开，也应当读得到要紧的结论。

[开源 Skill](https://github.com/xintiaoStark/wechat-crayon-interactions)

把仓库里的 skills/wechat-crayon-interactions 文件夹放进你的 Codex skills 目录，重新打开会话后调用 $wechat-crayon-interactions。也可以单独用 Python 运行脚本。

用 $wechat-crayon-interactions，把我的提示词对照做成第 01 张遮罩揭晓，给出能复制到公众号的版本和静态答案。

```sh
python scripts/press.py --config examples/reveal.json --out my-issue
```

[60 项完整体验页](https://xintiaostark.github.io/wechat-crayon-interactions/)

# 纸上有机关 · 梦飞AI的公众号互动排版 Skill

[打开 60 项互动样刊](https://xintiaostark.github.io/wechat-crayon-interactions/) · [Skill 入口](skills/wechat-crayon-interactions/SKILL.md) · [一张可以改字的示例](skills/wechat-crayon-interactions/examples/reveal.json)

给一篇文章加一个值得读者动手的瞬间。比如先猜提示词缺了什么，再点掉绿蜡；或把同一张图的线稿和彩稿放在原处切换。视觉语言取自 FH-014 · Crayon Editorial，作品以纸面、干蜡笔笔触和少量印色组织，无外部字体、CDN、登录或后台依赖。

**60 种在网页版均可操作。不是 60 种均已通过微信验收。**

正文沿用梦飞AI的阅读规格。正文字色 `#3E3E3E`，字号 16px、行高 28px、段后 24px；章节标题 20px 居中、小标题 18px 左齐，均用 `#6A5DF5`；图注和来源 13px、`#888888`。章节标题留白为上 56px、下 28px，小标题为上 40px、下 16px。网页和复制正文使用同一份字级定义，不插入空白段落撑高。封面题字和蜡笔插画使用独立的美术比例。

|数量|实现|复制到公众号的内容|
|---:|---|---|
|43|SVG / SMIL|无脚本试贴片段。包含揭晓、折叠、翻页、流程、图表及有限分支。|
|5|原生滚动与图层|无脚本试贴片段。滚动、吸附和定位在编辑器中可能被改写。|
|12|网页手势|真正的长按、拖动和状态组合在网页版；正文是另做的点播动作分镜及对应编号的链接，不能当作原手势。|

## 安装和使用

下载仓库，将 `skills/wechat-crayon-interactions` 这个**完整文件夹**放进支持本地 Skill 的客户端目录。Codex 常见用户目录为 `~/.codex/skills/`。重新打开会话后可以说：

> 用 $wechat-crayon-interactions，为我的 AI 绘画教程做第 01 张遮罩揭晓和第 11 张 A/B 对照，给出可试贴稿和静态稿。

不安装 Skill 也能直接做。需要 Python 3.10 或更新版本，不用装依赖。在仓库根目录执行：

```sh
cd skills/wechat-crayon-interactions
python scripts/press.py --list
python scripts/press.py --vocab 01
python scripts/press.py --config examples/reveal.json --out my-issue
```

打开 `my-issue/index.html`。整页、单章、单项均可复制；网页程序和工具栏不进入正文。`wechat.html` 是无脚本正文，`static.html` 是不含 SVG 的静态对照，封面 `print-cover.jpg`（或 PNG）与它们放在一起。另有文字稿和发布清单。导出只写指定目录，不替你部署自定义内容。

要生成全部样张，去掉 `--config`。要改成自己的文字、署名和题图，见 [配置说明](skills/wechat-crayon-interactions/references/config.md)。预览使用数据 URI 内嵌图片；微信后台缺图时手动上传封面。外链受账号和客户端影响，真机试过再发布。

## 验证

```sh
python -m unittest discover -s tests
```

测试包含片段中 ID 与事件引用的一致性、60 项编译、脚本边界、定制文案、静态降级和离线输出。公开样刊在 `docs/`，GitHub Pages 使用 main 分支的该目录。

## 版权范围

原创代码、示例文字和仓库内通用插画按 [MIT](LICENSE) 提供。工具栏使用的 Lucide 图标保留其[上游许可](skills/wechat-crayon-interactions/assets/lucide-LICENSE.txt)。通用封面是为本项目生成的蜡笔风插画，未使用原报道的代码或插画。

「梦飞AI」为作者署名，不授予冒用该账号或品牌背书的权利。作者的 IP 原图、IP 专属封面和待发布公众号文章不在此仓库，亦不在本项目许可范围内。

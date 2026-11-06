---
name: wechat-crayon-interactions
description: 把微信公众号文章中的揭晓、对照、展开、滚动、流程图或小测验做成可复用的互动样张，生成蜡笔社论风的网页体验、无脚本公众号试贴稿与静态对照。适用于公众号互动排版和 SVG 教程，不代为登录或发布。
---

# 公众号互动样刊

从一个具体的读者动作开始。答案、资料和下一步都要有普通文字版本。保留作者给的原文、署名与视觉身份；新稿才补写教程内容。示例的梦飞AI署名不是其他作者的默认署名。

1. 用 `python scripts/press.py --list` 查看 60 个编号及机制。在 [机制与边界](references/mechanisms.md) 中区分 SVG、原生滚动和依赖网页手势的效果。不要把动作分镜称为原手势。
2. 从 [单项改字示例](examples/reveal.json) 派生配置。只选文章需要的项；输入段落写在 `intro`、`guide`、`outro`，作者写在 `author`。保留正式结论于 `still`。改作品里的字先运行 `--vocab 01` 查可替换的原词，再把 `terms`、`cue`、`still` 一起改。不要传入可执行 HTML。输入字段见 [配置说明](references/config.md)。
3. 在本技能目录运行 `python scripts/press.py --config examples/reveal.json --out my-issue`。不提供配置会生成完整样刊；自有封面可用 `--cover cover.jpg`。使用新输出目录，仅在明确要重建时加 `--force`。脚本只需 Python 3.10+ 标准库。
4. 打开生成的 `index.html`，逐项操作，检查手机宽度。复制按钮写富文本，从未操作过的初始状态生成片段；不把预览脚本送进正文。交付 `wechat.html`、`static.html`、`article.md` 和发布清单。
5. 只有作者实测了某个草稿、某个客户端，才能为那个组合记录通过。新版本与新账号仍须重新试贴。清单中的公开样刊入口指向本仓库的示例，并不会自动托管作者新改的网页；改了网页专属互动时，提供作者自己实际部署的 `gallery_url`，否则不要把公共样刊描述成自定义内容。

不发布公众号，不上传用户图像，不自动同步第三方编辑器。开源代码与通用插画不含也不授权梦飞AI的 IP 形象。

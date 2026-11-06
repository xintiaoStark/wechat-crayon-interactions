"""One reading profile shared by the browser, rich clipboard and static manuscript."""
FONT="mp-quote,'PingFang SC',system-ui,-apple-system,BlinkMacSystemFont,'Helvetica Neue','Hiragino Sans GB','Microsoft YaHei UI','Microsoft YaHei',Arial,sans-serif"
BRAND="#6A5DF5"
BODY="#3E3E3E"
MUTED="#888888"
MEDIA="#7A81FA"
PAPER="#FFFFFF"
COMMON=f"margin:0 0 24px;padding:0;color:{BODY};font-family:{FONT};font-size:16px;line-height:1.75em;letter-spacing:0;text-align:left;"
OUTER=f"box-sizing:border-box;width:100%;margin:0;padding:0;background:{PAPER};color:{BODY};font-family:{FONT};font-size:16px;line-height:1.75em;letter-spacing:0;text-align:left;word-break:break-word;overflow-wrap:break-word;"
CHAPTER=f"margin:56px 0 28px;padding:0;color:{BRAND};font-family:{FONT};font-size:20px;line-height:1.5;font-weight:700;text-align:center;letter-spacing:0;"
SUBHEAD=f"margin:40px 0 16px;padding:0;color:{BRAND};font-family:{FONT};font-size:18px;line-height:1.6;font-weight:700;text-align:left;letter-spacing:0;"
CAPTION=f"margin:6px 0 24px;padding:0;color:{MUTED};font-family:{FONT};font-size:13px;line-height:1.7;text-align:center;letter-spacing:0;"
SOURCE=f"margin:0;padding:0;color:{MUTED};font-family:{FONT};font-size:13px;line-height:1.7;text-align:center;letter-spacing:0;overflow-wrap:anywhere;"
CODE=f"margin:0;padding:0;color:{BODY};font-family:Consolas,Monaco,monospace;font-size:13px;line-height:1.7;text-align:left;letter-spacing:0;overflow-wrap:anywhere;"
CODEBOX="box-sizing:border-box;margin:0 0 24px;padding:12px 14px;background:#F7F7FA;border:1px solid #E3E3EE;border-left:3px solid #6A5DF5;border-radius:0 6px 6px 0;"
SIGNBOX="margin:38px 0 10px;padding:20px 0 0;border-top:1px solid #DDD9FF;text-align:center;"
SIGN=f"margin:0;padding:0;color:{BRAND};font-family:{FONT};font-size:16px;font-weight:700;line-height:1.6;text-align:center;letter-spacing:0;"

def reader_rules():
    rules=[
        (":root",f"--brand:{BRAND};--body:{BODY};--muted:{MUTED};--media:{MEDIA};--sans:{FONT};"),
        (".story",f"color:{BODY};font-family:{FONT};"),
        (".story .prose,.story .lede,.story .cue,.chapter-head>p,.print-example>p,.closing>p:not(.source-note),.extra-sheet",COMMON),
        (".chapter,.effect,.closing","margin:0;padding:0;border:0;"),
        (".chapter-head","position:relative;display:flow-root;margin:0;padding:0;border:0;"),
        (".chapter h2,.closing h2",CHAPTER),
        (".effect-head","margin:40px 0 16px;gap:8px;"),
        (".effect .en,.effect h3",SUBHEAD+"margin:0;"),
        (".print-example","margin:0;padding:0;background:none;border:none;"),
        (".print-example h4",SUBHEAD),
        (".print-example .sample-code,.closing .sample-code",CODEBOX+CODE.replace("margin:0;padding:0;","")),
        (".story .reading-note",COMMON+"margin:0 0 24px;padding:0 0 0 16px;border-left:3px solid "+BRAND+";"),
        (".channel,.feedback,.eyeline",f"font:13px/1.7 {FONT};color:{MUTED};"),
        (".normal-after",CAPTION),
        (".source-note,.source-note a,.story .github",SOURCE+"color:"+MUTED+";"),
        (".story .source-note","margin:0 0 8px;"),
        (".story .end-mark",SIGN+SIGNBOX+"display:block;"),
        (".eff-foot","margin:6px auto 24px;"),
        (".plate,.pad,.scroll-art","border-bottom-color:"+MEDIA+";"),
        (".chapter-copy","position:absolute;right:0;top:8px;float:none;"),
        (".closing","display:flow-root;"),
        (".closing .eyeline","margin:40px 0 0;text-align:center;display:block;"),
        (".cover h1","color:"+BODY+";"),
        (".cover h1 span:last-child,.cover .folio,.imprint span,.rail a[aria-current]","color:"+BRAND+";"),
        (".cover .dek","color:"+BODY+";"),
        (".tool.primary",f"background:{BRAND};border-color:{BRAND};"),
        (".issue-rule,.cover .tiny",f"color:{MUTED};"),
    ]
    return '\n'.join(selector+'{'+style+'}' for selector,style in rules)

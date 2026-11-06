/* Shared rich-text clipboard transport. Nothing in this file enters the article. */
(function(){
  'use strict';
  function plainText(markup){
    const host=document.createElement('section');host.innerHTML=markup;
    return [...host.querySelectorAll('span[leaf],svg text,img')].map(node=>node.tagName.toLowerCase()==='img'?node.alt:node.textContent.trim()).filter(Boolean).join('\n');
  }
  function nativeCopy(markup,plain){
    const host=document.createElement('section');
    host.style.cssText='position:fixed;left:-12000px;top:0;width:430px;background:#fff;';
    host.contentEditable='true';host.tabIndex=-1;host.innerHTML=markup;
    const selection=window.getSelection(),ranges=[];
    if(selection)for(let i=0;i<selection.rangeCount;i++)ranges.push(selection.getRangeAt(i).cloneRange());
    const active=document.activeElement;let handled=false;
    const listener=event=>{if(!event.clipboardData)return;event.clipboardData.setData('text/html',markup);event.clipboardData.setData('text/plain',plain);event.preventDefault();handled=true;};
    try{
      document.body.append(host);host.focus({preventScroll:true});
      const range=document.createRange();range.selectNodeContents(host);selection.removeAllRanges();selection.addRange(range);
      document.addEventListener('copy',listener,true);
      if(!document.execCommand('copy')||!handled)throw new Error('native rich-text copy was not accepted');
      return 'native-rich-html';
    }finally{
      document.removeEventListener('copy',listener,true);host.remove();
      if(selection){selection.removeAllRanges();ranges.forEach(range=>{try{selection.addRange(range);}catch{}});}
      if(active&&active.isConnected)active.focus({preventScroll:true});
    }
  }
  async function write(markup){
    const plain=plainText(markup);
    try{return nativeCopy(markup,plain);}catch(nativeError){
      if(!navigator.clipboard||!window.ClipboardItem)throw nativeError;
      await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([markup],{type:'text/html'}),'text/plain':new Blob([plain],{type:'text/plain'})})]);
      return 'async-rich-html';
    }
  }
  window.MengfeiClipboard=Object.freeze({write,plainText});
})();

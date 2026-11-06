import json
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

SKILL=Path(__file__).resolve().parents[1]/"skills"/"wechat-crayon-interactions"
sys.path.insert(0,str(SKILL/"scripts"))
import press

class Nodes(HTMLParser):
    def __init__(self,html):
        super().__init__();self.nodes=[];self.words=[]
        self.feed(html);self.close()
    def handle_starttag(self,tag,attrs):
        self.nodes.append((tag,dict(attrs)))
    def handle_data(self,data):self.words.append(data)

class PressTest(unittest.TestCase):
    def test_contracts(self):
        self.assertEqual(len(press.EFFECTS),60)
        self.assertEqual([sum(press.kind(n)==k for n in press.EFFECTS) for k in ('svg','scroll','gesture')],[43,5,12])
        ids=set()
        for n in press.EFFECTS:
            with self.subTest(n=n):
                live,printed,vocab=press.core(n)
                doc=Nodes(printed)
                self.assertIn('<svg',live)
                if n in press.GESTURES:self.assertIn("动作分镜",printed)
                self.assertTrue(vocab)
                local=[at['id'] for _,at in doc.nodes if 'id' in at]
                self.assertEqual(len(local),len(set(local)))
                self.assertFalse(ids.intersection(local));ids.update(local)
                for tag,attrs in doc.nodes:
                    self.assertNotIn(tag,{"script","iframe","object","style","button","input","foreignobject","details"})
                    self.assertTrue(all(not k.startswith(("on","data-")) for k in attrs))
                    for attr in ('begin','end'):
                        for ref in re.findall(r'([a-zA-Z][a-zA-Z0-9]*)\.(?:click|begin|end)',attrs.get(attr,'')):
                            self.assertIn(ref,local)
    def test_first_made_personal(self):
        data=json.loads((SKILL/'examples'/'reveal.json').read_text(encoding='utf-8'))
        cfg,items=press.merge_config(data,[])
        out=press.assemble(cfg,items,press.picture(SKILL/'assets'/'cover.jpg'))
        artifact=Nodes(out['wechat.html'])
        self.assertIn("左侧留白，放四个标题字。",artifact.words)
        self.assertNotIn("先说清楚，这张图给谁看。",artifact.words)
        self.assertNotIn('<svg',out['static.html'])
        self.assertIn(items[1]['still'],out['static.html'])
        self.assertEqual(out['index.html'].count('class="effect"'),1)
    def test_text_escape_and_references(self):
        active={'点开这层绿蜡':"<script>not markup</script>"}
        _,printed,_=press.core(1,terms=active)
        self.assertNotIn('script',[n[0] for n in Nodes(printed).nodes])
        self.assertIn(active['点开这层绿蜡'],Nodes(printed).words)
        with self.assertRaises(ValueError):press.core(1,terms={'invented':'new'})
        with self.assertRaises(ValueError):press.merge_config({'effects':[1,1]},[])
        with self.assertRaises(ValueError):press.merge_config({'effects':[{'id':1,'terms':active}]},[])
        with self.assertRaises(ValueError):press.merge_config({'gallery_url':'javascript:alert(1)'},[])
    def test_cli_output_overwrite_and_portability(self):
        with TemporaryDirectory() as temp:
            cmd=[sys.executable,str(SKILL/'scripts'/'press.py'),'--config',str(SKILL/'examples'/'reveal.json'),'--out',str(Path(temp)/'issue')]
            base=Path(temp)/'issue'
            self.assertEqual(subprocess.run(cmd,cwd=temp,capture_output=True).returncode,0)
            self.assertTrue((base/'print-cover.jpg').is_file())
            clean=(base/'wechat.html').read_text(encoding='utf-8')
            self.assertIn('src="print-cover.jpg"',clean)
            self.assertNotIn(str(SKILL),clean)
            self.assertNotEqual(subprocess.run(cmd,cwd=temp,capture_output=True).returncode,0)
            self.assertEqual(subprocess.run(cmd+['--force'],cwd=temp,capture_output=True).returncode,0)

if __name__=='__main__':unittest.main()

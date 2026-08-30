import json, tempfile, unittest
from pathlib import Path
from brief_to_page import load, render

class T(unittest.TestCase):
    def test_render_sections_and_meta(self):
        p=Path(tempfile.mktemp(suffix='.json'))
        p.write_text(json.dumps({'brand':'Test','title':'Hello','hero':'World','sections':[{'title':'A','items':[{'title':'B','text':'C'}]}]}),encoding='utf-8')
        d=load(p); page=render(d)
        self.assertIn('<title>Hello</title>',page)
        self.assertIn('B',page)
        self.assertIn('viewport',page)
    def test_required(self):
        p=Path(tempfile.mktemp(suffix='.json')); p.write_text('{}')
        with self.assertRaises(ValueError): load(p)

    def test_rejects_palette_breakout_and_javascript_cta(self):
        base={'brand':'Test','title':'Hello','hero':'World','description':'World','sections':[],'palette':{},'cta':{}}
        bad_palette={**base,'palette':{'accent':'red;}</style><script>alert(1)</script><style>{'}}
        with self.assertRaisesRegex(ValueError, 'palette'):
            render(bad_palette)
        bad_href={**base,'cta':{'label':'go','href':'javascript:alert(1)'}}
        with self.assertRaisesRegex(ValueError, 'href scheme'):
            render(bad_href)
        safe={**base,'palette':{'accent':'#b34f71'},'cta':{'label':'go','href':'https://example.com/?a=1&b=2'}}
        page=render(safe)
        self.assertIn('href="https://example.com/?a=1&amp;b=2"',page)

if __name__=='__main__': unittest.main()

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

if __name__=='__main__': unittest.main()

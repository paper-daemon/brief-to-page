import json, tempfile, unittest
from pathlib import Path
from brief_to_page import load, render, validate_output_path

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

    def test_rejects_invalid_container_shapes(self):
        cases = [
            (['not','object'], 'brief root'),
            ({'brand':'Test','title':'Hello','hero':'World','sections':'oops'}, 'sections'),
            ({'brand':'Test','title':'Hello','hero':'World','palette':['red']}, 'palette'),
            ({'brand':'Test','title':'Hello','hero':'World','cta':['go']}, 'cta'),
            ({'brand':'Test','title':'Hello','hero':'World','sections':[{'title':'A','items':'oops'}]}, 'items'),
        ]
        for data, message in cases:
            p=Path(tempfile.mktemp(suffix='.json'))
            p.write_text(json.dumps(data),encoding='utf-8')
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    load(p)

    def test_rejects_explicit_falsey_nonlist_items(self):
        base={'brand':'Test','title':'Hello','hero':'World'}
        for value in ['',0,{},None,False]:
            p=Path(tempfile.mktemp(suffix='.json'))
            p.write_text(json.dumps({**base,'sections':[{'title':'A','items':value}]}),encoding='utf-8')
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, 'items must be a list of objects'):
                    load(p)
        p=Path(tempfile.mktemp(suffix='.json'))
        p.write_text(json.dumps({**base,'sections':[{'title':'A'}]}),encoding='utf-8')
        self.assertNotIn('items',load(p)['sections'][0],'omitting items remains valid')

    def test_output_cannot_overwrite_input_brief(self):
        p=Path(tempfile.mktemp(suffix='.json'))
        p.write_text(json.dumps({'brand':'Test','title':'Hello','hero':'World'}),encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'must not overwrite'):
            validate_output_path(p,p)
        out=p.parent/'index.html'
        validate_output_path(p,out)

if __name__=='__main__': unittest.main()

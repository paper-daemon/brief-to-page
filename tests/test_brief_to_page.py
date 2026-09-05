import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from brief_to_page import load, render, validate_output_path, validate_brief

class T(unittest.TestCase):
    def make_brief(self, **extra):
        data={'brand':'Test','title':'Hello','hero':'World'}
        data.update(extra)
        p=Path(tempfile.mktemp(suffix='.json'))
        p.write_text(json.dumps(data),encoding='utf-8')
        return p

    def test_render_sections_and_meta(self):
        p=self.make_brief(sections=[{'title':'A','items':[{'title':'B','text':'C'}]}])
        d=load(p); page=render(d)
        self.assertIn('<title>Hello</title>',page)
        self.assertIn('B',page)
        self.assertIn('viewport',page)
        self.assertIn('<html lang="ja">',page)

    def test_international_language_and_seo_meta(self):
        p=self.make_brief(lang='en-US',canonical='https://example.com/page',og_image='https://example.com/og.png')
        page=render(validate_brief(p))
        self.assertIn('<html lang="en-US">',page)
        self.assertIn('rel="canonical" href="https://example.com/page"',page)
        self.assertIn('property="og:image" content="https://example.com/og.png"',page)

    def test_required(self):
        p=Path(tempfile.mktemp(suffix='.json')); p.write_text('{}')
        with self.assertRaises(ValueError): load(p)

    def test_rejects_palette_breakout_and_javascript_cta(self):
        base={'brand':'Test','title':'Hello','hero':'World','description':'World','sections':[],'palette':{},'cta':{},'lang':'ja'}
        bad_palette={**base,'palette':{'accent':'red;}</style><script>alert(1)</script><style>{'}}
        with self.assertRaisesRegex(ValueError, 'palette'):
            render(bad_palette)
        bad_href={**base,'cta':{'label':'go','href':'javascript:alert(1)'}}
        with self.assertRaisesRegex(ValueError, 'href scheme'):
            render(bad_href)
        safe={**base,'palette':{'accent':'#b34f71'},'cta':{'label':'go','href':'https://example.com/?a=1&b=2'}}
        page=render(safe)
        self.assertIn('href="https://example.com/?a=1&amp;b=2"',page)

    def test_rejects_invalid_meta_urls_and_lang(self):
        for field, value, message in [
            ('canonical','javascript:alert(1)','canonical'),
            ('og_image','/relative.png','og_image'),
            ('lang','en" onclick="x','lang'),
        ]:
            p=self.make_brief(**{field:value})
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, message):
                    validate_brief(p)

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
        p=self.make_brief()
        with self.assertRaisesRegex(ValueError, 'must not overwrite'):
            validate_output_path(p,p)
        out=p.parent/'index.html'
        validate_output_path(p,out)

    def test_validate_only_cli_does_not_write_output(self):
        base=Path(tempfile.mkdtemp())
        brief=base/'brief.json'; out=base/'index.html'
        brief.write_text(json.dumps({'brand':'Test','title':'Hello','hero':'World','lang':'en'}),encoding='utf-8')
        cp=subprocess.run([sys.executable,'brief_to_page.py',str(brief),'--output',str(out),'--validate-only'],text=True,capture_output=True)
        self.assertEqual(cp.returncode,0)
        self.assertIn('valid=1',cp.stdout)
        self.assertFalse(out.exists())

    def test_validate_only_checks_render_time_safety(self):
        base=Path(tempfile.mkdtemp())
        brief=base/'brief.json'
        brief.write_text(json.dumps({'brand':'Test','title':'Hello','hero':'World','cta':{'label':'x','href':'javascript:alert(1)'}}),encoding='utf-8')
        cp=subprocess.run([sys.executable,'brief_to_page.py',str(brief),'--validate-only'],text=True,capture_output=True)
        self.assertNotEqual(cp.returncode,0)
        self.assertIn('href scheme',cp.stderr)

if __name__=='__main__': unittest.main()

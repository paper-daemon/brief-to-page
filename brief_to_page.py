#!/usr/bin/env python3
import argparse, html, json, re
from urllib.parse import urlsplit
from pathlib import Path

REQUIRED=('brand','title','hero')

def load(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('brief root must be a JSON object')
    missing=[k for k in REQUIRED if not data.get(k)]
    if missing: raise ValueError('missing required: '+', '.join(missing))
    data.setdefault('description',data['hero'])
    data.setdefault('sections',[]); data.setdefault('cta',{})
    data.setdefault('palette',{})
    if not isinstance(data['sections'], list):
        raise ValueError('sections must be a list')
    if not isinstance(data['cta'], dict):
        raise ValueError('cta must be an object')
    if not isinstance(data['palette'], dict):
        raise ValueError('palette must be an object')
    for index, section in enumerate(data['sections']):
        if not isinstance(section, dict):
            raise ValueError(f'sections[{index}] must be an object')
        items=section.get('items') or []
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise ValueError(f'sections[{index}].items must be a list of objects')
    return data

def esc(v): return html.escape(str(v or ''))

COLOR = re.compile(r'^(?:#[0-9a-fA-F]{3,4}|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{8}|[A-Za-z]{3,24})$')

def safe_color(value, default):
    value=str(value or default).strip()
    if not COLOR.fullmatch(value):
        raise ValueError('palette colors must be hex or simple named colors')
    return value

def safe_href(value):
    value=str(value or '').strip()
    if value.startswith(('#','/','./','../')):
        return value
    parsed=urlsplit(value)
    if parsed.scheme.lower() not in {'http','https','mailto','tel'}:
        raise ValueError('cta href scheme is not allowed')
    return value

def section_html(section):
    items=section.get('items') or []
    cards=''.join(f'<article><h3>{esc(i.get("title"))}</h3><p>{esc(i.get("text"))}</p></article>' for i in items)
    body=f'<p>{esc(section.get("text"))}</p>' if section.get('text') else ''
    return f'<section><div class="eyebrow">{esc(section.get("eyebrow"))}</div><h2>{esc(section.get("title"))}</h2>{body}<div class="cards">{cards}</div></section>'

def render(d):
    p=d['palette']; bg=safe_color(p.get('background'),'#f4efe8'); paper=safe_color(p.get('paper'),'#fffaf2')
    ink=safe_color(p.get('ink'),'#292421'); accent=safe_color(p.get('accent'),'#b34f71'); sage=safe_color(p.get('secondary'),'#75836d')
    sections=''.join(section_html(s) for s in d['sections'])
    cta=d.get('cta') or {}; cta_html=''
    if cta.get('label') and cta.get('href'):
        cta_html=f'<a class="cta" href="{esc(safe_href(cta["href"]))}">{esc(cta["label"])} ↗</a>'
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(d['title'])}</title><meta name="description" content="{esc(d['description'])}"><meta property="og:title" content="{esc(d['title'])}"><meta property="og:description" content="{esc(d['description'])}">
<style>:root{{--bg:{bg};--paper:{paper};--ink:{ink};--accent:{accent};--sage:{sage}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,'Noto Sans JP',sans-serif}}main{{max-width:1040px;margin:auto;padding:24px}}nav{{display:flex;justify-content:space-between;padding:18px 0;font-weight:800}}.hero{{background:var(--paper);border:1px solid #ddd1c4;padding:clamp(36px,8vw,88px);margin:28px 0 70px}}.hero h1{{font-family:serif;font-size:clamp(2.6rem,8vw,6rem);line-height:1;margin:.1em 0 .25em;letter-spacing:-.05em}}.hero p{{font-size:1.05rem;line-height:1.9;max-width:650px}}.tag{{color:var(--accent);font-weight:800}}section{{padding:58px 0;border-top:1px solid #bdb1a6}}section h2{{font-family:serif;font-size:clamp(1.8rem,5vw,3rem);margin:.2em 0 .6em}}.eyebrow{{font:700 .75rem monospace;color:var(--sage)}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}article{{background:var(--paper);padding:20px;border:1px solid #ddd1c4}}article h3{{margin-top:0}}.cta{{display:inline-block;margin-top:18px;padding:13px 18px;background:var(--ink);color:var(--paper);text-decoration:none;border-radius:999px;font-weight:800}}footer{{padding:40px 0 70px;color:#756b63;font-size:.8rem}}@media(max-width:700px){{.cards{{grid-template-columns:1fr}}.hero{{padding:38px 24px}}}}</style></head><body><main><nav><span>{esc(d['brand'])}</span><span>{esc(d.get('nav_note',''))}</span></nav><div class="hero"><div class="tag">{esc(d.get('tagline',''))}</div><h1>{esc(d['title'])}</h1><p>{esc(d['hero'])}</p>{cta_html}</div>{sections}<footer>{esc(d['brand'])} · generated with Brief to Page</footer></main></body></html>'''
def main():
    ap=argparse.ArgumentParser(description='Turn a small JSON brief into a responsive single-file landing page.')
    ap.add_argument('brief'); ap.add_argument('--output',default='index.html')
    a=ap.parse_args(); data=load(a.brief); out=Path(a.output)
    out.write_text(render(data),encoding='utf-8')
    print(f'generated={out} sections={len(data["sections"])} brand={data["brand"]}')

if __name__=='__main__':
    main()

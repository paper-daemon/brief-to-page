# Brief to Page

**Turn a small structured JSON brief into a responsive, single-file landing page.**

Brief to Page is a dependency-free Python CLI for fast prototypes, portfolio pages, campaign drafts, and small service pages. Content, CTA, sections, palette and basic SEO metadata stay in data instead of being scattered through hand-edited HTML.

> 日本語: 短いJSON要件から、レスポンシブな1ページLPを単一HTMLとして生成する無料OSSです。生成前のvalidation、URL境界、入力brief保護にも対応しています。

## Quick start

```bash
python brief_to_page.py brief.json --output index.html
```

Validate the entire brief without writing HTML:

```bash
python brief_to_page.py brief.json --validate-only
```

The validation-only mode checks not just JSON shape, but also render-time boundaries such as palette values, CTA URL schemes, language tags, canonical URLs, and Open Graph image URLs.

## Example brief

```json
{
  "lang": "en",
  "brand": "Northstar Ops",
  "title": "Make the workflow boring again.",
  "hero": "Small automation systems with clear failure behavior.",
  "description": "Automation and reliability services for small teams.",
  "canonical": "https://example.com/automation",
  "og_image": "https://example.com/og.png",
  "tagline": "AUTOMATION / RELIABILITY",
  "cta": {
    "label": "Start a project",
    "href": "https://example.com/contact"
  },
  "palette": {
    "background": "#f4efe8",
    "paper": "#fffaf2",
    "ink": "#292421",
    "accent": "#b34f71"
  },
  "sections": [
    {
      "eyebrow": "01 / SERVICES",
      "title": "What we build",
      "items": [
        {"title": "API automation", "text": "One workflow, tested end to end."},
        {"title": "Data QA", "text": "Validate inputs before downstream work."}
      ]
    }
  ]
}
```

## What it generates

- responsive one-page HTML
- no external CSS or JavaScript dependency
- brand, title, hero and structured content sections
- card grids from brief data
- CTA with restricted URL schemes
- title, description and Open Graph text metadata
- optional canonical URL and Open Graph image
- configurable document language such as `ja`, `en`, or `en-US`
- configurable color palette with a deliberately narrow safety boundary

## Safety and validation boundaries

Brief to Page treats generated HTML as a delivery artifact, so malformed or unsafe inputs fail before the output is written.

- `--output` cannot resolve to the same file as the source brief.
- Palette colors must be hex values or simple named colors.
- CTA links allow local paths, anchors, `http`, `https`, `mailto`, and `tel` only.
- Canonical and Open Graph image URLs must be absolute HTTP(S) URLs.
- `lang` must use a simple BCP 47-style language tag.
- Text content is HTML escaped.
- Section containers and card items are shape-checked before rendering.

See [`SECURITY_BOUNDARIES.md`](SECURITY_BOUNDARIES.md) and [`docs/brief-shape-boundaries.md`](docs/brief-shape-boundaries.md) for the intentionally supported boundary.

## Why validation-only matters

A content pipeline can validate a generated or human-authored brief before committing the resulting page:

```yaml
- name: Validate landing-page brief
  run: python brief_to_page.py campaign/brief.json --validate-only

- name: Generate landing page
  run: python brief_to_page.py campaign/brief.json --output public/index.html
```

That makes the JSON brief reviewable in a pull request while keeping HTML generation deterministic and repeatable.

## Test suite

```bash
python -m unittest -v tests.test_brief_to_page
```

Regression coverage includes container-shape errors, unsafe URL schemes, CSS palette breakout attempts, input/output path collisions, international metadata and validation-only behavior.

## Good fits

- fast campaign and service landing pages
- client-approved content briefs
- AI-assisted content pipelines with a validation boundary
- portfolio prototypes
- internal tool front pages
- reproducible static-page handoff

## Project links

- OSS: https://github.com/paper-daemon/brief-to-page
- BOOTH free download: https://amase-memo.booth.pm/items/8778713
- Builder portfolio: https://paper-daemon.github.io/global.html

Python 3.10+ / standard library only / MIT License.

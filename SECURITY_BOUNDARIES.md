# Input safety boundaries

`brief-to-page` turns small JSON briefs into static HTML, so brief values are treated as untrusted input.

## Palette values

Palette colors are intentionally narrow. Use hexadecimal colors or simple named colors such as `#1f2937`, `white`, or `navy`.

Values that try to break out of the CSS declaration are rejected rather than copied into generated markup.

## CTA URLs

CTA links accept normal web/contact destinations and local document links:

- `https://...`
- `http://...`
- `mailto:...`
- `tel:...`
- relative paths such as `/pricing` or `./demo.html`
- fragments such as `#contact`

Executable or unexpected schemes such as `javascript:` are rejected.

## HTML attributes

Text that reaches HTML attributes remains escaped before rendering. Do not bypass the renderer by concatenating raw brief values into generated tags.

## Regression tests

`tests/test_brief_to_page.py` includes cases for unsafe palette values and CTA URLs. Run:

```bash
python -m pytest -q
```

When adding a new brief field that reaches CSS, HTML, or a URL, add a hostile-input regression case alongside the feature.

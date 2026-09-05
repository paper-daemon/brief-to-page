# Changelog

## 1.1.0
- Add `--validate-only` to run full brief and render-boundary validation without writing HTML.
- Add configurable document language through `lang` with a constrained BCP 47-style format.
- Add optional canonical URL and Open Graph image metadata with absolute HTTP(S) validation.
- Validate unsafe CTA schemes and render-time palette boundaries before output is written.
- Reject `--output` when it resolves to the same path as the input brief, preventing accidental JSON-to-HTML overwrite.
- Expand regression coverage and English-first documentation for automation and content-pipeline use.

## 1.0.0
- Initial public release.

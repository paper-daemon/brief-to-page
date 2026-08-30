# Brief to Page

短いJSON要件から、レスポンシブな1ページLPを1枚のHTMLとして生成する無料OSSです。

```bash
python brief_to_page.py brief.json --output index.html
```

## できること
- brand / title / hero / sections / CTA をJSONで管理
- スマホ対応の1ページHTMLを生成
- title / description / OGPの基本メタを自動生成
- カラー指定に対応
- 複数カードのセクションを生成
- 外部CSS/JSなしの単一HTML

試作品、ポートフォリオ、告知ページ、小規模サービスLPの叩き台向け。

- [JSON briefのshape境界とエラー例](docs/brief-shape-boundaries.md)

## Output safety boundary

`--output` は入力briefとは別の実体pathである必要があります。入力JSONと同じpathを指定した場合は、HTML生成前にエラー終了し、元briefを上書きしません。

Python 3.10+ / 外部ライブラリ不要 / MIT License。
- BOOTH 0円DL: https://amase-memo.booth.pm/items/8778713
- 作者サイト: https://paper-daemon.github.io/


# Brief JSON shape boundaries

`Brief to Page` はJSONを読めれば何でも受けるのではなく、LPの構造として扱えるcontainer shapeだけを受けます。

## 今回確認した境界

修正前は次の入力が `AttributeError` で落ちていました。

- JSON root が配列
- `sections` が文字列
- `palette` が配列
- `cta` が配列
- `sections[n].items` が配列以外（空文字、`0`、`false`、`null`、空objectも含む）

たとえば root が `['not', 'object']` の場合は `list object has no attribute get` になり、利用者から見ると何が不正なのか分かりにくい状態でした。

## 現在の挙動

入力のshapeを `load()` の入口で検証し、次のような `ValueError` にします。

```text
brief root must be a JSON object
sections must be a list
palette must be an object
cta must be an object
sections[0].items must be a list of objects
```

`items` 自体を省略したsectionは従来どおり有効ですが、明示した `items` がlistでない場合はfalseyな値でも黙って空listへ丸めません。

HTMLへ入る文字列のescape、palette breakout拒否、`javascript:` CTA拒否は従来の境界を維持しています。

## 検証

```bash
python3 -m unittest -v tests/test_brief_to_page.py
```

公開mainで 5 / 5 tests PASS。既存の正常LP生成、required fields、palette / CTA safetyに加えて、malformed container shapeとfalsey bypassの回帰テストを含みます。

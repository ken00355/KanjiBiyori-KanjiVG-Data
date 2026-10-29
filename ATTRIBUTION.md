# Attribution / 出典・改変表示

本データは **KanjiVGを使用し、改変したもの** です。

## 原著作物

- 名称: KanjiVG (Kanji Vector Graphics)
- 著作者: Ulrich Apel
- 公式サイト: https://kanjivg.tagaini.net/
- 公式ソース: https://github.com/KanjiVG/kanjivg
- 使用リリース: [r20260714](https://github.com/KanjiVG/kanjivg/releases/tag/r20260714)
- 使用配布物: [kanjivg-20260714-main.zip](https://github.com/KanjiVG/kanjivg/releases/download/r20260714/kanjivg-20260714-main.zip)
- 配布物SHA-256: `b5df6cd2bc249dd49b8041eb99e38ba9f8dc6b9ea57962a80084b4a315d1a7fc`
- 収録元SVG全205ファイルの著作権表示: **Copyright (C) 2009/2010/2011 Ulrich Apel.**
- ライセンス: **Creative Commons Attribution-ShareAlike 3.0 Unported（CC BY-SA 3.0／表示–継承3.0非移植）**
- 概要: https://creativecommons.org/licenses/by-sa/3.0/
- 法文: https://creativecommons.org/licenses/by-sa/3.0/legalcode （同梱の[LICENSE](LICENSE)も参照）

2026-10-29確認時点で公式サイト全体には「copyright © 2009-2026 Ulrich Apel」と表示されています。ここでは使用したリリースの収録元SVGに実際に付されている上記の著作権表示を保持しています。

## かんじ日和での改変

変換・公開用整理: かんじ日和。原データの著作者の表示を置き換えるものではありません。

1. SVGのパス（M・C・c・S・s、相対座標を含む）を始点と絶対座標の三次ベジェ列に変換しました。
2. S・sの省略された制御点を展開し、座標を小数3桁に丸めました。
3. アプリで使用する205字（小4の202字＋紀・型・液）を選び、アプリ内の順序でJSONに収録しました。
4. 部品のグループ、画番号の表示位置などのメタデータを除去し、各画の種類（kvg:type）を保持しました。
5. 座標系109×109を維持しています。丸めを除き、字形・位置・筆順・画の方向への個別調整や画の並べ替えはしていません。

JSONの`source.modifications`にも元の変換時の改変表示をそのまま保持しています。
この公開用パッケージではJSONの内容を変更していません。
`scripts/convert.py`は元のアプリ用変換スクリプトの説明とパスを独立配布向けに変更し、文字リストのUTF-8読み込みとJSONのUTF-8・LFによるバイト単位の入出力・比較を明示しました。字形の変換ロジックは維持しました。
文字リストと検証用の小4文字リストを同梱し、配布物のハッシュ検証スクリプトと説明文書を追加しました。

## English credit

This dataset uses and adapts KanjiVG by Ulrich Apel, release r20260714.
Original SVG copyright notice: Copyright (C) 2009/2010/2011 Ulrich Apel.
Source: https://kanjivg.tagaini.net/

The adaptation by Kanji Biyori converts SVG paths into absolute cubic Bézier curves, expands implicit S/s control points, rounds coordinates to three decimal places, selects and orders 205 characters, and removes component grouping and stroke-number positions while retaining stroke types. No per-character geometry, stroke-order or stroke-direction adjustments are made beyond coordinate rounding. The original 109×109 coordinate system is retained.

The adapted JSON and the supporting scripts, character lists and documentation included in this package are provided under CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/ . No endorsement by KanjiVG or the original author is implied.

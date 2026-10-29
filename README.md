# KanjiBiyori-KanjiVG-Data

「かんじ日和」で使用する、KanjiVG由来の205字・2024画の字形・筆順データです。
KanjiVGの改変物であるJSONを **Creative Commons Attribution-ShareAlike 3.0 Unported（CC BY-SA 3.0／表示–継承3.0非移植）** で提供します。
KanjiVG（Copyright (C) 2009/2010/2011 Ulrich Apel.）を使用しています。

- [KanjiVG公式サイト](https://kanjivg.tagaini.net/)
- [使用リリース r20260714](https://github.com/KanjiVG/kanjivg/releases/tag/r20260714)
- [ライセンス概要](https://creativecommons.org/licenses/by-sa/3.0/)・[法文](https://creativecommons.org/licenses/by-sa/3.0/legalcode)
- 出典・著作権表示・変更点: [ATTRIBUTION.md](ATTRIBUTION.md)
- 同梱ライセンス全文: [LICENSE](LICENSE)

## 内容

```text
.gitattributes           Gitチェックアウト時も全テキストをLFに固定
data/KanjiVGStrokes.json   アプリ同梱JSONのバイト単位のコピー
scripts/convert.py        公式配布ZIPからの生成・検証（Python標準ライブラリのみ）
scripts/characters.txt    205字と収録順
scripts/grade4_kanji.txt  小4の202字がそろうことを検証する文字リスト
scripts/verify.py         同梱物のハッシュ・形式検証、任意でアプリJSONとの比較
README.md
LICENSE
ATTRIBUTION.md
SHA256SUMS                このファイル自身を除く全公開ファイルのSHA-256
```

対象は小学4年の202字と「紀・型・液」。読み・意味・問題・学習履歴・手書き判定ロジックは含みません。
JSONの`source`に出典・版・ライセンス・著作権・元ZIPのハッシュ・改変内容、`kanji`に文字順の配列を保持しています。
各文字の`character`は文字、`codepoint`は5桁の小文字16進Unicodeコードポイント、`strokeCount`は画数です。
`strokes`は筆順の配列で、`start: [x,y]`と`curves: [[x1,y1,x2,y2,x,y], ...]`による絶対座標の三次ベジェ列、`type`によるKanjiVGの画種を収録しています。座標系は109×109です。

## 再生成と検証

Python 3.9以上。リポジトリのルートで実行してください。外部パッケージは不要です。

1. [公式ZIP](https://github.com/KanjiVG/kanjivg/releases/download/r20260714/kanjivg-20260714-main.zip)を別途取得します。このZIPは本配布物には同梱しません。
2. ZIPのSHA-256は `b5df6cd2bc249dd49b8041eb99e38ba9f8dc6b9ea57962a80084b4a315d1a7fc` です。スクリプトでも検証し、異なるZIPは拒否します。
3. 次のコマンドで同梱データとの再生成一致を確認できます。

```sh
python3 scripts/convert.py /path/to/kanjivg-20260714-main.zip --check
python3 -B scripts/verify.py
```

生成する場合は`--check`を外します。JSONを手編集せず、版を変更する場合はスクリプトの版・ZIP名・元ZIPハッシュ、出典文書、SHA256SUMSを一緒に更新してください。
`--check`は生成内容との一致、画IDの連番、重複、202字の包含、画数、座標の範囲や形式などを検証します。`verify.py`はさらに205字の収録順と同梱全ファイルのバイト単位ハッシュを確認します。
ルートの通常の`.git/`管理ディレクトリだけは検証から除外します。それ以外の余分なファイルやシンボリックリンクはエラーになります。
文字リストはUTF-8で読み、JSONはUTF-8・LFのバイト列で生成・比較します。`.gitattributes`でWindowsのチェックアウト時もLFを維持します。

アプリ側のJSONが手元にある場合は、別途バイト単位でも比較できます。

```sh
python3 -B scripts/verify.py --app-json /path/to/app/ThirdParty/KanjiVG/KanjiVGStrokes.json
```

準備時点のJSON（末尾改行を含むUTF-8）のSHA-256:

```text
999e4d6b0e9206784639f27ba59d19f3aa985c282223e437032a23e0ec96a53f
```

SHA256SUMSは配布物の整合性確認用であり、署名や発行者の真正性を保証するものではありません。

## 再利用と範囲

JSON、文字リスト、およびこの公開パッケージ内の変換・検証スクリプトと説明文書はCC BY-SA 3.0で提供します。LICENSEは同ライセンスの法文です。
条件に従い、商用利用を含む複製・再配布・改変が可能です。再配布では出典・著作権表示・ライセンスへのリンクを維持し、改変した場合はその旨を示してください。改変データは継承条件に従って提供し、ライセンス上の権利を制限する追加条件や技術的制限を課さないでください。正確な条件はLICENSEをご覧ください。

このパッケージに含まれないアプリ本体のソースコード、画像、名称・商標などへの利用許諾を与えるものではありません。KanjiVGや原著作者による本アプリの推薦・承認を意味しません。

このデータをアプリ外から入手できる形で配布することだけで、App Store配布におけるDRM（FairPlay）とCC BY-SA 3.0の適合性が完全に解決すると保証するものではありません。アプリを含む配布形態とライセンスの適用範囲は別途確認が必要です。

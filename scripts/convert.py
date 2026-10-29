#!/usr/bin/env python3
"""KanjiVG r20260714 → かんじ日和の205字JSON（CC BY-SA 3.0）。

  python3 scripts/convert.py /path/to/kanjivg-20260714-main.zip
  python3 scripts/convert.py /path/to/kanjivg-20260714-main.zip --check

出典・ライセンス・改変内容は ../ATTRIBUTION.md と ../LICENSE を参照。
公開用にパスと説明を変更。変換・検証ロジックはアプリ側の変換スクリプトと同じ。
"""
import argparse, hashlib, json, math, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHARACTERS = REPO / "scripts/characters.txt"
GRADE4 = REPO / "scripts/grade4_kanji.txt"
OUTPUT = REPO / "data/KanjiVGStrokes.json"
RELEASE = "r20260714"
ARCHIVE = "kanjivg-20260714-main.zip"
ARCHIVE_SHA256 = "b5df6cd2bc249dd49b8041eb99e38ba9f8dc6b9ea57962a80084b4a315d1a7fc"
MODIFICATIONS = [
    "SVGのパス（M・C・c・S・s、相対座標を含む）を、始点と絶対座標の三次ベジェ列に書き換えた（S・sの省略された制御点を補った）。座標は小数3桁に丸めた。",
    "画の形・位置・筆順・向きは変更していない。",
    "アプリで使う205字だけを収録し、部品のグループ・画番号の表示位置などのメタデータを除いた。各画の種類（kvg:type）は残した。",
]

NS = "{http://www.w3.org/2000/svg}"
KVG = "{http://kanjivg.tagaini.net}"
TOKEN = re.compile(r"[MmCcSs]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def parse_path(d):
    """KanjiVG のパス（M と三次ベジェだけ）→ (始点, [x1, y1, x2, y2, x, y] の列)。"""
    toks = TOKEN.findall(d)
    if re.search(r"[^MmCcSs0-9eE.,\s+-]", d):
        raise ValueError(f"unsupported path command: {d}")
    i, cmd, cur, start, last_c2, curves = 0, None, None, None, None, []
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]; i += 1
        n = {"M": 2, "C": 6, "S": 4}[cmd.upper()]
        v = [float(x) for x in toks[i:i + n]]
        if len(v) != n:
            raise ValueError(f"truncated path: {d}")
        i += n
        ox, oy = cur if cmd.islower() and cur else (0.0, 0.0)
        if cmd in "Mm":
            if start is not None:
                raise ValueError(f"multiple subpaths: {d}")
            cur = start = (ox + v[0], oy + v[1])
            cmd = "c" if cmd == "m" else "C"  # M の後に続く数値は SVG では lineto だが KanjiVG では使われない
            continue
        if cmd in "Cc":
            c1, c2, p = (ox + v[0], oy + v[1]), (ox + v[2], oy + v[3]), (ox + v[4], oy + v[5])
        else:
            c1 = (2 * cur[0] - last_c2[0], 2 * cur[1] - last_c2[1]) if last_c2 else cur
            c2, p = (ox + v[0], oy + v[1]), (ox + v[2], oy + v[3])
        curves.append([round(x, 3) for x in (*c1, *c2, *p)])
        cur, last_c2 = p, c2
    if start is None or not curves:
        raise ValueError(f"empty path: {d}")
    return [round(start[0], 3), round(start[1], 3)], curves


def glyph(archive, ch):
    cp = f"{ord(ch):05x}"
    text = archive.read(f"kanji/{cp}.svg").decode("utf-8")
    copyright = re.search(r"Copyright \(C\)[^\n]*", text).group(0).strip()
    root = ET.fromstring(text)
    paths = [p for p in root.iter(NS + "path") if p.get("id", "").startswith(f"kvg:{cp}-s")]
    numbers = [int(p.get("id").rsplit("-s", 1)[1]) for p in paths]
    if numbers != list(range(1, len(paths) + 1)):
        raise ValueError(f"{ch}: stroke ids out of order {numbers}")
    strokes = []
    for p in paths:
        start, curves = parse_path(p.get("d"))
        strokes.append({"start": start, "curves": curves, "type": p.get(KVG + "type")})
    return {"character": ch, "codepoint": cp, "strokeCount": len(strokes), "strokes": strokes}, copyright


def build(zip_path):
    digest = hashlib.sha256(Path(zip_path).read_bytes()).hexdigest()
    if digest != ARCHIVE_SHA256:
        sys.exit(f"{zip_path}: SHA-256 {digest} が {ARCHIVE}（{RELEASE}）と一致しない。版を上げるときは RELEASE・ARCHIVE・ARCHIVE_SHA256 を更新する")
    chars = list(CHARACTERS.read_text(encoding="utf-8").strip())
    with zipfile.ZipFile(zip_path) as archive:
        pairs = [glyph(archive, ch) for ch in chars]
    copyrights = sorted({c for _, c in pairs})
    return {
        "source": {
            "name": "KanjiVG",
            "release": RELEASE,
            "url": "https://kanjivg.tagaini.net/",
            "license": "CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/)",
            "copyright": " ".join(copyrights),
            "coordinateSize": 109,
            "archive": ARCHIVE,
            "archiveSHA256": ARCHIVE_SHA256,
            "modifications": MODIFICATIONS,
        },
        "kanji": [g for g, _ in pairs],
    }


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"


def validate(data):
    problems = []
    chars = [g["character"] for g in data["kanji"]]
    if len(set(chars)) != len(chars):
        problems.append("duplicate characters")
    missing = [c for c in GRADE4.read_text(encoding="utf-8").strip() if c not in chars]
    if missing:
        problems.append(f"grade-4 kanji missing: {''.join(missing)}")
    for g in data["kanji"]:
        ch = g["character"]
        if g["codepoint"] != f"{ord(ch):05x}" or g["strokeCount"] != len(g["strokes"]) or not g["strokes"]:
            problems.append(f"{ch}: header mismatch")
        for k, s in enumerate(g["strokes"], 1):
            nums = s["start"] + [x for c in s["curves"] for x in c]
            if not s["curves"] or any(len(c) != 6 for c in s["curves"]):
                problems.append(f"{ch} #{k}: malformed curves")
            if any(not math.isfinite(x) or not -5 <= x <= 114 for x in nums):
                problems.append(f"{ch} #{k}: coordinate out of range")
            end = s["curves"][-1][4:6] if s["curves"] else s["start"]
            if math.dist(s["start"], end) < 1 and len(s["curves"]) == 1:
                problems.append(f"{ch} #{k}: zero-length stroke")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    data = build(a.zip)
    problems = validate(data)
    for p in problems:
        print("NG", p)
    if problems:
        sys.exit(1)
    # バイナリ入出力で、OSの既定文字コード・改行変換に依存しない。
    payload = serialize(data).encode("utf-8")
    if a.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            sys.exit(f"{OUTPUT.relative_to(REPO)} が再生成結果と一致しない（convert.py を実行して更新する）")
        print(f"OK: {len(data['kanji'])}字・{sum(g['strokeCount'] for g in data['kanji'])}画、同梱データは再生成結果と一致")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)
        print(f"{OUTPUT.relative_to(REPO)}: {len(data['kanji'])}字・{sum(g['strokeCount'] for g in data['kanji'])}画")

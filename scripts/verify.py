#!/usr/bin/env python3
"""配布物のSHA-256・データ構造・収録文字を検証する。CC BY-SA 3.0。

出典と条件は ../ATTRIBUTION.md および ../LICENSE を参照。
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

# import時のキャッシュを公開パッケージに残さない。
sys.dont_write_bytecode = True
import convert

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-json', type=Path)
    args = parser.parse_args()
    manifest = ROOT / 'SHA256SUMS'
    expected = {}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or name in expected:
            raise ValueError('invalid manifest path')
        expected[name] = digest
    entries = []
    pending = [ROOT]
    while pending:
        for path in pending.pop().iterdir():
            # cloneで作られるルートの管理ディレクトリだけを除外する。
            # .gitという通常ファイルやシンボリックリンクは検証対象に残す。
            if path == ROOT / '.git' and path.is_dir() and not path.is_symlink():
                continue
            entries.append(path)
            if path.is_dir() and not path.is_symlink():
                pending.append(path)
    if any(p.is_symlink() for p in entries):
        raise ValueError('symlink in package')
    if any(not p.is_file() and not p.is_dir() for p in entries):
        raise ValueError('non-regular file in package')
    actual = {p.relative_to(ROOT).as_posix() for p in entries if p.is_file()}
    if actual != set(expected) | {'SHA256SUMS'}:
        raise ValueError('package file list differs from SHA256SUMS')
    for name, digest in expected.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'hash mismatch: {name}')
    payload = (ROOT / 'data/KanjiVGStrokes.json').read_bytes()
    data = json.loads(payload)
    problems = convert.validate(data)
    chars = [g['character'] for g in data['kanji']]
    if len(chars) != 205 or chars != list(convert.CHARACTERS.read_text(encoding='utf-8').strip()):
        problems.append('205-character count/order mismatch')
    source = data['source']
    if (source['release'], source['archive'], source['archiveSHA256']) != (
        convert.RELEASE, convert.ARCHIVE, convert.ARCHIVE_SHA256
    ):
        problems.append('source version mismatch')
    if problems:
        raise ValueError('; '.join(problems))
    if args.app_json is not None and args.app_json.read_bytes() != payload:
        raise ValueError('app JSON differs from published JSON')
    print(f"OK: {len(actual)} files, 205 characters, {sum(g['strokeCount'] for g in data['kanji'])} strokes")
    print('JSON SHA-256:', hashlib.sha256(payload).hexdigest())
    if args.app_json is not None:
        print('OK: app JSON and published JSON are byte-identical')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f'NG: {error}')

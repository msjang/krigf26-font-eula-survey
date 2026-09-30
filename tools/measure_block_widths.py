#!/usr/bin/env python3
"""글꼴마다 문자 블록별 advance width 를 em 기준으로 잰다.

무엇을 묻는 물음인가
  글꼴이 없어 다른 글꼴로 대체될 때 **조판 폭이 유지되는가**. 한글·한자·가나가
  모두 1 em 고정이라면 대체되어도 줄바꿈이 그대로다. 라틴만 어긋난다.
  그 전제가 실제로 성립하는지를 글꼴 전수로 확인한다.

무엇을 재나
  블록마다 `advance width / unitsPerEm` 의 고유값 개수와 최빈값을 낸다.
  고유값이 1개면 그 블록은 고정폭이다.

무엇을 하지 않나
  글꼴을 고치지 않는다. 규격이 정한 자리(`hmtx`·`head`)의 값을 읽을 뿐이다.

사용법
  python3 measure_block_widths.py <디렉터리 또는 파일> [...] [--json]
"""

import argparse
import collections
import glob
import json
import os
import sys

from fontTools.ttLib import TTFont, TTCollection

BLOCKS = [
    ("한글", 0xAC00, 0xD7A3),
    ("한자", 0x4E00, 0x9FFF),
    ("히라가나", 0x3040, 0x309F),
    ("가타카나", 0x30A0, 0x30FF),
    ("전각기호", 0x3000, 0x303F),
    ("ASCII", 0x20, 0x7E),
]
EXT = (".ttf", ".otf", ".ttc", ".otc")


def faces(path):
    if path.lower().endswith((".ttc", ".otc")):
        for i, f in enumerate(TTCollection(path).fonts):
            yield i, f
    else:
        yield 0, TTFont(path, lazy=True)


def measure(font):
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upem = font["head"].unitsPerEm
    out = {}
    for name, lo, hi in BLOCKS:
        cps = [c for c in range(lo, hi + 1) if c in cmap]
        if not cps:
            out[name] = None
            continue
        widths = collections.Counter(hmtx[cmap[c]][0] for c in cps)
        top, n = widths.most_common(1)[0]
        out[name] = {"chars": len(cps), "unique": len(widths),
                     "em": round(top / upem, 4), "share": round(n / len(cps), 4)}
    return upem, out


def family(font):
    for nid in (16, 1):
        for rec in font["name"].names:
            if rec.nameID == nid:
                try:
                    return rec.toUnicode()
                except Exception:
                    pass
    return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-hangul", type=int, default=1000,
                    help="한글 음절이 이보다 적은 글꼴은 건너뛴다")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        p = os.path.expanduser(p)
        files.extend(sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True))
                     if os.path.isdir(p) else [p])
    rows, seen = [], set()
    for path in files:
        if not path.lower().endswith(EXT):
            continue
        try:
            for idx, font in faces(path):
                fam = family(font)
                if fam in seen:
                    font.close()
                    continue
                upem, blocks = measure(font)
                font.close()
                if not blocks["한글"] or blocks["한글"]["chars"] < args.min_hangul:
                    continue
                seen.add(fam)
                rows.append({"family": fam, "file": os.path.basename(path),
                             "upem": upem, "blocks": blocks})
        except Exception:
            continue

    rows.sort(key=lambda r: (r["blocks"]["한글"]["em"], r["family"]))
    if args.json:
        json.dump({"blocks": [b[0] for b in BLOCKS], "fonts": rows},
                  sys.stdout, ensure_ascii=False, indent=1)
        return

    print(f"{'글꼴':22s} {'upem':>5s} " +
          " ".join(f"{b[0]:>10s}" for b in BLOCKS))
    for r in rows:
        cells = []
        for name, _, _ in BLOCKS:
            b = r["blocks"][name]
            if not b:
                cells.append(f"{'—':>10s}")
            elif b["unique"] == 1:
                cells.append(f"{b['em']:>10.3f}")
            else:
                cells.append(f"{'가변('+str(b['unique'])+')':>10s}")
        print(f"{r['family'][:22]:22s} {r['upem']:5d} " + " ".join(cells))
    print(f"\n{len(rows)}종. 숫자는 그 블록의 폭(em)이고 고유값이 하나일 때만 적었다",
          file=sys.stderr)


if __name__ == "__main__":
    main()

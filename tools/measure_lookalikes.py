#!/usr/bin/env python3
"""눈으로 구분하기 어려운 문자들의 폭과 세로 위치를 글꼴별로 잰다.

왜 재나
  문서를 쓰는 사람은 **모양을 보고 고른다.** 가운뎃점처럼 보이는 문자가 여럿
  있고, 조금 작아 보이면 더 작은 불릿을 쓰기도 한다. 말줄임표도 점이 바닥에
  깔린 것과 가운데 있는 것이 따로 있다. 그렇게 고른 문자마다 **폭이 다르면
  글꼴이 바뀔 때 조판이 어긋난다.**

무엇을 재나
  advance width(em)와 **잉크의 세로 중심**(em, 0이 베이스라인). 세로 중심은
  같은 문자라도 글꼴에 따라 점이 바닥에 깔리는지 가운데 오는지를 말해 준다.

  그리고 그 문자가 **KS X 1001(1987) 완성형에 있었는지**를 함께 적는다.
  한글 글꼴은 이 국가 표준에 맞춰 만들어졌다. 표준 안에 있던 문자는 모든
  글꼴이 갖고 폭도 안정적인데, 밖에 있던 문자는 제작자가 각자 넣어서
  있거나 없고 폭도 흔들린다. 그 경계가 위험의 경계다.

주의
  문자는 **코드포인트에서 만든다**(`chr()`). 원본에 글자를 직접 적으면
  `U+318D ㆍ` 와 `U+11A2 ᆞ` 처럼 비슷하게 생긴 것을 잘못 넣기 쉽다.

사용법
  python3 measure_lookalikes.py --fonts <디렉터리 또는 파일> [...] [--json]
"""

import argparse
import glob
import json
import os
import sys
import unicodedata
import warnings

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont, TTCollection

warnings.filterwarnings("ignore")

GROUPS = [
    ("가운뎃점처럼 보이는 것", [
        0x00B7,   # MIDDLE DOT — 한국 공문서가 실제로 쓰는 것
        0x0387,   # GREEK ANO TELEIA — 모양이 같다
        0x2022,   # BULLET
        0x2027,   # HYPHENATION POINT
        0x2219,   # BULLET OPERATOR
        0x22C5,   # DOT OPERATOR
        0x25CF,   # BLACK CIRCLE
        0x25CB,   # WHITE CIRCLE
        0x25E6,   # WHITE BULLET
        0x30FB,   # KATAKANA MIDDLE DOT
        0xFF65,   # HALFWIDTH KATAKANA MIDDLE DOT
        0x318D,   # HANGUL LETTER ARAEA — 홀로 쓰는 아래아
        0x11A2,   # HANGUL JUNGSEONG ARAEA — 조합용. 폭 0 이 정상이다
        0x002E,   # FULL STOP — 대조용
    ]),
    ("말줄임표처럼 보이는 것", [
        0x2026,   # HORIZONTAL ELLIPSIS
        0x22EF,   # MIDLINE HORIZONTAL ELLIPSIS
        0x2025,   # TWO DOT LEADER
        0x2024,   # ONE DOT LEADER
        0x22EE,   # VERTICAL ELLIPSIS
        0xFE19,   # PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS
    ]),
]
EXT = (".ttf", ".otf", ".ttc", ".otc")


def load(paths):
    fonts = {}
    for p in paths:
        p = os.path.expanduser(p)
        for path in (sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True))
                     if os.path.isdir(p) else glob.glob(p)):
            if not path.lower().endswith(EXT):
                continue
            try:
                items = (TTCollection(path).fonts
                         if path.lower().endswith((".ttc", ".otc"))
                         else [TTFont(path, lazy=True)])
            except Exception:
                continue
            for f in items:
                try:
                    name = next(r.toUnicode() for r in f["name"].names
                                if r.nameID == 1)
                except Exception:
                    continue
                fonts.setdefault(name, f)
    return fonts


def in_ksx1001(cp):
    """KS X 1001(1987) 완성형에 그 문자가 있었나. euc-kr 코덱이 그 대응을 담는다."""
    try:
        chr(cp).encode("euc_kr")
        return True
    except Exception:
        return False


def measure(font, cp):
    cmap = font.getBestCmap()
    if cp not in cmap:
        return None
    upem = font["head"].unitsPerEm
    g = cmap[cp]
    width = font["hmtx"][g][0] / upem
    mid = None
    try:
        pen = BoundsPen(font.getGlyphSet())
        font.getGlyphSet()[g].draw(pen)
        if pen.bounds:
            mid = (pen.bounds[1] + pen.bounds[3]) / 2 / upem
    except Exception:
        pass
    return {"em": round(width, 4),
            "inkMid": round(mid, 3) if mid is not None else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", nargs="+", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    fonts = load(args.fonts)
    if not fonts:
        sys.exit("글꼴을 찾지 못했다")

    out = []
    for title, cps in GROUPS:
        rows = []
        for cp in cps:
            row = {"cp": f"U+{cp:04X}", "char": chr(cp),
                   "name": unicodedata.name(chr(cp), "?"),
                   "category": unicodedata.category(chr(cp)),
                   "ksx1001": in_ksx1001(cp), "fonts": {}}
            for fam, font in fonts.items():
                row["fonts"][fam] = measure(font, cp)
            vals = {v["em"] for v in row["fonts"].values() if v}
            row["distinctWidths"] = len(vals)
            row["minEm"] = min(vals) if vals else None
            row["maxEm"] = max(vals) if vals else None
            row["missing"] = sum(1 for v in row["fonts"].values() if not v)
            rows.append(row)
        out.append({"group": title, "chars": rows})

    if args.json:
        json.dump({"fonts": list(fonts), "groups": out},
                  sys.stdout, ensure_ascii=False, indent=1)
        return

    names = list(fonts)
    print("값은  폭(em) / 잉크 세로중심(em, 0 = 베이스라인)\n")
    for g in out:
        print(f"### {g['group']}")
        print(f"{'코드':8s} {'글자':3s} {'KS':>3s} " + " ".join(f"{n[:10]:>11s}" for n in names)
              + "   폭 범위")
        for r in g["chars"]:
            cells = []
            for n in names:
                v = r["fonts"][n]
                cells.append("       없음" if not v else
                             f"{v['em']:5.3f}/{(v['inkMid'] if v['inkMid'] is not None else 0):+.2f}")
            span = ("—" if r["minEm"] is None
                    else f"{r['minEm']:.3f}~{r['maxEm']:.3f}"
                         + (f"  ({r['maxEm']/r['minEm']:.1f}배)" if r["minEm"] else ""))
            ks = " ○ " if r["ksx1001"] else " · "
            print(f"{r['cp']:8s} {r['char']:3s} {ks:>3s} "
                  + " ".join(f"{c:>11s}" for c in cells) + f"   {span}")
        print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""대체 연쇄를 문자 블록별로 따라가며 조판이 어디서 깨지는지 찾는다.

왜 블록별인가
  `fontinfo.dat` 은 대체 선언을 **언어별 섹션으로 나눠** 둔다. 한 문서의 한글과
  한자와 라틴이 서로 다른 연쇄를 탄다는 뜻이다. 그러니 "이 글꼴이 저 글꼴로
  바뀐다" 가 아니라 **"이 글꼴의 한글은 이리로, 한자는 저리로 간다"** 로 봐야 한다.

무엇을 재나
  연쇄의 각 단계에서 그 블록의 advance width(em)를 재고, **처음 값이 달라지는
  지점**을 찾는다. 그 지점이 줄바꿈과 쪽 수가 어긋나기 시작하는 곳이다.
  블록이 고정폭인지(고유 폭 1개) 가변인지도 함께 적는다.

무엇을 하지 않나
  HFT 는 열지 않는다. 공개 규격이 아니다. 연쇄가 TTF 에 닿은 뒤부터 잰다.

사용법
  python3 trace_subst_chain.py --fonts <글꼴 디렉터리> [...] [--start 굴림 바탕]
  python3 trace_subst_chain.py --fonts ... --json
"""

import argparse
import collections
import glob
import json
import os
import sys

from fontTools.ttLib import TTFont, TTCollection

MAC = "/Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared"

# 문자 블록 ↔ fontinfo.dat 의 섹션. 대체 연쇄가 이 단위로 따로 선언돼 있다
PARTITIONS = [
    ("한글", "Hangul", 0xAC00, 0xD7A3),
    ("한자", "Hanja", 0x4E00, 0x9FFF),
    ("가나", "Japanese", 0x3040, 0x30FF),
    ("전각기호", "Symbol", 0x3000, 0x303F),
    ("ASCII", "Latin", 0x20, 0x7E),
]
EXT = (".ttf", ".otf", ".ttc", ".otc")


def read_ini(path):
    with open(path, "rb") as fp:
        text = fp.read().decode("utf-16-le", "replace").lstrip("﻿")
    out, sec = {}, None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("["):
            sec = line.strip("[]")
            out[sec] = []
        elif sec:
            out[sec].append(line)
    return out


def subst_sections(root):
    """섹션마다 (이름, 형식) → (이름, 형식) 대응을 따로 만든다."""
    ini = read_ini(os.path.join(root, "Fonts", "fontinfo.dat"))
    tables = {}
    for sec, lines in ini.items():
        if not sec.startswith("Subst Fonts"):
            continue
        lang = sec.split("-")[-1].strip()
        table = {}
        for line in lines:
            if "=" not in line:
                continue
            left, right = line.split("=", 1)
            src = tuple(x.strip() for x in left.rsplit(",", 1))
            dst = tuple(x.strip() for x in right.split(",")[:2])
            if len(src) == 2 and len(dst) == 2:
                table.setdefault(src, dst)
        tables[lang] = table
    return tables


def aliases(font):
    """한 글꼴이 갖는 모든 이름. 한글 이름과 영문 이름이 따로 들어 있어
    `함초롬바탕` 과 `HCR Batang` 을 같은 것으로 이어 주려면 둘 다 필요하다."""
    out = set()
    for rec in font["name"].names:
        if rec.nameID in (1, 4, 16):
            try:
                v = rec.toUnicode().strip()
            except Exception:
                continue
            if v:
                out.add(v)
    return out


def width_index(dirs):
    """글꼴 이름 → 블록별 폭(em)·고유값 개수."""
    index = {}
    files = []
    for d in dirs:
        d = os.path.expanduser(d)
        files.extend(sorted(glob.glob(os.path.join(d, "**", "*"), recursive=True))
                     if os.path.isdir(d) else [d])
    for path in files:
        if not path.lower().endswith(EXT):
            continue
        try:
            fonts = (TTCollection(path).fonts
                     if path.lower().endswith((".ttc", ".otc"))
                     else [TTFont(path, lazy=True)])
        except Exception:
            continue
        for font in fonts:
            try:
                cmap = font.getBestCmap()
                hmtx = font["hmtx"]
                upem = font["head"].unitsPerEm
                blocks = {}
                for label, _, lo, hi in PARTITIONS:
                    cps = [c for c in range(lo, hi + 1) if c in cmap]
                    if not cps:
                        blocks[label] = None
                        continue
                    w = collections.Counter(hmtx[cmap[c]][0] for c in cps)
                    top, n = w.most_common(1)[0]
                    blocks[label] = {"em": round(top / upem, 4),
                                     "unique": len(w), "chars": len(cps)}
                for name in aliases(font):
                    index.setdefault(name, {"file": os.path.basename(path),
                                            "blocks": blocks})
            except Exception:
                pass
            finally:
                font.close()
    return index


def trace(tables, index, start, label, section, limit=12):
    """한 블록의 연쇄를 따라가며 각 단계의 폭을 붙인다."""
    table = tables.get(section, {})
    steps, cur, seen = [], start, {start}
    while len(steps) < limit:
        nxt = table.get(cur)
        if not nxt or nxt in seen:
            break
        seen.add(nxt)
        cur = nxt
        name, kind = cur
        info = index.get(name) if kind == "T" else None
        blk = info["blocks"].get(label) if info else None
        steps.append({
            "font": name,
            "type": "TTF" if kind == "T" else "HFT",
            "installed": bool(info),
            "em": blk["em"] if blk else None,
            "unique": blk["unique"] if blk else None,
            "covers": bool(blk),
        })
    return steps


def first_break(steps, base=None):
    """폭이 처음 달라지는 지점.

    기준은 **시작 글꼴 자신의 폭**이다. 시작이 HFT 라 잴 수 없으면 연쇄에서
    처음 잰 값을 기준으로 삼는다 — 그때는 HFT→첫 TTF 구간의 차이를 모른다.
    """
    for i, s in enumerate(steps):
        if s["em"] is None:
            continue
        if base is None:
            base = s["em"]
            continue
        if abs(s["em"] - base) > 1e-9:
            return i, base, s
    return None, base, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=MAC)
    ap.add_argument("--fonts", nargs="+", required=True,
                    help="설치 글꼴을 찾을 디렉터리")
    ap.add_argument("--start", nargs="*",
                    help="추적을 시작할 글꼴 이름 (없으면 선언된 전부)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = os.path.expanduser(args.root)
    tables = subst_sections(root)
    index = width_index(args.fonts)

    starts = set()
    for table in tables.values():
        starts.update(table.keys())
    if args.start:
        want = set(args.start)
        starts = {s for s in starts if s[0] in want}

    results = []
    for name, kind in sorted(starts):
        entry = {"font": name, "type": "TTF" if kind == "T" else "HFT",
                 "partitions": {}}
        for label, section, _, _ in PARTITIONS:
            steps = trace(tables, index, (name, kind), label, section)
            if not steps:
                continue
            own = index.get(name, {}).get("blocks", {}).get(label) if kind == "T" else None
            hop, base, bad = first_break(steps, own["em"] if own else None)
            entry["partitions"][label] = {
                "self": {"em": own["em"], "unique": own["unique"]} if own else None,
                "baseIsSelf": own is not None,
                "chain": steps,
                "breaksAt": hop,
                "baseEm": base,
                "breakTo": bad["font"] if bad else None,
                "breakEm": bad["em"] if bad else None,
            }
        if entry["partitions"]:
            results.append(entry)

    if args.json:
        json.dump({"source": "한컴오피스 fontinfo.dat · 설치 글꼴 실측",
                   "partitions": [p[0] for p in PARTITIONS],
                   "fonts": results}, sys.stdout, ensure_ascii=False, indent=1)
        return

    for r in results:
        print(f"\n■ {r['font']} [{r['type']}]")
        for label, info in r["partitions"].items():
            chain = " → ".join(
                f"{s['font']}"
                + (f"({s['em']:.3f})" if s["em"] is not None
                   else ("(HFT)" if s["type"] == "HFT"
                         else ("(미설치)" if not s["installed"] else "(미포함)")))
                for s in info["chain"])
            own = info["self"]
            head = f"{own['em']:.3f}" if own else "?"
            mark = ""
            if info["breaksAt"] is not None:
                mark = (f"   ⚠ {info['breaksAt']+1}번째에서 "
                        f"{info['baseEm']:.3f} → {info['breakEm']:.3f}")
            print(f"   {label:6s} [{head}] {chain}{mark}")


if __name__ == "__main__":
    main()

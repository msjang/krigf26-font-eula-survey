#!/usr/bin/env python3
"""메트릭 호환 폰트(MCF)와 원본 폰트를 비교한다.

무엇을 보려는가
  MCF의 성립 조건은 두 가지가 동시에 참인 것이다.
    (1) 배치 수치(advance width, 수직 메트릭)가 원본과 일치한다  -> 레이아웃이 보존된다
    (2) 글리프 윤곽선은 원본과 다르다                            -> 원본의 표현을 복제하지 않는다
  대법원 2001. 6. 29. 선고 99다23246은 서체파일의 보호 대상을
  "윤곽선의 제어점들의 좌표값과 그 지시·명령어의 선택"으로 특정하고
  침해 판단 기준을 소스코드 동일성으로 삼았다. (2)는 그 층위를 비켜간다는 사실을,
  (1)은 그럼에도 실용적 목적이 달성된다는 사실을 각각 수치로 보인다.

무엇을 하지 않는가
  원본 폰트를 개변하지 않는다. 두 파일을 각각 규격대로 읽어 수치를 대조할 뿐이다.

사용법
  python3 metric_compat.py <원본.ttf> <MCF.ttf> [--json]
  python3 metric_compat.py --pairs pairs.json
"""

import argparse
import json
import sys
import unicodedata

from fontTools.ttLib import TTFont, TTCollection

# 라틴 본문에서 실제로 조판 폭을 좌우하는 문자 집합
SAMPLE = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    " .,;:!?'\"()[]{}-–—/\\@#$%&*+=<>"
)


def load(path):
    if path.lower().endswith((".ttc", ".otc")):
        return TTCollection(path, lazy=True).fonts[0]
    return TTFont(path, fontNumber=0, lazy=True)


def advance_widths(font):
    """문자 -> advance width(폰트 단위, upem 정규화 전)"""
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    out = {}
    for ch in SAMPLE:
        name = cmap.get(ord(ch))
        if name and name in hmtx.metrics:
            out[ch] = hmtx.metrics[name][0]
    return out


def vertical_metrics(font):
    out = {}
    try:
        hhea = font["hhea"]
        out["hhea.ascender"] = hhea.ascender
        out["hhea.descender"] = hhea.descender
        out["hhea.lineGap"] = hhea.lineGap
    except Exception:
        pass
    try:
        os2 = font["OS/2"]
        out["OS/2.sTypoAscender"] = os2.sTypoAscender
        out["OS/2.sTypoDescender"] = os2.sTypoDescender
        out["OS/2.sTypoLineGap"] = os2.sTypoLineGap
        out["OS/2.usWinAscent"] = os2.usWinAscent
        out["OS/2.usWinDescent"] = os2.usWinDescent
    except Exception:
        pass
    return out


def outline_signature(font, ch):
    """한 문자의 윤곽선 제어점 좌표 목록. 표현(expression) 층위의 비교용."""
    cmap = font.getBestCmap()
    name = cmap.get(ord(ch))
    if not name:
        return None
    try:
        glyf = font["glyf"]
    except KeyError:
        return None  # CFF(OTF)는 glyf가 없다
    glyph = glyf[name]
    if glyph.numberOfContours <= 0:
        return None
    coords, _, _ = glyph.getCoordinates(glyf)
    return [tuple(pt) for pt in coords]


def compare(original_path, mcf_path, tolerance=1.0):
    """tolerance: em당 1000 단위로 정규화한 뒤 허용할 차이.

    두 폰트의 unitsPerEm이 다르면(예: 2048 대 1000) 정수 격자 자체가 달라
    완전 일치는 원리상 불가능하다. 1000 단위로 환산한 뒤 tolerance 이내면
    같은 것으로 본다. 기본값 1.0은 본문 10pt 기준 약 0.01pt로, 조판 결과에
    영향을 주지 않는 범위다.
    """
    a, b = load(original_path), load(mcf_path)
    upem_a = a["head"].unitsPerEm
    upem_b = b["head"].unitsPerEm

    def norm(value, upem):
        return value * 1000.0 / upem

    def close(x, y):
        return abs(norm(x, upem_a) - norm(y, upem_b)) <= tolerance

    wa, wb = advance_widths(a), advance_widths(b)
    common = sorted(set(wa) & set(wb))
    same = [c for c in common if close(wa[c], wb[c])]
    diff = [(c, wa[c], wb[c], round(norm(wa[c], upem_a) - norm(wb[c], upem_b), 2))
            for c in common if not close(wa[c], wb[c])]

    va, vb = vertical_metrics(a), vertical_metrics(b)
    vkeys = sorted(set(va) & set(vb))
    vsame = [k for k in vkeys if close(va[k], vb[k])]
    vdiff = [(k, va[k], vb[k], round(norm(va[k], upem_a) - norm(vb[k], upem_b), 2))
             for k in vkeys if not close(va[k], vb[k])]

    # 윤곽선 비교 — 같은 문자에 대해 제어점 좌표가 일치하는지
    outline_same, outline_diff, outline_skip = [], [], []
    for ch in "AEHMOSaenos0123":
        sa, sb = outline_signature(a, ch), outline_signature(b, ch)
        if sa is None or sb is None:
            outline_skip.append(ch)
        elif sa == sb:
            outline_same.append(ch)
        else:
            outline_diff.append((ch, len(sa), len(sb)))

    a.close(); b.close()
    return {
        "original": original_path,
        "mcf": mcf_path,
        "unitsPerEm": {"original": upem_a, "mcf": upem_b},
        "advanceWidth": {
            "compared": len(common),
            "identical": len(same),
            "different": len(diff),
            "differences": diff[:20],
        },
        "verticalMetrics": {
            "compared": len(vkeys),
            "identical": len(vsame),
            "different": len(vdiff),
            "differences": vdiff,
        },
        "outlines": {
            "comparedChars": len(outline_same) + len(outline_diff),
            "identical": len(outline_same),
            "different": len(outline_diff),
            "identicalChars": outline_same,
            "pointCounts": outline_diff[:20],
            "skipped": outline_skip,
        },
    }


def render(result):
    aw = result["advanceWidth"]
    vm = result["verticalMetrics"]
    ol = result["outlines"]
    pct = (100 * aw["identical"] // aw["compared"]) if aw["compared"] else 0
    print(f"\n원본 : {result['original']}")
    print(f"MCF  : {result['mcf']}")
    print(f"upem : 원본 {result['unitsPerEm']['original']} / MCF {result['unitsPerEm']['mcf']}")
    print(f"  advance width  {aw['identical']}/{aw['compared']} 일치 ({pct}%)")
    if aw["differences"]:
        print("     불일치:", ", ".join(f"{c!r} {x}->{y} (Δ{d})" for c, x, y, d in aw["differences"][:8]))
    print(f"  수직 메트릭     {vm['identical']}/{vm['compared']} 일치")
    if vm["differences"]:
        for k, x, y, d in vm["differences"]:
            print(f"     {k}: 원본 {x} / MCF {y} (Δ{d})")
    if ol["comparedChars"]:
        print(f"  글리프 윤곽선   {ol['different']}/{ol['comparedChars']} 문자에서 제어점 좌표 상이"
              + (f"  (동일: {ol['identicalChars']})" if ol["identicalChars"] else "  (동일한 문자 없음)"))
    else:
        print(f"  글리프 윤곽선   비교 불가 (CFF/OTF 등) — 건너뜀 {ol['skipped']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original", nargs="?")
    ap.add_argument("mcf", nargs="?")
    ap.add_argument("--pairs", help="[[label, original, mcf], ...] 형태의 JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results = []
    if args.pairs:
        for label, orig, mcf in json.load(open(args.pairs)):
            res = compare(orig, mcf)
            res["label"] = label
            results.append(res)
            if not args.json:
                print(f"\n{'='*70}\n[{label}]", end="")
                render(res)
    elif args.original and args.mcf:
        res = compare(args.original, args.mcf)
        results.append(res)
        if not args.json:
            render(res)
    else:
        sys.exit(__doc__)

    if args.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()

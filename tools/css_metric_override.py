#!/usr/bin/env python3
"""폰트를 만들지 않고 CSS 만으로 메트릭을 맞출 수 있는 범위를 계산한다.

CSS `@font-face` 는 `size-adjust` 로 글꼴을 비례 확대·축소하고,
`unicode-range` 로 그 규칙이 적용될 문자 구간을 한정한다. 같은 family 이름으로
구간별 규칙을 여러 개 선언하면 **문자마다 다른 배율**을 줄 수 있다.

이 스크립트는 원본 글꼴과 대체 글꼴을 받아
  - 문자마다 필요한 배율(원본 advance / 대체 advance)을 구하고
  - 허용오차 안에서 묶어 `@font-face` 규칙을 생성하고
  - 배율이 크게 벗어나 시각적으로 어색해질 문자를 따로 뽑는다

마지막 항목이 핵심이다. `size-adjust` 는 폭만이 아니라 **글리프 크기도 함께**
바꾸므로, 폭을 정확히 맞추려 들면 그 글자만 크거나 작게 그려진다. 그런 문자는
CSS 로 해결하지 말고 **직접 그려서 얹는 편**이 낫다. 몇 자인지, 얼마나 복잡한지를
세어 그 판단의 근거를 준다.

사용법
  pip install fonttools
  python3 css_metric_override.py <설정.json> [--json] [--css]

설정 형식
  {"original": "굴림", "originalPath": "...", "originalFace": null,
   "fallback": "Noto Sans CJK KR", "fallbackPath": "...", "fallbackFace": null,
   "familyName": "굴림호환", "tolerance": 0.005, "outlierThreshold": 0.10}
"""

import collections
import json
import sys

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont, TTCollection

# 공문서에 실제로 나타나는 문자 집합
def default_charset():
    chars = set(chr(c) for c in range(0xAC00, 0xD7A4))   # 한글 음절 11,172자
    chars |= set(chr(c) for c in range(0x20, 0x7F))      # ASCII
    chars |= set("·…‘’“”〔〕《》「」→←↑↓※○●◎△▲▽▼□■◇◆")
    chars |= set("₩％℃㎡㎏㎞㎖①②③④⑤⑥⑦⑧⑨⑩ⅠⅡⅢⅣⅤ")
    chars |= set("一二三四五六七八九十百千萬國家民主共和年月日時分長官部處廳課")
    return chars


def load(path, face=None):
    if path.lower().endswith((".ttc", ".otc")):
        for f in TTCollection(path).fonts:
            names = {n.toUnicode() for n in f["name"].names if n.nameID in (1, 6)}
            if face is None or face in names:
                return f
        return None
    return TTFont(path)


def reader(f):
    upem = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    gs = f.getGlyphSet()

    def width(ch):
        n = cmap.get(ord(ch))
        return hmtx[n][0] / upem if n else None

    def points(ch):
        """글리프의 제어점 수. 직접 그릴 때의 품이 얼마나 되는지 가늠용."""
        n = cmap.get(ord(ch))
        if not n:
            return None
        pen = DecomposingRecordingPen(gs)
        gs[n].draw(pen)
        total = 0
        for op, args in pen.value:
            if op in ("moveTo", "lineTo"):
                total += 1
            elif op == "qCurveTo":
                total += len([a for a in args if a is not None])
            elif op == "curveTo":
                total += len(args)
        return total

    return width, points, upem


def vertical_overrides(orig, fallback):
    """ascent/descent/line-gap 재정의 값. 원본의 수직 메트릭을 em 비율로 낸다."""
    o = orig["hhea"]
    u = orig["head"].unitsPerEm
    return {"ascent-override": f"{o.ascent / u * 100:.2f}%",
            "descent-override": f"{abs(o.descent) / u * 100:.2f}%",
            "line-gap-override": f"{o.lineGap / u * 100:.2f}%"}


def to_unicode_range(codepoints):
    """연속된 코드포인트를 U+AC00-D7A3 형태로 압축한다."""
    cps = sorted(codepoints)
    out, start, prev = [], cps[0], cps[0]
    for c in cps[1:]:
        if c == prev + 1:
            prev = c
            continue
        out.append((start, prev))
        start = prev = c
    out.append((start, prev))
    return ", ".join(f"U+{a:04X}" if a == b else f"U+{a:04X}-{b:04X}"
                     for a, b in out)


def main(argv):
    as_json = "--json" in argv
    as_css = "--css" in argv
    paths = [x for x in argv if not x.startswith("--")]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))

    a = load(cfg["originalPath"], cfg.get("originalFace"))
    b = load(cfg["fallbackPath"], cfg.get("fallbackFace"))
    if a is None or b is None:
        sys.exit("face 를 찾지 못했다")
    aw, _, _ = reader(a)
    bw, bp, _ = reader(b)

    tol = cfg.get("tolerance", 0.005)
    thr = cfg.get("outlierThreshold", 0.10)
    family = cfg.get("familyName", "호환글꼴")

    ratios = {}
    for ch in default_charset():
        x, y = aw(ch), bw(ch)
        if x and y and y > 0:
            ratios[ch] = x / y
    if not ratios:
        sys.exit("두 글꼴에 공통으로 있는 문자가 없다")

    # 지배적 배율 — 가장 많은 문자가 요구하는 값. 시각적 기준이 된다
    counts = collections.Counter(round(v, 6) for v in ratios.values())
    dominant = counts.most_common(1)[0][0]

    # 허용오차 안에서 묶기
    groups, order = [], sorted(ratios.items(), key=lambda kv: kv[1])
    cur = [order[0]]
    for ch, r in order[1:]:
        if (r - cur[0][1]) / cur[0][1] <= tol:
            cur.append((ch, r))
        else:
            groups.append(cur)
            cur = [(ch, r)]
    groups.append(cur)

    rules = []
    for g in sorted(groups, key=lambda x: -len(x)):
        adj = sum(r for _, r in g) / len(g)
        rules.append({"sizeAdjust": round(adj * 100, 2), "chars": len(g),
                      "unicodeRange": to_unicode_range([ord(c) for c, _ in g])})

    outliers = []
    for ch, r in ratios.items():
        dev = abs(r - dominant) / dominant
        if dev > thr:
            outliers.append({"char": ch, "codepoint": f"U+{ord(ch):04X}",
                             "ratio": round(r * 100, 1),
                             "deviationPct": round(dev * 100, 1),
                             "points": bp(ch)})
    outliers.sort(key=lambda x: -x["deviationPct"])
    pts = sum(o["points"] or 0 for o in outliers)

    result = {
        "original": cfg["original"], "fallback": cfg["fallback"],
        "familyName": family, "tolerance": tol, "outlierThreshold": thr,
        "charsCompared": len(ratios),
        "dominantSizeAdjust": round(dominant * 100, 2),
        "dominantCoverage": round(100 * counts[dominant] / len(ratios), 2),
        "ruleCount": len(rules), "rules": rules,
        "verticalOverrides": vertical_overrides(a, b),
        "outlierCount": len(outliers), "outlierPoints": pts,
        "outliers": outliers,
    }

    if as_css:
        v = result["verticalOverrides"]
        print(f"/* {cfg['original']} 호환 — {cfg['fallback']} 기반, "
              f"규칙 {len(rules)}개, 직접 그려야 할 글자 {len(outliers)}자 */")
        for r in rules:
            print(f"@font-face {{\n  font-family: \"{family}\";\n"
                  f"  src: local(\"{cfg['fallback']}\");\n"
                  f"  size-adjust: {r['sizeAdjust']}%;\n"
                  f"  ascent-override: {v['ascent-override']};\n"
                  f"  descent-override: {v['descent-override']};\n"
                  f"  line-gap-override: {v['line-gap-override']};\n"
                  f"  unicode-range: {r['unicodeRange']};\n}}")
        return
    if as_json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return

    print(f"{cfg['original']} → {cfg['fallback']} · 비교 문자 {len(ratios):,}자")
    print(f"지배적 배율 {result['dominantSizeAdjust']}% 가 "
          f"{result['dominantCoverage']}% 를 덮는다")
    print(f"허용오차 {tol * 100:.1f}% 기준 @font-face {len(rules)}개")
    print()
    print("| size-adjust | 문자 수 | 비율 |")
    print("|---:|---:|---:|")
    for r in rules[:10]:
        print(f"| {r['sizeAdjust']}% | {r['chars']:,} | "
              f"{100 * r['chars'] / len(ratios):.2f}% |")
    if len(rules) > 10:
        print(f"| … 외 {len(rules) - 10}개 | | |")
    print()
    print(f"지배적 배율에서 {thr * 100:.0f}% 넘게 벗어나는 문자: "
          f"**{len(outliers)}자**, 제어점 합계 **{pts:,}개**")
    print(" ".join(o["char"] for o in outliers))


if __name__ == "__main__":
    main(sys.argv[1:])

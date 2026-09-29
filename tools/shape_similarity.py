#!/usr/bin/env python3
"""MCF 와 원본 글꼴의 글리프가 얼마나 닮았는지 세 층위로 잰다.

`metric_compat.py` 는 "좌표가 같은가" 를 본다. 그 값이 0 이라는 것은
**베끼지 않았다**는 뜻이지 **달라 보인다**는 뜻이 아니다. 전체를 1유닛씩
평행이동해도 좌표 일치는 0 이 되기 때문이다.

그래서 질문에 따라 다른 측정이 필요하다.

  좌표 동일성   99다23246 이 침해 기준으로 삼은 층위.
                "소스코드가 동일하면 의존하여 작성된 것으로 추정" — 법적 질문
  점 개수 동일성 평행이동·확대축소 같은 아핀 변환 복제인지 가린다.
                점 개수가 다르면 변환한 사본이 아니라 다시 그린 것이다
  래스터 겹침    각 글리프를 자기 bbox 에 맞춰 정규화해 렌더링하고
                교집합/합집합(IoU)을 낸다. 사람이 같은 계열로 보는지의 근사치 — 시장 질문

세 값은 서로 대체하지 못한다. 어느 질문에 답하려는지에 따라 골라 써야 한다.

사용법
  pip install fonttools pillow
  python3 shape_similarity.py <설정.json> [--json]

설정 형식
  {"pairs": [{"original": "Arial", "originalPath": "...",
              "mcf": "Liberation Sans", "mcfPath": "...",
              "originalFace": null, "mcfFace": null}],
   "chars": "AaBb..."}
"""

import json
import sys

from PIL import Image, ImageDraw
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont, TTCollection

RASTER = 256      # 래스터 한 변(px)
MARGIN = 4        # 여백(px)
CURVE_STEPS = 12  # 곡선 하나를 나눌 직선 수
DEFAULT_CHARS = "AaBbCcEeGgMmNnRrSsWw0248?&@"


def pick_face(path, face):
    fonts = (TTCollection(path).fonts
             if path.lower().endswith((".ttc", ".otc")) else [TTFont(path)])
    for f in fonts:
        if face is None:
            return f
        names = {n.toUnicode() for n in f["name"].names if n.nameID in (1, 6)}
        if face in names:
            return f
    return None


def _quad(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(1, n + 1))]


def _cubic(p0, p1, p2, p3, n):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0]
             + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1]
             + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1])
            for t in (i / n for i in range(1, n + 1))]


def flatten(recorded):
    """기록된 경로를 직선 다각형 목록으로 편다."""
    polys, cur = [], []
    for op, args in recorded:
        if op == "moveTo":
            if len(cur) > 2:
                polys.append(cur)
            cur = [tuple(args[0])]
        elif op == "lineTo":
            cur.append(tuple(args[0]))
        elif op == "qCurveTo":
            pts = [tuple(a) for a in args if a is not None]
            p0 = cur[-1]
            for i in range(len(pts) - 1):
                ctrl = pts[i]
                end = (pts[i + 1] if i == len(pts) - 2 else
                       ((pts[i][0] + pts[i + 1][0]) / 2,
                        (pts[i][1] + pts[i + 1][1]) / 2))
                cur += _quad(p0, ctrl, end, CURVE_STEPS)
                p0 = end
        elif op == "curveTo":
            pts = [tuple(a) for a in args]
            cur += _cubic(cur[-1], pts[0], pts[1], pts[2], CURVE_STEPS)
        elif op == "closePath":
            if len(cur) > 2:
                polys.append(cur)
            cur = []
    if len(cur) > 2:
        polys.append(cur)
    return polys


def render(font, char):
    """글리프를 자기 bbox 에 맞춰 정규화해 렌더링한다.

    정규화하는 이유: 폰트마다 upem 과 글자 크기가 달라서, 그대로 겹치면
    크기 차이가 모양 차이로 잘못 잡힌다. 여기서 재려는 것은 형태다.
    """
    cmap = font.getBestCmap()
    name = cmap.get(ord(char))
    if not name:
        return None
    pen = DecomposingRecordingPen(font.getGlyphSet())
    font.getGlyphSet()[name].draw(pen)
    polys = flatten(pen.value)
    if not polys:
        return None
    xs = [p[0] for pl in polys for p in pl]
    ys = [p[1] for pl in polys for p in pl]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    if w <= 0 or h <= 0:
        return None
    scale = (RASTER - 2 * MARGIN) / max(w, h)
    img = Image.new("1", (RASTER, RASTER), 0)
    draw = ImageDraw.Draw(img)
    for pl in polys:
        draw.polygon([(MARGIN + (x - min(xs)) * scale,
                       RASTER - MARGIN - (y - min(ys)) * scale) for x, y in pl],
                     fill=1)
    return {"image": img, "contours": len(polys),
            "points": sum(len(pl) for pl in polys)}


def raw_coords(font, char):
    """정규화 전 원시 좌표. 좌표 동일성 판정용."""
    cmap = font.getBestCmap()
    name = cmap.get(ord(char))
    glyf = font.get("glyf")
    if not name or glyf is None:
        return None
    try:
        g = glyf[name]
    except Exception:
        return None
    if g.numberOfContours <= 0:
        return None
    return [tuple(c) for c in g.getCoordinates(glyf)[0]]


def compare(a, b, chars):
    rows = []
    for ch in chars:
        ra, rb = render(a, ch), render(b, ch)
        if not ra or not rb:
            continue
        # mode "1" 은 비트를 묶어 저장하므로 "L" 로 펴서 바이트 단위로 비교한다
        pa = ra["image"].convert("L").tobytes()
        pb = rb["image"].convert("L").tobytes()
        inter = sum(1 for x, y in zip(pa, pb) if x and y)
        union = sum(1 for x, y in zip(pa, pb) if x or y)
        ca, cb = raw_coords(a, ch), raw_coords(b, ch)
        rows.append({
            "char": ch,
            "sameCoords": bool(ca and cb and ca == cb),
            "pointsOriginal": ra["points"], "pointsMcf": rb["points"],
            "samePointCount": ra["points"] == rb["points"],
            "iou": round(inter / union, 4) if union else 0.0,
        })
    return rows


def main(argv):
    as_json = "--json" in argv
    paths = [x for x in argv if x != "--json"]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))
    chars = cfg.get("chars", DEFAULT_CHARS)

    out = {"raster": RASTER, "chars": chars, "pairs": []}
    for spec in cfg["pairs"]:
        a = pick_face(spec["originalPath"], spec.get("originalFace"))
        b = pick_face(spec["mcfPath"], spec.get("mcfFace"))
        if a is None or b is None:
            print(f"# face 를 찾지 못했다: {spec['original']}", file=sys.stderr)
            continue
        rows = compare(a, b, chars)
        ious = [r["iou"] for r in rows]
        out["pairs"].append({
            "original": spec["original"], "mcf": spec["mcf"],
            "glyphs": len(rows),
            "sameCoordsCount": sum(r["sameCoords"] for r in rows),
            "samePointCountCount": sum(r["samePointCount"] for r in rows),
            "iouMean": round(sum(ious) / len(ious), 4) if ious else 0,
            "iouMin": round(min(ious), 4) if ious else 0,
            "iouMax": round(max(ious), 4) if ious else 0,
            "glyphRows": rows,
        })

    if as_json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return

    print(f"글리프 {len(chars)}자 · 래스터 {RASTER}px · 각 글리프를 자기 bbox 로 정규화")
    print()
    print("| 원본 → MCF | 글자 | 좌표 동일 | 점 개수 동일 | 래스터 겹침 평균 | 최소 | 최대 |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for p in out["pairs"]:
        print(f"| {p['original']} → **{p['mcf']}** | {p['glyphs']} | "
              f"**{p['sameCoordsCount']}** | {p['samePointCountCount']} | "
              f"**{p['iouMean'] * 100:.1f}%** | {p['iouMin'] * 100:.1f}% | "
              f"{p['iouMax'] * 100:.1f}% |")


if __name__ == "__main__":
    main(sys.argv[1:])

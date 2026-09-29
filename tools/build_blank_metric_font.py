#!/usr/bin/env python3
"""조판 수치만 담고 글리프는 비운 폰트를 만든다 — '투명 도화지' 폰트.

무엇을 만드나
  모든 글리프의 윤곽선이 비어 있고 advance width 만 원본과 같은 폰트다.
  화면에는 아무것도 나타나지 않지만, 줄바꿈과 쪽 수는 원본과 똑같이 나온다.

무엇에 쓰나
  쪽 수·줄 수 계산, 서식 회귀 시험, 대체 글꼴 후보 평가처럼
  **배치만 알면 되고 모양은 필요 없는 작업**이다.
  읽을 수 없으므로 원본 글꼴을 대신하는 용도로는 쓸 수 없다.

무엇이 들어가고 무엇이 안 들어가나
  들어간다   advance width, 수직 메트릭, (선택) 실측한 커닝 값
  안 들어간다 글리프 윤곽선. 제어점이 **하나도** 없다

  커닝은 원본의 lookup 구성을 가져오지 않는다. HarfBuzz 로 조판해
  `shape(XY) - adv(X) - adv(Y)` 로 **실효값을 측정**한 뒤, 그 숫자를
  이 스크립트가 짠 GPOS 규칙에 넣는다. 가져오는 것은 값뿐이다.

무엇을 하지 않나
  원본 폰트를 고치지 않는다. 규격이 정한 자리에서 수치를 읽을 뿐이다.

사용법
  pip install fonttools uharfbuzz
  python3 build_blank_metric_font.py <설정.json> [--verify]

설정 형식
  {"sourcePath": "...", "sourceFace": null,
   "familyName": "Metric Blank X", "psName": "MetricBlankX-Regular",
   "out": "MetricBlankX-Regular.ttf",
   "kerning": true}
"""

import itertools
import json
import os
import sys

import uharfbuzz as hb
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, TTCollection


def charset():
    """공문서에 실제로 나타나는 문자."""
    chars = [chr(c) for c in range(0xAC00, 0xD7A4)]          # 한글 음절
    chars += [chr(c) for c in range(0x20, 0x7F)]             # ASCII
    chars += list("·…‘’“”〔〕《》「」→←↑↓※○●◎△▲▽▼□■◇◆")
    chars += list("₩％℃①②③④⑤⑥⑦⑧⑨⑩")
    return chars


def load(path, face=None):
    if path.lower().endswith((".ttc", ".otc")):
        for i, f in enumerate(TTCollection(path).fonts):
            names = {n.toUnicode() for n in f["name"].names if n.nameID in (1, 6)}
            if face is None or face in names:
                return f, i
        return None, 0
    return TTFont(path), 0


def shaper(path, index):
    font = hb.Font(hb.Face(hb.Blob.from_file_path(path), index))

    def run(text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf)
        return sum(p.x_advance for p in buf.glyph_positions), len(buf.glyph_positions)

    return run


def measure_kerning(run, advances, letters):
    """실효 커닝을 잰다. 원본이 어떤 방식으로 구현했는지는 보지 않는다."""
    pairs = {}
    for x, y in itertools.product(letters, repeat=2):
        width, _ = run(x + y)
        delta = width - (advances[x] + advances[y])
        if delta:
            pairs[(x, y)] = delta
    return pairs


def build(cfg):
    src, index = load(cfg["sourcePath"], cfg.get("sourceFace"))
    if src is None:
        sys.exit("face 를 찾지 못했다")
    upem = src["head"].unitsPerEm
    cmap = src.getBestCmap()
    hmtx = src["hmtx"]

    chars = [c for c in charset() if ord(c) in cmap]
    adv = {c: hmtx[cmap[ord(c)]][0] for c in chars}
    name_of = lambda c: f"u{ord(c):04X}"

    kern = {}
    if cfg.get("kerning", True):
        run = shaper(cfg["sourcePath"], index)
        ascii_chars = [c for c in chars if 0x21 <= ord(c) < 0x7F]
        kern = measure_kerning(run, adv, ascii_chars)

    fb = FontBuilder(upem, isTTF=True)
    names = [".notdef"] + [name_of(c) for c in chars]
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({ord(c): name_of(c) for c in chars})

    empty = TTGlyphPen(None).glyph()          # 윤곽선 0개
    fb.setupGlyf({n: empty for n in names})

    metrics = {".notdef": (adv[chars[0]], 0)}
    metrics.update({name_of(c): (adv[c], 0) for c in chars})
    fb.setupHorizontalMetrics(metrics)

    hhea, os2 = src["hhea"], src["OS/2"]
    fb.setupHorizontalHeader(ascent=hhea.ascent, descent=hhea.descent,
                             lineGap=hhea.lineGap)
    fb.setupNameTable({
        "familyName": cfg["familyName"], "styleName": "Regular",
        "psName": cfg["psName"], "version": "Version 0.1",
        "copyright": ("Layout metrics measured per the OpenType specification. "
                      "Contains no glyph outlines."),
    })
    fb.setupOS2(sTypoAscender=os2.sTypoAscender, sTypoDescender=os2.sTypoDescender,
                sTypoLineGap=os2.sTypoLineGap, usWinAscent=os2.usWinAscent,
                usWinDescent=os2.usWinDescent, fsType=0)
    fb.setupPost()

    if kern:
        fea = ["languagesystem DFLT dflt;", "languagesystem latn dflt;",
               "feature kern {"]
        fea += [f"  pos {name_of(a)} {name_of(b)} {int(round(v))};"
                for (a, b), v in sorted(kern.items())]
        fea.append("} kern;")
        addOpenTypeFeaturesFromString(fb.font, "\n".join(fea))

    fb.save(cfg["out"])
    return {"chars": len(chars), "kernPairs": len(kern), "upem": upem,
            "bytes": os.path.getsize(cfg["out"])}


def verify(cfg):
    """원본과 조판 결과가 같은지 확인한다."""
    src, index = load(cfg["sourcePath"], cfg.get("sourceFace"))
    upem = src["head"].unitsPerEm
    a, b = shaper(cfg["sourcePath"], index), shaper(cfg["out"], 0)
    tests = [
        ("공문서 문단",
         "행정안전부는 2026년 9월 29일 공공문서 서식의 상호운용성 개선 방안을 "
         "발표하였다. 본문 글꼴로 지정된 굴림, 바탕, 돋움 등 9종에 대하여 "
         "메트릭 호환 대체 글꼴(Metric-Compatible Font, MCF)의 확보 필요성이 "
         "제기되었다. 붙임 1(추진계획) 참고."),
        ("라틴·커닝", "AVATAR To We Yo P. LT Wa Ty AWAY"),
        ("문장부호", "(v1.3) [Type A] {2026-09-29} 100%, 50;"),
    ]
    rows = []
    for label, text in tests:
        wa = a(text)[0] / upem
        wb = b(text)[0] / upem
        rows.append({"label": label, "sourceEm": round(wa, 4),
                     "blankEm": round(wb, 4), "delta": round(abs(wa - wb), 8)})
    return rows


def main(argv):
    paths = [x for x in argv if not x.startswith("--")]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))
    info = build(cfg)

    out = TTFont(cfg["out"])
    glyf = out["glyf"]
    points = sum(len(glyf[n].getCoordinates(glyf)[0])
                 for n in out.getGlyphOrder() if glyf[n].numberOfContours > 0)

    print(f"생성: {cfg['out']}  {info['bytes']:,} 바이트")
    print(f"  문자 {info['chars']:,}자 · upem {info['upem']} · "
          f"커닝 규칙 {info['kernPairs']}개")
    print(f"  윤곽선이 있는 글리프 "
          f"{sum(1 for n in out.getGlyphOrder() if glyf[n].numberOfContours > 0)}개 · "
          f"제어점 {points}개")

    if "--verify" in argv:
        print()
        print("| 시험 문자열 | 원본(em) | 투명본(em) | 차이 |")
        print("|---|---:|---:|---:|")
        for r in verify(cfg):
            print(f"| {r['label']} | {r['sourceEm']} | {r['blankEm']} | "
                  f"{r['delta']:.8f} |")


if __name__ == "__main__":
    main(sys.argv[1:])

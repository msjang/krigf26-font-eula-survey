#!/usr/bin/env python3
"""조판기가 실제로 내놓는 결과가 같은지 비교한다.

`metric_compat.py` 는 `hmtx` 의 advance width 만 본다. 그러나 실제 조판에서는
두 가지가 더 개입한다.

  커닝(GPOS)   특정 글자쌍이 붙을 때 간격을 좁히거나 넓힌다
  합자(GSUB)   `fi` 같은 연속이 한 글리프로 치환되어 폭이 두 폭의 합이 아니게 된다

advance width 를 전부 맞춰도 이 둘이 다르면 줄바꿈이 달라진다. 그래서
"메트릭 호환" 이 성립하는지는 **셰이핑 결과**로 확인해야 한다.

재는 것
  셰이핑 폭    HarfBuzz 로 문자열을 조판해 총 advance 를 em 단위로 비교
  실효 커닝    shape("XY") - (adv(X) + adv(Y)). 구현 방식과 무관한 실제 조정값
  합자 형성    시험 연속의 셰이핑 후 글리프 수가 같은지
  내부 구조    GSUB/GPOS lookup 수와 합자 규칙 수. 같은 출력을 내는 방식이
               같은지 다른지를 본다

마지막 항목이 중요하다. 99다23246 이 보호 대상으로 특정한 것은
"좌표값과 **그 지시·명령어의 선택**" 이다. 출력이 같아도 규칙 구성이 다르면
그 '선택' 을 가져오지 않았다는 뜻이 된다.

사용법
  pip install fonttools uharfbuzz
  python3 shaping_compat.py <설정.json> [--json]
"""

import itertools
import json
import sys

import uharfbuzz as hb
from fontTools.ttLib import TTFont, TTCollection

# 커닝이 잘 걸리는 글자들. 23자 x 23자 = 529 쌍을 모두 시험한다
KERN_LETTERS = "AVTWYFPLoaevwyr.,:;-1470"
# 합자 시험 연속
LIGATURES = ["fi", "fl", "ff", "ffi", "ffl", "ft", "st", "Th"]
# 셰이핑 폭 비교용 문장
SENTENCES = [
    ("합자 유발", "office affiliate difficult fluffy"),
    ("커닝 유발", "AVATAR To We Yo P. LT Wa Ty"),
    ("혼합 본문", "2026 KrIGF HWPX office file (v1.3) - Type A."),
    ("숫자·기호", "0123456789 %&@#$ (2026-09-29)"),
]
EPS = 1e-6


def load_ft(path, face=None):
    if path.lower().endswith((".ttc", ".otc")):
        for i, f in enumerate(TTCollection(path).fonts):
            names = {n.toUnicode() for n in f["name"].names if n.nameID in (1, 6)}
            if face is None or face in names:
                return f, i
        return None, 0
    return TTFont(path), 0


class Shaper:
    """HarfBuzz 로 실제 조판을 수행한다. 폰트를 고치지 않고 읽기만 한다."""

    def __init__(self, path, index, upem):
        self.font = hb.Font(hb.Face(hb.Blob.from_file_path(path), index))
        self.upem = upem

    def run(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf)
        return (sum(p.x_advance for p in buf.glyph_positions) / self.upem,
                len(buf.glyph_positions))


def structure(f):
    """같은 출력을 내는 '방식' 이 같은지 보기 위한 구조 지표."""
    out = {"gsubLookups": 0, "gposLookups": 0, "pairKernRecords": 0,
           "classKernCells": 0, "ligatureRules": 0}
    gsub = f.get("GSUB")
    if gsub:
        out["gsubLookups"] = len(gsub.table.LookupList.Lookup)
        for lk in gsub.table.LookupList.Lookup:
            if lk.LookupType != 4:
                continue
            for st in lk.SubTable:
                for _, rows in (getattr(st, "ligatures", {}) or {}).items():
                    out["ligatureRules"] += len(rows)
    gpos = f.get("GPOS")
    if gpos:
        out["gposLookups"] = len(gpos.table.LookupList.Lookup)
        for lk in gpos.table.LookupList.Lookup:
            if lk.LookupType != 2:
                continue
            for st in lk.SubTable:
                fmt = getattr(st, "Format", None)
                if fmt == 1:
                    out["pairKernRecords"] += sum(
                        len(ps.PairValueRecord) for ps in st.PairSet)
                elif fmt == 2:
                    out["classKernCells"] += st.Class1Count * st.Class2Count
    return out


def compare(a, b):
    """실효 커닝·합자·셰이핑 폭을 비교한다."""
    adv_a, adv_b = {}, {}

    def adv(sh, cache, ch):
        if ch not in cache:
            cache[ch] = sh.run(ch)[0]
        return cache[ch]

    kern_a = kern_b = same = diff = 0
    examples = []
    for x, y in itertools.product(KERN_LETTERS, repeat=2):
        wa = a.run(x + y)[0] - (adv(a, adv_a, x) + adv(a, adv_a, y))
        wb = b.run(x + y)[0] - (adv(b, adv_b, x) + adv(b, adv_b, y))
        ka, kb = abs(wa) > EPS, abs(wb) > EPS
        kern_a += ka
        kern_b += kb
        if ka or kb:
            if abs(wa - wb) < EPS:
                same += 1
            else:
                diff += 1
                if len(examples) < 5:
                    examples.append({"pair": x + y, "original": round(wa, 5),
                                     "mcf": round(wb, 5)})

    ligs = []
    for s in LIGATURES:
        ga, gb = a.run(s)[1], b.run(s)[1]
        ligs.append({"seq": s, "glyphsOriginal": ga, "glyphsMcf": gb,
                     "same": ga == gb})

    sents = []
    for label, text in SENTENCES:
        wa, ga = a.run(text)
        wb, gb = b.run(text)
        sents.append({"label": label, "emOriginal": round(wa, 4),
                      "emMcf": round(wb, 4),
                      "deltaPct": round(100 * (wb - wa) / wa, 3) if wa else 0,
                      "glyphsOriginal": ga, "glyphsMcf": gb})

    return {"kernPairsOriginal": kern_a, "kernPairsMcf": kern_b,
            "kernSame": same, "kernDiff": diff, "kernDiffExamples": examples,
            "ligatures": ligs,
            "ligatureSame": sum(l["same"] for l in ligs),
            "sentences": sents}


def main(argv):
    as_json = "--json" in argv
    paths = [x for x in argv if x != "--json"]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))

    out = {"kernLetters": KERN_LETTERS, "ligatureTests": LIGATURES, "pairs": []}
    for spec in cfg["pairs"]:
        fa, ia = load_ft(spec["originalPath"], spec.get("originalFace"))
        fb, ib = load_ft(spec["mcfPath"], spec.get("mcfFace"))
        if fa is None or fb is None:
            print(f"# face 를 찾지 못했다: {spec['original']}", file=sys.stderr)
            continue
        a = Shaper(spec["originalPath"], ia, fa["head"].unitsPerEm)
        b = Shaper(spec["mcfPath"], ib, fb["head"].unitsPerEm)
        row = {"original": spec["original"], "mcf": spec["mcf"],
               **compare(a, b),
               "structureOriginal": structure(fa), "structureMcf": structure(fb)}
        out["pairs"].append(row)

    if as_json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return

    print(f"커닝 시험 {len(KERN_LETTERS)}x{len(KERN_LETTERS)} = "
          f"{len(KERN_LETTERS) ** 2}쌍 · 합자 {len(LIGATURES)}종 · "
          f"문장 {len(SENTENCES)}개 (HarfBuzz 셰이핑)")
    print()
    print("| 원본 → MCF | 커닝 쌍 | 값 동일 | 값 다름 | 합자 동일 | 문장 폭 최대 차이 |")
    print("|---|---:|---:|---:|---:|---:|")
    for p in out["pairs"]:
        worst = max(abs(s["deltaPct"]) for s in p["sentences"])
        print(f"| {p['original']} → **{p['mcf']}** | "
              f"{p['kernPairsOriginal']}/{p['kernPairsMcf']} | "
              f"**{p['kernSame']}** | {p['kernDiff']} | "
              f"{p['ligatureSame']}/{len(LIGATURES)} | **{worst:.2f}%** |")
    print()
    print("| 원본 → MCF | GSUB lookup | GPOS lookup | 합자 규칙 | 쌍 커닝 레코드 |")
    print("|---|---|---|---|---|")
    for p in out["pairs"]:
        so, sm = p["structureOriginal"], p["structureMcf"]
        print(f"| {p['original']} → {p['mcf']} | "
              f"{so['gsubLookups']} → {sm['gsubLookups']} | "
              f"{so['gposLookups']} → {sm['gposLookups']} | "
              f"{so['ligatureRules']:,} → {sm['ligatureRules']:,} | "
              f"{so['pairKernRecords']:,} → {sm['pairKernRecords']:,} |")


if __name__ == "__main__":
    main(sys.argv[1:])

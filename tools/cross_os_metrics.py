#!/usr/bin/env python3
"""같은 문서를 OS 를 바꿔 열었을 때 조판이 얼마나 달라지는지 잰다.

공문서가 지정한 글꼴(굴림·바탕 등)은 Windows 에만 있다. macOS·Linux 에서는
그 자리에 다른 글꼴이 대신 들어간다(폰트 폴백). 이 스크립트는 대신 들어가는
글꼴들의 배치 수치를 기준 글꼴과 대조한다.

재는 것
  한글 전각 폭      음절 300자의 최빈 advance width (em 단위)
  라틴 평균 폭      A-Z a-z 52자의 평균
  숫자·공백·괄호·마침표 폭
  문단 폭           한글·라틴·숫자·공백이 섞인 실제 공문서투 문단의 총 advance
  줄 수             그 문단을 고정 폭에 흘렸을 때의 줄 수 (공백 기준 단순 배치)
  쪽 수             같은 문단을 REPEAT 번 이어 붙인 문서의 줄 수와 쪽 수
                    서식은 쪽이 밀리면 서명란·표가 무너지므로 쪽 단위를 따로 본다

모두 OpenType 규격이 정한 hmtx·head 테이블의 값을 읽는 것이며,
목적 코드를 원시 코드로 환원하는 과정을 포함하지 않는다.

사용법
  python3 cross_os_metrics.py <설정.json> [--json]

설정 형식
  {"baseline": "굴림",
   "fonts": [{"group":"Windows 기본","font":"굴림","path":"...","face":"굴림"}, ...]}
  face 는 TTC 에서 고를 name ID 1 또는 6 값이며, 단일 폰트면 생략한다
"""

import collections
import json
import sys

from fontTools.ttLib import TTFont, TTCollection

# 한글 음절 300자. 빈도 상위 위주로 골랐고, 폭이 하나로 수렴하는지 보기 위한 표본이다
SYLLABLES = (
    "가각간갈감강개거건검게겨결경고공과관광교구국군권그금기김나남내년노논능"
    "다단달담답대더도독동두들등라로루류르리마만말망매머명모목무문물미민"
    "바박반발방배백버번법변보복본부북분불비사산상새생서석선설성세소속수순"
    "시식신실심아안알암야어언업여연열영예오온와완외요용우운원월위유은음의"
    "이인일임입자작잡장재저적전절점정제조종좌주준중즉지직진질집차찬참창책"
    "처천청체초총최추출충취치침카크키타탁탄탈태택토통투특파판팔평포표품피"
    "필하학한할함합해행향허험현협형혜호홍화확환활황회획효후훈휘흑희")
LATIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# 공문서투 문단. 한글·라틴·숫자·괄호·마침표·공백이 실제 비율에 가깝게 섞이도록 썼다
PARAGRAPH = (
    "행정안전부는 2026년 9월 29일 공공문서 서식의 상호운용성 개선 방안을 발표하였다. "
    "이번 방안은 HWP 및 HWPX 형식으로 작성된 문서가 운영체제와 무관하게 동일하게 "
    "표시되도록 하는 것을 목표로 한다. 특히 본문 글꼴로 지정된 굴림, 바탕, 돋움 등 "
    "9종에 대하여 메트릭 호환 대체 글꼴(Metric-Compatible Font, MCF)의 확보 필요성이 "
    "제기되었다. 관계 부처는 2027년 상반기까지 시범 적용을 완료할 계획이며, "
    "세부 내용은 붙임 1(추진계획) 및 붙임 2(적용 대상 서식 목록)를 참고하기 바란다.")

# A4 본문 폭 기준값. 210mm - 좌우 여백 30mm씩 = 150mm, 10pt 기준 em 환산
LINE_EM = 150.0 / (10 * 25.4 / 72)

# A4 한 쪽에 들어가는 줄 수. 297mm - 상하 여백 20mm씩 = 257mm,
# 10pt 에 줄간격 160% = 16pt = 5.644mm
LINES_PER_PAGE = int((297.0 - 40.0) / (10 * 1.6 * 25.4 / 72))

# 문서 길이. 위 문단을 이만큼 이어 붙여 한 흐름으로 흘린다
REPEAT = 40

# 서식의 표 칸. 공문서 서식에서 흔한 60mm 폭 기입란을 가정한다.
# 서식은 칸 높이가 고정이거나 칸이 늘면 아래가 전부 밀리므로,
# 본문 한 줄보다 이쪽이 먼저 깨진다
FIELD_EM = 60.0 / (10 * 25.4 / 72)

# 기입란에 들어갈 법한 문구들. 한글·라틴·숫자·괄호가 섞인 실제 항목값이다
FIELD_TEXTS = [
    "한국과학기술정보연구원 과학기술연구망센터",
    "2026년 9월 29일부터 2027년 3월 31일까지",
    "공공문서 서식 상호운용성 개선 사업(1차)",
    "HWPX 기반 개방형 문서 표준 적용 방안 연구",
    "서울특별시 종로구 세종대로 209 정부서울청사 1층",
]


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


def measure(path, face=None):
    f = pick_face(path, face)
    if f is None:
        return None
    upem = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]

    def w(ch):
        """글자 하나의 advance 를 em 단위로. cmap 에 없으면 None."""
        g = cmap.get(ord(ch))
        return hmtx[g][0] / upem if g else None

    counts = collections.Counter(
        hmtx[cmap[ord(c)]][0] for c in SYLLABLES if ord(c) in cmap)
    latin = [w(c) for c in LATIN if w(c) is not None]

    # 문단 폭. cmap 에 없는 글자는 한글 전각 폭으로 대신한다
    hangul_em = counts.most_common(1)[0][0] / upem
    total = 0.0
    for ch in PARAGRAPH:
        v = w(ch)
        total += hangul_em if v is None else v

    # 줄 수. 공백으로 끊어 고정 폭에 흘리는 단순 배치다
    space = w(" ") or 0.25

    def flow_width(text, width):
        """text 를 width(em) 에 흘렸을 때의 줄 수. 공백 기준 단순 배치."""
        lines, cur = 1, 0.0
        for word in text.split(" "):
            ww = sum((w(c) if w(c) is not None else hangul_em) for c in word)
            if cur and cur + space + ww > width:
                lines += 1
                cur = ww
            else:
                cur += (space if cur else 0) + ww
        return lines

    def flow(text):
        return flow_width(text, LINE_EM)

    lines = flow(PARAGRAPH)
    field_lines = [flow_width(t, FIELD_EM) for t in FIELD_TEXTS]
    # 문단 하나는 줄 수가 정수라 차이가 뭉툭하다. 문단 경계 없이
    # 하나로 이어 흘려서 누적 차이를 본다
    doc_lines = flow(" ".join([PARAGRAPH] * REPEAT))
    pages = -(-doc_lines // LINES_PER_PAGE)

    return {
        "upem": upem,
        "hangulEm": round(hangul_em, 4),
        "hangulVariants": len(counts),
        "latinAvgEm": round(sum(latin) / len(latin), 4),
        "digitEm": round(w("0") or 0, 4),
        "spaceEm": round(space, 4),
        "parenEm": round(w("(") or 0, 4),
        "periodEm": round(w(".") or 0, 4),
        "paragraphEm": round(total, 2),
        "lines": lines,
        "docLines": doc_lines,
        "pages": pages,
        "fieldLines": field_lines,
        "fieldLinesTotal": sum(field_lines),
    }


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))

    rows = []
    for spec in cfg["fonts"]:
        m = measure(spec["path"], spec.get("face"))
        if m is None:
            print(f"# face 를 찾지 못했다: {spec['font']}", file=sys.stderr)
            continue
        rows.append({"group": spec["group"], "font": spec["font"], **m})

    base = next(r for r in rows if r["font"] == cfg["baseline"])
    for r in rows:
        r["hangulDeltaPct"] = round(
            100 * (r["hangulEm"] - base["hangulEm"]) / base["hangulEm"], 2)
        r["paragraphDeltaPct"] = round(
            100 * (r["paragraphEm"] - base["paragraphEm"]) / base["paragraphEm"], 2)
        r["lineDelta"] = r["lines"] - base["lines"]
        r["docLineDelta"] = r["docLines"] - base["docLines"]
        r["pageDelta"] = r["pages"] - base["pages"]
        r["fieldLinesDelta"] = r["fieldLinesTotal"] - base["fieldLinesTotal"]
        r["fieldsChanged"] = sum(
            1 for a, b in zip(r["fieldLines"], base["fieldLines"]) if a != b)

    out = {"baseline": cfg["baseline"], "lineWidthEm": round(LINE_EM, 2),
           "linesPerPage": LINES_PER_PAGE, "documentRepeat": REPEAT,
           "documentChars": len(PARAGRAPH) * REPEAT,
           "paragraphChars": len(PARAGRAPH),
           "fieldWidthEm": round(FIELD_EM, 2), "fieldTexts": FIELD_TEXTS,
           "fonts": rows}
    if as_json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return

    print(f"기준 글꼴: {cfg['baseline']} · 줄 폭 {LINE_EM:.1f} em "
          f"(A4 본문 150mm, 10pt) · 문단 {len(PARAGRAPH)}자 · "
          f"문서 {len(PARAGRAPH) * REPEAT:,}자 · 쪽당 {LINES_PER_PAGE}줄 · "
          f"표 칸 {FIELD_EM:.1f} em(60mm) 기입란 {len(FIELD_TEXTS)}개")
    print()
    print("| 구분 | 폰트 | 한글(em) | vs 기준 | 문단 폭 | vs 기준 | 문서 줄 | 쪽 | 기입란 줄 | 칸 변동 |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        dl = "" if not r["docLineDelta"] else f" ({r['docLineDelta']:+d})"
        dp = "" if not r["pageDelta"] else f" ({r['pageDelta']:+d})"
        fc = r["fieldsChanged"]
        print(f"| {r['group']} | {r['font']} | {r['hangulEm']} | "
              f"{r['hangulDeltaPct']:+.1f}% | {r['paragraphEm']} | "
              f"{r['paragraphDeltaPct']:+.1f}% | "
              f"{r['docLines']}{dl} | {r['pages']}{dp} | "
              f"{r['fieldLinesTotal']} | {fc}/{len(FIELD_TEXTS)} |")


if __name__ == "__main__":
    main(sys.argv[1:])

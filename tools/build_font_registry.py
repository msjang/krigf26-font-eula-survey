#!/usr/bin/env python3
"""공문서에 실제로 등장한 폰트의 권리자·라이선스 대조표를 만든다.

입력
  data/gov-doc-fonts_2026-09-24.json     공문서 450건의 폰트 테이블
  data/font-openness-db.json             폰트 -> 개방성 판정
  data/font-license-census_2026-09-24.json  폰트 파일 내장 저작권·라이선스
  data/hft-registry_2026-09-24.json      HFT 폰트의 공급사·저작권·빌드일자

출력
  font-registry.md   폰트 전수 표 (등장률, 포맷, 권리자, 라이선스, 출처 링크)

사용법
  python3 build_font_registry.py > ../font-registry.md
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

VERDICT_LABEL = {
    "free": "자유",
    "freeware": "무료",
    "unlicensed": "권리불명",
    "proprietary": "상용",
    "unknown": "불명",
}

# 권리자별 약관 출처 — 이 저장소가 확인한 1차 자료
HOLDER_SOURCE = {
    "(주)한양정보통신": "[EULA](https://www.hanyang.co.kr/license_20131011.php)",
    "(주)한글과컴퓨터": "[한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md)",
    "(주)윤디자인연구소": "[FONCO 사용범위](https://font.co.kr/policy/license)",
    "Microsoft / Monotype": "[폰트 내장 고지](findings-licenses.md)",
    "Monotype": "[폰트 내장 고지](findings-licenses.md)",
    "휴먼컴퓨터": "-",
    "신명시스템즈 / (주)한글과컴퓨터": "-",
}


def load(name):
    path = os.path.join(DATA, name)
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def main():
    sys.path.insert(0, HERE)
    from openness_check import Judge

    db = load("font-openness-db.json")
    judge = Judge(db)
    docs = load("gov-doc-fonts_2026-09-24.json")["documents"]
    census = {r.get("family"): r for r in load("font-license-census_2026-09-24.json")
              if "error" not in r}
    hft = {}
    for row in load("hft-registry_2026-09-24.json") or []:
        for name in row.get("names") or []:
            hft.setdefault(name, row)

    total = len(docs)
    counts, formats, substitutes = collections.Counter(), {}, {}
    for doc in docs:
        subs = {s["requested"]: s["substituted"] for s in doc["substitutions"]}
        seen = set()
        for _, fonts in doc["fonts"].items():
            for f in fonts:
                seen.add(f["face"])
                formats.setdefault(f["face"], set()).add(f["type"])
                if f["face"] in subs:
                    substitutes.setdefault(f["face"], subs[f["face"]])
        for face in seen:
            counts[face] += 1

    rows = []
    for face, n in counts.most_common():
        verdict, reason, own, _ = judge.judge(
            {"name": face, "substitute": substitutes.get(face)})
        holder = own.get("holder") or ""
        if not holder and face in hft:
            holder = hft[face].get("vendor") or ""
        license_text = own.get("license") or own.get("note") or ""
        source = own.get("source") or ""
        if source.startswith("http"):
            source_md = f"[원문]({source})"
        elif holder in HOLDER_SOURCE:
            source_md = HOLDER_SOURCE[holder]
        else:
            source_md = "-"
        copyright_text = ""
        if face in census:
            copyright_text = (census[face].get("copyright") or "")[:70]
        elif face in hft:
            copyright_text = (hft[face].get("copyright") or "")[:70]
        rows.append({
            "font": face,
            "documents": n,
            "pct": round(100.0 * n / total),
            "format": "/".join(sorted(formats.get(face, {"?"}))),
            "verdict": verdict,
            "status": own.get("status", "unknown"),
            "holder": holder or "-",
            "license": license_text,
            "copyright": copyright_text,
            "source": source_md,
            "substitute": substitutes.get(face) or "",
        })

    print("# 국내 공문서 폰트 목록 — 권리자와 라이선스")
    print()
    print("- 대상: 정책브리핑 보도자료 HWPX **450건**에 등장한 고유 폰트 "
          f"**{len(rows)}종** (2026-09-21~23 게시분)")
    print("- 생성: [`tools/build_font_registry.py`](tools/build_font_registry.py) "
          "— 아래 자료를 대조해 자동 생성")
    print("  - [`data/gov-doc-fonts_2026-09-24.json`](data/gov-doc-fonts_2026-09-24.json) 공문서 폰트 테이블")
    print("  - [`data/font-openness-db.json`](data/font-openness-db.json) 개방성 판정")
    print("  - [`data/font-license-census_2026-09-24.json`](data/font-license-census_2026-09-24.json) 폰트 파일 내장 저작권")
    print("  - [`data/hft-registry_2026-09-24.json`](data/hft-registry_2026-09-24.json) HFT 레지스트리")
    print()
    print("> 판정은 **위법 여부가 아니라 재현 가능성**입니다. "
          "이 저장소의 조사에서 폰트 메트릭 추출을 금지하는 약관 조항은 한 건도 확인되지 않았습니다.")
    print()
    print("## 판정 구분")
    print()
    print("| 표기 | 뜻 |")
    print("|---|---|")
    print("| **자유** | 수정·재배포까지 자유 (OFL 등) |")
    print("| **무료** | 무료 사용·임베딩 허용, 수정 금지. 문서 재현에는 제약 없음 |")
    print("| **권리불명** | 한컴이 \"라이선스를 보유한 것이 아니다\"라고 공지한 Windows 기본 글꼴 9종 |")
    print("| **상용** | 제품 내 사용으로 한정 |")
    print("| **불명** | 판정 근거를 찾지 못함 |")
    print()

    summary = collections.Counter(r["status"] for r in rows)
    print("## 요약")
    print()
    print("| 판정 | 폰트 수 |")
    print("|---|---:|")
    for key in ("free", "freeware", "unlicensed", "proprietary", "unknown"):
        if summary.get(key):
            print(f"| {VERDICT_LABEL[key]} | {summary[key]} |")
    print(f"| **합계** | **{len(rows)}** |")
    print()

    print("## 전체 목록")
    print()
    print("등장 문서 수 내림차순. 비율은 450건 기준.")
    print()
    print("| 폰트 | 문서 | 비율 | 포맷 | 판정 | 권리자 | 저작권 표시 / 라이선스 | 출처 |")
    print("|---|---:|---:|---|---|---|---|---|")
    for r in rows:
        note = r["license"] or r["copyright"] or "-"
        note = note.replace("|", "／")[:78]
        print(f"| {r['font']} | {r['documents']} | {r['pct']}% | {r['format']} | "
              f"{VERDICT_LABEL[r['status']]} | {r['holder']} | {note} | {r['source']} |")
    print()
    print("## 라이선스 원문 보존 사본")
    print()
    print("| 문서 | 사본 | 원 출처 |")
    print("|---|---|---|")
    print("| 한컴 서체 라이선스 | [사본](sources/licenses/hancom-fonts_license_2026-09-24.md) "
          "| https://font.hancom.com/pc/sub/sub3_1.php |")
    print("| 한컴 FAQ 2681 (Windows 기본 글꼴) | "
          "[사본](sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md) "
          "| https://www.hancom.com/support/faqCenter/faq/detail/2681 |")
    print("| (주)한양정보통신 EULA | 발췌 인용 — [clause-matrix.md](clause-matrix.md) "
          "| https://www.hanyang.co.kr/license_20131011.php |")
    print("| 윤디자인 FONCO 사용범위 | 발췌 인용 — [clause-matrix.md](clause-matrix.md) "
          "| https://font.co.kr/policy/license |")
    print("| 함초롬체 안내 | 발췌 인용 — [findings-openness.md](findings-openness.md) "
          "| https://noonnu.cc/font_page/654 |")
    print("| 한컴오피스 제품 EULA | 발췌 인용 — [clause-matrix.md](clause-matrix.md) "
          "| 설치본 `Contents/Resources/Readme/eula_ko.pdf` |")
    print()
    print("## 한계")
    print()
    print("- 표본은 2026-09-21~23 게시분 450건이다. 다른 시기·기관에서는 구성이 다를 수 있다")
    print("- 폰트 테이블 등재가 곧 본문 사용을 뜻하지 않는다")
    print("- 권리자가 `-`인 항목은 이 컴퓨터에 설치되어 있지 않아 파일 저작권을 확인하지 못한 것이다")
    print("- 이름 계열 추정(`HY*` → 한양정보통신 등)이 섞여 있으며, 개별 폰트의 실제 권리 귀속과 다를 수 있다")
    print("- 라이선스 요약은 공개 고지를 옮긴 것이며, 개별 구매·계약 조건과 다를 수 있다")


if __name__ == "__main__":
    main()

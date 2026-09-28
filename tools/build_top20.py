#!/usr/bin/env python3
"""공문서에 가장 많이 쓰이는 폰트 상위 N종을 MCF 판정과 함께 표로 만든다.

font-registry.md 는 415종 전수라 한눈에 들어오지 않는다. 이 문서는 실제로
움직여야 할 대상을 좁혀 보여준다.

MCF 판정 기준
  불필요      무료 사용과 임베딩이 허용된다. 번들하거나 문서에 임베드하면 된다
  필요        상용이고 자유 대체재가 없다. 권리자 약관에 역설계 금지 조항이 없다
  필요·유의   위와 같으나 권리자 약관에 역설계 금지 조항이 있다
  필요·권리불명 한컴이 "라이선스를 보유한 것이 아니다" 라고 공지한 Windows 기본 글꼴
  판단 불가   라이선스 근거를 찾지 못했다

출력
  font-top20.md

사용법
  python3 build_top20.py [상위 N] > ../font-top20.md
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# 판정 -> (표기, 설명)
MCF = {
    "freeware":    ("불필요", "무료 사용·임베딩 허용"),
    "free":        ("불필요", "수정·재배포까지 자유"),
    "proprietary": ("필요", "상용, 자유 대체재 없음"),
    "unlicensed":  ("필요·권리불명", "한컴이 라이선스 보유를 부인"),
    "unknown":     ("판단 불가", "라이선스 근거 미확인"),
}

HOLDER_LICENSE = {
    "(주)한양정보통신": "[EULA](https://www.hanyang.co.kr/license_20131011.php)",
    "(주)한글과컴퓨터": "[한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md)",
    "(주)윤디자인연구소": "[FONCO 사용범위](https://font.co.kr/policy/license)",
    "Microsoft / Monotype": "[폰트 내장 고지](findings-licenses.md)",
    "Monotype": "[폰트 내장 고지](findings-licenses.md)",
}
WINDOWS_LICENSE = ("[한컴 FAQ 2681]"
                   "(sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md)")


def load_documents():
    docs, seen = [], set()
    for path in sorted(glob.glob(os.path.join(DATA, "gov-doc-fonts*.json"))):
        rows = json.load(open(path, encoding="utf-8")).get("documents")
        if not rows:
            continue
        for r in rows:
            if r["url"] in seen:
                continue
            seen.add(r["url"])
            docs.append(r)
    return docs


def main(top_n=20):
    sys.path.insert(0, HERE)
    from openness_check import Judge

    judge = Judge(json.load(open(os.path.join(DATA, "font-openness-db.json"),
                                encoding="utf-8")))
    docs = load_documents()
    total = len(docs)

    counts, formats = collections.Counter(), {}
    for doc in docs:
        seen = set()
        for _, fonts in doc["fonts"].items():
            for f in fonts:
                seen.add(f["face"])
                formats.setdefault(f["face"], set()).add(f["type"])
        for face in seen:
            counts[face] += 1

    years = sorted({r["year"] for r in docs if r.get("year")})
    span = f"{years[0]}~{years[-1]}년" if years else "2026년"

    print("# 공문서 상위 폰트 20종 — 권리자·라이선스·MCF 판정")
    print()
    print(f"- 대상: 정책브리핑 첨부 공문서 **{total:,}건**({span}, HWP·HWPX)")
    print(f"- 등장 문서 수 내림차순. 비율은 {total:,}건 기준")
    print("- 생성: [`tools/build_top20.py`](tools/build_top20.py) — 전수는 "
          "[font-registry.md](font-registry.md)")
    print()
    print("> **MCF 판정은 적법성 판단이 아닙니다.** "
          "이 저장소의 조사에서 폰트 메트릭 추출을 금지하는 약관 조항은 한 건도 "
          "확인되지 않았습니다. 여기서 재는 것은 "
          "**그 폰트에 메트릭 호환 폰트가 필요한가, 만들 때 무엇이 걸리는가** 입니다.")
    print()
    print("## 판정 구분")
    print()
    print("| 표기 | 뜻 |")
    print("|---|---|")
    print("| **불필요** | 무료 사용과 임베딩이 허용된다. 자유 도구가 번들하거나 "
          "문서에 임베드하면 원본과 같은 조판이 나온다 |")
    print("| **필요** | 상용이고 자유 대체재가 없다. 권리자 약관에 역설계 금지 조항은 없다 |")
    print("| **필요·유의** | 위와 같으나 권리자 약관에 **역설계 금지 조항이 있다**. "
          "메트릭 판독이 그 문언에 포섭되는지는 변호사 검토가 필요하다 |")
    print("| **필요·권리불명** | 한컴이 \"저작권자와의 계약을 통해 라이선스를 보유한 "
          "것은 아니다\" 라고 공지한 Windows 기본 글꼴. 권리자를 확인할 창구가 "
          "사용자에게 열려 있지 않다 |")
    print("| **판단 불가** | 라이선스 근거를 찾지 못했다 |")
    print()
    print("## 상위 20종")
    print()
    print("| 폰트 | 문서 | 비율 | 권리자 | 라이선스 | MCF | 비고 |")
    print("|---|---:|---:|---|---|---|---|")

    tally = collections.Counter()
    for face, n in counts.most_common(top_n):
        own = judge.lookup(face)
        status = own.get("status", "unknown")
        verdict, note = MCF[status]
        if status == "proprietary" and own.get("reverseEngineeringClause"):
            verdict, note = "필요·유의", "약관에 '역 설계' 문언 있음"
        holder = own.get("holder") or "-"
        if status == "unlicensed":
            license_md, holder = WINDOWS_LICENSE, "불명 (한컴 라이선스 보유 부인)"
        elif status == "freeware":
            license_md = f"[{(own.get('license') or '')[:22]}…]({own.get('source', '')})"
        elif status == "free":
            license_md = f"[{(own.get('license') or '')[:22]}]({own.get('source', '')})"
        else:
            license_md = HOLDER_LICENSE.get(holder, "-")
        fmts = "/".join(sorted(formats.get(face, set())))
        if "HFT" in fmts and status == "proprietary":
            note += " · HFT(1990년대 빌드)"
        tally[verdict] += 1
        print(f"| **{face}** | {n:,} | {100 * n // total}% | {holder} | "
              f"{license_md} | **{verdict}** | {note} |")

    print()
    print("## 요약")
    print()
    print("| MCF 판정 | 폰트 수 |")
    print("|---|---:|")
    for k in ("불필요", "필요", "필요·유의", "필요·권리불명", "판단 불가"):
        if tally.get(k):
            print(f"| {k} | {tally[k]} |")
    print(f"| **합계** | **{sum(tally.values())}** |")
    print()
    print("## 읽는 법")
    print()
    print("- **불필요** 로 분류된 폰트는 이미 길이 있다. 함초롬체는 한컴이 무료로 "
          "배포하고 임베딩까지 허용하므로, 자유 도구가 번들하거나 문서가 임베드하면 "
          "원본과 같은 조판이 나온다. MCF 를 만들 이유가 없다")
    print("- **필요** 로 분류된 폰트가 실제 병목이다. 공문서 본문의 상수인 "
          "`한양신명조`·`명조`·`휴먼명조` 가 여기 있고, 세 폰트 모두 "
          "17년 내내 98% 이상으로 등장한다 ([findings-trend.md](findings-trend.md))")
    print("- **필요·권리불명** 은 성격이 다르다. 권리자와 협의하려 해도 "
          "그 상대가 누구인지부터 확정되지 않는다")
    print("- 문서에 대체 폰트가 지정되어 있어도 폭이 보존되지 않는다. "
          "따라서 '대체 지정이 있으니 MCF 가 필요 없다' 고 볼 수 없다 "
          "([findings-substfont.md](findings-substfont.md))")
    print()
    print("## 한계")
    print()
    print("- 폰트 테이블 등재가 곧 본문 사용을 뜻하지 않는다. 비율은 "
          "\"그 폰트를 참조하는 문서의 비율\" 이다")
    print("- 권리자가 `-` 이거나 판정이 `판단 불가` 인 항목은 이 컴퓨터에 "
          "설치되어 있지 않아 파일의 저작권 표시를 확인하지 못한 것이다")
    print("- 라이선스 요약은 공개 고지를 옮긴 것이며 개별 구매·계약 조건과 다를 수 있다")
    print("- MCF 판정은 **기술적 필요와 약관 문언**만 본 것이다. 적법 여부가 아니다")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20)

#!/usr/bin/env python3
"""폰트 내장 라이선스 문구(name ID 13)를 분류별 키워드로 검색한다.

dump_font_licenses.py 가 뽑은 JSON 을 받아, 이 조사가 묻는 네 가지 규율
유형이 실제로 문구에 나타나는지 센다. findings-licenses.md 다. 절의 표가
이 도구의 출력이다.

세는 단위가 둘이다.
  폰트 수    해당 키워드를 가진 face 수
  고유 문구  해당 키워드를 가진 서로 다른 ID 13 문자열 수

사용법
  python3 scan_license_keywords.py <census.json> [...] 
  python3 scan_license_keywords.py --json <census.json> [...]   # 기계 판독용
"""

import collections
import json
import re
import sys

# 분류 -> (설명, 검색어). 검색어는 대소문자 구분 없이 부분 일치로 찾는다
CATEGORIES = [
    ("A", "메트릭·수치 추출",
     ["metric", "kerning", "advance width", "side bearing", "spacing",
      "자간", "장평", "간격", "수치"]),
    ("B", "역설계",
     ["reverse engineer", "decompile", "disassemble",
      "역설계", "역 설계", "디컴파일", "리버스"]),
    ("C", "수정·개작",
     ["modify", "alter", "adapt", "derivative", "개작", "수정", "변형"]),
    ("E", "복제·배포",
     ["copy", "distribute", "redistribute", "복제", "배포"]),
]


def load(paths):
    """census JSON 여러 개를 읽어 오류 행을 빼고 합친다. 중복 face 는 남긴다."""
    rows = []
    for p in paths:
        for r in json.load(open(p, encoding="utf-8")):
            if not r.get("error"):
                rows.append(r)
    return rows


def scan(rows):
    texts = [r.get("license") or "" for r in rows]
    having = [t for t in texts if t]
    uniq = sorted(set(having))

    out = {
        "fonts": len(rows),
        "withLicense": len(having),
        "uniqueStrings": len(uniq),
        "bySource": dict(collections.Counter(r.get("source", "?") for r in rows)),
        "categories": [],
    }
    for code, label, words in CATEGORIES:
        pat = re.compile("|".join(re.escape(w) for w in words), re.I)
        hit_u = [s for s in uniq if pat.search(s)]
        out["categories"].append({
            "code": code, "label": label, "keywords": words,
            "fonts": sum(1 for t in having if pat.search(t)),
            "uniqueStrings": len(hit_u),
            "samples": [s[:160] for s in hit_u[:6]],
        })
    return out


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        sys.exit(__doc__)
    result = scan(load(paths))
    if as_json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return
    print(f"대상 face {result['fonts']:,} / 내장 문구 보유 "
          f"{result['withLicense']:,} / 고유 문구 {result['uniqueStrings']:,}")
    for s, n in sorted(result["bySource"].items()):
        print(f"  {s:<28} {n:,}")
    print()
    print("| 분류 | 검색어 | 해당 폰트 | 고유 문구 |")
    print("|---|---|---:|---:|")
    for c in result["categories"]:
        kw = ", ".join(c["keywords"])
        print(f"| **{c['code']} {c['label']}** | {kw} | "
              f"**{c['fonts']:,}** | **{c['uniqueStrings']}** |")


if __name__ == "__main__":
    main(sys.argv[1:])

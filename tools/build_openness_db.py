#!/usr/bin/env python3
"""폰트 이름 -> 개방성 판정 데이터베이스를 만든다.

근거는 이 저장소가 수집한 1차 자료뿐이다.
  - data/font-license-census_2026-09-24.json   폰트 파일 내장 라이선스·저작권
  - data/hft-registry_2026-09-24.json          HFT 폰트의 공급사·저작권
  - data/oss-font-license_2026-09-24.json      오픈소스·MCF 폰트
  - 아래 KNOWN_FREE / RIGHTS_HOLDERS          공개 라이선스 문서로 확인한 것

판정값
  free        자유 라이선스가 확인됨 (OFL, Apache, 공공 무료배포 등)
  proprietary 상용·독점 폰트임이 저작권 표시나 약관으로 확인됨
  unknown     판단 근거를 찾지 못함

중요
  이 DB는 "무엇이 불법인가"를 판정하지 않는다. 확인된 라이선스 상태와,
  권리자 약관에 어떤 조항이 있는지를 기록할 뿐이다. 이 저장소의 조사 결과는
  메트릭 추출을 금지하는 조항이 한 건도 없었다는 것이다.

사용법
  python3 build_openness_db.py > data/font-openness-db.json
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# 권리자별 약관 조사 결과 — clause-matrix.md 참조
RIGHTS_HOLDERS = {
    "한양정보통신": {
        "holder": "(주)한양정보통신",
        "reverseEngineeringClause": True,
        "clauseNote": "EULA 2-2)-①에 '역 설계', '폰트간격 및 자간 수정' 문언 있음. "
                      "다만 목적어는 라이선스 받은 폰트 파일 자체이며 측정·판독을 "
                      "가리키는 문언은 없음",
        "source": "https://www.hanyang.co.kr/license_20131011.php",
    },
    "한글과컴퓨터": {
        "holder": "(주)한글과컴퓨터",
        "reverseEngineeringClause": False,
        "clauseNote": "제품 EULA 12개 조 전문에 역설계·디컴파일·분해 계열 문언 없음. "
                      "글꼴 조항(제7조)은 금지가 아니라 원권리자 문의 안내",
        "source": "한컴오피스 한/글 for Mac 12.30.0 제품 EULA",
    },
    "윤디자인": {
        "holder": "(주)윤디자인연구소",
        "reverseEngineeringClause": False,
        "clauseNote": "공개 라이선스 문서 2종에 역설계·수정 금지 문언 없음. 매체별 사용 범위만 열거",
        "source": "https://font.co.kr/policy/license",
    },
    "Microsoft": {
        "holder": "Microsoft / Monotype",
        "reverseEngineeringClause": False,
        "clauseNote": "내장 문구에 역설계 금지 없음. 다만 'Any other use is prohibited'라는 "
                      "포괄 조항이 있어 문언상 범위가 불명확",
        "source": "폰트 파일 name ID 13",
    },
    "Monotype": {
        "holder": "Monotype",
        "reverseEngineeringClause": False,
        "clauseNote": "금지 범위가 'You may not copy or distribute this software'까지",
        "source": "폰트 파일 name ID 13",
    },
}

# 저작권 문자열 -> 권리자 키
COPYRIGHT_PATTERNS = [
    (r"hanyang|한양", "한양정보통신"),
    (r"hangul\s*&\s*computer|hancom|한컴|한글과컴퓨터", "한글과컴퓨터"),
    (r"yoondesign|윤디자인", "윤디자인"),
    (r"microsoft", "Microsoft"),
    (r"monotype", "Monotype"),
]

# 공개 라이선스 문서로 자유 이용이 확인된 폰트 (이름 접두 일치)
KNOWN_FREE = {
    "나눔": ("SIL Open Font License 1.1", "https://hangeul.naver.com/font"),
    "본고딕": ("SIL Open Font License 1.1", "https://github.com/adobe-fonts/source-han-sans"),
    "본명조": ("SIL Open Font License 1.1", "https://github.com/adobe-fonts/source-han-serif"),
    "Noto": ("SIL Open Font License 1.1", "https://fonts.google.com/noto"),
    "Pretendard": ("SIL Open Font License 1.1", "https://github.com/orioncactus/pretendard"),
    "고딕 A1": ("SIL Open Font License 1.1", "https://fonts.google.com/specimen/Gothic+A1"),
    "고운": ("SIL Open Font License 1.1", "https://fonts.google.com/"),
    "IBM Plex": ("SIL Open Font License 1.1", "https://github.com/IBM/plex"),
    "D2Coding": ("SIL Open Font License 1.1", "https://github.com/naver/d2codingfont"),
    "서울": ("서울특별시 서울서체 — 자유 이용 허용", "https://www.seoul.go.kr/seoul/font.do"),
    "KoPub": ("한국출판인회의 무료 배포", "https://www.kopus.org/biz-01-02/"),
    "Liberation": ("SIL Open Font License 1.1", "https://github.com/liberationfonts/liberation-fonts"),
    "Carlito": ("SIL Open Font License 1.1", "https://github.com/googlefonts/carlito"),
    "Caladea": ("SIL Open Font License 1.1", "https://github.com/huertatipografica/Caladea"),
}

FREE_LICENSE_RE = re.compile(
    r"open font license|\bOFL\b|apache license|mit license|gpl|public domain", re.I)


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    return json.load(open(path, encoding="utf-8"))


def classify_holder(copyright_text, vendor=None):
    blob = f"{copyright_text or ''} {vendor or ''}"
    for pattern, key in COPYRIGHT_PATTERNS:
        if re.search(pattern, blob, re.I):
            return key
    return None


def known_free(name):
    for prefix, (license_name, url) in KNOWN_FREE.items():
        if name and name.startswith(prefix):
            return {"license": license_name, "source": url}
    return None


def add(db, name, entry):
    """이름이 겹치면 판정 근거가 더 확실한 쪽을 남긴다."""
    if not name:
        return
    rank = {"free": 2, "proprietary": 2, "unknown": 0}
    cur = db.get(name)
    if cur is None or rank[entry["status"]] > rank[cur["status"]]:
        db[name] = entry


def main():
    db = {}

    # 1. TrueType/OpenType census
    for row in load("font-license-census_2026-09-24.json"):
        if "error" in row:
            continue
        name = row.get("family") or ""
        lic = row.get("license") or ""
        free = known_free(name)
        if free or FREE_LICENSE_RE.search(lic):
            add(db, name, {
                "status": "free",
                "license": (free or {}).get("license") or lic[:120],
                "source": (free or {}).get("source") or "폰트 파일 name ID 13",
            })
            continue
        holder_key = classify_holder(row.get("copyright"), row.get("trademark"))
        if holder_key:
            meta = RIGHTS_HOLDERS[holder_key]
            add(db, name, {
                "status": "proprietary",
                "holder": meta["holder"],
                "reverseEngineeringClause": meta["reverseEngineeringClause"],
                "clauseNote": meta["clauseNote"],
                "source": meta["source"],
                "copyright": (row.get("copyright") or "")[:120],
            })
        else:
            add(db, name, {
                "status": "unknown",
                "copyright": (row.get("copyright") or "")[:120],
                "source": "폰트 파일 저작권 표시",
            })

    # 2. HFT 레지스트리
    for row in load("hft-registry_2026-09-24.json"):
        holder_key = classify_holder(row.get("copyright"), row.get("vendor"))
        for name in row.get("names") or []:
            if known_free(name):
                continue
            if holder_key:
                meta = RIGHTS_HOLDERS[holder_key]
                add(db, name, {
                    "status": "proprietary",
                    "holder": meta["holder"],
                    "reverseEngineeringClause": meta["reverseEngineeringClause"],
                    "clauseNote": meta["clauseNote"],
                    "source": meta["source"],
                    "format": "HFT",
                    "copyright": (row.get("copyright") or "")[:120],
                    "buildDate": row.get("buildDate"),
                })
            else:
                add(db, name, {
                    "status": "unknown",
                    "format": "HFT",
                    "vendor": row.get("vendor"),
                    "source": "hftinfo.dat / HFT 헤더",
                })

    # 3. 오픈소스·MCF 폰트
    for row in load("oss-font-license_2026-09-24.json"):
        if "error" in row:
            continue
        name = row.get("family") or ""
        free = known_free(name)
        lic = row.get("license") or ""
        if free or FREE_LICENSE_RE.search(lic):
            add(db, name, {
                "status": "free",
                "license": (free or {}).get("license") or lic[:120],
                "source": (free or {}).get("source") or "폰트 파일 name ID 13",
            })

    # 4. 명시적 자유 폰트 목록 (설치되어 있지 않아도 이름으로 판정)
    for prefix, (license_name, url) in KNOWN_FREE.items():
        add(db, prefix, {"status": "free", "license": license_name,
                         "source": url, "matchMode": "prefix"})

    out = {
        "generated": "2026-09-24",
        "note": "이 DB는 위법 여부를 판정하지 않는다. 확인된 라이선스 상태와 "
                "권리자 약관의 조항 유무를 기록한 것이다.",
        "prefixRules": sorted(KNOWN_FREE),
        "fonts": dict(sorted(db.items())),
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

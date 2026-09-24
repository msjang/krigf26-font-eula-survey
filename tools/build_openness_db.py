#!/usr/bin/env python3
"""폰트 이름 -> 개방성 판정 데이터베이스를 만든다.

근거는 이 저장소가 수집한 1차 자료뿐이다.
  - data/font-license-census_2026-09-24.json   폰트 파일 내장 라이선스·저작권
  - data/hft-registry_2026-09-24.json          HFT 폰트의 공급사·저작권
  - data/oss-font-license_2026-09-24.json      오픈소스·MCF 폰트
  - 아래 KNOWN_FREE / RIGHTS_HOLDERS          공개 라이선스 문서로 확인한 것

판정값
  free        수정·재배포까지 자유 (OFL, Apache 등)
  freeware    무료 사용과 임베딩이 허용되나 수정은 금지 (함초롬체, 한컴 서체,
              문체부체, 지자체 배포 서체 등). 문서 재현 목적에는 충분하다
  unlicensed  한컴이 "우리가 라이선스를 보유한 것은 아니다"라고 밝힌 Windows 기본
              글꼴 9종. 권리 관계를 확인할 창구가 사용자에게 열려 있지 않다
  proprietary 제품 내 사용으로 한정되는 상용 폰트
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

# 무료 사용·임베딩이 허용되나 수정은 금지된 폰트.
# 문서를 그대로 재현하는 데는 제약이 없으므로 개방성 판정에서는 재현 가능으로 본다.
KNOWN_FREEWARE = {
    "함초롬": ("한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. "
             "수정·상업적 배포 금지",
             "https://noonnu.cc/font_page/654"),
    "한컴 산스": ("한컴 서체 라이선스 — 상업적 사용·임베딩·서버 탑재 허용, 수정·재배포 금지",
                "https://font.hancom.com/pc/sub/sub3_1.php"),
    "한컴 말랑말랑": ("한컴 서체 라이선스 — 상업적 사용·임베딩·서버 탑재 허용, 수정·재배포 금지",
                  "https://font.hancom.com/pc/sub/sub3_1.php"),
    "한컴 훈민정음": ("한컴 서체 라이선스 — 상업적 사용·임베딩·서버 탑재 허용, 수정·재배포 금지",
                  "https://font.hancom.com/pc/sub/sub3_1.php"),
    "한컴 울주": ("한컴 서체 라이선스 — 상업적 사용·임베딩·서버 탑재 허용, 수정·재배포 금지",
                "https://font.hancom.com/pc/sub/sub3_1.php"),
    "문체부": ("출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지",
             "https://www.happyjung.com/font/21"),
    "경기천년": ("경기도 배포 무료 글꼴", "https://www.gg.go.kr/contents/contents.do?ciIdx=679"),
    "전주 완판본": ("전주시 배포 무료 글꼴", "https://www.jeonju.go.kr/"),
}

# 한컴이 "라이선스를 보유한 것은 아니다"라고 명시한 Windows 기본 글꼴 9종
# 출처: https://www.hancom.com/support/faqCenter/faq/detail/2681
WINDOWS_BUNDLED = {
    "굴림", "굴림체", "궁서", "궁서체", "돋움", "돋움체", "맑은 고딕", "바탕", "바탕체",
}
WINDOWS_NOTE = ("한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 "
                "라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권자에게 문의해야 함")
WINDOWS_SOURCE = "https://www.hancom.com/support/faqCenter/faq/detail/2681"

# 수정·재배포까지 자유로운 폰트 (이름 접두 일치)
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


def known_freeware(name):
    for prefix, (license_name, url) in KNOWN_FREEWARE.items():
        if name and name.startswith(prefix):
            return {"license": license_name, "source": url}
    return None


def windows_bundled(name):
    return name in WINDOWS_BUNDLED


def add(db, name, entry):
    """이름이 겹치면 판정 근거가 더 확실한 쪽을 남긴다."""
    if not name:
        return
    rank = {"free": 3, "freeware": 3, "unlicensed": 3, "proprietary": 2, "unknown": 0}
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
        if windows_bundled(name):
            add(db, name, {"status": "unlicensed", "note": WINDOWS_NOTE,
                           "source": WINDOWS_SOURCE,
                           "copyright": (row.get("copyright") or "")[:120]})
            continue
        ware = known_freeware(name)
        if ware:
            add(db, name, {"status": "freeware", "license": ware["license"],
                           "source": ware["source"], "reproducible": True,
                           "copyright": (row.get("copyright") or "")[:120]})
            continue
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
            if windows_bundled(name):
                add(db, name, {"status": "unlicensed", "note": WINDOWS_NOTE,
                               "source": WINDOWS_SOURCE, "format": "HFT"})
                continue
            ware = known_freeware(name)
            if ware:
                add(db, name, {"status": "freeware", "license": ware["license"],
                               "source": ware["source"], "reproducible": True,
                               "format": "HFT"})
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

    # 4. 이름만으로 판정 가능한 목록 (설치되어 있지 않아도 적용)
    for prefix, (license_name, url) in KNOWN_FREE.items():
        add(db, prefix, {"status": "free", "license": license_name,
                         "source": url, "matchMode": "prefix"})
    for prefix, (license_name, url) in KNOWN_FREEWARE.items():
        add(db, prefix, {"status": "freeware", "license": license_name,
                         "source": url, "reproducible": True, "matchMode": "prefix"})
    for name in WINDOWS_BUNDLED:
        add(db, name, {"status": "unlicensed", "note": WINDOWS_NOTE,
                       "source": WINDOWS_SOURCE})

    out = {
        "generated": "2026-09-24",
        "note": "이 DB는 위법 여부를 판정하지 않는다. 확인된 라이선스 상태와 "
                "권리자 약관의 조항 유무를 기록한 것이다.",
        "prefixRules": sorted(set(KNOWN_FREE) | set(KNOWN_FREEWARE)),
        "fonts": dict(sorted(db.items())),
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""폰트 파일이 주장하는 상표가 국내에 실제로 등록되어 있는지 KIPRIS 에서 조회한다.

왜 필요한가
  폰트 파일의 `name` ID 7 에는 "X is a registered trademark of Y" 같은 문구가
  들어 있다. 그러나 이는 **파일에 적힌 주장**일 뿐이며, 어느 나라 등록인지·
  현재 존속하는지를 말해 주지 않는다. 국내 권리 여부는 특허청 자료로 확인해야 한다.

무엇을 하나
  KIPRIS 상표 검색에 (상표명칭, 출원인) 조건을 넣어 결과 유무와 목록을 읽는다.
  읽기만 하며 로그인·다운로드를 하지 않는다.

  조회 1 — 상표명칭만: 그 이름으로 등록된 상표와 출원인을 본다
  조회 2 — 상표명칭 + 출원인: 특정 회사의 등록 여부를 직접 확인한다

무엇을 하지 않나
  등록의 유효성이나 효력 범위를 판단하지 않는다. 조회 결과를 옮길 뿐이다.

사용법
  pip install playwright && playwright install chromium
  python3 kipris_trademark_check.py <설정.json> [--json]

설정 형식
  {"marks": ["바탕", "굴림"], "applicant": "마이크로소프트", "headless": true}
"""

import json
import re
import sys
import time

BASE = "https://www.kipris.or.kr/khome/search/searchResult.do?tab=trademark"
SEL_NAME = "#sd010301_g05_text"        # 상표명칭(TN)
SEL_APPLICANT = "#sd010301_g07_text_01"  # 출원인(AP)
ROW = re.compile(r"\[(\d+)\]\s*\n(\d{10,13})\s*\n(.+?)\n", re.S)
DETAIL = re.compile(
    r"\[(\d+)\]\s*\n(\d{10,13})\s*\n(.+?)\n(?:.*?상품분류\s*\n(\d+)\s*\n)?"
    r"(?:.*?출원인\s*\n(.+?)\n)?", re.S)


def query(page, mark=None, applicant=None, wait=6.0):
    """KIPRIS 상표 검색 결과 첫 페이지를 읽어 온다."""
    page.goto(BASE, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(2600)
    if mark:
        page.fill(SEL_NAME, mark)
    if applicant:
        page.fill(SEL_APPLICANT, applicant)
    page.keyboard.press("Enter")
    page.wait_for_timeout(int(wait * 1000))
    body = page.inner_text("body")
    rows = []
    for m in DETAIL.finditer(body):
        rows.append({"no": m.group(1), "appNo": m.group(2),
                     "name": m.group(3).strip()[:80],
                     "class": m.group(4),
                     "applicant": (m.group(5) or "").strip()[:60]})
    return {"rows": rows, "count": len(rows),
            "noResult": len(rows) == 0}


def main(argv):
    as_json = "--json" in argv
    paths = [x for x in argv if not x.startswith("--")]
    if not paths:
        sys.exit(__doc__)
    cfg = json.load(open(paths[0], encoding="utf-8"))
    marks = cfg["marks"]
    applicant = cfg.get("applicant")

    from playwright.sync_api import sync_playwright

    out = {"queriedAt": time.strftime("%Y-%m-%d"),
           "source": "KIPRIS 상표 검색 (www.kipris.or.kr)",
           "note": ("결과 첫 페이지만 읽는다. 목록 전체를 소진하지 않으므로 "
                    "'명칭만' 조회의 0건은 '없음'의 증명이 아니다. "
                    "명칭+출원인 동시 조회의 결과 없음이 더 강한 근거다"),
           "applicant": applicant, "byMark": {}, "byMarkAndApplicant": {}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=cfg.get("headless", True))
        page = browser.new_page(locale="ko-KR",
                                viewport={"width": 1600, "height": 1500})
        for mark in marks:
            out["byMark"][mark] = query(page, mark=mark)
            if applicant:
                out["byMarkAndApplicant"][mark] = query(
                    page, mark=mark, applicant=applicant)
        browser.close()

    if as_json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return

    print(f"KIPRIS 상표 검색 · {out['queriedAt']}")
    print()
    print("| 상표명칭 | 첫 페이지 결과 | 출원인에 "
          f"{applicant or '-'} | 제9류 |")
    print("|---|---:|---|---:|")
    for mark in marks:
        a = out["byMark"][mark]
        b = out["byMarkAndApplicant"].get(mark, {})
        cls9 = sum(1 for r in a["rows"] if r["class"] == "9")
        hit = "**결과 없음**" if b.get("noResult") else f"{b.get('count', '-')}건"
        print(f"| {mark} | {a['count']} | {hit} | {cls9} |")


if __name__ == "__main__":
    main(sys.argv[1:])

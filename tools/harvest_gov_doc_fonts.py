#!/usr/bin/env python3
"""정책브리핑(korea.kr) 보도자료 첨부 HWPX에서 폰트 사용 실태를 집계한다.

왜 이 자료인가
  - 각 부처가 실제로 배포하는 공문서이고, 첨부가 HWPX(ZIP+XML)여서
    Contents/header.xml의 fontfaces 테이블을 규격대로 읽을 수 있다.
  - substFont 항목은 "문서가 요청했으나 저장 시점 환경에 없어 대체된 폰트"를
    기록한다. 즉 문서 스스로가 남긴 폰트 대체(=레이아웃 깨짐) 증거다.

수집 원칙
  - robots.txt 확인: www.korea.kr 은 User-Agent * 에 Allow: / (2026-09-24 확인)
  - 순차 요청 + 요청 간 지연으로 부하를 주지 않는다
  - 본문 내용은 저장하지 않는다. 폰트 이름과 메타데이터만 추출한다

사용법
  python3 harvest_gov_doc_fonts.py --pages 40 --out gov-doc-fonts.json
"""

import argparse
import html
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import Counter, defaultdict

BASE = "https://www.korea.kr"
LIST_URL = BASE + "/briefing/pressReleaseList.do?pageIndex={page}"
VIEW_URL = BASE + "/briefing/pressReleaseView.do?newsId={news_id}"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15")

FONT_RE = re.compile(
    r'<hh:font\s+id="(?P<id>\d+)"\s+face="(?P<face>[^"]*)"\s+type="(?P<type>[^"]*)"'
    r'(?P<rest>.*?)</hh:font>|'
    r'<hh:font\s+id="(?P<id2>\d+)"\s+face="(?P<face2>[^"]*)"\s+type="(?P<type2>[^"]*)"[^>]*/>',
    re.S)
SUBST_RE = re.compile(r'<hh:substFont\s+face="([^"]*)"')
FACE_BLOCK_RE = re.compile(
    r'<hh:fontface\s+lang="(?P<lang>[^"]*)"[^>]*>(?P<body>.*?)</hh:fontface>', re.S)


def fetch(url, referer=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if referer:
        req.add_header("Referer", referer)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def list_news_ids(page):
    raw = fetch(LIST_URL.format(page=page)).decode("utf-8", errors="replace")
    ids = re.findall(r'pressReleaseView\.do\?newsId=(\d+)', raw)
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def list_attachments(news_id):
    """(다운로드 URL, 파일명) 목록. 파일명은 앵커 텍스트에서 뽑는다."""
    url = VIEW_URL.format(news_id=news_id)
    raw = fetch(url).decode("utf-8", errors="replace")
    out = []
    for m in re.finditer(
            r'href="(?P<href>/common/download\.do\?fileId=\d+[^"]*)"(?P<tail>.{0,400}?)</a>',
            raw, re.S):
        href = html.unescape(m.group("href"))
        text = re.sub(r"<[^>]+>", " ", m.group("tail"))
        text = html.unescape(" ".join(text.split()))
        out.append((BASE + href, text, url))
    return out


def parse_hwpx_fonts(blob):
    """HWPX의 fontfaces 테이블에서 (언어별 폰트, 대체 기록)을 뽑는다."""
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = set(z.namelist())
        if "Contents/header.xml" not in names:
            return None
        header = z.read("Contents/header.xml").decode("utf-8", errors="replace")

    per_lang, substitutions = {}, []
    for block in FACE_BLOCK_RE.finditer(header):
        lang = block.group("lang")
        faces = []
        for fm in re.finditer(
                r'<hh:font\s+[^>]*face="([^"]*)"[^>]*type="([^"]*)"[^>]*'
                r'(?:/>|>(.*?)</hh:font>)', block.group("body"), re.S):
            face, ftype, inner = fm.group(1), fm.group(2), fm.group(3) or ""
            faces.append({"face": face, "type": ftype})
            for subst in SUBST_RE.findall(inner):
                substitutions.append({"lang": lang, "requested": face,
                                      "substituted": subst, "type": ftype})
        per_lang[lang] = faces
    return {"fonts": per_lang, "substitutions": substitutions}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=20)
    ap.add_argument("--delay", type=float, default=0.4)
    ap.add_argument("--max-docs", type=int, default=600)
    ap.add_argument("--out", default="gov-doc-fonts.json")
    args = ap.parse_args()

    records, errors = [], []
    seen_files = set()

    for page in range(1, args.pages + 1):
        try:
            news_ids = list_news_ids(page)
        except Exception as exc:
            errors.append({"stage": "list", "page": page, "error": str(exc)})
            continue
        print(f"[list] page {page}: {len(news_ids)} articles",
              file=sys.stderr, flush=True)
        time.sleep(args.delay)

        for news_id in news_ids:
            if len(records) >= args.max_docs:
                break
            try:
                attachments = list_attachments(news_id)
            except Exception as exc:
                errors.append({"stage": "view", "newsId": news_id, "error": str(exc)})
                continue
            time.sleep(args.delay)

            for url, label, referer in attachments:
                if ".hwpx" not in label.lower():
                    continue
                if url in seen_files:
                    continue
                seen_files.add(url)
                try:
                    blob = fetch(url, referer=referer)
                    parsed = parse_hwpx_fonts(blob)
                except Exception as exc:
                    errors.append({"stage": "download", "url": url, "error": str(exc)})
                    continue
                finally:
                    time.sleep(args.delay)
                if not parsed:
                    continue
                records.append({
                    "newsId": news_id,
                    "filename": label,
                    "url": url,
                    "fonts": parsed["fonts"],
                    "substitutions": parsed["substitutions"],
                })
                print(f"  [doc {len(records)}] {label[:60]}",
                      file=sys.stderr, flush=True)
        if len(records) >= args.max_docs:
            break

    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump({"collected": time.strftime("%Y-%m-%d"),
                   "source": "korea.kr 정책브리핑 보도자료 첨부 HWPX",
                   "documents": records,
                   "errors": errors}, fp, ensure_ascii=False, indent=1)

    hangul = Counter()
    for rec in records:
        for f in rec["fonts"].get("HANGUL", []):
            hangul[f["face"]] += 1
    subst = Counter((s["requested"], s["substituted"])
                    for r in records for s in r["substitutions"])

    print(f"\n문서 {len(records)}건, 오류 {len(errors)}건 → {args.out}", file=sys.stderr)
    print("\n[한글 폰트 상위 25]", file=sys.stderr)
    for face, n in hangul.most_common(25):
        print(f"  {n:5d}  {face}", file=sys.stderr)
    print("\n[폰트 대체 상위 20]", file=sys.stderr)
    for (req, sub), n in subst.most_common(20):
        print(f"  {n:5d}  {req}  ->  {sub}", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""정책브리핑(korea.kr) 보도자료 첨부에서 폰트 사용 실태를 연도·부처별로 수집한다.

왜 이 자료인가
  - 각 부처가 실제로 배포하는 공문서이고, 첨부가 HWPX(ZIP+XML) 또는 HWP(CFB)여서
    폰트 테이블을 규격대로 읽을 수 있다.
  - 목록 페이지가 게시일과 부처명을 함께 제공하므로 층화 표본을 만들 수 있다.
  - 대체 폰트 지정(substFont / FaceName 레코드)은 해당 폰트가 저장 시점 환경에
    없었음을 뜻한다.

표본 설계
  --years 로 연도 구간을 지정하면 각 연도에서 --weeks 개의 주를 고르게 뽑고,
  각 주에서 목록 앞쪽부터 문서를 모은다. 부처는 사후 집계한다(목록이 제공).
  korea.kr 아카이브는 2010년까지 확인되었다.

수집 원칙
  - robots.txt 확인: www.korea.kr 은 User-Agent * 에 Allow: / (2026-09-24 확인)
  - 순차 요청 + 요청 간 지연
  - 본문 내용은 저장하지 않는다. 폰트 이름과 메타데이터만 추출한다

사용법
  python3 harvest_gov_doc_fonts.py --years 2010-2026 --per-year 60 \
      --out ../data/gov-doc-fonts.json
"""

import argparse
import datetime
import html
import io
import json
import os
import re
import struct
import sys
import time
import urllib.request
import zipfile
import zlib
from collections import Counter

BASE = "https://www.korea.kr"

# korea.kr 에서 HWP/HWPX 첨부가 확인된 섹션. 문서 장르가 서로 다르다.
SECTIONS = {
    "press": {
        "label": "보도자료",
        "list": "/briefing/pressReleaseList.do",
        "view": "/briefing/pressReleaseView.do",
        "idKey": "newsId",
        "viewPattern": r"pressReleaseView\.do\?newsId=(?P<id>\d+)",
        "dateFilter": True,
        "hasAgency": True,
    },
    "briefing": {
        "label": "브리핑 속기자료",
        "list": "/briefing/briefingHomeList.do",
        "view": "/briefing/policyBriefingView.do",
        "idKey": "newsId",
        "viewPattern": r"policyBriefingView\.do\?newsId=(?P<id>\d+)",
        "dateFilter": False,   # 목록이 startDate/endDate 를 무시한다
        "hasAgency": False,
    },
    "actually": {
        "label": "보도참고·해명자료",
        "list": "/briefing/actuallyList.do",
        "view": "/briefing/actuallyView.do",
        "idKey": "newsId",
        "viewPattern": r"actuallyView\.do\?newsId=(?P<id>\d+)",
        "dateFilter": True,
        "hasAgency": True,
    },
}
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15")

HWPTAG_FACE_NAME = 19
FACE_PROP_HAS_SUBSTITUTE = 0x80

# 목록 항목의 출처 표기. 섹션에 따라 부처명이 없고 날짜만 있는 경우가 있다.
SOURCE_RE = (r'.*?<span class="source">\s*(?:<span>)?(?P<date>[\d.\-]{8,10})(?:</span>)?'
             r'(?:\s*<span>(?P<agency>[^<]*)</span>)?')
ATTACH_RE = re.compile(
    r'href="(?P<href>/common/download\.do\?fileId=\d+[^"]*)"(?P<tail>.{0,400}?)</a>', re.S)


def fetch(url, referer=None, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if referer:
        req.add_header("Referer", referer)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


# ------------------------------------------------------------------ 목록

def list_items(section, start, end, page, rep_code=None):
    """(newsId, 게시일, 부처) 목록. 목록 페이지가 셋을 함께 제공한다."""
    url = (BASE + section["list"] +
           f"?startDate={start}&endDate={end}&period=direct&pageIndex={page}")
    if rep_code:
        url += f"&repCodeType={rep_code[0]}&repCode={rep_code}"
    raw = fetch(url).decode("utf-8", errors="replace")
    item_re = re.compile(section["viewPattern"] + SOURCE_RE, re.S)
    out, seen = [], set()
    for m in item_re.finditer(raw):
        news_id = m.group("id")
        if news_id in seen:
            continue
        seen.add(news_id)
        out.append({
            "newsId": news_id,
            "date": m.group("date").replace(".", "-"),   # 목록은 . 또는 - 를 쓴다
            "agency": html.unescape(m.group("agency") or "").strip() or "(미표기)",
        })
    return out


def list_attachments(section, news_id):
    url = f"{BASE}{section['view']}?{section['idKey']}={news_id}"
    raw = fetch(url).decode("utf-8", errors="replace")
    out = []
    for m in ATTACH_RE.finditer(raw):
        label = re.sub(r"<[^>]+>", " ", m.group("tail"))
        label = html.unescape(" ".join(label.split()))
        out.append((BASE + html.unescape(m.group("href")), label, url))
    return out


# ------------------------------------------------------------------ 폰트 판독

def parse_hwpx(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        if "Contents/header.xml" not in z.namelist():
            return None
        header = z.read("Contents/header.xml").decode("utf-8", errors="replace")
    per_lang, subs = {}, []
    for block in re.finditer(
            r'<hh:fontface\s+lang="(?P<lang>[^"]*)"[^>]*>(?P<body>.*?)</hh:fontface>',
            header, re.S):
        lang, faces = block.group("lang"), []
        for fm in re.finditer(
                r'<hh:font\s+[^>]*face="([^"]*)"[^>]*type="([^"]*)"[^>]*'
                r'(?:/>|>(.*?)</hh:font>)', block.group("body"), re.S):
            face, ftype, inner = fm.group(1), fm.group(2), fm.group(3) or ""
            faces.append({"face": face, "type": ftype})
            for sub in re.findall(r'<hh:substFont\s+face="([^"]*)"', inner):
                subs.append({"lang": lang, "requested": face,
                             "substituted": sub, "type": ftype})
        per_lang[lang] = faces
    return {"fonts": per_lang, "substitutions": subs, "format": "HWPX"}


def parse_hwp(blob):
    try:
        import olefile
    except ImportError:
        return None
    ole = olefile.OleFileIO(io.BytesIO(blob))
    try:
        header = ole.openstream("FileHeader").read()
        if not header.startswith(b"HWP Document File"):
            return None
        flags = struct.unpack("<I", header[36:40])[0]
        if flags & 0x02:
            return None  # 암호화
        raw = ole.openstream("DocInfo").read()
        data = zlib.decompress(raw, -15) if flags & 0x01 else raw
    except Exception:
        return None
    finally:
        ole.close()

    faces, subs, pos = [], [], 0
    while pos + 4 <= len(data):
        head = struct.unpack("<I", data[pos:pos + 4])[0]
        pos += 4
        tag, size = head & 0x3FF, (head >> 20) & 0xFFF
        if size == 0xFFF:
            size = struct.unpack("<I", data[pos:pos + 4])[0]
            pos += 4
        body, pos = data[pos:pos + size], pos + size
        if tag != HWPTAG_FACE_NAME:
            continue
        try:
            i = 0
            prop = body[i]; i += 1
            ln = struct.unpack("<H", body[i:i + 2])[0]; i += 2
            name = body[i:i + ln * 2].decode("utf-16-le").strip("\x00"); i += ln * 2
            faces.append({"face": name, "type": "HWP"})
            if prop & FACE_PROP_HAS_SUBSTITUTE:
                i += 1
                sl = struct.unpack("<H", body[i:i + 2])[0]; i += 2
                sub = body[i:i + sl * 2].decode("utf-16-le").strip("\x00")
                if sub:
                    subs.append({"lang": "ALL", "requested": name,
                                 "substituted": sub, "type": "HWP"})
        except Exception:
            continue
    if not faces:
        return None
    return {"fonts": {"ALL": faces}, "substitutions": subs, "format": "HWP 5.0"}


def parse_document(blob, label):
    lower = label.lower()
    if ".hwpx" in lower:
        return parse_hwpx(blob)
    if ".hwp" in lower:
        return parse_hwp(blob)
    return None


# ------------------------------------------------------------------ 표본 설계

def sample_windows(years, weeks_per_year):
    """각 연도에서 weeks_per_year 개의 주를 달마다 고르게 흩어 고른다."""
    windows = []
    for year in years:
        for k in range(weeks_per_year):
            month = 1 + int(12 * k / weeks_per_year)
            day = 1 + (k * 7) % 21
            try:
                start = datetime.date(year, month, day)
            except ValueError:
                continue
            end = start + datetime.timedelta(days=6)
            if start > datetime.date.today():
                continue
            windows.append((start.isoformat(), end.isoformat(), year))
    return windows


def parse_years(spec):
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return list(range(int(lo), int(hi) + 1))
    return [int(spec)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="2010-2026", help="예: 2010-2026")
    ap.add_argument("--weeks", type=int, default=6, help="연도당 표본 주 수")
    ap.add_argument("--per-year", type=int, default=60, help="연도당 목표 문서 수")
    ap.add_argument("--pages", type=int, default=2, help="주당 목록 페이지 수")
    ap.add_argument("--delay", type=float, default=0.35)
    ap.add_argument("--section", default="press", choices=sorted(SECTIONS),
                    help="수집할 korea.kr 섹션 (문서 장르)")
    ap.add_argument("--rep-codes", default="",
                    help="쉼표로 구분한 부처 코드. 지정하면 부처별로 균등 수집한다 "
                         "(예: A00009,B00004). 목록은 --list-agencies 로 확인")
    ap.add_argument("--per-agency", type=int, default=0,
                    help="부처당 목표 문서 수 (--rep-codes 사용 시)")
    ap.add_argument("--list-agencies", action="store_true",
                    help="부처 코드 목록만 출력하고 종료")
    ap.add_argument("--out", default="gov-doc-fonts.json")
    args = ap.parse_args()
    section = SECTIONS[args.section]

    years = parse_years(args.years)
    windows = sample_windows(years, args.weeks)
    records, errors, seen_files = [], [], set()
    per_year = Counter()

    for start, end, year in windows:
        if per_year[year] >= args.per_year:
            continue
        for page in range(1, args.pages + 1):
            if per_year[year] >= args.per_year:
                break
            try:
                items = list_items(section, start, end, page)
            except Exception as exc:
                errors.append({"stage": "list", "window": start, "error": str(exc)})
                continue
            time.sleep(args.delay)
            for item in items:
                if per_year[year] >= args.per_year:
                    break
                try:
                    attachments = list_attachments(section, item["newsId"])
                except Exception as exc:
                    errors.append({"stage": "view", "newsId": item["newsId"],
                                   "error": str(exc)})
                    continue
                time.sleep(args.delay)
                for url, label, referer in attachments:
                    if ".hwp" not in label.lower():
                        continue
                    if url in seen_files:
                        continue
                    seen_files.add(url)
                    try:
                        blob = fetch(url, referer=referer)
                        parsed = parse_document(blob, label)
                    except Exception as exc:
                        errors.append({"stage": "download", "url": url,
                                       "error": str(exc)})
                        continue
                    finally:
                        time.sleep(args.delay)
                    if not parsed:
                        continue
                    records.append({
                        "newsId": item["newsId"],
                        "date": item["date"],
                        "year": year,
                        "agency": item["agency"],
                        "docType": section["label"],
                        "filename": label,
                        "url": url,
                        "format": parsed["format"],
                        "fonts": parsed["fonts"],
                        "substitutions": parsed["substitutions"],
                    })
                    per_year[year] += 1
                    break  # 문서당 첨부 1건만
        print(f"[{year}] {start}~{end} 누적 {per_year[year]}건 "
              f"(전체 {len(records)})", file=sys.stderr, flush=True)

    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump({
            "collected": time.strftime("%Y-%m-%d"),
            "source": f"korea.kr 정책브리핑 {section['label']} 첨부 (HWP / HWPX)",
            "section": args.section,
            "sampling": {
                "years": years, "weeksPerYear": args.weeks,
                "targetPerYear": args.per_year,
                "dateFilterSupported": section.get("dateFilter", True),
                "agencyRecorded": section.get("hasAgency", True),
                "note": ("연도별 층화 표본. 각 연도에서 달마다 흩어진 주를 골라 수집. "
                         "dateFilterSupported 가 false 인 섹션은 목록이 날짜 조건을 "
                         "무시하므로 연도 층화가 적용되지 않는다"),
            },
            "documents": records,
            "errors": errors,
        }, fp, ensure_ascii=False, indent=1)

    print(f"\n문서 {len(records)}건, 오류 {len(errors)}건 → {args.out}", file=sys.stderr)
    print("\n[연도별]", file=sys.stderr)
    for y in sorted(per_year):
        print(f"  {y}  {per_year[y]:4d}건", file=sys.stderr)
    print("\n[부처별 상위 15]", file=sys.stderr)
    for a, n in Counter(r["agency"] for r in records).most_common(15):
        print(f"  {n:4d}  {a}", file=sys.stderr)
    print("\n[문서 장르]", file=sys.stderr)
    for t, n in Counter(r["docType"] for r in records).most_common():
        print(f"  {n:4d}  {t}", file=sys.stderr)
    print("\n[형식별]", file=sys.stderr)
    for f, n in Counter(r["format"] for r in records).most_common():
        print(f"  {n:4d}  {f}", file=sys.stderr)


if __name__ == "__main__":
    main()

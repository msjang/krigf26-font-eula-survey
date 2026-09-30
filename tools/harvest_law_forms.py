#!/usr/bin/env python3
"""법제처 국가법령정보 OPEN API 로 법령 서식의 폰트 사용 실태를 수집한다.

왜 이 자료인가
  보도자료는 읽기 전용이지만 **서식은 국민이 채워 넣는 문서**다. 대체 글꼴로
  조판이 달라지면 실제 피해가 생기는 쪽이 이쪽이다. MCF 의 필요성을 재려면
  편집되는 문서를 봐야 한다.

무엇을 재는가
  법령 공포일과 **서식 파일이 실제로 만들어진 시점**은 다르다. 법을 고쳐도
  서식은 손대지 않고 그대로 재게시하는 일이 흔하다. HWP 안의 수정 시각이
  그 사실을 드러낸다. 그래서 "지금 유효한 서식이 몇 년도 파일인가" 를 잰다.

수집 원칙
  - robots.txt 확인: law.go.kr 은 User-agent * 에 Allow: / (2026-09-30 확인)
  - 공개 OPEN API 를 쓴다. 목록은 API, 본문은 API 가 알려 준 링크로 받는다
  - 순차 요청 + 요청 간 지연
  - 받은 파일은 저장소에 보관한다. 같은 서식을 다시 내려받지 않기 위해서다

저장 구조 (--store, 기본 ~/dev/law-form-data)
  list/page-0001.xml       목록 API 응답 원문. 재현용
  files/<끝2자리>/<flSeq>.hwp   내려받은 서식 원본
  manifest.jsonl           한 줄에 한 건. 받는 즉시 덧붙인다 (중단·재개용)
  index.json               manifest 를 모아 만든 배포본

사용법
  python3 harvest_law_forms.py --oc <인증키> --limit 200
  python3 harvest_law_forms.py --oc <인증키> --all
  python3 harvest_law_forms.py --build-index          # 망 접속 없이 index.json 만
"""

import argparse
import collections
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import olefile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harvest_gov_doc_fonts import parse_hwp, parse_hwpx  # 같은 판독기를 쓴다

API = "https://www.law.go.kr/DRF/lawSearch.do"
BASE = "https://www.law.go.kr"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
KND_FORM = 2   # 별표종류: 1 별표 / 2 서식 / 3 별지 / 4 별도 / 5 부록
STORE = os.path.expanduser("~/dev/law-form-data")

FIELD = re.compile(r"<([가-힣A-Za-z]+)>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</\1>", re.S)

# 목록 API 필드 → 레코드 키
COLUMNS = {
    "별표일련번호": "bylSeq",
    "별표번호": "bylNo",
    "별표명": "title",
    "별표종류": "kind",
    "관련법령명": "lawName",
    "관련법령ID": "lawId",
    "관련법령일련번호": "lawSeq",
    "법령종류": "lawKind",
    "소관부처명": "agency",
    "공포일자": "promulgated",
    "공포번호": "promulgationNo",
    "제개정구분명": "revisionType",
}


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Referer": BASE + "/"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def list_page(oc, page, display=100, knd=KND_FORM, save_to=None):
    """서식 목록 한 쪽. API 가 HWP·PDF 링크를 함께 준다."""
    q = urllib.parse.urlencode({"OC": oc, "target": "licbyl", "type": "XML",
                                "query": "*", "knd": knd,
                                "display": display, "page": page})
    raw = fetch(f"{API}?{q}")
    if save_to:
        os.makedirs(os.path.dirname(save_to), exist_ok=True)
        with open(save_to, "wb") as fp:
            fp.write(raw)
    xml = raw.decode("utf-8", "replace")
    total = re.search(r"<totalCnt>(\d+)</totalCnt>", xml)
    rows = []
    for block in re.findall(r"<licbyl id=\"\d+\">(.*?)</licbyl>", xml, re.S):
        row = {}
        for m in FIELD.finditer(block):
            value = m.group(2).strip()
            if value:
                row[m.group(1)] = value
        if row:
            rows.append(row)
    return int(total.group(1)) if total else 0, rows


def internal_mtime(blob):
    """HWP(OLE) 안에 기록된 마지막 수정 시각. 서식이 실제로 만들어진 때다."""
    try:
        ole = olefile.OleFileIO(io.BytesIO(blob))
        return ole.root.getmtime()
    except Exception:
        return None


def parse(blob):
    """매직 바이트로 고른다. 깨진 파일이 있어 예외는 삼킨다 —
    한 건 때문에 수집 전체가 멈추면 안 된다."""
    try:
        if blob[:4] == b"\xd0\xcf\x11\xe0":
            return parse_hwp(blob), "hwp"
        if blob[:2] == b"PK":
            return parse_hwpx(blob), "hwpx"
    except Exception:
        return None, ("hwp" if blob[:4] == b"\xd0\xcf\x11\xe0" else "hwpx")
    if blob[:4] == b"%PDF":
        return None, "pdf"
    return None, "bin"


def dedup_fonts(fonts):
    """HWP 는 한글·영문·한자·일어·기타·기호·사용자 칸마다 글꼴을 따로 적는다.
    같은 이름이 여러 번 나오므로 합치고, 몇 칸에 쓰였는지를 slots 로 남긴다."""
    counter = collections.Counter()
    for entries in fonts.values():
        for f in entries:
            counter[(f.get("face"), f.get("type"))] += 1
    return [{"face": face, "type": kind, "slots": n}
            for (face, kind), n in sorted(counter.items(),
                                          key=lambda kv: (-kv[1], kv[0][0] or ""))]


def load_manifest(path):
    """이미 받은 건을 flSeq 로 색인한다. 깨진 줄은 건너뛴다."""
    done = {}
    if not os.path.exists(path):
        return done
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            done[rec["flSeq"]] = rec
    return done


def shard(store, fl_seq, ext):
    return os.path.join(store, "files", fl_seq[-2:], f"{fl_seq}.{ext}")


def build_index(store, total=None):
    """manifest.jsonl → index.json. 망 접속 없이 언제든 다시 만들 수 있다."""
    manifest = os.path.join(store, "manifest.jsonl")
    records = list(load_manifest(manifest).values())
    records.sort(key=lambda r: int(r["flSeq"]))

    first_seen = {}
    for rec in records:
        digest = rec.get("sha256")
        rec["dupOf"] = None
        if not digest:
            continue
        if digest in first_seen:
            rec["dupOf"] = first_seen[digest]
        else:
            first_seen[digest] = rec["flSeq"]

    out = os.path.join(store, "index.json")
    with open(out, "w", encoding="utf-8") as fp:
        json.dump({
            "collected": time.strftime("%Y-%m-%d"),
            "source": "법제처 국가법령정보 OPEN API (target=licbyl, knd=2 서식)",
            "sampling": {
                "total": total,
                "collected": len(records),
                "unique": len(first_seen),
                "robots": "law.go.kr — User-agent * 에 Allow: / (2026-09-30 확인)",
                "note": ("fileMtime 은 HWP(OLE) 안에 기록된 수정 시각으로 "
                         "법령 공포일과 다르다. 서식이 실제로 만들어진 시점을 뜻한다. "
                         "lag 은 공포연도 − 파일연도, 곧 서식이 몇 해 묵었는가다"),
                "store": store,
            },
            "documents": records,
        }, fp, ensure_ascii=False, indent=1)
    return out, len(records), len(first_seen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oc", help="OPEN API 인증키")
    ap.add_argument("--store", default=STORE, help="원본·목록을 보관할 디렉터리")
    ap.add_argument("--limit", type=int, default=200, help="수집할 서식 수")
    ap.add_argument("--all", action="store_true", help="전수 수집")
    ap.add_argument("--display", type=int, default=100)
    ap.add_argument("--delay", type=float, default=0.35)
    ap.add_argument("--build-index", action="store_true",
                    help="내려받지 않고 manifest 로 index.json 만 만든다")
    args = ap.parse_args()

    store = os.path.expanduser(args.store)
    manifest = os.path.join(store, "manifest.jsonl")

    if args.build_index:
        out, n, uniq = build_index(store)
        print(f"{n:,}건 (고유 {uniq:,}) → {out}", file=sys.stderr)
        return

    if not args.oc:
        ap.error("--oc 가 필요합니다")
    os.makedirs(store, exist_ok=True)

    total, _ = list_page(args.oc, 1, 1)
    target = total if args.all else min(args.limit, total)
    done = load_manifest(manifest)
    print(f"서식 전체 {total:,}건 · 목표 {target:,}건 · 보유 {len(done):,}건",
          file=sys.stderr)

    log = open(manifest, "a", encoding="utf-8")
    fresh = errors = skipped = 0
    page = 1
    while len(done) < target:
        try:
            _, rows = list_page(args.oc, page, args.display,
                                save_to=os.path.join(store, "list",
                                                     f"page-{page:04d}.xml"))
        except Exception as exc:
            print(f"  목록 {page}쪽 실패: {exc}", file=sys.stderr)
            break
        if not rows:
            break
        time.sleep(args.delay)

        for row in rows:
            if len(done) >= target:
                break
            link = row.get("별표서식파일링크")
            if not link:
                continue
            m = re.search(r"flSeq=(\d+)", link)
            if not m:
                continue
            fl = m.group(1)
            if fl in done:
                skipped += 1
                continue
            try:
                blob = fetch(BASE + link)
            except Exception as exc:
                errors += 1
                print(f"  받기 실패 flSeq={fl}: {exc}", file=sys.stderr)
                time.sleep(args.delay)
                continue
            time.sleep(args.delay)

            parsed, ext = parse(blob)
            path = shard(store, fl, ext)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fp:
                fp.write(blob)

            mtime = internal_mtime(blob)
            pdf = row.get("별표서식PDF파일링크")
            promulgated = row.get("공포일자") or ""
            rec = {"flSeq": fl,
                   "url": BASE + link,
                   "path": os.path.relpath(path, store),
                   "fetched": time.strftime("%Y-%m-%dT%H:%M:%S")}
            for src, dst in COLUMNS.items():
                rec[dst] = row.get(src)
            rec.update({
                "pdfUrl": BASE + pdf if pdf else None,
                "format": parsed["format"] if parsed else ext.upper(),
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "fileMtime": mtime.isoformat() if mtime else None,
                "fileYear": mtime.year if mtime else None,
                "lag": (int(promulgated[:4]) - mtime.year
                        if mtime and promulgated[:4].isdigit() else None),
                "fonts": dedup_fonts(parsed["fonts"]) if parsed else [],
                "substitutions": parsed["substitutions"] if parsed else [],
            })
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            done[fl] = rec
            fresh += 1

        print(f"  {page}쪽 · 보유 {len(done):,}건 "
              f"(새로 {fresh:,} · 건너뜀 {skipped:,} · 오류 {errors})",
              file=sys.stderr, flush=True)
        page += 1

    log.close()
    out, n, uniq = build_index(store, total)
    print(f"\n{n:,}건 (고유 {uniq:,}) · 새로 {fresh:,} · 오류 {errors} → {out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()

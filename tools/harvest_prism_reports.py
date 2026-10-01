#!/usr/bin/env python3
"""정책연구관리시스템(PRISM)에서 기관별·문서종류별 보고서의 폰트 사용을 수집한다.

왜 이 자료인가
  법령 서식이 '국민이 채워 넣는 문서' 라면, 정책연구 산출물은 **기관이 끝까지
  만들어 낸 완성본**이다. 보도자료(읽기 전용)와 서식(빈칸) 사이에 빠져 있던
  종류다. 표지·목차·표·각주·참고문헌이 다 들어간 긴 문서라 조판이 어긋나면
  쪽 수가 크게 밀린다.

무엇이 다양한가
  한 과제에 문서가 여러 벌 붙는다. 최종보고서만이 아니라 과업지시서·용역계약서·
  심의신청서·평가결과서·중간점검결과서·활용결과보고서까지 있다. **같은 기관이
  같은 시기에 만든 서로 다른 장르**를 한자리에서 볼 수 있다.

수집 원칙
  - robots.txt 확인: prism.go.kr 은 User-agent * 에 Disallow: (제한 없음)
  - 공개 목록에 '공개' 로 표시된 과제만 받는다
  - 공공누리(KOGL) 유형이 함께 제공되므로 그대로 기록한다
  - 순차 요청 + 요청 간 지연. 본문은 저장하되 폰트·메타데이터만 집계한다
  - PDF 는 받지 않는다. PDF 로는 한컴 고유 포맷(HFT) 글꼴을 식별할 수 없다

접근 방식
  PRISM 은 SPA 이고 API 앞에 비정상 접근 차단이 걸려 있다. 그래서 브라우저를
  띄워 **페이지 문맥 안에서** 같은 API 를 호출한다. 사람이 쓰는 경로와 같다.

저장 구조 (--store, 기본 ~/dev/prism-report-data)
  files/<기관번호>/<과제ID>__<파일명>    내려받은 원본
  manifest.jsonl                       한 줄에 한 파일. 받는 즉시 덧붙인다
  index.json                           manifest 를 모아 만든 배포본

사용법
  python3 harvest_prism_reports.py --central --per-inst 30
  python3 harvest_prism_reports.py --all-inst --per-inst 20
  python3 harvest_prism_reports.py --build-index
"""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import sys
import time

import olefile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harvest_gov_doc_fonts import parse_hwp, parse_hwpx

BE = "https://api.prism.go.kr/prism-be-asmt"
HOME = "https://www.prism.go.kr/"
STORE = os.path.expanduser("~/dev/prism-report-data")

# 중앙행정기관으로 볼 이름. 지방자치단체(도·시·군·구)와 교육청을 가른다
CENTRAL = re.compile(r"(부|처|청|원|위원회|실)$")
LOCAL = re.compile(r"(특별시|광역시|특별자치|도\s|시$|군$|구$|교육청|도교육청)")

# 파일 종류 코드 → 읽을 수 있는 이름. 코드표가 공개돼 있지 않아
# 실제 파일명에서 되짚어 정리했다. 모르는 코드는 코드 그대로 남긴다
FILE_KIND = {
    "D0150003": "부분공개·요약본",
    "D0150004": "최종보고서",
    "D0150005": "평가 결과서",
    "D0150006": "과업지시서",
    "D0150007": "용역계약서",
    "D0150008": "심의결과서",
    "D0150009": "연구계획서",
    "D0150010": "심의신청서",
    "D0150011": "선정 결과보고서",
    "D0150012": "추진계획서·착수보고서",
    "D0150013": "선정 결과보고서",
    "D0150014": "중간점검 결과서",
    "D0150015": "중간점검 결과서",
    "D0150016": "평가 결과서",
    "D0150018": "활용결과 보고서",
    "D0150019": "윤리 준수 서약서",
    "D0150020": "심의신청서",
    "D0150022": "윤리 자가점검표",
}

FETCH_JSON = """async ([u, b]) => {
  const r = await fetch(u, {method:'POST',
    headers:{'Content-Type':'application/json'}, body:b});
  return r.status + '|' + (await r.text());
}"""

FETCH_BIN = """async ([u, b]) => {
  const r = await fetch(u, {method:'POST',
    headers:{'Content-Type':'application/json'}, body:b});
  const v = new Uint8Array(await r.arrayBuffer());
  let s = '';
  const CH = 0x8000;
  for (let i = 0; i < v.length; i += CH)
    s += String.fromCharCode.apply(null, v.subarray(i, i + CH));
  return r.status + '|' + btoa(s);
}"""


class Prism:
    """브라우저를 한 번 띄워 두고 페이지 문맥으로 API 를 부른다."""

    def __init__(self, delay=0.35):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self.page = self._browser.new_page()
        self.page.goto(HOME, wait_until="networkidle", timeout=60000)
        self.page.wait_for_timeout(1500)
        self.delay = delay

    def close(self):
        self._browser.close()
        self._pw.stop()

    def json(self, path, payload):
        raw = self.page.evaluate(FETCH_JSON, [BE + path, json.dumps(payload)])
        time.sleep(self.delay)
        status, body = raw.split("|", 1)
        if status != "200":
            raise RuntimeError(f"{path} → HTTP {status}")
        return json.loads(body)["resultData"]

    def binary(self, path, payload):
        raw = self.page.evaluate(FETCH_BIN, [BE + path, json.dumps(payload)])
        time.sleep(self.delay)
        status, b64 = raw.split("|", 1)
        if status != "200":
            raise RuntimeError(f"{path} → HTTP {status}")
        return base64.b64decode(b64 + "=" * (-len(b64) % 4))


def institutions(api, central_only):
    rows = api.json("/v1/entire/list-inst", {})["instList"]
    if not central_only:
        return rows
    return [r for r in rows
            if CENTRAL.search(r["instNm"]) and not LOCAL.search(r["instNm"])]


def internal_mtime(blob):
    try:
        return olefile.OleFileIO(io.BytesIO(blob)).root.getmtime()
    except Exception:
        return None


def parse(blob):
    """확장자를 믿지 않고 매직 바이트로 고른다. 그래도 깨진 파일이 있어
    예외는 삼킨다 — 한 건 때문에 수집 전체가 멈추면 안 된다."""
    try:
        if blob[:4] == b"\xd0\xcf\x11\xe0":
            return parse_hwp(blob)
        if blob[:2] == b"PK":
            return parse_hwpx(blob)
    except Exception:
        return None
    return None


def dedup_fonts(fonts):
    """HWP 는 언어 칸마다 글꼴을 따로 적는다. 합치고 칸 수를 남긴다."""
    import collections
    c = collections.Counter()
    for entries in fonts.values():
        for f in entries:
            c[(f.get("face"), f.get("type"))] += 1
    return [{"face": a, "type": b, "slots": n}
            for (a, b), n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0][0] or ""))]


def safe(name, limit=80):
    name = re.sub(r"[/\\:\x00-\x1f]", "_", name).strip()
    return name[:limit] or "unnamed"


def load_manifest(path):
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
            done[rec["key"]] = rec
    return done


def build_index(store):
    records = list(load_manifest(os.path.join(store, "manifest.jsonl")).values())
    records.sort(key=lambda r: (r.get("agency") or "", r["asmtId"], r["key"]))
    first = {}
    for rec in records:
        d = rec.get("sha256")
        rec["dupOf"] = first.get(d)
        first.setdefault(d, rec["key"])
    out = os.path.join(store, "index.json")
    with open(out, "w", encoding="utf-8") as fp:
        json.dump({
            "collected": time.strftime("%Y-%m-%d"),
            "source": "정책연구관리시스템 PRISM 공개 API (entire/list-organtheme · entire/info)",
            "sampling": {
                "files": len(records),
                "tasks": len({r["asmtId"] for r in records}),
                "agencies": len({r.get("agency") for r in records}),
                "robots": "prism.go.kr — User-agent * 에 Disallow: (2026-09-30 확인)",
                "note": ("HWP·HWPX 만 받는다. PDF 로는 한컴 고유 포맷(HFT) 글꼴을 "
                         "식별할 수 없기 때문이다. kogl 은 과제에 표시된 공공누리 유형이다"),
                "store": store,
            },
            "documents": records,
        }, fp, ensure_ascii=False, indent=1)
    return out, len(records)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=STORE)
    ap.add_argument("--per-inst", type=int, default=30, help="기관당 과제 수")
    ap.add_argument("--central", action="store_true", help="중앙행정기관만")
    ap.add_argument("--all-inst", action="store_true", help="지자체 포함 전체 기관")
    ap.add_argument("--since", default="2010.01.01")
    ap.add_argument("--until", default=time.strftime("%Y.%m.%d"))
    ap.add_argument("--per-year", type=int, metavar="N",
                    help="기관 × 연도 칸마다 최대 N건. 최근 편향을 없앤다")
    ap.add_argument("--years", default="2010-2026", help="--per-year 와 함께 쓸 연도 범위")
    ap.add_argument("--delay", type=float, default=0.35)
    ap.add_argument("--build-index", action="store_true")
    args = ap.parse_args()

    store = os.path.expanduser(args.store)
    manifest = os.path.join(store, "manifest.jsonl")

    if args.build_index:
        out, n = build_index(store)
        print(f"{n:,}개 파일 → {out}", file=sys.stderr)
        return

    os.makedirs(store, exist_ok=True)
    done = load_manifest(manifest)
    api = Prism(args.delay)
    try:
        insts = institutions(api, central_only=not args.all_inst)
        print(f"기관 {len(insts)}곳 · 기관당 과제 {args.per_inst}건 · 보유 파일 "
              f"{len(done):,}개", file=sys.stderr)

        log = open(manifest, "a", encoding="utf-8")
        got = errors = 0
        if args.per_year:
            lo, hi = (int(v) for v in args.years.split("-"))
            windows = [(f"{y}.01.01", f"{y}.12.31", y) for y in range(lo, hi + 1)]
            size = args.per_year
        else:
            windows = [(args.since, args.until, None)]
            size = args.per_inst

        for i, inst in enumerate(insts, 1):
            gno, name = inst["instGrntNo"], inst["instNm"]
            tasks, before = [], got
            for start, end, year in windows:
                try:
                    rd = api.json("/v1/entire/list-organtheme", {
                        "asmtNm": "", "startDate": start, "endDate": end,
                        "rcmdtnAsmtYn": "", "instGrntNo": gno,
                        "currentPage": 1, "pageSize": size})
                except Exception as exc:
                    print(f"  [{i}/{len(insts)}] {name} {year or ''} 목록 실패: {exc}",
                          file=sys.stderr)
                    errors += 1
                    continue
                tasks.extend(rd.get("organthemeRschList") or [])

            for t in tasks:
                asmt = t["asmtId"]
                try:
                    detail = api.json("/v1/entire/info", {"asmtId": asmt})
                except Exception:
                    errors += 1
                    continue
                files = detail.get("asmtFileList") or []
                kogl = (detail.get("koglDetail") or {}).get("cdNm")
                head = detail.get("asmtDetail") or {}
                for f in files:
                    ext = f["fileNm"].rsplit(".", 1)[-1].lower()
                    if ext not in ("hwp", "hwpx"):
                        continue          # PDF 는 HFT 를 못 잡는다
                    key = f"{asmt}|{f['fileTypeCd']}|{f['fileSn']}|{f['fileWkky']}"
                    if key in done:
                        continue
                    try:
                        blob = api.binary("/v1/progress/download-file", {
                            "asmtId": asmt, "fileTypeCd": f["fileTypeCd"],
                            "fileSn": f["fileSn"], "fileWkky": f["fileWkky"],
                            "pdfTrsfYn": f.get("pdfTrsfYn", "N")})
                    except Exception:
                        errors += 1
                        continue
                    if len(blob) < 512:
                        errors += 1
                        continue
                    path = os.path.join(store, "files", str(gno),
                                        f"{asmt}__{safe(f['fileNm'])}")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "wb") as fp:
                        fp.write(blob)
                    parsed = parse(blob)
                    mtime = internal_mtime(blob)
                    log.write(json.dumps({
                        "key": key,
                        "asmtId": asmt,
                        "asmtNm": t.get("asmtNm"),
                        "agency": t.get("instNm"),
                        "instGrntNo": gno,
                        "researcher": t.get("rschInstNm"),
                        "category": t.get("clsfSysNm") or head.get("clsfSysNm"),
                        "categoryTop": head.get("hghrkFwkClsfSysNm"),
                        "status": t.get("prgrsSttsCd"),
                        "begin": t.get("rschBgngYmd"), "end": t.get("rschEndYmd"),
                        "kogl": kogl,
                        "fileName": f["fileNm"],
                        "fileTypeCd": f["fileTypeCd"],
                        "docKind": FILE_KIND.get(f["fileTypeCd"], f["fileTypeCd"]),
                        "path": os.path.relpath(path, store),
                        "format": parsed["format"] if parsed else None,
                        "bytes": len(blob),
                        "sha256": hashlib.sha256(blob).hexdigest(),
                        "fileMtime": mtime.isoformat() if mtime else None,
                        "fileYear": mtime.year if mtime else None,
                        "fonts": dedup_fonts(parsed["fonts"]) if parsed else [],
                        "substitutions": parsed["substitutions"] if parsed else [],
                        "fetched": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }, ensure_ascii=False) + "\n")
                    log.flush()
                    done[key] = True
                    got += 1

            print(f"  [{i}/{len(insts)}] {name} · 과제 {len(tasks)} · "
                  f"파일 +{got - before} (누적 {got:,} · 오류 {errors})",
                  file=sys.stderr, flush=True)
        log.close()
    finally:
        api.close()

    out, n = build_index(store)
    print(f"\n파일 {n:,}개 · 이번에 {got:,}개 · 오류 {errors} → {out}", file=sys.stderr)


if __name__ == "__main__":
    main()

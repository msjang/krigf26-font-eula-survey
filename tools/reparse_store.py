#!/usr/bin/env python3
"""저장해 둔 원본을 다시 읽어 manifest 를 갱신한다 — 다시 내려받지 않는다.

왜 필요한가
  판독기를 고치면 이미 모은 자료도 다시 읽어야 한다. 원본을 저장소에 두는
  이유가 이것이다. 망에 다시 요청하지 않고 같은 파일로 다시 판독한다.

무엇을 갱신하나
  fonts · substitutions · format 만 덮어쓴다. 수집 당시의 메타데이터
  (언제 받았는가, 어디서 받았는가, 해시)는 건드리지 않는다.

사용법
  python3 reparse_store.py --store ~/dev/law-form-data
  python3 reparse_store.py --store ~/dev/prism-report-data
"""

import argparse
import collections
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harvest_gov_doc_fonts import parse_hwp, parse_hwpx


def parse(blob):
    try:
        if blob[:4] == b"\xd0\xcf\x11\xe0":
            return parse_hwp(blob)
        if blob[:2] == b"PK":
            return parse_hwpx(blob)
    except Exception:
        return None
    return None


def dedup_fonts(fonts):
    c = collections.Counter()
    for entries in fonts.values():
        for f in entries:
            c[(f.get("face"), f.get("type"))] += 1
    return [{"face": a, "type": b, "slots": n}
            for (a, b), n in sorted(c.items(),
                                    key=lambda kv: (-kv[1], kv[0][0] or ""))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    store = os.path.expanduser(args.store)
    manifest = os.path.join(store, "manifest.jsonl")
    records = []
    with open(manifest, encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    changed = missing = failed = 0
    for rec in records:
        path = os.path.join(store, rec.get("path") or "")
        if not rec.get("path") or not os.path.exists(path):
            missing += 1
            continue
        with open(path, "rb") as fp:
            parsed = parse(fp.read())
        if not parsed:
            failed += 1
            continue
        before = json.dumps(rec.get("substitutions"), sort_keys=True)
        rec["fonts"] = dedup_fonts(parsed["fonts"])
        rec["substitutions"] = parsed["substitutions"]
        rec["format"] = parsed["format"]
        if json.dumps(rec["substitutions"], sort_keys=True) != before:
            changed += 1

    print(f"{len(records):,}건 · 대체 지정이 달라진 것 {changed:,} · "
          f"파일 없음 {missing} · 판독 실패 {failed}", file=sys.stderr)
    if args.dry_run:
        return

    shutil.copy(manifest, manifest + ".bak")
    with open(manifest, "w", encoding="utf-8") as fp:
        for rec in records:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"manifest 갱신 (이전본 {os.path.basename(manifest)}.bak)", file=sys.stderr)


if __name__ == "__main__":
    main()

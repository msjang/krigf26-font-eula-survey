#!/usr/bin/env python3
"""여러 벌로 모은 보도자료 표본을 하나로 합치고 중복을 제거한다.

왜 필요한가
  보도자료는 설계를 바꿔 가며 일곱 벌을 모았다(연도 층화, 부처 집중, 장르 비교…).
  그런데 서로 겹친다. 합치지 않고 "표본 두 벌" 이라 부르면 **같은 문서를 두 번
  센다.** 실제로 연도 층화 1,020건과 3,200건 사이에 571건이 겹쳤다.

무엇을 하나
  `newsId` 로 같은 문서를 묶는다. 같은 문서가 여러 벌에 있으면 **글꼴 정보가 더
  풍부한 쪽**(판독한 글꼴 수가 많은 쪽)을 남기고, 어느 표본에서 왔는지를
  `samples` 에 모두 적는다.

사용법
  python3 merge_press_samples.py data/gov-doc-fonts*.json --out data/merged.json
"""

import argparse
import collections
import glob
import json
import os
import sys


def load(path):
    with open(path, encoding="utf-8") as fp:
        d = json.load(fp)
    return d.get("documents") or [], d.get("sampling") or {}


def richness(doc):
    """어느 사본을 남길지 고르는 기준 — 판독한 글꼴이 많을수록 낫다."""
    f = doc.get("fonts")
    if isinstance(f, dict):
        return sum(len(v) for v in f.values())
    return len(f or [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    files = []
    for p in args.paths:
        files.extend(sorted(glob.glob(p)))

    best, origin, per_file = {}, collections.defaultdict(set), {}
    for path in files:
        docs, _ = load(path)
        if not docs:
            continue
        tag = os.path.basename(path)
        per_file[tag] = len(docs)
        for doc in docs:
            key = str(doc.get("newsId") or doc.get("url") or doc.get("filename"))
            if not key or key == "None":
                continue
            origin[key].add(tag)
            if key not in best or richness(doc) > richness(best[key]):
                best[key] = doc

    for key, doc in best.items():
        doc["samples"] = sorted(origin[key])

    merged = sorted(best.values(), key=lambda d: (str(d.get("date") or ""), str(d.get("newsId"))))
    total = sum(per_file.values())
    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump({
            "collected": "2026-10-01",
            "source": "정책브리핑(korea.kr) 보도자료 첨부 — 표본 7벌을 newsId 로 합친 것",
            "sampling": {
                "inputs": per_file,
                "rows": total,
                "unique": len(merged),
                "duplicates": total - len(merged),
                "note": ("같은 문서가 여러 표본에 들어 있어 합쳤다. 어느 표본에서 왔는지는 "
                         "문서마다 samples 에 적었다. 설계가 다른 표본을 합친 것이므로 "
                         "연도·부처 분포는 어느 한 설계를 따르지 않는다"),
            },
            "documents": merged,
        }, fp, ensure_ascii=False, indent=1)

    print(f"입력 {len(per_file)}벌 · 행 {total:,} · 고유 {len(merged):,} · "
          f"중복 {total - len(merged):,}", file=sys.stderr)
    for k, v in sorted(per_file.items()):
        print(f"   {k:46s} {v:6,}", file=sys.stderr)
    c = collections.Counter(len(d["samples"]) for d in merged)
    print(f"\n표본 중복도: " + " · ".join(f"{k}벌 {v:,}건" for k, v in sorted(c.items())),
          file=sys.stderr)


if __name__ == "__main__":
    main()

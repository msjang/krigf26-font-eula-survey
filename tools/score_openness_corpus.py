#!/usr/bin/env python3
"""수집해 둔 문서 모음에 개방성 점수를 매긴다 — 파일을 다시 열지 않는다.

왜 따로 두나
  [`openness_check.py`](openness_check.py) 는 문서 **한 건**을 열어 채점한다.
  이 조사는 자료원 세 벌(법령 서식·정책연구·보도자료)을 모아 두었고, 그 안에
  이미 글꼴 이름과 대체 지정이 들어 있다. 같은 판정 기준을 그 기록에 그대로
  적용해 **자료원끼리 견줄 수 있게** 한다.

무엇을 견주나
  문서 하나의 점수는 `재현 가능한 글꼴 수 / 전체 글꼴 수 × 100` 이다.
  자료원마다 평균·중앙값과 **0점 문서의 비율**을 낸다. 0점은 그 문서를
  자유 소프트웨어만으로 같은 조판으로 재현할 길이 전혀 없다는 뜻이다.

사용법
  python3 score_openness_corpus.py <수집본.json[.gz]> [...] [--json out.json]
"""

import argparse
import collections
import gzip
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openness_check import DB_PATH, Judge


def load(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fp:
        return json.load(fp)


def fonts_of(doc):
    """수집본마다 fonts 모양이 달라 둘 다 받는다 — 목록이거나 언어별 묶음이다."""
    f = doc.get("fonts") or []
    if isinstance(f, dict):
        f = [e for v in f.values() for e in v]
    out = []
    for e in f:
        out.append(e.get("face") if isinstance(e, dict) else e)
    return [n for n in dict.fromkeys(out) if n]


def subs_of(doc):
    m = {}
    for s in doc.get("substitutions") or []:
        if isinstance(s, dict) and s.get("requested"):
            m.setdefault(s["requested"], s.get("substituted"))
    return m


def score(doc, judge):
    names = fonts_of(doc)
    if not names:
        return None
    sub = subs_of(doc)
    verdicts = [judge.judge({"name": n, "substitute": sub.get(n)})[0] for n in names]
    ok = sum(1 for v in verdicts if v == "OK")
    return {"score": round(100.0 * ok / len(names), 1),
            "fonts": len(names), "ok": ok,
            "verdicts": collections.Counter(verdicts)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json")
    args = ap.parse_args()

    judge = Judge(json.load(open(DB_PATH, encoding="utf-8")))
    summary = []
    for path in args.paths:
        d = load(path)
        docs = d.get("documents") or []
        rows = [r for r in (score(x, judge) for x in docs) if r]
        if not rows:
            print(f"{os.path.basename(path)}: 채점 0", file=sys.stderr)
            continue
        s = [r["score"] for r in rows]
        v = collections.Counter()
        for r in rows:
            v.update(r["verdicts"])
        zero = sum(1 for x in s if x == 0)
        item = {
            "corpus": os.path.basename(path),
            "documents": len(rows),
            "mean": round(statistics.mean(s), 1),
            "median": round(statistics.median(s), 1),
            "zeroScore": zero,
            "zeroPct": round(100.0 * zero / len(rows), 1),
            "fullScore": sum(1 for x in s if x == 100),
            "fontsPerDoc": round(sum(r["fonts"] for r in rows) / len(rows), 1),
            "verdicts": dict(v),
        }
        summary.append(item)
        print(f"\n=== {item['corpus']}  {item['documents']:,}건")
        print(f"   평균 {item['mean']}점 · 중앙 {item['median']}점 · "
              f"문서당 글꼴 {item['fontsPerDoc']}종")
        print(f"   0점 {zero:,}건 ({item['zeroPct']}%) · 100점 {item['fullScore']:,}건")
        print(f"   글꼴 판정 {dict(v)}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fp:
            json.dump({"judgedWith": os.path.basename(DB_PATH),
                       "note": ("점수는 재현 가능한 글꼴 수 / 전체 글꼴 수. "
                                "0점은 자유 소프트웨어만으로 같은 조판을 만들 길이 "
                                "전혀 없다는 뜻이다"),
                       "corpora": summary}, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

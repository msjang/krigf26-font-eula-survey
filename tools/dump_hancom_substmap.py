#!/usr/bin/env python3
"""한컴오피스가 스스로 선언한 글꼴 대체표를 그대로 읽어 정리한다.

무엇을 읽나
  Hnc/Shared/Fonts/hftinfo.dat   — 한컴 고유 포맷(HFT) 글꼴 목록
  Hnc/Shared/Fonts/fontinfo.dat  — [Subst Fonts - *] 대체 선언

무엇을 알 수 있나
  대체 선언은 한 단계 대응이 아니라 **연쇄**다. `,H` 는 HFT, `,T` 는 TTF 이고,
  설치된 글꼴이 나올 때까지 타고 내려간다. 그래서 같은 글꼴이라도 그 컴퓨터에
  무엇이 깔려 있느냐에 따라 착지점이 달라진다.

무엇을 하지 않나
  글꼴 파일을 열지 않는다. 제품이 평문으로 배포한 설정 파일만 읽는다.

사용법
  python3 dump_hancom_substmap.py [--root <Hnc/Shared 경로>] [--json]
"""

import argparse
import json
import os
import re
import sys

MAC = ("/Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# 저작권 문자열 → 권리자. 표기가 제각각이라 묶어서 본다
HOLDER = [
    ("한양정보통신", ("hanyang i&c", "hanyang information", "한양정보통신")),
    ("한양시스템즈", ("hanyang system", "한양시스템")),
    # 원문에 오타가 있다 — "Hangul & Copmuter". 표기 흔들림을 함께 잡는다
    ("한글과컴퓨터", ("hangul & comp", "hangul & copmu", "hangul and comp",
                 "hancom", "hnc", "한글과컴퓨터")),
    ("휴먼컴퓨터", ("human computers", "human license", "휴먼컴퓨터")),
    ("양재", ("yangjae", "양재")),
    ("한미디어", ("han media", "한미디어")),
    ("Microsoft", ("microsoft",)),
    ("Monotype", ("monotype",)),
    ("Bitstream", ("bitstream",)),
    ("Linotype/Heidelberger", ("heidelberger", "linotype")),
    ("윤디자인", ("yoondesign", "yoon design", "윤디자인")),
    ("산돌", ("sandoll", "산돌")),
]


# 권리자 → 계열. 이름이 달라도 같은 뿌리로 보이는 것을 한 칸에 모은다.
# 법인격이 같다는 뜻이 아니라, 표에서 나란히 보이게 하려는 묶음이다
LINEAGE = {
    "한양정보통신": "한양",
    "한양시스템즈": "한양",
    "한글과컴퓨터": "한컴",
    "휴먼컴퓨터": "휴먼",
    "양재": "양재",
    "한미디어": "한미",
    "윤디자인": "윤디",
    "산돌": "산돌",
    "Microsoft": "마소",
    "Monotype": "모노",
    "Bitstream": "비트",
    "Linotype/Heidelberger": "라이노",
}

# 글꼴 이름 자체가 권리자를 말하는 경우. 저작권 문자열을 못 읽었을 때 쓴다
NAME_HINT = (("한양", ("한양", "HY")),)


def lineage_from_name(name):
    for group, keys in NAME_HINT:
        if any(name.startswith(k) or k in name for k in keys):
            return group
    return None


def lineage(names):
    """권리자 목록을 계열로 줄인다."""
    out = []
    for n in (names if isinstance(names, list) else [names]):
        g = LINEAGE.get(n)
        if g and g not in out:
            out.append(g)
    return out


def holder(text):
    """저작권 문자열에서 권리자를 읽는다. 모르면 원문 앞부분을 돌려준다."""
    if not text:
        return None
    low = text.lower()
    for name, keys in HOLDER:
        if any(k in low for k in keys):
            return name
    return text.strip()[:38]


def hft_copyrights():
    """HFT 파일별 저작권 — 파일 헤더의 평문 문자열에서 읽은 것."""
    path = os.path.join(DATA, "hft-registry_2026-09-24.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fp:
        return {r["file"]: r.get("copyright") for r in json.load(fp)}


def ttf_copyrights():
    """글꼴 이름 → 저작권 — 이미 수행한 폰트 내장 라이선스 전수 조사에서."""
    out = {}
    for name in ("font-license-census_2026-09-24.json",
                 "win10-font-license-census_2026-09-29.json"):
        path = os.path.join(DATA, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fp:
            rows = json.load(fp)
        rows = rows if isinstance(rows, list) else rows.get("fonts", [])
        for r in rows:
            fam = r.get("family")
            if fam and r.get("copyright"):
                out.setdefault(fam, r["copyright"])
    return out


def read_ini(path):
    with open(path, "rb") as fp:
        text = fp.read().decode("utf-16-le", "replace").lstrip("﻿")
    out, sec = {}, None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("["):
            sec = line.strip("[]")
            out[sec] = []
        elif sec:
            out[sec].append(line)
    return out


def hft_names(root):
    """hftinfo.dat 이 선언한 HFT 글꼴 이름 → 언어 칸별 파일.

    한 글꼴 이름이 한글·영문·한자·일어·기타·기호·사용자 칸마다 **서로 다른
    파일**을 갖는다. 예컨대 `한양신명조` 는 한글 HGSMJ, 영문 ENSMJ(이탤릭
    ENSMJI 포함), 한자 HJSMJ, 일어 JPSMJ, 기타 FLSMJ, 기호 SPSMJ 로 여섯이다.
    이름 하나에 파일 하나가 아니다.
    """
    ini = read_ini(os.path.join(root, "Fonts", "hftinfo.dat"))
    names = {}
    for sec, lines in ini.items():
        if not sec.startswith("Font Definition"):
            continue
        lang = sec.split("-")[-1].strip()
        for line in lines:
            if "=" not in line:
                continue
            name, val = line.split("=", 1)
            parts = [p.strip() for p in val.split(",")]
            slots = [p for p in parts[:4] if p]      # Regular/Bold/Italic/BoldItalic
            rec = names.setdefault(name.strip(),
                                   {"files": {}, "vendor": "", "langs": []})
            if slots:
                rec["files"][lang] = slots
                rec["langs"].append(lang)
            if len(parts) > 4 and parts[4] and not rec["vendor"]:
                rec["vendor"] = parts[4]
    return names


def subst_table(root):
    """fontinfo.dat 의 [Subst Fonts - *] 를 (이름, 형식) → (이름, 형식) 로."""
    ini = read_ini(os.path.join(root, "Fonts", "fontinfo.dat"))
    table = {}
    for sec, lines in ini.items():
        if not sec.startswith("Subst Fonts"):
            continue
        for line in lines:
            if "=" not in line:
                continue
            left, right = line.split("=", 1)
            src = tuple(x.strip() for x in left.rsplit(",", 1))
            dst = tuple(x.strip() for x in right.split(",")[:2])
            if len(src) == 2 and len(dst) == 2:
                table.setdefault(src, dst)
    return table


def resolve(table, start, limit=12):
    """연쇄를 따라가며 경로를 모은다. 처음 만나는 TTF 가 착지점이다."""
    path, cur, seen = [], start, {start}
    while cur in table and len(path) < limit:
        cur = table[cur]
        if cur in seen:
            path.append(("(순환)", ""))
            break
        seen.add(cur)
        path.append(cur)
        if cur[1] == "T":
            break
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=MAC)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--table", action="store_true",
                    help="전수를 마크다운 표로 낸다 — 연쇄를 풀지 않고 선언된 한 단계만")
    ap.add_argument("--ask", action="store_true",
                    help="문의용 간이 표 — 글꼴 두 칸과 권리자 흐름만")
    args = ap.parse_args()
    root = os.path.expanduser(args.root)

    names = hft_names(root)
    table = subst_table(root)
    hft_cr = hft_copyrights()
    ttf_cr = ttf_copyrights()
    # 1차 — 이름마다 HFT 저작권자를 먼저 모은다. 대체 대상이 HFT 일 때
    # 그쪽 권리자도 같은 표에서 찾아 써야 하기 때문이다
    holders_of = {}
    for name, meta in names.items():
        hs = []
        for slots in meta["files"].values():
            for f in slots:
                h = holder(hft_cr.get(f))
                if h and h not in hs:
                    hs.append(h)
        if not hs and meta["vendor"]:
            hs = [holder(meta["vendor"]) or meta["vendor"]]
        holders_of[name] = hs

    rows = []
    for name, meta in sorted(names.items()):
        path = resolve(table, (name, "H"))
        first_ttf = next((p for p in path if p[1] == "T"), None)
        files = meta["files"]
        holders = holders_of[name]          # 언어 칸마다 다를 수 있어 목록이다
        dest = path[0][0] if path else None
        dest_holders = []
        if path and path[0][1] == "T":
            h = holder(ttf_cr.get(dest))
            dest_holders = [h] if h else ["미설치"]   # 이 컴퓨터에 없어 확인 못 함
        elif path:
            dest_holders = holders_of.get(dest, []) or ["확인 못 함"]
        src_line, dst_line = lineage(holders), lineage(dest_holders)
        # 저작권 문자열을 못 읽었으면 이름에서 읽는다 (HY·한양 → 한양)
        if not src_line:
            g = lineage_from_name(name)
            if g:
                src_line = [g]
        if dest and not dst_line:
            g = lineage_from_name(dest)
            if g:
                dst_line = [g]
        rows.append({
            "hft": name,
            "files": files,
            "fileCount": sum(len(v) for v in files.values()),
            "langs": meta["langs"],
            "vendor": meta["vendor"],
            "declared": path[0][0] if path else None,
            "declaredType": {"H": "HFT", "T": "TTF"}.get(path[0][1]) if path else None,
            "hftHolder": holders,
            "hftLineage": src_line,
            "substHolder": " · ".join(dest_holders) or None,
            "substLineage": dst_line,
            "sameHolder": bool(dst_line) and bool(set(src_line) & set(dst_line)),
            "chain": [f"{n}[{ 'HFT' if t=='H' else 'TTF' }]" for n, t in path],
            "landsOnTTF": first_ttf[0] if first_ttf else None,
            "hops": len(path),
        })

    if args.ask:
        order = {"TTF": 0, "HFT": 1, None: 2}
        rows.sort(key=lambda r: (order[r["declaredType"]],
                                 0 if r["sameHolder"] else 1,
                                 "·".join(r["hftLineage"]) or "~",
                                 "·".join(r["substLineage"]) or "~",
                                 r["hft"]))
        print("| # | HFT 폰트 | TTF 폰트 | 저작권자 | 메트릭 일치? |")
        print("|---:|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            dest = r["declared"] or "**선언 없음**"
            if r["declaredType"] == "HFT":
                dest += " (HFT)"
            flow = f"{'·'.join(r['hftLineage']) or '?'} → {'·'.join(r['substLineage']) or '?'}"
            if r["sameHolder"]:
                flow = f"**{flow}**"
            print(f"| {i} | {r['hft']} | {dest} | {flow} | |")
        return

    if args.table:
        # 같은 권리자 조합끼리 붙어 나오게 정렬한다
        order = {"TTF": 0, "HFT": 1, None: 2}
        rows.sort(key=lambda r: (order[r["declaredType"]],
                                 0 if r["sameHolder"] else 1,
                                 "·".join(r["hftLineage"]) or "~",
                                 "·".join(r["substLineage"]) or "~",
                                 r["hft"]))
        print("| # | **계열** | HFT 글꼴 | **HFT 저작권자** | 선언된 대체 | 형식 | "
              "**대체 저작권자** | 권리자 | 메트릭 일치? |")
        print("|---:|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            same = ("**같음**" if r["sameHolder"]
                    else ("다름" if r["substLineage"] else "—"))
            pair = " → ".join(["·".join(r["hftLineage"]) or "?",
                               "·".join(r["substLineage"]) or "?"])
            print(f"| {i} | {pair} | {r['hft']} | "
                  f"{' · '.join(r['hftHolder']) or '—'} | "
                  f"{r['declared'] or '**선언 없음**'} | {r['declaredType'] or '—'} | "
                  f"{r['substHolder'] or '—'} | {same} | |")
        return

    if args.json:
        json.dump({"source": "한컴오피스 hftinfo.dat · fontinfo.dat",
                   "root": root, "fonts": rows},
                  sys.stdout, ensure_ascii=False, indent=1)
        return

    declared = [r for r in rows if r["declared"]]
    print(f"HFT 글꼴 {len(rows)}종 · 대체 선언이 있는 것 {len(declared)}종 "
          f"· TTF 로 내려가는 것 {sum(1 for r in rows if r['landsOnTTF'])}종",
          file=sys.stderr)
    print(f"{'HFT 글꼴':22s} {'직접 대체':18s} {'TTF 착지':16s} 단계")
    for r in rows:
        if not r["declared"]:
            continue
        print(f"{r['hft']:22s} {(r['declared'] or '-')+'['+(r['declaredType'] or '')+']':18s} "
              f"{r['landsOnTTF'] or '-':16s} {r['hops']}  파일 {r['fileCount']}")


if __name__ == "__main__":
    main()

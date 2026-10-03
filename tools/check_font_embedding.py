#!/usr/bin/env python3
"""문서가 글꼴을 품고 있는지, 그리고 품을 수 있는지를 본다.

두 가지를 가른다
  **품고 있는가**  문서 안에 글꼴 파일이 실제로 들어 있는가
                 HWPX 는 `Contents/header.xml` 의 `isEmbedded` 와 `BinData/`,
                 HWP 5.0 은 `BinData` 스트림을 본다. 스트림 내용은 매직 바이트로
                 글꼴인지 이미지인지 가른다
  **품을 수 있는가** 그 글꼴의 `OS/2` `fsType` 이 임베딩을 허용하는가
                 0 Installable · 4 Preview&Print · 8 Editable 은 허용,
                 2 Restricted 는 금지. 그리고 **0x100 비트가 서브셋 금지**다.
                 "문서에 쓰인 글자만 넣기" 가 되는지는 이 비트가 가른다

왜 나누나
  "라이선스가 막아서 못 넣는다" 와 "넣을 수 있는데 안 넣는다" 는 전혀 다른
  문제다. 앞은 권리 문제이고 뒤는 지침 문제다.

한계
  한컴 고유 포맷(HFT)에는 `OS/2` 테이블이 없다. **허락 여부를 표시할 표준 자리가
  없으므로 이 도구로는 판정할 수 없다.**

사용법
  python3 check_font_embedding.py --docs <수집본.json[.gz]> [--sample N]
  python3 check_font_embedding.py --scan <문서 디렉터리> [--sample N]
"""

import argparse
import collections
import glob
import gzip
import json
import os
import random
import re
import sys
import zipfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CENSUS = ["font-license-census_2026-09-24.json", "win10-font-license-census_2026-09-29.json"]

SFNT = {b"\x00\x01\x00\x00": "TTF", b"OTTO": "OTF", b"true": "TTF", b"ttcf": "TTC"}
IMAGE = {b"\x89PNG": "PNG", b"GIF8": "GIF", b"BM": "BMP", b"\xff\xd8": "JPEG",
         b"II*\x00": "TIFF", b"MM\x00*": "TIFF"}


def kind_of(blob):
    for sig, name in SFNT.items():
        if blob.startswith(sig):
            return "FONT:" + name
    for sig, name in IMAGE.items():
        if blob.startswith(sig):
            return "IMG:" + name
    return "기타"


def scan_hwpx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        header = (z.read("Contents/header.xml").decode("utf-8", "replace")
                  if "Contents/header.xml" in names else "")
        flags = collections.Counter(re.findall(r'isEmbedded="(\d)"', header))
        kinds = collections.Counter()
        for n in names:
            if not n.startswith("BinData/"):
                continue
            blob = z.read(n)[:8]
            kinds[kind_of(blob)] += 1
    return flags, kinds


def scan_hwp(path):
    import olefile
    ole = olefile.OleFileIO(path)
    try:
        kinds = collections.Counter()
        for st in ole.listdir():
            if st[0] != "BinData":
                continue
            raw = ole.openstream(st).read()
            try:
                blob = zlib.decompress(raw, -15)[:8]
            except Exception:
                blob = raw[:8]
            kinds[kind_of(blob)] += 1
    finally:
        ole.close()
    return collections.Counter(), kinds


def load_fstype():
    out = {}
    for name in CENSUS:
        p = os.path.join(DATA, name)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as fp:
            rows = json.load(fp)
        rows = rows if isinstance(rows, list) else rows.get("fonts", [])
        for r in rows:
            fam, t = r.get("family"), r.get("fsType")
            if fam and t is not None:
                out.setdefault(fam, t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", help="문서 디렉터리 — 실제로 품고 있는지 본다")
    ap.add_argument("--docs", help="수집본 — 쓰인 글꼴이 품을 수 있는지 본다")
    ap.add_argument("--sample", type=int, default=1500)
    ap.add_argument("--json")
    args = ap.parse_args()
    report = {}

    if args.scan:
        files = [f for f in glob.glob(os.path.join(os.path.expanduser(args.scan), "**", "*"),
                                      recursive=True)
                 if f.lower().endswith((".hwp", ".hwpx"))]
        random.seed(1)
        if args.sample and len(files) > args.sample:
            files = random.sample(files, args.sample)
        flags, kinds, bad = collections.Counter(), collections.Counter(), 0
        for p in files:
            try:
                f, k = scan_hwpx(p) if p.lower().endswith(".hwpx") else scan_hwp(p)
            except Exception:
                bad += 1
                continue
            flags.update(f)
            kinds.update(k)
        fonts = sum(v for k, v in kinds.items() if k.startswith("FONT:"))
        report["embedded"] = {"files": len(files), "failed": bad,
                              "isEmbeddedFlags": dict(flags),
                              "binDataKinds": dict(kinds), "fontStreams": fonts}
        print(f"문서 {len(files):,}건 (판독 실패 {bad})")
        print(f"  isEmbedded 속성: {dict(flags) or '없음'}")
        print(f"  BinData 내용   : {dict(kinds) or '없음'}")
        print(f"  **글꼴 스트림   : {fonts}개**")

    if args.docs:
        opener = gzip.open if args.docs.endswith(".gz") else open
        with opener(args.docs, "rt", encoding="utf-8") as fp:
            docs = json.load(fp)["documents"]
        use = collections.Counter()
        for x in docs:
            f = x.get("fonts") or []
            if isinstance(f, dict):
                f = [e for v in f.values() for e in v]
            for e in {(e.get("face") if isinstance(e, dict) else e) for e in f}:
                if e:
                    use[e] += 1
        fs = load_fstype()
        known = {f: fs[f] for f in use if f in fs}
        restricted = [f for f, t in known.items() if t["raw"] & 0x0002]
        nosub = [f for f, t in known.items() if t["no_subsetting"]]
        report["permission"] = {
            "documents": len(docs), "fontsUsed": len(use),
            "fsTypeKnown": len(known), "fsTypeUnknown": len(use) - len(known),
            "restricted": sorted(restricted), "noSubsetting": sorted(nosub),
        }
        print(f"\n문서 {len(docs):,}건에 등장한 글꼴 {len(use):,}종")
        print(f"  fsType 확인 가능 {len(known)}종 · 불가 {len(use)-len(known)}종 "
              f"(HFT 등 OS/2 테이블이 없는 글꼴)")
        print(f"  **임베딩 금지(Restricted) {len(restricted)}종** {sorted(restricted) or ''}")
        print(f"  **서브셋 금지          {len(nosub)}종** {sorted(nosub) or ''}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fp:
            json.dump(report, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

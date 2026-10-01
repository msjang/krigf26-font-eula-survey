#!/usr/bin/env python3
"""문서를 만든 **프로그램과 그 판본**을 읽는다.

왜 보나
  공문서의 글꼴 구성이 바뀐 시점을 연도로만 보면 상관관계에 머문다. 파일에는
  그것을 만든 한컴오피스의 **빌드 번호**가 들어 있다. 같은 해에 저장된 문서라도
  빌드가 다르면 글꼴 구성이 다를 수 있으므로, 연도가 아니라 **도구 판본**으로
  갈라 보면 원인에 한 걸음 더 간다.

어디에 있나
  HWP 5.0  `\\x05HwpSummaryInformation` 속성 집합. 표준 PropertySet 형식이다
  HWPX     `version.xml` 의 `application` · `appVersion` 속성

개인정보 유의
  이 속성 집합에는 **작성자·최종 저장자의 이름**이 들어 있다. 실명인 경우가 많다.
  이 도구는 이름을 **그대로 내보내지 않는다.** 집계에 필요한 만큼만 해시로 바꾸고
  (`authorHash`), 원문은 `--with-names` 를 준 경우에만 담는다. 공개 자료에는
  해시만 싣는다.

사용법
  python3 dump_hwp_producer.py <디렉터리> [--json out.json] [--limit N]
"""

import argparse
import collections
import glob
import hashlib
import json
import os
import re
import struct
import sys
import zipfile

import olefile

STREAM = "\x05HwpSummaryInformation"
# 속성 집합의 표준 PID. 한컴도 이 번호를 따른다
PIDSI = {2: "title", 3: "subject", 4: "author", 5: "keywords", 6: "comments",
         8: "lastAuthor", 9: "revNumber", 12: "created", 13: "lastSaved",
         14: "pages", 18: "appName"}
BUILD = re.compile(r"(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")
PLATFORM = re.compile(r"(WIN32LE|WIN64LE|MAC|LINUX|ANDROID)?\s*"
                      r"(Windows[_A-Za-z0-9]*|Mac[_A-Za-z0-9.]*|Linux[_A-Za-z0-9]*)")


def read_propertyset(blob):
    """표준 PropertySet 을 직접 읽는다. olefile 의 파서가 한컴 스트림에서
    문자열 경계를 잘못 잡아 값이 서로 섞여 나오기에 따로 구현한다."""
    if len(blob) < 48:
        return {}
    num = struct.unpack_from("<I", blob, 24)[0]
    if not num:
        return {}
    sec = struct.unpack_from("<I", blob, 44)[0]          # 첫 섹션 오프셋
    if sec + 8 > len(blob):
        return {}
    count = struct.unpack_from("<I", blob, sec + 4)[0]
    out = {}
    for i in range(min(count, 64)):
        base = sec + 8 + i * 8
        if base + 8 > len(blob):
            break
        pid, off = struct.unpack_from("<II", blob, base)
        at = sec + off
        if at + 4 > len(blob):
            continue
        vt = struct.unpack_from("<I", blob, at)[0]
        try:
            if vt == 31:                                  # VT_LPWSTR
                n = struct.unpack_from("<I", blob, at + 4)[0]
                raw = blob[at + 8: at + 8 + n * 2]
                out[pid] = raw.decode("utf-16-le", "replace").rstrip("\x00")
            elif vt == 30:                                # VT_LPSTR
                n = struct.unpack_from("<I", blob, at + 4)[0]
                out[pid] = blob[at + 4 + 4: at + 8 + n].decode("cp949", "replace").rstrip("\x00")
            elif vt == 3:                                 # VT_I4
                out[pid] = struct.unpack_from("<i", blob, at + 4)[0]
            elif vt == 64:                                # VT_FILETIME
                lo, hi = struct.unpack_from("<II", blob, at + 4)
                out[pid] = (hi << 32) | lo
        except Exception:
            continue
    return out


def parse_build(text):
    if not text:
        return None, None, None
    m = BUILD.search(text)
    build = ".".join(m.groups()) if m else None
    p = PLATFORM.search(text[m.end():] if m else text)
    return build, (p.group(1) if p and p.group(1) else None), \
           (p.group(2) if p and p.group(2) else None)


def from_hwp(path):
    ole = olefile.OleFileIO(path)
    try:
        if not ole.exists(STREAM):
            return None
        props = read_propertyset(ole.openstream(STREAM).read())
        mtime = ole.root.getmtime()
    finally:
        ole.close()
    named = {PIDSI[k]: v for k, v in props.items() if k in PIDSI}
    # 빌드 문자열은 appName(18) 에 있는 것이 정석이나 한컴은 자리를 옮겨 쓰기도 한다
    src = next((str(v) for k, v in sorted(props.items())
                if isinstance(v, str) and BUILD.search(v)), None)
    build, abi, osname = parse_build(src)
    return {"format": "HWP 5.0", "build": build, "abi": abi, "os": osname,
            "appRaw": (src or "").strip() or None,
            "title": named.get("title"), "author": named.get("author"),
            "lastAuthor": named.get("lastAuthor"),
            "mtime": mtime.isoformat() if mtime else None,
            "year": mtime.year if mtime else None}


def from_hwpx(path):
    with zipfile.ZipFile(path) as z:
        if "version.xml" not in z.namelist():
            return None
        x = z.read("version.xml").decode("utf-8", "replace")
    attr = dict(re.findall(r'(\w+)="([^"]*)"', x))
    build, abi, osname = parse_build(attr.get("appVersion"))
    return {"format": "HWPX", "build": build, "abi": abi, "os": osname,
            "appRaw": attr.get("appVersion"), "application": attr.get("application"),
            "xmlVersion": attr.get("xmlVersion"),
            "major": attr.get("major"), "minor": attr.get("minor"),
            "title": None, "author": None, "lastAuthor": None,
            "mtime": None, "year": None}


def anonymise(rec, keep):
    """이름은 해시로 바꾼다. 집계에는 해시로 충분하다."""
    for k in ("author", "lastAuthor"):
        v = rec.get(k)
        if not v:
            continue
        rec[k + "Hash"] = hashlib.sha256(v.encode("utf-8")).hexdigest()[:12]
        if not keep:
            rec[k] = None
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--with-names", action="store_true",
                    help="작성자 이름을 그대로 담는다. 공개 자료에는 쓰지 않는다")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        p = os.path.expanduser(p)
        files.extend(sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True))
                     if os.path.isdir(p) else glob.glob(p))
    files = [f for f in files if f.lower().endswith((".hwp", ".hwpx"))]
    if args.limit:
        files = files[:args.limit]

    rows, fail = [], 0
    for f in files:
        try:
            rec = from_hwpx(f) if f.lower().endswith(".hwpx") else from_hwp(f)
        except Exception:
            rec = None
        if not rec:
            fail += 1
            continue
        rec["file"] = os.path.basename(f)
        rows.append(anonymise(rec, args.with_names))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fp:
            json.dump({"files": len(files), "parsed": len(rows), "failed": fail,
                       "note": ("작성자 이름은 해시로만 담는다. 원문은 --with-names "
                                "를 준 경우에만 들어간다"),
                       "documents": rows}, fp, ensure_ascii=False, indent=1)

    print(f"{len(rows):,} / {len(files):,} 판독 (실패 {fail:,})", file=sys.stderr)
    b = collections.Counter(r["build"] for r in rows if r["build"])
    print("\n빌드 상위 12")
    for k, v in b.most_common(12):
        print(f"   {k:16s} {v:6,}")
    o = collections.Counter(r["os"] for r in rows if r.get("os"))
    print("\n작성 OS:", o.most_common(8))


if __name__ == "__main__":
    main()

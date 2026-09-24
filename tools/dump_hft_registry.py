#!/usr/bin/env python3
"""한컴오피스 번들 HFT 폰트의 공급사·저작권·빌드일자를 수집한다.

HFT는 "Han Unified Font File" — 한컴 고유의 폰트 포맷이다. TrueType과 달리
name/OS-2 테이블이 없으므로 다음 두 곳에서 정보를 모은다.

  1. hftinfo.dat   폰트명=파일.HFT,,,,공급사,LCID,영문명   (UTF-16LE)
  2. 각 .HFT 파일 헤더의 평문 저작권 문자열과 8자리 빌드일자

이 스크립트는 파일을 규격/평문 그대로 읽을 뿐 개변하지 않는다.

사용법
  python3 dump_hft_registry.py [폰트디렉터리] > hft-registry.json

기본 경로
  /Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared/Fonts
"""

import json
import os
import re
import sys

DEFAULT_DIR = ("/Applications/Hancom Office HWP.app/Contents/Resources"
               "/Hnc/Shared/Fonts")
HEADER_MAGIC = b"Han Unified Font File"
COPYRIGHT_RE = re.compile(r"\(c\)\s*Copyright[^\x00\x1a]{0,80}", re.I)
BUILD_DATE_RE = re.compile(r"\b(?:19|20)\d{6}\b")
# hftinfo.dat 은 UTF-16LE INI 형식이다.
#   [Font Definition - Hangul]
#   명조=HGMJ.HFT,,,,한글과컴퓨터,1033,Myeongjo
#   HCI Tulip=HMETR.HFT,HMETRB.HFT,HMETRI.HFT,HMETRBI.HFT,휴먼컴퓨터,1033,HCI Tulip
# 값의 앞 4칸은 Regular/Bold/Italic/BoldItalic 파일 슬롯(비어 있을 수 있음),
# 그 다음이 공급사, LCID, 영문명이다.
STYLE_SLOTS = 4
VENDOR_INDEX = 4
LATIN_INDEX = 6
STYLES = ("Regular", "Bold", "Italic", "BoldItalic")


def read_hftinfo(path):
    """hftinfo.dat -> {대문자 파일명: {names, vendor, latinName, sections, styles}}"""
    if not os.path.exists(path):
        return {}
    text = open(path, "rb").read().decode("utf-16-le", errors="ignore")
    out = {}
    section = None
    for line in text.replace("\r", "\n").split("\n"):
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if "=" not in line or ".HFT" not in line.upper():
            continue
        name, rest = line.split("=", 1)
        name = name.strip()
        parts = [p.strip() for p in rest.split(",")]
        vendor = parts[VENDOR_INDEX] if len(parts) > VENDOR_INDEX else ""
        latin = parts[LATIN_INDEX] if len(parts) > LATIN_INDEX else ""
        # 공급사 자리에 파일명이 들어오는 변형은 채택하지 않는다
        if vendor.upper().endswith(".HFT"):
            vendor = ""
        for slot, filename in enumerate(parts[:STYLE_SLOTS]):
            if not filename.upper().endswith(".HFT"):
                continue
            entry = out.setdefault(filename.upper(), {
                "names": [], "vendor": None, "latinName": None,
                "sections": [], "styles": []})
            if name and name not in entry["names"]:
                entry["names"].append(name)
            if section and section not in entry["sections"]:
                entry["sections"].append(section)
            if STYLES[slot] not in entry["styles"]:
                entry["styles"].append(STYLES[slot])
            entry["vendor"] = entry["vendor"] or (vendor or None)
            entry["latinName"] = entry["latinName"] or (latin or None)
    return out


def read_hft_header(path):
    """HFT 헤더의 저작권 문자열과 빌드일자."""
    with open(path, "rb") as fp:
        head = fp.read(4096)
    if not head.startswith(HEADER_MAGIC):
        return None
    text = head.decode("latin-1")
    cop = COPYRIGHT_RE.search(text)
    date = BUILD_DATE_RE.search(text)
    return {
        "copyright": cop.group(0).strip() if cop else None,
        "buildDate": date.group(0) if date else None,
    }


def main(font_dir):
    info = read_hftinfo(os.path.join(font_dir, "hftinfo.dat"))
    rows = []
    for filename in sorted(os.listdir(font_dir)):
        if not filename.upper().endswith(".HFT"):
            continue
        header = read_hft_header(os.path.join(font_dir, filename))
        if header is None:
            continue
        meta = info.get(filename.upper(), {})
        names = meta.get("names") or []
        rows.append({
            "file": filename,
            "name": names[0] if names else None,
            "names": names,
            "vendor": meta.get("vendor"),
            "latinName": meta.get("latinName"),
            "styles": meta.get("styles") or [],
            "sections": meta.get("sections") or [],
            "copyright": header["copyright"],
            "buildDate": header["buildDate"],
        })
    json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR)

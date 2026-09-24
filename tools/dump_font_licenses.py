#!/usr/bin/env python3
"""폰트 파일에 내장된 라이선스 정보를 전수 추출한다.

TrueType/OpenType의 name table과 OS/2 table은 공개 표준(OpenType spec)이
정한 위치·형식에 따라 기록되어 있다. 이 스크립트는 규격에 따라 해당 필드를
읽어 표로 만들 뿐, 목적 코드를 원시 코드로 환원하는 과정을 포함하지 않는다.

추출 항목
  name ID 0   Copyright notice
  name ID 1   Font Family name
  name ID 4   Full font name
  name ID 5   Version string
  name ID 7   Trademark
  name ID 13  License Description   <- 파일에 내장된 라이선스 문구
  name ID 14  License Info URL
  OS/2 fsType 임베딩 제한 비트

TrueType Collection(.ttc/.otc)은 컬렉션에 담긴 모든 face를 각각 기록한다.

사용법
  pip install fonttools
  python3 dump_font_licenses.py <레이블>=<디렉터리> [...] > out.json
  python3 dump_font_licenses.py <디렉터리> [...] > out.json   # 레이블 생략 가능

예
  python3 dump_font_licenses.py \
    "macOS=/System/Library/Fonts" \
    "macOS=/System/Library/Fonts/Supplemental" \
    "MS Office=/Applications/Microsoft Word.app/Contents/Resources/DFonts" \
    "한컴오피스=/Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared/TTF/Install" \
    > fonts.json
"""

import glob
import json
import os
import sys

from fontTools.ttLib import TTFont, TTCollection

# OS/2 fsType 하위 4비트 — 임베딩 허용 수준
FSTYPE = {
    0: "Installable (제한 없음)",
    2: "Restricted License",
    4: "Preview & Print",
    8: "Editable",
}

WANTED_NAME_IDS = (0, 1, 3, 4, 5, 7, 13, 14)
EXTENSIONS = ("ttf", "otf", "ttc", "otc", "dfont")
COLLECTION_EXTENSIONS = (".ttc", ".otc")


def parse_args(argv):
    """`레이블=경로` 또는 `경로` 형태를 (레이블, 경로) 목록으로 만든다."""
    out = []
    for arg in argv:
        if "=" in arg and not os.path.exists(arg):
            label, path = arg.split("=", 1)
        else:
            label, path = os.path.basename(arg.rstrip("/")), arg
        out.append((label, path))
    return out


def collect_paths(path):
    if os.path.isfile(path):
        return [path]
    found = []
    for ext in EXTENSIONS:
        found += glob.glob(os.path.join(path, "*." + ext))
        found += glob.glob(os.path.join(path, "*." + ext.upper()))
    return sorted(set(found))


def read_names(font):
    """플랫폼/언어가 중복될 때는 Windows(3) + en-US/ko-KR 레코드를 우선한다."""
    out = {}
    try:
        records = font["name"].names
    except Exception:
        return out
    for rec in records:
        if rec.nameID not in WANTED_NAME_IDS:
            continue
        try:
            value = " ".join(rec.toUnicode().split())
        except Exception:
            continue
        preferred = rec.platformID == 3 and rec.langID in (0x409, 0x412)
        if rec.nameID not in out or preferred:
            out[rec.nameID] = value
    return out


def read_fstype(font):
    try:
        raw = font["OS/2"].fsType
    except Exception:
        return None
    return {
        "raw": raw,
        "embedding": FSTYPE.get(raw & 0x0F, f"other({raw & 0xF})"),
        "no_subsetting": bool(raw & 0x100),
        "bitmap_only": bool(raw & 0x200),
    }


def describe(font, path, label, face_index=None):
    names = read_names(font)
    row = {
        "source": label,
        "file": os.path.basename(path),
        "dir": os.path.dirname(path),
        "family": names.get(1, ""),
        "full": names.get(4, ""),
        "version": names.get(5, ""),
        "copyright": names.get(0, ""),
        "trademark": names.get(7, ""),
        "license": names.get(13, ""),
        "licenseURL": names.get(14, ""),
        "fsType": read_fstype(font),
    }
    if face_index is not None:
        row["faceIndex"] = face_index
    return row


def main(args):
    rows = []
    seen = set()
    for label, root in parse_args(args):
        for path in collect_paths(root):
            if path in seen:
                continue
            seen.add(path)
            is_collection = path.lower().endswith(COLLECTION_EXTENSIONS)
            try:
                if is_collection:
                    collection = TTCollection(path, lazy=True)
                    for index, font in enumerate(collection.fonts):
                        rows.append(describe(font, path, label, index))
                    collection.close()
                else:
                    font = TTFont(path, fontNumber=0, lazy=True)
                    rows.append(describe(font, path, label))
                    font.close()
            except Exception as exc:
                rows.append({"source": label,
                             "file": os.path.basename(path),
                             "dir": os.path.dirname(path),
                             "error": str(exc)})
    json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])

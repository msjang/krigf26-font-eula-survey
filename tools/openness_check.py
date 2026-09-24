#!/usr/bin/env python3
"""HWP / HWPX 문서의 개방성을 점검한다.

무엇을 재는가
  "이 문서를 자유 소프트웨어만으로 같은 레이아웃으로 재현할 수 있는가."

  상용 폰트를 쓰는 것 자체는 문제가 아니다. 문제는 그 폰트의 자리를 대신할
  제약 없는 구현체가 없어서, 자유 도구로는 같은 조판을 만들 수 없는 상태다.
  HWP/HWPX는 폰트마다 대체 폰트를 문서 안에 지정할 수 있으므로(substFont),
  거기에 자유 라이선스 폰트가 지정되어 있으면 재현 경로가 확보된다.

점수
  재현 가능한 폰트 수 / 전체 폰트 수 x 100

  폰트별 판정
    OK        수정까지 자유롭거나(OFL 등), 무료 사용·임베딩이 허용된 폰트다.
              후자는 수정이 금지되어 있으나 문서를 그대로 재현하는 데는 제약이 없다
    OK        상용이지만 재현 가능한 대체 폰트가 문서에 지정되어 있다
    MISSING   상용인데 대체 지정이 없거나, 지정된 대체 폰트도 상용이다
    권리불명   한컴이 "라이선스를 보유한 것이 아니다"라고 밝힌 Windows 기본 글꼴 9종
    UNKNOWN   라이선스를 확인할 근거를 찾지 못했다

무엇을 판정하지 않는가
  위법 여부를 판정하지 않는다. 이 저장소의 조사 결과는 폰트 메트릭 추출을
  금지하는 약관 조항이 한 건도 확인되지 않았다는 것이다. 실제 문제는
  "금지되어 있다"가 아니라 "적법한지 사전에 확인받을 경로가 없다"는 점이다.

사용법
  python3 openness_check.py 문서.hwpx [문서2.hwp ...]
  python3 openness_check.py --json 문서.hwpx
"""

import argparse
import io
import json
import os
import re
import struct
import sys
import zipfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "..", "data", "font-openness-db.json")

# 이름만으로 권리자를 추정할 수 있는 계열 — 한컴 도움말의 권리자 목록과
# 폰트 파일 저작권 표시에서 확인된 대응 관계
NAME_PATTERNS = [
    (r"^(HY|에이치와이)", "(주)한양정보통신"),
    (r"^한양", "(주)한양정보통신"),
    (r"^(굴림|돋움|바탕|궁서)", "(주)한양정보통신"),
    (r"^함초롬", "(주)한글과컴퓨터"),
    (r"^한컴", "(주)한글과컴퓨터"),
    (r"^(#|신명)", "신명시스템즈 / (주)한글과컴퓨터"),
    (r"^휴먼", "휴먼컴퓨터"),
    (r"^(-?윤|HCR)", "(주)윤디자인연구소"),
    (r"^HCI", "휴먼컴퓨터"),
    (r"^(맑은|Malgun)", "Microsoft / Monotype"),
]

HWPTAG_FACE_NAME = 19  # HWPTAG_BEGIN(16) + 3
FACE_PROP_HAS_SUBSTITUTE = 0x80
FACE_PROP_HAS_TYPE_INFO = 0x40
FACE_PROP_HAS_BASE_FONT = 0x20


# ---------------------------------------------------------------- 문서 판독

def read_hwpx(path):
    """HWPX(ZIP+XML) -> [{name, substitute, script}]"""
    with zipfile.ZipFile(path) as z:
        if "Contents/header.xml" not in z.namelist():
            raise ValueError("HWPX 헤더를 찾을 수 없습니다")
        header = z.read("Contents/header.xml").decode("utf-8", errors="replace")

    fonts = {}
    block_re = re.compile(
        r'<hh:fontface\s+lang="(?P<lang>[^"]*)"[^>]*>(?P<body>.*?)</hh:fontface>', re.S)
    font_re = re.compile(
        r'<hh:font\s+[^>]*face="(?P<face>[^"]*)"[^>]*?(?:/>|>(?P<inner>.*?)</hh:font>)', re.S)
    subst_re = re.compile(r'<hh:substFont\s+face="([^"]*)"')

    for block in block_re.finditer(header):
        lang = block.group("lang")
        for m in font_re.finditer(block.group("body")):
            face = m.group("face")
            inner = m.group("inner") or ""
            sub = subst_re.search(inner)
            entry = fonts.setdefault(face, {"name": face, "substitute": None,
                                            "scripts": []})
            if lang not in entry["scripts"]:
                entry["scripts"].append(lang)
            if sub and not entry["substitute"]:
                entry["substitute"] = sub.group(1)
    return list(fonts.values())


def read_hwp(path):
    """HWP 5.0(CFB) DocInfo 스트림의 FaceName 레코드 -> [{name, substitute}]"""
    try:
        import olefile
    except ImportError:
        raise RuntimeError("HWP(바이너리) 판독에는 olefile이 필요합니다: pip install olefile")

    ole = olefile.OleFileIO(path)
    try:
        header = ole.openstream("FileHeader").read()
        if not header.startswith(b"HWP Document File"):
            raise ValueError("HWP 5.0 서명이 아닙니다")
        flags = struct.unpack("<I", header[36:40])[0]
        if flags & 0x02:
            raise ValueError("암호화된 문서는 판독할 수 없습니다")
        raw = ole.openstream("DocInfo").read()
        data = zlib.decompress(raw, -15) if flags & 0x01 else raw
    finally:
        ole.close()

    fonts, pos = {}, 0
    while pos + 4 <= len(data):
        head = struct.unpack("<I", data[pos:pos + 4])[0]
        pos += 4
        tag = head & 0x3FF
        size = (head >> 20) & 0xFFF
        if size == 0xFFF:
            size = struct.unpack("<I", data[pos:pos + 4])[0]
            pos += 4
        body = data[pos:pos + size]
        pos += size
        if tag != HWPTAG_FACE_NAME:
            continue
        try:
            name, sub = _parse_face_name(body)
        except Exception:
            continue
        entry = fonts.setdefault(name, {"name": name, "substitute": None,
                                        "scripts": []})
        if sub and not entry["substitute"]:
            entry["substitute"] = sub
    return list(fonts.values())


def _parse_face_name(body):
    i = 0
    prop = body[i]
    i += 1
    length = struct.unpack("<H", body[i:i + 2])[0]
    i += 2
    name = body[i:i + length * 2].decode("utf-16-le")
    i += length * 2
    substitute = None
    if prop & FACE_PROP_HAS_SUBSTITUTE:
        i += 1  # 대체 폰트 종류
        slen = struct.unpack("<H", body[i:i + 2])[0]
        i += 2
        substitute = body[i:i + slen * 2].decode("utf-16-le")
    return name.strip("\x00"), (substitute.strip("\x00") if substitute else None)


def read_document(path):
    lower = path.lower()
    if lower.endswith((".hwpx", ".zip")) or zipfile.is_zipfile(path):
        return read_hwpx(path), "HWPX"
    if lower.endswith(".hwp"):
        return read_hwp(path), "HWP 5.0"
    raise ValueError("지원하지 않는 형식입니다 (.hwp / .hwpx)")


# ---------------------------------------------------------------- 판정

class Judge:
    def __init__(self, db):
        self.fonts = db["fonts"]
        self.prefixes = db.get("prefixRules", [])

    def lookup(self, name):
        if not name:
            return {"status": "unknown"}
        hit = self.fonts.get(name)
        if hit:
            return hit
        for prefix in self.prefixes:
            if name.startswith(prefix):
                entry = self.fonts.get(prefix)
                if entry:
                    return entry
        for pattern, holder in NAME_PATTERNS:
            if re.match(pattern, name):
                return {"status": "proprietary", "holder": holder,
                        "source": "폰트 이름 계열로 추정"}
        return {"status": "unknown"}

    REPRODUCIBLE = ("free", "freeware")

    def judge(self, font):
        own = self.lookup(font["name"])
        if own["status"] == "free":
            return "OK", "수정·재배포까지 자유로운 폰트", own, None
        if own["status"] == "freeware":
            return "OK", "무료 사용·임베딩 허용 (수정은 금지)", own, None
        sub_name = font.get("substitute")
        sub = self.lookup(sub_name) if sub_name else None
        if sub and sub["status"] in self.REPRODUCIBLE:
            return "OK", f"재현 가능한 대체 폰트 지정됨 ({sub_name})", own, sub
        if own["status"] == "unlicensed":
            return "UNLICENSED", own.get("note", "권리 관계 불명"), own, sub
        if own["status"] == "proprietary":
            if sub_name:
                return "MISSING", f"대체 지정이 있으나 그것도 상용 ({sub_name})", own, sub
            return "MISSING", "제약 없는 대체 폰트가 지정되지 않음", own, None
        return "UNKNOWN", "라이선스를 확인할 근거 없음", own, sub


def analyse(path, judge):
    fonts, fmt = read_document(path)
    rows = []
    for font in sorted(fonts, key=lambda f: f["name"]):
        verdict, reason, own, sub = judge.judge(font)
        rows.append({
            "font": font["name"],
            "substitute": font.get("substitute"),
            "verdict": verdict,
            "reason": reason,
            "status": own.get("status"),
            "holder": own.get("holder"),
            "license": own.get("license"),
            "reverseEngineeringClause": own.get("reverseEngineeringClause"),
        })
    total = len(rows)
    ok = sum(1 for r in rows if r["verdict"] == "OK")
    return {
        "file": os.path.basename(path),
        "format": fmt,
        "fontCount": total,
        "reproducible": ok,
        "score": round(100.0 * ok / total, 1) if total else 0.0,
        "fonts": rows,
    }


# ---------------------------------------------------------------- 출력

MARK = {"OK": "  OK   ", "MISSING": " 미확보 ", "UNLICENSED": " 권리불명 ", "UNKNOWN": " 불명  "}


def render(result):
    print(f"\n{'='*74}")
    print(f"{result['file']}   [{result['format']}]")
    print(f"{'='*74}")
    print(f"\n  개방성 점수  {result['score']:.0f}점"
          f"   (자유 도구로 재현 가능한 폰트 {result['reproducible']}/{result['fontCount']})\n")

    print(f"  {'판정':7s} {'폰트':22s} {'라이선스 / 권리자':30s} 대체 지정")
    print(f"  {'-'*7} {'-'*22} {'-'*30} {'-'*20}")
    for r in result["fonts"]:
        who = r.get("license") or r.get("holder") or "-"
        print(f"  {MARK[r['verdict']]} {r['font'][:22]:22s} {who[:30]:30s} "
              f"{r['substitute'] or '-'}")

    missing = [r for r in result["fonts"] if r["verdict"] == "MISSING"]
    unlicensed = [r for r in result["fonts"] if r["verdict"] == "UNLICENSED"]
    unknown = [r for r in result["fonts"] if r["verdict"] == "UNKNOWN"]

    print()
    if unlicensed:
        print(f"  Windows 기본 글꼴 {len(unlicensed)}종이 쓰였습니다: "
              f"{', '.join(r['font'] for r in unlicensed)}")
        print("  한컴은 이 글꼴들에 대해 \"저작권자와의 계약을 통해 라이선스를 보유한 것은")
        print("  아니다\"라고 공지하고 있습니다. 권리 관계를 확인할 창구가 사용자에게")
        print("  열려 있지 않은 상태입니다.")
        print("    https://www.hancom.com/support/faqCenter/faq/detail/2681")
        print()
    if not missing and not unknown and not unlicensed:
        print("  이 문서는 자유 소프트웨어만으로 같은 레이아웃을 재현할 수 있습니다.")
        return

    if missing:
        print(f"  이 문서는 상용 폰트 {len(missing)}종에 의존하며, 그 자리를 대신할")
        print(f"  제약 없는 구현체가 문서에 지정되어 있지 않습니다.")
        print()
        print("  자유 도구로 같은 조판을 만들려면 메트릭 호환 폰트(MCF)가 필요한데,")
        print("  국내에는 공적으로 제작·배포되는 MCF가 없고, 개인이 만들 경우")
        print("  그것이 적법한지 사전에 확인받을 경로도 없습니다.")
        print()
        print("  참고: 이 저장소의 약관 조사에서 폰트 메트릭 추출을 금지하는 조항은")
        print("        한 건도 확인되지 않았습니다. 문제는 금지가 아니라 불확실성입니다.")
        clause = [r for r in missing if r.get("reverseEngineeringClause")]
        if clause:
            names = ", ".join(r["font"] for r in clause[:5])
            print()
            print(f"  이 중 {len(clause)}종은 권리자 약관에 역설계 금지 조항이 있는 폰트입니다.")
            print(f"    {names}")
    if unknown:
        print()
        print(f"  라이선스를 확인하지 못한 폰트 {len(unknown)}종이 있습니다.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--db", default=DB_PATH)
    args = ap.parse_args()

    judge = Judge(json.load(open(args.db, encoding="utf-8")))
    results = []
    for path in args.paths:
        try:
            results.append(analyse(path, judge))
        except Exception as exc:
            results.append({"file": os.path.basename(path), "error": str(exc)})

    if args.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return
    for r in results:
        if "error" in r:
            print(f"\n{r['file']}: {r['error']}")
        else:
            render(r)


if __name__ == "__main__":
    main()

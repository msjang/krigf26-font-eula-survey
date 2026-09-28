#!/usr/bin/env python3
"""대체 폰트로 바뀌었을 때 줄바꿈이 얼마나 달라지는지 계산한다.

한글·숫자·라틴이 섞인 공문서 문단을 A4 본문 폭에 배치해 줄 수를 센다.
공백 기준 단순 알고리즘이므로 실제 워드프로세서의 금칙처리·자간 조정과는 다르다.

사용법
  python3 simulate_linebreak.py
"""

from fontTools.ttLib import TTFont
import glob
H="/Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared/TTF/"
idx={}
for base in (H+"Install/", H+"All/", H+"Hwp/"):
    for p in glob.glob(base+"*.[tT][tT][fF]"):
        try:
            f=TTFont(p,lazy=True)
            for r in f['name'].names:
                if r.nameID in (1,4):
                    try: nm=r.toUnicode().strip()
                    except Exception: continue
                    if nm: idx.setdefault(nm,p)
            f.close()
        except Exception: pass
def widths(name):
    p=idx[name]; f=TTFont(p,lazy=True); c=f.getBestCmap(); h=f['hmtx']; u=f['head'].unitsPerEm
    def W(ch):
        n=c.get(ord(ch))
        return h.metrics[n][0]*1000.0/u if n else 500.0
    return W
# 실제 공문서 문단 (한글 + 숫자 + 라틴 혼용)
TEXT=("정부는 2026년 9월 23일 국무회의를 열어 「행정업무의 운영 및 혁신에 관한 규정」 일부개정령안을 "
 "심의·의결하였다. 이번 개정은 공문서 서식의 설계 기준을 합리화하고, HWPX 등 개방형 표준 문서 포맷의 "
 "활용을 확대하기 위한 것이다. 행정안전부는 2027년 1월 1일부터 전 중앙행정기관에 적용할 계획이며, "
 "지방자치단체는 2027년 7월 1일부터 단계적으로 시행한다. 자세한 내용은 정부24(www.gov.kr)에서 "
 "확인할 수 있다. 문의: 행정안전부 정부혁신조직실 (044-205-1234)")*4
def measure(name, col):
    W=widths(name); lines=1; x=0
    for ch in TEXT:
        w=W(ch)
        if x+w>col: lines+=1; x=w
        else: x+=w
    return lines, sum(W(c) for c in TEXT)
COL=42000   # A4 본문 폭 근사 (1000 단위)
print(f"{'대체 쌍':34s} {'원본줄':>6s} {'대체줄':>6s} {'차이':>5s} {'총폭비':>8s}")
print('-'*66)
PAIRS=[('함초롬바탕','한컴바탕'),('한컴바탕','함초롬바탕'),('휴먼명조','한컴바탕'),
       ('함초롬돋움','한컴돋움'),('굴림','한컴바탕'),('HY헤드라인M','한컴바탕'),
       ('함초롬바탕','휴먼명조')]
for a,b in PAIRS:
    if a not in idx or b not in idx:
        print(f"{a+' -> '+b:34s} (미설치)"); continue
    la,ta=measure(a,COL); lb,tb=measure(b,COL)
    print(f"{a+' -> '+b:34s} {la:6d} {lb:6d} {lb-la:+5d} {100*tb/ta:7.2f}%")

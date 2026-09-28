#!/usr/bin/env python3
"""대체 폰트 쌍의 메트릭을 실측한다.

HWP/HWPX 가 지정한 대체 폰트가 원본과 배치 수치를 유지하는지 확인한다.
설치된 폰트에서 이름을 색인한 뒤, 한글 전각 폭·라틴 폭·공백 폭을 1000 단위로
환산해 대조한다.

사용법
  python3 measure_subst_metrics.py
"""

from fontTools.ttLib import TTFont
import glob
H="/Applications/Hancom Office HWP.app/Contents/Resources/Hnc/Shared/TTF/"
D="/Applications/Microsoft Word.app/Contents/Resources/DFonts/"
S="/System/Library/Fonts/Supplemental/"
idx={}
for base in (H+"Install/", H+"All/", H+"Hwp/", D, S):
    for p in glob.glob(base+"*.[tT][tT][fF]"):
        try:
            f=TTFont(p,lazy=True)
            for r in f['name'].names:
                if r.nameID in (1,4,16):
                    try: nm=r.toUnicode().strip()
                    except Exception: continue
                    if nm: idx.setdefault(nm,p)
            f.close()
        except Exception: pass
want=['한컴바탕','한컴돋움','함초롬바탕','함초롬돋움','휴먼명조','HY각헤드라인M','HY헤드라인M',
      'HY중고딕','Arial','굴림','바탕','돋움','한양중고딕','한양신명조','KoPub바탕체 Light']
print(f"{'폰트':16s} {'설치':>4s} {'upem':>6s} {'한글폭':>7s} {'em비':>6s} {'A':>6s} {'a':>6s} {'0':>6s} {'공백':>6s}")
print('-'*72)
res={}
for w in want:
    p=idx.get(w)
    if not p:
        print(f"{w:16s} {'X':>4s}"); continue
    f=TTFont(p,lazy=True); c=f.getBestCmap(); h=f['hmtx']; u=f['head'].unitsPerEm
    def W(ch):
        n=c.get(ord(ch)); return h.metrics[n][0]*1000.0/u if n else None
    han=W('가'); lat=[W(x) for x in 'Aa0 ']
    res[w]=(u,han,lat)
    print(f"{w:16s} {'O':>4s} {u:6d} {(han if han else -1):7.0f} {((han or 0)/1000):6.3f} "
          + " ".join(f"{x:6.0f}" if x is not None else "     -" for x in lat))
    f.close()
print()
print("=== 대체 쌍의 한글 em비 차이 ===")
PAIRS=[('HY각헤드라인M','한컴바탕',4627),('-윤고딕220','함초롬돋움',4388),('휴먼명조','한컴바탕',2379),
       ('한컴바탕','함초롬바탕',313),('함초롬바탕','한컴바탕',238),('Arial','한컴바탕',217)]
for a,b,n in PAIRS:
    ra,rb=res.get(a),res.get(b)
    if not ra or not rb:
        print(f"  {a:16s} -> {b:10s} {n:6d}건   (한쪽 미설치, 측정 불가)"); continue
    ha,hb=ra[1],rb[1]
    if ha and hb:
        print(f"  {a:16s} -> {b:10s} {n:6d}건   한글폭 {ha:.0f} -> {hb:.0f}  ({100*(hb-ha)/ha:+.1f}%)")
    else:
        la,lb=ra[2][0],rb[2][0]
        print(f"  {a:16s} -> {b:10s} {n:6d}건   'A'폭 {la:.0f} -> {lb:.0f}  ({100*(lb-la)/la:+.1f}%)  ※ 한글 없음")

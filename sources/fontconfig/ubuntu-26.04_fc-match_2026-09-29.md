# Ubuntu 26.04 — fontconfig 이 실제로 고르는 대체 글꼴

- 수집일: 2026-09-29
- 대상: Ubuntu 26.04 LTS (Lubuntu 데스크톱), `LANG=ko_KR.UTF-8`
- 방법: `fc-match <글꼴명>` — fontconfig 이 그 이름을 요청받았을 때 실제로 반환하는 글꼴
- 편집하지 않은 명령 출력이다

```
굴림 -> NotoSansCJK-Regular.ttc: "Noto Sans CJK KR" "Regular"
Gulim -> NotoSansCJK-Regular.ttc: "Noto Sans CJK KR" "Regular"
굴림체 -> NotoSansCJK-Regular.ttc: "Noto Sans Mono CJK KR" "Regular"
돋움 -> NotoSansCJK-Regular.ttc: "Noto Sans CJK KR" "Regular"
바탕 -> NotoSerifCJK-Regular.ttc: "Noto Serif CJK KR" "Regular"
Batang -> NotoSerifCJK-Regular.ttc: "Noto Serif CJK KR" "Regular"
맑은 고딕 -> NotoSansCJK-Regular.ttc: "Noto Sans CJK KR" "Regular"
함초롬바탕 -> NotoSansCJK-Regular.ttc: "Noto Sans CJK JP" "Regular"
sans-serif:lang=ko -> NotoSansCJK-Regular.ttc: "Noto Sans CJK JP" "Regular"

Ubuntu 26.04 LTS
877
fonts-nanum 20250212-1
fonts-noto-cjk 1:20240730+repack1-1build1
```

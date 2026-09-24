# 데이터

모든 파일은 2026-09-24 수집·생성. 재현 도구는 [`../tools/`](../tools/).

| 파일 | 내용 | 레코드 |
|---|---|---:|
| `font-license-census_2026-09-24.json` | macOS·MS Office·한컴오피스 폰트의 name table(ID 0/7/13/14) 및 OS/2 fsType 전수 | 1,862 |
| `oss-font-license_2026-09-24.json` | 오픈소스·MCF 폰트 동일 항목 | 27 |
| `gov-doc-fonts_2026-09-24.json` | 공문서 HWPX 450건의 언어별 폰트 테이블과 substFont 기록 | 450 |
| `gov-doc-fonts_summary_2026-09-24.json` | 위 집계 — 폰트별 등장 문서 수, 대체 쌍 | — |
| `mcf-metric-verification_2026-09-24.json` | MCF 7쌍의 advance width·수직 메트릭·윤곽선 대조 | 7 |
| `mcf-pairs_2026-09-24.json` | 위 비교에 사용한 원본/MCF 파일 경로 | 7 |

## 스키마

### font-license-census / oss-font-license

```jsonc
{
  "source": "한컴오피스",           // 수집 구분 레이블
  "file": "HANBatang.ttf",
  "dir": "/Applications/...",
  "family": "함초롬바탕",            // name ID 1
  "full": "함초롬바탕",              // name ID 4
  "version": "Version 2.100; ...",  // name ID 5
  "copyright": "Copyright (c) ...", // name ID 0
  "trademark": "HCR Batang is ...", // name ID 7
  "license": "YoonDesign Inc.",     // name ID 13  ← 내장 라이선스 문구
  "licenseURL": "http://...",       // name ID 14
  "fsType": {
    "raw": 8,
    "embedding": "Editable",        // 0 Installable / 2 Restricted / 4 Preview&Print / 8 Editable
    "no_subsetting": false,
    "bitmap_only": false
  },
  "faceIndex": 0                    // .ttc 컬렉션인 경우에만
}
```

### gov-doc-fonts

```jsonc
{
  "collected": "2026-09-24",
  "source": "korea.kr 정책브리핑 보도자료 첨부 HWPX",
  "documents": [{
    "newsId": "156783168",
    "filename": "...hwpx",
    "url": "https://www.korea.kr/common/download.do?fileId=...",
    "fonts": {
      "HANGUL": [{"face": "함초롬바탕", "type": "TTF"}],
      "LATIN":  [...], "HANJA": [...], "JAPANESE": [...],
      "OTHER":  [...], "SYMBOL": [...], "USER": [...]
    },
    "substitutions": [
      {"lang": "HANGUL", "requested": "-윤고딕220",
       "substituted": "함초롬돋움", "type": "TTF"}
    ]
  }],
  "errors": [...]
}
```

`substitutions` 는 HWPX의 `hh:substFont` 항목이다. **문서가 요청했으나 저장 시점 환경에 없어 대체된 폰트**를 뜻하며, 문서가 스스로 남긴 레이아웃 훼손의 기록이다.

### mcf-metric-verification

```jsonc
{
  "label": "Calibri -> Carlito",
  "original": "/.../Calibri.ttf",
  "mcf": "/.../Carlito-Regular.ttf",
  "unitsPerEm": {"original": 2048, "mcf": 2048},
  "advanceWidth":    {"compared": 92, "identical": 92, "different": 0,
                      "differences": [/* [문자, 원본값, MCF값, 1000단위 편차] */]},
  "verticalMetrics": {"compared": 8, "identical": 8, "different": 0, "differences": []},
  "outlines":        {"comparedChars": 13, "identical": 0, "different": 13,
                      "identicalChars": [], "pointCounts": [/* [문자, 원본점수, MCF점수] */]}
}
```

`outlines.identical` 이 0이라는 것은 **비교한 문자 전부에서 윤곽선 제어점 좌표가 달랐다**는 뜻이다.

## 수집 시 유의한 것

- 원본 폰트를 개변하지 않았다. 규격(OpenType 사양, HWPX/OWPML)이 정한 위치의 값을 읽었을 뿐이다
- 공문서 수집은 robots.txt를 확인하고 순차 요청 + 0.35초 지연으로 진행했다. 본문 내용은 저장하지 않았다
- 정보공개포털(open.go.kr)·NTIS는 robots.txt가 `Disallow: /` 이므로 수집하지 않았다

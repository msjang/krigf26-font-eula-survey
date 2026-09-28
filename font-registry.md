# 국내 공문서 폰트 목록 — 권리자와 라이선스

- 대상: 정책브리핑 첨부 공문서 **2,286건**(2010~2026년, HWP·HWPX)에 등장한 고유 폰트 **415종**
- 생성: [`tools/build_font_registry.py`](tools/build_font_registry.py) — 아래 자료를 대조해 자동 생성
  - `data/gov-doc-fonts*.json` 공문서 폰트 테이블 (URL 로 중복 제거)
  - [`data/font-openness-db.json`](data/font-openness-db.json) 개방성 판정
  - [`data/font-license-census_2026-09-24.json`](data/font-license-census_2026-09-24.json) 폰트 파일 내장 저작권
  - [`data/hft-registry_2026-09-24.json`](data/hft-registry_2026-09-24.json) HFT 레지스트리

> 판정은 **위법 여부가 아니라 재현 가능성**입니다. 이 저장소의 조사에서 폰트 메트릭 추출을 금지하는 약관 조항은 한 건도 확인되지 않았습니다.

## 판정 구분

| 표기 | 뜻 |
|---|---|
| **자유** | 수정·재배포까지 자유 (OFL 등) |
| **무료** | 무료 사용·임베딩 허용, 수정 금지. 문서 재현에는 제약 없음 |
| **권리불명** | 한컴이 "라이선스를 보유한 것이 아니다"라고 공지한 Windows 기본 글꼴 9종 |
| **상용** | 제품 내 사용으로 한정 |
| **불명** | 판정 근거를 찾지 못함 |

## 요약

| 판정 | 폰트 수 |
|---|---:|
| 자유 | 33 |
| 무료 | 16 |
| 권리불명 | 9 |
| 상용 | 215 |
| 불명 | 142 |
| **합계** | **415** |

## 전체 목록

등장 문서 수 내림차순. 비율은 2,286건 기준.

| 폰트 | 문서 | 비율 | 포맷 | 판정 | 권리자 | 저작권 표시 / 라이선스 | 출처 |
|---|---:|---:|---|---|---|---|---|
| 한양신명조 | 2270 | 99% | HFT/HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1997 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 명조 | 2268 | 99% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼명조 | 2257 | 99% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HCI Poppy | 2248 | 98% | HFT/HWP/TTF | 불명 | 휴먼컴퓨터 | - | - |
| HY헤드라인M | 2091 | 91% | HWP/TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. All rights reserved. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 바탕 | 1933 | 85% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 맑은 고딕 | 1811 | 79% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 굴림 | 1745 | 76% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 한컴바탕 | 1663 | 73% | HWP/TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. 2001-2017. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한양중고딕 | 1483 | 65% | HFT/HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 함초롬바탕 | 1481 | 65% | HWP/TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 산세리프 | 1403 | 61% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 함초롬돋움 | 1263 | 55% | HWP/TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 돋움 | 1244 | 54% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 돋움체 | 1063 | 47% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| HY중고딕 | 926 | 41% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 신명 견명조 | 805 | 35% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신명조 | 784 | 34% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 태명조 | 776 | 34% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Copmuter Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 바탕체 | 775 | 34% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 한양견명조 | 775 | 34% | HFT/HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 신명조■얒a | 771 | 34% | HWP/TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| #세명조 | 768 | 34% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤고딕130 | 764 | 33% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| HCI Tulip | 762 | 33% | HFT/HWP | 불명 | 휴먼컴퓨터 | - | - |
| HY각헤드라인M | 708 | 31% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| -윤고딕220 | 677 | 30% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 굴림체 | 520 | 23% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| Arial | 461 | 20% | HWP/TTF | 상용 | Monotype | © 2015 The Monotype Corporation. All Rights Reserved. Hebrew OpenType  | [폰트 내장 고지](findings-licenses.md) |
| HY견고딕 | 438 | 19% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한양견고딕 | 371 | 16% | HFT/HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1993 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 휴먼고딕 | 355 | 16% | HWP/TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Times New Roman | 313 | 14% | HWP/TTF | 상용 | Monotype | © 2014 The Monotype Corporation. All Rights Reserved. Hebrew OpenType  | [폰트 내장 고지](findings-licenses.md) |
| #중고딕 | 291 | 13% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HCI Hollyhock | 262 | 11% | HFT/HWP | 불명 | 휴먼컴퓨터 | - | - |
| HY울릉도M | 248 | 11% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| HY그래픽M | 213 | 9% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| #태고딕 | 150 | 7% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 백제 M | 139 | 6% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 신명 신명조 | 138 | 6% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤고딕120 | 130 | 6% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명 태고딕 | 128 | 6% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼옛체 | 90 | 4% | HWP/TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTER | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #세고딕 | 89 | 4% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신세고딕 | 88 | 4% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Arial-BoldMT | 87 | 4% | HWP/TTF | 불명 | - | - | - |
| 궁서 | 84 | 4% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 나눔고딕 | 83 | 4% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 한컴돋움 | 77 | 3% | HWP/TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. 2001-2017. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 필기 | 75 | 3% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 세명조 | 74 | 3% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한양궁서 | 74 | 3% | HFT/HWP | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| HY신명조 | 73 | 3% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| -윤명조120 | 72 | 3% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명 태그래픽 | 70 | 3% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HY울릉도B | 67 | 3% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 신명 중명조 | 63 | 3% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| AmeriGarmnd BT | 62 | 3% | HWP/TTF | 상용 | (주)한글과컴퓨터 | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 중고딕 | 62 | 3% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| KoPub바탕체 Light | 61 | 3% | HWP/TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| HY견명조 | 59 | 3% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| Arial TUR | 55 | 2% | HWP/TTF | 불명 | - | - | - |
| Arial Narrow | 52 | 2% | HWP/TTF | 상용 | Monotype | Typeface © The Monotype Corporation plc. Data © The Monotype Corporati | [폰트 내장 고지](findings-licenses.md) |
| 나눔고딕 ExtraBold | 51 | 2% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 한컴 윤고딕 230 | 51 | 2% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| Arial Unicode MS | 51 | 2% | HWP/TTF | 상용 | Monotype | Digitized data copyright (C) 1993-2000 Agfa Monotype Corporation. All  | [폰트 내장 고지](findings-licenses.md) |
| -윤고딕330 | 50 | 2% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Calibri | 48 | 2% | HWP/TTF | 상용 | Microsoft / Monotype | © 2014 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| HY바다L | 48 | 2% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴 윤체 B | 48 | 2% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 옥수수 | 47 | 2% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 나눔고딕 Light | 47 | 2% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 휴먼아미체 | 46 | 2% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 한양그래픽 | 43 | 2% | HFT/HWP | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴 쿨재즈 M | 43 | 2% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 새굴림 | 43 | 2% | HWP/TTF | 불명 | - | - | - |
| KoPub돋움체 Light | 43 | 2% | HWP/TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| 함초롬바탕 확장B | 42 | 2% | HWP/TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 고딕 | 42 | 2% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 윤고딕 240 | 41 | 2% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| HY그래픽 | 41 | 2% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| -윤고딕320 | 40 | 2% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 궁서체 | 39 | 2% | HWP/TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 신명 신문명조 | 38 | 2% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼엑스포 | 37 | 2% | HWP/TTF | 상용 | 휴먼컴퓨터 | - | - |
| KoPub돋움체 Bold | 35 | 2% | HWP/TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| 신명 견고딕 | 33 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #태명조 | 32 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 함초롬돋움 확장 | 28 | 1% | HWP | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 산돌고딕 M | 28 | 1% | HWP/TTF | 불명 | - | - | - |
| 산돌명조 L | 27 | 1% | HWP/TTF | 불명 | - | - | - |
| 태 나무 | 27 | 1% | HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #견명조 | 27 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HY태고딕 | 26 | 1% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 나눔손글씨 붓 | 25 | 1% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| Tahoma | 25 | 1% | HWP/TTF | 상용 | Microsoft / Monotype | © 2016 Microsoft Corporation. All rights reserved. Hebrew OpenType Lay | [폰트 내장 고지](findings-licenses.md) |
| KoPub돋움체 Medium | 24 | 1% | HWP/TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| 시스템 | 23 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994-1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 양재 다운명조M | 23 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1996 Yangjae LAB | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 태 가는 헤드라인T | 23 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 순명조 | 23 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신문견명 | 23 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼편지체 | 22 | 1% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 한양신명조V | 22 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1997 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤고딕110 | 21 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명 신신명조 | 20 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼모음T | 20 | 1% | HWP/TTF | 상용 | 휴먼컴퓨터 | - | - |
| #견고딕 | 20 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Cambria | 19 | 1% | HWP/TTF | 상용 | Microsoft / Monotype | © 2013 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| 산돌고딕 L | 19 | 1% | HWP/TTF | 불명 | - | - | - |
| -윤고딕140 | 19 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| -윤고딕120-90% | 17 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| MD솔체 | 17 | 1% | HWP/TTF | 불명 | - | (c) Copyright MorrisDesign. All Rights Reserved. | - |
| 나눔고딕_코딩 | 17 | 1% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| #신문견고 | 17 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 문체부 바탕체 | 17 | 1% | HWP/TTF | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 휴먼둥근헤드라인 | 16 | 1% | HWP/TTF | 상용 | 휴먼컴퓨터 | - | - |
| 신명조확장둘 | 16 | 1% | HWP/TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| HY Sinmyeongjo | 16 | 1% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Myeongjo | 16 | 1% | HWP | 불명 | - | - | - |
| 신명 궁서 | 16 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 수식 | 16 | 1% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 나눔명조 | 15 | 1% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 가는안상수체 | 15 | 1% | HWP/TTF | 불명 | 휴먼컴퓨터 | - | - |
| #그래픽 | 15 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 고딕 | 14 | 1% | TTF | 상용 | (주)한글과컴퓨터 | Copyright (c) 2017 Hancom Inc. All rights reserved. Font designed by F | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신그래픽 | 14 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 양재 튼튼B | 14 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1996 Yangjae LAB | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 윤고딕 720 | 14 | 1% | TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| #중명조 | 13 | 1% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 산돌고딕 L\,한컴돋움 | 13 | 1% | HWP/TTF | 불명 | - | - | - |
| 한컴산뜻돋움 | 13 | 1% | HWP/TTF | 상용 | (주)한글과컴퓨터 | Copyright (c) 2017 Hancom Inc. All rights reserved. Font designed by F | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한양해서 | 13 | 1% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2017 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 휴먼명조\,한컴돋움 | 13 | 1% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 신명조 | 13 | 1% | HWP/TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| -윤고딕310 | 12 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 한컴 윤고딕 250 | 12 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 한컴 윤고딕 760 | 12 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| MS Mincho | 12 | 1% | HWP/TTF | 상용 | Microsoft / Monotype | © 2017 data:RICOH Co.,Ltd. typeface:RYOBI IMAGIX CO. | [폰트 내장 고지](findings-licenses.md) |
| -아이리스M | 12 | 1% | HWP | 불명 | - | - | - |
| -윤명조320 | 12 | 1% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명조 간자 | 11 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1998 Han Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼굵은팸체 | 11 | 0% | HWP | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Garamond | 10 | 0% | HWP/TTF | 상용 | Monotype | Digitized data copyright Monotype Typography, Ltd 1991-1995. All right | [폰트 내장 고지](findings-licenses.md) |
| 신명조\,한컴돋움 | 10 | 0% | HWP/TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| Trebuchet MS | 10 | 0% | HWP | 상용 | Microsoft / Monotype | Copyright (c) 1996 Microsoft Corporation. All rights reserved. | [폰트 내장 고지](findings-licenses.md) |
| 신명 신그래픽 | 10 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 태 헤드라인T | 10 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명조 약자 | 10 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Aptos | 10 | 0% | HWP/TTF | 불명 | - | - | - |
| #궁서 | 9 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 산돌명조 M | 9 | 0% | HWP | 불명 | - | - | - |
| 맑은 고딕 Semilight | 9 | 0% | HWP/TTF | 상용 | Microsoft / Monotype | © 2015 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| #신문태명 | 9 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신디나루 | 9 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HY강B | 9 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한양중고딕&quot; | 9 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| HY수평선B | 8 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| MS Sans Serif | 8 | 0% | HWP/TTF | 불명 | - | - | - |
| -윤명조110 | 8 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| HY크리스탈M | 8 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 중고딕 | 8 | 0% | HWP/TTF | 불명 | - | - | - |
| 나눔바른고딕 | 7 | 0% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| -햇살B | 7 | 0% | HWP | 불명 | - | - | - |
| HCI Acacia | 7 | 0% | HFT/HWP | 불명 | 휴먼컴퓨터 | - | - |
| 가는각진제목체 | 6 | 0% | HWP | 불명 | - | - | - |
| 08서울한강체 M | 6 | 0% | HWP/TTF | 불명 | - | - | - |
| 산돌명조 L\,한컴돋움 | 6 | 0% | HWP/TTF | 불명 | - | - | - |
| MD아트체 | 6 | 0% | HWP | 불명 | - | (c) Copyright MorrisDesign. All Rights Reserved. | - |
| 한양중고딕V | 6 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1997 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 세고딕 | 6 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤고딕340 | 6 | 0% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 나눔고딕OTF | 6 | 0% | HWP | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| Franklin Gothic Medium | 6 | 0% | HWP | 상용 | Microsoft / Monotype | ITC Franklin Gothic is a trademark of The International Typeface Corpo | [폰트 내장 고지](findings-licenses.md) |
| 해수체B | 5 | 0% | TTF | 불명 | - | - | - |
| SimSun | 5 | 0% | HWP/TTF | 불명 | - | © Copyright ZHONGYI Electronic Co. 2001 | - |
| Helvetica Neue | 5 | 0% | HWP/TTF | 상용 | Monotype | Part of the digitally encoded machine readable outline data for produc | [폰트 내장 고지](findings-licenses.md) |
| #태그래픽 | 5 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HY궁서B | 5 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| -윤명조140 | 5 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 산돌신문제비B | 5 | 0% | HWP | 불명 | - | - | - |
| -파랑새B | 5 | 0% | HWP | 불명 | - | - | - |
| 옥션고딕 B | 5 | 0% | HWP/TTF | 불명 | - | - | - |
| Hobo BT | 5 | 0% | HWP/TTF | 상용 | (주)한글과컴퓨터 | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 태 가는 헤드라인D | 5 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 양재 참숯B | 5 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1997 Yangjae Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Asia신헤드-TTF | 5 | 0% | HWP | 불명 | - | - | - |
| 한컴 윤고딕 740 | 4 | 0% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| 한양중고딕\,한컴돋움 | 4 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| HY특견명조 | 4 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 산돌향기B | 4 | 0% | HWP | 불명 | - | - | - |
| -소망M | 4 | 0% | HWP | 불명 | - | - | - |
| 문체부 제목 돋음체 | 4 | 0% | HWP/TTF | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| HY울릉도L | 4 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| HY수평선L | 4 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Yoon가변 윤고딕 120_TT | 4 | 0% | HWP/TTF | 불명 | - | - | - |
|  @산돌퍼즐Bk | 4 | 0% | HWP | 불명 | - | - | - |
| a아시아헤드3 | 4 | 0% | HWP | 불명 | - | - | - |
| HCI Hollyhock Narrow | 4 | 0% | HWP | 불명 | 휴먼컴퓨터 | - | - |
| 가는둥근제목체 | 4 | 0% | HWP/TTF | 불명 | - | - | - |
| Courier New | 4 | 0% | HWP/TTF | 상용 | Monotype | © 2015 The Monotype Corporation. All Rights Reserved. Hebrew OpenType  | [폰트 내장 고지](findings-licenses.md) |
| -윤고딕110-WinCharSetFFFF-H | 4 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Noto Sans CJK KR | 4 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://fonts.google.com/noto) |
| KoPub바탕체 Bold | 4 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| KoPubWorld돋움체 Light | 4 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| 08서울남산체 B | 3 | 0% | HWP/TTF | 불명 | - | - | - |
| 나눔명조 ExtraBold | 3 | 0% | HWP | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 뫼비우스 Regular | 3 | 0% | HWP | 불명 | - | - | - |
| NanumGothic | 3 | 0% | HWP | 불명 | - | - | - |
| HY궁서 | 3 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 나눔고딕 Bold | 3 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| MD개성체 | 3 | 0% | HWP | 불명 | - | (c) Copyright MorrisDesign. All Rights Reserved. | - |
| HY둥근고딕M | 3 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 양재난초체M | 3 | 0% | HWP | 불명 | - | (c) Copyright Yangjae Media Corp. All Rights Reserved. | - |
| 중고딕 간자 | 3 | 0% | HFT/HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1999 Han Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 문화바탕제목 | 3 | 0% | HFT/HWP/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #디나루 | 3 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 양재튼튼체B | 3 | 0% | HWP | 불명 | - | (c) Copyright Yangjae Media Corp. All Rights Reserved. | - |
| 중고딕 약자 | 3 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1999 Han Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HY동녘B | 3 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴 윤체 M | 3 | 0% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| Century | 3 | 0% | HWP/TTF | 상용 | Monotype | Digitized data copyright (C) 1992-1997 The Monotype Corporation. All r | [폰트 내장 고지](findings-licenses.md) |
| 견고딕 | 3 | 0% | HWP | 불명 | - | - | - |
| 산돌향기 M | 3 | 0% | HWP | 불명 | - | - | - |
| 휴면명조 | 3 | 0% | HWP | 불명 | - | - | - |
| HY강M | 3 | 0% | HWP/TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| -소망L | 3 | 0% | HWP | 불명 | - | - | - |
| Franklin Gothic Demi Cond | 3 | 0% | HWP | 상용 | Microsoft / Monotype | ITC Franklin Gothic is a trademark of The International Typeface Corpo | [폰트 내장 고지](findings-licenses.md) |
| 휴먼신문고딕 | 3 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 다음_Regular | 3 | 0% | HWP/TTF | 불명 | - | - | - |
| 타이포_씨고딕 120 | 3 | 0% | HWP | 불명 | - | - | - |
| 한컴 소망 M | 3 | 0% | HWP/TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 맑은고딕 | 3 | 0% | HWP/TTF | 상용 | Microsoft / Monotype | - | [폰트 내장 고지](findings-licenses.md) |
| 문체부 돋음체 | 3 | 0% | HWP | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 나눔명조OTF ExtraBold | 3 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| -윤명조310 | 3 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Symbol | 3 | 0% | TTF | 상용 | Monotype | Typeface © The Monotype Corporation plc. Data © The Monotype Corporati | [폰트 내장 고지](findings-licenses.md) |
| KoPubWorld돋움체 Bold | 3 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| -윤명조330 | 2 | 0% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Book Antiqua | 2 | 0% | TTF | 상용 | Monotype | Digitized data copyright The Monotype Corporation 1991-1995. All right | [폰트 내장 고지](findings-licenses.md) |
| -윤고딕160 | 2 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 㡸ƪ명조Ÿ?Ј | 2 | 0% | HWP | 불명 | - | - | - |
| ੠Ƭ명조Ÿ?Ј | 2 | 0% | HWP | 불명 | - | - | - |
| 䍐ƨ명조Ÿ?Ј | 2 | 0% | HWP | 불명 | - | - | - |
| 逈Ƭ명조Ÿ?Ј | 2 | 0% | HWP | 불명 | - | - | - |
| 태 헤드라인D | 2 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Asia신고딕 | 2 | 0% | HWP | 불명 | - | - | - |
| (환)환붓예서(굵은) | 2 | 0% | HWP | 불명 | - | - | - |
| Gulim | 2 | 0% | HWP | 불명 | - | - | - |
| MS Gothic | 2 | 0% | HWP/TTF | 상용 | Microsoft / Monotype | © 2017 data:RICOH Co.,Ltd. typeface:RYOBI IMAGIX CO. | [폰트 내장 고지](findings-licenses.md) |
| Arial Rounded MT Bold | 2 | 0% | HWP | 상용 | Monotype | Copyright © 1993 , Monotype Typography ltd. | [폰트 내장 고지](findings-licenses.md) |
| Rix명조 M | 2 | 0% | TTF | 불명 | - | - | - |
| Calibri Light | 2 | 0% | TTF | 상용 | Microsoft / Monotype | © 2017 Microsoft Corporation. All Rights Reserved. Hebrew OpenType Lay | [폰트 내장 고지](findings-licenses.md) |
| 경기천년바탕 Regular | 2 | 0% | TTF | 무료 | - | 경기도 배포 무료 글꼴 | [원문](https://www.gg.go.kr/contents/contents.do?ciIdx=679) |
| Aptos Narrow | 2 | 0% | TTF | 불명 | - | - | - |
| 08서울남산체 EB | 2 | 0% | HWP | 불명 | - | - | - |
| 한컴 쿨재즈 B | 2 | 0% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| -윤명조230 | 2 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| HY태명조 | 2 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 창인 신명조 | 2 | 0% | HWP | 불명 | - | - | - |
| HY수평선M | 2 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 나눔바른고딕OTF | 2 | 0% | HWP | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| Yoon가변 윤고딕 320_TT | 2 | 0% | HWP | 불명 | - | - | - |
| HY동녘M | 2 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴바탕확장 | 2 | 0% | HWP | 불명 | - | Copyright(c) Founder Corporation.2003 | - |
| HY백송B | 2 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| Bembo | 2 | 0% | HWP | 불명 | - | - | - |
| -윤명조350 | 2 | 0% | HWP/TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| �쌱삃력옓 | 2 | 0% | HWP | 불명 | - | - | - |
| 력옓 | 2 | 0% | HWP | 불명 | - | - | - |
| @필기체 | 2 | 0% | HWP | 불명 | - | - | - |
| -윤명조130 | 2 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명조체 | 2 | 0% | HWP | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| Helvetica | 2 | 0% | HWP | 불명 | - | © 1990-2006 Apple Computer Inc. © 1981 Linotype AG © 1990-91 Type Solu | - |
| Andale WT | 2 | 0% | HWP/TTF | 불명 | - | - | - |
| Rix고딕 B | 2 | 0% | HWP/TTF | 불명 | - | - | - |
| Microsoft Sans Serif | 2 | 0% | HWP/TTF | 상용 | Microsoft / Monotype | © 2006 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| 나눔스퀘어 ExtraBold | 2 | 0% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| -윤고딕330\,한컴돋움 | 2 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 나눔스퀘어 네오 ExtraBold | 2 | 0% | HWP/TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 함초롬바탕 확장 | 2 | 0% | TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| (한)문화방송 | 2 | 0% | TTF | 불명 | - | - | - |
| Aptos Display | 2 | 0% | TTF | 불명 | - | - | - |
| Yoon가변 윤고딕 110_TT | 2 | 0% | TTF | 불명 | - | - | - |
| 영화체 | 2 | 0% | TTF | 불명 | - | - | - |
| HYHeadLine M | 2 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Verdana | 2 | 0% | TTF | 상용 | Microsoft / Monotype | © 2016 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| Arial Black | 1 | 0% | HWP | 상용 | Monotype | © 2012 The Monotype Corporation. All Rights Reserved. Arial is a trade | [폰트 내장 고지](findings-licenses.md) |
| 산돌제비 L | 1 | 0% | HWP | 불명 | - | - | - |
| 문체부 쓰기 정체 | 1 | 0% | TTF | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 오뚜기산스 Light | 1 | 0% | TTF | 불명 | - | - | - |
| ARIAL | 1 | 0% | HWP | 불명 | - | - | - |
| 문체부 궁체 정자체 | 1 | 0% | HWP | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| Impact | 1 | 0% | HWP | 상용 | Monotype | © 2006 The Monotype Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| -윤명조340 | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Rix고딕 L | 1 | 0% | HWP | 불명 | - | - | - |
| BundesSerif Regular | 1 | 0% | HWP | 불명 | - | - | - |
| Haansoft Batang | 1 | 0% | HWP | 불명 | - | - | - |
| MD이솝체 | 1 | 0% | HWP | 불명 | - | (c) Copyright MorrisDesign. All Rights Reserved. | - |
| (한)고인돌B | 1 | 0% | HWP | 불명 | - | - | - |
| 가는으뜸체 | 1 | 0% | HWP | 불명 | - | - | - |
| Century Gothic | 1 | 0% | HWP | 상용 | Monotype | Typeface © The Monotype Corporation plc. Data © The Monotype Corporati | [폰트 내장 고지](findings-licenses.md) |
| 경기천년바탕 Bold | 1 | 0% | TTF | 무료 | - | 경기도 배포 무료 글꼴 | [원문](https://www.gg.go.kr/contents/contents.do?ciIdx=679) |
| 휴먼중간팸체 | 1 | 0% | TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTER | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| \0022맑은 고딕\0022 | 1 | 0% | TTF | 불명 | - | - | - |
| HCI Bellflower | 1 | 0% | HWP | 불명 | 휴먼컴퓨터 | - | - |
| 제목바탕체 | 1 | 0% | HWP | 불명 | - | - | - |
| 타이프 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 오이 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한양태고딕 | 1 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| !Y2KBUG | 1 | 0% | HWP | 불명 | - | - | - |
| !백묵 신세대체(견중) | 1 | 0% | HWP | 불명 | - | - | - |
| 휴먼세엑스포 | 1 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 현대하모니 M | 1 | 0% | HWP | 불명 | - | - | - |
| #신문고딕 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| #신문태고 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| ����ü | 1 | 0% | HWP | 불명 | - | - | - |
| -윤고딕230 | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 한컴 백제 B | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| Yoon가변 윤명조 320_TT | 1 | 0% | HWP | 불명 | - | - | - |
| 양재백두체B | 1 | 0% | HWP | 불명 | - | (c) Copyright Yangjae Media Corp. All Rights Reserved. | - |
| Yoon 윤고딕 520_TT | 1 | 0% | HWP | 불명 | - | - | - |
| 제주명조 | 1 | 0% | HWP | 불명 | - | - | - |
| 폴라리스새바탕-함초롬바탕호환 | 1 | 0% | HWP | 불명 | - | - | - |
| 서울들국화 | 1 | 0% | HWP | 자유 | - | 서울특별시 서울서체 — 자유 이용 허용 | [원문](https://www.seoul.go.kr/seoul/font.do) |
| -가시나무M | 1 | 0% | HWP | 불명 | - | - | - |
| 조선일보명조 | 1 | 0% | HWP | 불명 | - | - | - |
| 휴먼궁서 | 1 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| HY특신명조 | 1 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Bembo Semi Bold | 1 | 0% | HWP | 불명 | - | - | - |
| HY목판L | 1 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 휴먼매직체 | 1 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| -윤고딕240 | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 큐닉스궁서체 | 1 | 0% | HWP | 불명 | - | - | - |
| HY부활B | 1 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| �럟력옓 | 1 | 0% | HWP | 불명 | - | - | - |
| 한컴 솔잎 M | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 신명 디나루 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 태-행복R | 1 | 0% | HWP | 불명 | - | - | - |
| 가는공한 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 그래픽체 | 1 | 0% | HWP | 불명 | - | - | - |
| 휴먼태그래픽 | 1 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 관리원 | 1 | 0% | HWP | 불명 | - | - | - |
| Swis721 BT | 1 | 0% | HWP | 불명 | - | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | - |
| (한)신명조 | 1 | 0% | HWP | 불명 | - | - | - |
| HY엽서L | 1 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Yoon 윤고딕 140_TT | 1 | 0% | HWP | 불명 | - | - | - |
| Human Myeongjo | 1 | 0% | HWP | 불명 | - | - | - |
| arial | 1 | 0% | HWP | 불명 | - | - | - |
| Moebius | 1 | 0% | HWP | 불명 | - | - | - |
| NSimSun | 1 | 0% | HWP | 불명 | - | - | - |
| Palatino Linotype | 1 | 0% | HWP | 상용 | Microsoft / Monotype | Copyright 1981-1983, 1989,1993, 1998 Heidelberger Druckmaschinen AG. A | [폰트 내장 고지](findings-licenses.md) |
| Apple SD 산돌고딕 Neo 일반체 | 1 | 0% | HWP | 불명 | - | - | - |
| 굴림 굴림 | 1 | 0% | HWP | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 08서울남산체 M | 1 | 0% | HWP | 불명 | - | - | - |
| HY센스L | 1 | 0% | HWP | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| ±¼¸² | 1 | 0% | HWP | 불명 | - | - | - |
| 양재소슬체S | 1 | 0% | HWP | 불명 | - | (c) Copyright Yangjae Media Corp. All Rights Reserved. | - |
| #태신명조 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 굵은안상수체 | 1 | 0% | HWP | 불명 | 휴먼컴퓨터 | - | - |
| 해서 약자 | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | (c) Copyright 1999 Han Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| GulimChe | 1 | 0% | HWP | 불명 | - | - | - |
| -아이리스L | 1 | 0% | HWP | 불명 | - | - | - |
| 한컴 소망 B | 1 | 0% | HWP | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| 해수체M | 1 | 0% | HWP | 불명 | - | - | - |
| Bodoni Bd BT | 1 | 0% | HWP | 상용 | (주)한글과컴퓨터 | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Franklin Gothic Demi | 1 | 0% | HWP | 상용 | Microsoft / Monotype | ITC Franklin Gothic is a trademark of The International Typeface Corpo | [폰트 내장 고지](findings-licenses.md) |
| Times New Roman Bold | 1 | 0% | HWP | 불명 | - | - | - |
| Rix고딕 M | 1 | 0% | HWP | 불명 | - | - | - |
| Rix고딕 EB | 1 | 0% | HWP | 불명 | - | - | - |
| Malgun Gothic | 1 | 0% | HWP | 상용 | Microsoft / Monotype | - | [폰트 내장 고지](findings-licenses.md) |
| 문체부 궁체 흘림체 | 1 | 0% | HWP | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 휴먼태엑스포 | 1 | 0% | HWP | 상용 | 휴먼컴퓨터 | - | - |
| 본고딕 KR Heavy | 1 | 0% | HWP | 자유 | - | SIL Open Font License 1.1 | [원문](https://github.com/adobe-fonts/source-han-sans) |
| 본고딕 KR Regular | 1 | 0% | HWP | 자유 | - | SIL Open Font License 1.1 | [원문](https://github.com/adobe-fonts/source-han-s
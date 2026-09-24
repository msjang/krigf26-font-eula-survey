# 국내 공문서 폰트 목록 — 권리자와 라이선스

- 대상: 정책브리핑 보도자료 HWPX **450건**에 등장한 고유 폰트 **184종** (2026-09-21~23 게시분)
- 생성: [`tools/build_font_registry.py`](tools/build_font_registry.py) — 아래 자료를 대조해 자동 생성
  - [`data/gov-doc-fonts_2026-09-24.json`](data/gov-doc-fonts_2026-09-24.json) 공문서 폰트 테이블
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
| 자유 | 20 |
| 무료 | 9 |
| 권리불명 | 9 |
| 상용 | 106 |
| 불명 | 40 |
| **합계** | **184** |

## 전체 목록

등장 문서 수 내림차순. 비율은 450건 기준.

| 폰트 | 문서 | 비율 | 포맷 | 판정 | 권리자 | 저작권 표시 / 라이선스 | 출처 |
|---|---:|---:|---|---|---|---|---|
| 함초롬바탕 | 445 | 99% | TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 한양신명조 | 443 | 98% | HFT/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1997 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 명조 | 443 | 98% | HFT/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼명조 | 440 | 98% | HFT/TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HCI Poppy | 438 | 97% | HFT/TTF | 불명 | 휴먼컴퓨터 | - | - |
| 함초롬돋움 | 435 | 97% | TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 돋움체 | 431 | 96% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 바탕 | 423 | 94% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 맑은 고딕 | 416 | 92% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| HY헤드라인M | 384 | 85% | TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. All rights reserved. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴바탕 | 365 | 81% | TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. 2001-2017. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 돋움 | 329 | 73% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 산세리프 | 323 | 72% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 굴림 | 319 | 71% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 신명조■얒a | 285 | 63% | TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| HY중고딕 | 281 | 62% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| -윤고딕130 | 280 | 62% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명 태명조 | 279 | 62% | HFT/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Copmuter Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 견명조 | 278 | 62% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HCI Tulip | 277 | 62% | HFT | 불명 | 휴먼컴퓨터 | - | - |
| 한양견명조 | 275 | 61% | HFT/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| #신명조 | 275 | 61% | HFT/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤고딕220 | 274 | 61% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| HY각헤드라인M | 273 | 61% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| #세명조 | 272 | 60% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 바탕체 | 214 | 48% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 한양중고딕 | 153 | 34% | HFT/TTF | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| Times New Roman | 45 | 10% | TTF | 상용 | Monotype | © 2014 The Monotype Corporation. All Rights Reserved. Hebrew OpenType  | [폰트 내장 고지](findings-licenses.md) |
| Arial | 38 | 8% | TTF | 상용 | Monotype | © 2015 The Monotype Corporation. All Rights Reserved. Hebrew OpenType  | [폰트 내장 고지](findings-licenses.md) |
| 굴림체 | 29 | 6% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| HY울릉도M | 28 | 6% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 휴먼고딕 | 27 | 6% | TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 윤고딕 230 | 25 | 6% | TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| KoPub돋움체 Bold | 21 | 5% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| HY견고딕 | 18 | 4% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴 윤고딕 240 | 18 | 4% | TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| KoPub바탕체 Light | 18 | 4% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| Arial-BoldMT | 16 | 4% | TTF | 불명 | - | - | - |
| KoPub돋움체 Light | 16 | 4% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| Calibri | 16 | 4% | TTF | 상용 | Microsoft / Monotype | © 2014 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| Arial TUR | 15 | 3% | TTF | 불명 | - | - | - |
| -윤명조120 | 14 | 3% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 한컴돋움 | 14 | 3% | TTF | 상용 | (주)한양정보통신 | (C) Copyright HanYang I&C Co.,Ltd. 2001-2017. | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 나눔고딕 | 13 | 3% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 한양견고딕 | 12 | 3% | HFT | 상용 | (주)한양정보통신 | (c) Copyright 1992,1993 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 신명 신명조 | 11 | 2% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| HCI Hollyhock | 10 | 2% | HFT | 불명 | 휴먼컴퓨터 | - | - |
| 함초롬바탕 확장B | 10 | 2% | TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| 신명 세명조 | 10 | 2% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Cambria | 9 | 2% | TTF | 상용 | Microsoft / Monotype | © 2013 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| 한양중고딕&quot; | 9 | 2% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| KoPub돋움체 Medium | 9 | 2% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| Aptos | 9 | 2% | TTF | 불명 | - | - | - |
| -윤고딕120 | 8 | 2% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| #태고딕 | 8 | 2% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 태고딕 | 8 | 2% | HFT/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 문체부 바탕체 | 8 | 2% | TTF | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 신명 중고딕 | 8 | 2% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한컴 윤고딕 720 | 7 | 2% | TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| HY신명조 | 6 | 1% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| HY울릉도B | 6 | 1% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2003 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| MD솔체 | 6 | 1% | TTF | 불명 | - | (c) Copyright MorrisDesign. All Rights Reserved. | - |
| 궁서 | 6 | 1% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 한컴 윤고딕 250 | 6 | 1% | TTF | 상용 | (주)윤디자인연구소 | Copyright (C) 1989-2009 YoonDesign Inc. All Rights Reserved. | [원문](https://font.co.kr/policy/license) |
| -윤고딕320 | 5 | 1% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| -윤고딕330 | 5 | 1% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| HY그래픽 | 5 | 1% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 한컴 고딕 | 5 | 1% | TTF | 상용 | (주)한글과컴퓨터 | Copyright (c) 2017 Hancom Inc. All rights reserved. Font designed by F | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| MS Mincho | 4 | 1% | TTF | 상용 | Microsoft / Monotype | © 2017 data:RICOH Co.,Ltd. typeface:RYOBI IMAGIX CO. | [폰트 내장 고지](findings-licenses.md) |
| 신명조 간자 | 4 | 1% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1998 Han Media | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한양신명조V | 4 | 1% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1997 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 해수체B | 4 | 1% | TTF | 불명 | - | - | - |
| 한양궁서 | 4 | 1% | HFT | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 휴먼옛체 | 4 | 1% | TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTER | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 새굴림 | 4 | 1% | TTF | 불명 | - | - | - |
| Noto Sans CJK KR | 4 | 1% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://fonts.google.com/noto) |
| 한컴 윤고딕 760 | 4 | 1% | TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| KoPub바탕체 Bold | 4 | 1% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| HY견명조 | 4 | 1% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 신명 세고딕 | 4 | 1% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| KoPubWorld돋움체 Light | 4 | 1% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| 신명조 | 4 | 1% | TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| 나눔바른고딕 | 3 | 1% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| -윤명조310 | 3 | 1% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 나눔명조OTF ExtraBold | 3 | 1% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| Arial Narrow | 3 | 1% | TTF | 상용 | Monotype | Typeface © The Monotype Corporation plc. Data © The Monotype Corporati | [폰트 내장 고지](findings-licenses.md) |
| Symbol | 3 | 1% | TTF | 상용 | Monotype | Typeface © The Monotype Corporation plc. Data © The Monotype Corporati | [폰트 내장 고지](findings-licenses.md) |
| 중고딕 | 3 | 1% | TTF | 불명 | - | - | - |
| 시스템 | 3 | 1% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994-1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 순명조 | 3 | 1% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 산돌명조 L | 3 | 1% | TTF | 불명 | - | - | - |
| -윤고딕120-90% | 3 | 1% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| SimSun | 3 | 1% | TTF | 불명 | - | © Copyright ZHONGYI Electronic Co. 2001 | - |
| KoPubWorld돋움체 Bold | 3 | 1% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| (한)문화방송 | 2 | 0% | TTF | 불명 | - | - | - |
| -윤고딕340 | 2 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 신명조확장둘 | 2 | 0% | TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| 신명조\,한컴돋움 | 2 | 0% | TTF | 상용 | 신명시스템즈 / (주)한글과컴퓨터 | - | - |
| Aptos Display | 2 | 0% | TTF | 불명 | - | - | - |
| 한컴산뜻돋움 | 2 | 0% | TTF | 상용 | (주)한글과컴퓨터 | Copyright (c) 2017 Hancom Inc. All rights reserved. Font designed by F | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 나눔명조 | 2 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| #그래픽 | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 한양그래픽 | 2 | 0% | HFT | 상용 | (주)한양정보통신 | (c) Copyright 1992,1995 Hanyang Systems | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| 가는안상수체 | 2 | 0% | TTF | 불명 | 휴먼컴퓨터 | - | - |
| 신명 중명조 | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 가는둥근제목체 | 2 | 0% | TTF | 불명 | - | - | - |
| -윤고딕310 | 2 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| Yoon가변 윤고딕 110_TT | 2 | 0% | TTF | 불명 | - | - | - |
| 영화체 | 2 | 0% | TTF | 불명 | - | - | - |
| HY특견명조 | 2 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| HCI Acacia | 2 | 0% | HFT | 불명 | 휴먼컴퓨터 | - | - |
| #신세고딕 | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 다음_Regular | 2 | 0% | TTF | 불명 | - | - | - |
| #세고딕 | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 문체부 제목 돋음체 | 2 | 0% | TTF | 무료 | - | 출처를 밝히고 자유롭게 활용 가능. 글꼴 자체의 유료 판매만 금지 | [원문](https://www.happyjung.com/font/21) |
| 신명 태그래픽 | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 산돌명조 L\,한컴돋움 | 2 | 0% | TTF | 불명 | - | - | - |
| HYHeadLine M | 2 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Tahoma | 2 | 0% | TTF | 상용 | Microsoft / Monotype | © 2016 Microsoft Corporation. All rights reserved. Hebrew OpenType Lay | [폰트 내장 고지](findings-licenses.md) |
| Verdana | 2 | 0% | TTF | 상용 | Microsoft / Monotype | © 2016 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| 양재 튼튼B | 2 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1996 Yangjae LAB | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| -윤명조350 | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| -윤명조320 | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 태 나무 | 1 | 0% | TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1996 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| AmeriGarmnd BT | 1 | 0% | TTF | 상용 | (주)한글과컴퓨터 | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 바른공군체 Bold | 1 | 0% | TTF | 불명 | - | - | - |
| 강한공군체 Bold | 1 | 0% | TTF | 불명 | - | - | - |
| 경기천년바탕 Regular | 1 | 0% | TTF | 무료 | - | 경기도 배포 무료 글꼴 | [원문](https://www.gg.go.kr/contents/contents.do?ciIdx=679) |
| HY그래픽M | 1 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| 맑은고딕 | 1 | 0% | TTF | 상용 | Microsoft / Monotype | - | [폰트 내장 고지](findings-licenses.md) |
| 고딕 | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1989,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| KAI/KASB | 1 | 0% | HFT | 불명 | - | - | - |
| 한컴 윤고딕 740 | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | Copyright © 2012-2013 YoonDesign Inc. All rights reserved. | [원문](https://font.co.kr/policy/license) |
| 궁서체 | 1 | 0% | TTF | 권리불명 | - | 한컴 공지: Windows 기본 글꼴로, (주)한글과컴퓨터가 저작권자와의 계약을 통해 라이선스를 보유한 것이 아님. 권리 관계는 글꼴 저작권 | [원문](https://www.hancom.com/support/faqCenter/faq/detail/2681) |
| 나눔스퀘어 네오 ExtraBold | 1 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| 옥션고딕 B | 1 | 0% | TTF | 불명 | - | - | - |
| -윤고딕140 | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 학교안심 바른돋움 R | 1 | 0% | TTF | 불명 | - | - | - |
| KoPub바탕체 Medium | 1 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| NanumSquare | 1 | 0% | TTF | 불명 | - | - | - |
| 태 가는 헤드라인D | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 신그래픽 | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Hobo BT | 1 | 0% | TTF | 상용 | (주)한글과컴퓨터 | Copyright 1990-1992 as an unpublished work by Bitstream Inc. All right | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 휴먼모음T | 1 | 0% | TTF | 상용 | 휴먼컴퓨터 | - | - |
| 산돌고딕M | 1 | 0% | TTF | 불명 | - | - | - |
| 문화바탕제목 | 1 | 0% | HFT/TTF | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| Calibri \(Body\) | 1 | 0% | TTF | 불명 | - | - | - |
| 은 돋움 | 1 | 0% | TTF | 불명 | - | - | - |
| 경기천년제목 Light | 1 | 0% | TTF | 무료 | - | 경기도 배포 무료 글꼴 | [원문](https://www.gg.go.kr/contents/contents.do?ciIdx=679) |
| 신명 견고딕 | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| KOHI나눔 Bold | 1 | 0% | TTF | 불명 | - | - | - |
| KOHI나눔 Light | 1 | 0% | TTF | 불명 | - | - | - |
| 한양신명조\,한컴돋움 | 1 | 0% | TTF | 상용 | (주)한양정보통신 | - | [EULA](https://www.hanyang.co.kr/license_20131011.php) |
| Helvetica Neue | 1 | 0% | TTF | 상용 | Monotype | Part of the digitally encoded machine readable outline data for produc | [폰트 내장 고지](findings-licenses.md) |
| 산돌고딕 M | 1 | 0% | TTF | 불명 | - | - | - |
| 한컴 훈민정음 가로쓰기 | 1 | 0% | TTF | 무료 | - | 한컴 서체 라이선스 — 상업적 사용·임베딩·서버 탑재 허용, 수정·재배포 금지 | [원문](https://font.hancom.com/pc/sub/sub3_1.php) |
| HY궁서 | 1 | 0% | TTF | 상용 | (주)한양정보통신 | (c) Copyright HanYang I&C Co.,Ltd. 2002 | [원문](https://www.hanyang.co.kr/license_20131011.php) |
| Noto Sans CJK SC | 1 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://fonts.google.com/noto) |
| 함초롬바탕 확장 | 1 | 0% | TTF | 무료 | - | 한컴 — 무료 제공, 모든 출판물·저작물에 사용 가능, 임베딩 허용. 수정·상업적 배포 금지 | [원문](https://noonnu.cc/font_page/654) |
| Microsoft YaHei | 1 | 0% | TTF | 상용 | Microsoft / Monotype | © 2008 Microsoft Corporation. All Rights Reserved. Portions © 2008 Bei | [폰트 내장 고지](findings-licenses.md) |
| KoPubWorld바탕체 Light | 1 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| D2Coding | 1 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://github.com/naver/d2codingfont) |
| MS Gothic | 1 | 0% | TTF | 상용 | Microsoft / Monotype | © 2017 data:RICOH Co.,Ltd. typeface:RYOBI IMAGIX CO. | [폰트 내장 고지](findings-licenses.md) |
| THE명품고딕B_U | 1 | 0% | TTF | 불명 | - | - | - |
| Yoon 윤명조 550_TT | 1 | 0% | TTF | 불명 | - | - | - |
| 휴먼신문명조 | 1 | 0% | TTF | 상용 | 휴먼컴퓨터 | - | - |
| 휴먼엑스포 | 1 | 0% | TTF | 상용 | 휴먼컴퓨터 | - | - |
| Garamond | 1 | 0% | TTF | 상용 | Monotype | Digitized data copyright Monotype Typography, Ltd 1991-1995. All right | [폰트 내장 고지](findings-licenses.md) |
| Aptos Narrow | 1 | 0% | TTF | 불명 | - | - | - |
| AppleSDGothicNeoR00 | 1 | 0% | TTF | 불명 | - | - | - |
| 휴먼굵은샘체 | 1 | 0% | TTF | 상용 | (주)한글과컴퓨터 | HUMAN LICENSE TO HANGUL&COMPUTERS | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 다음_SemiBold | 1 | 0% | TTF | 불명 | - | - | - |
| Rix모던고딕 M | 1 | 0% | TTF | 불명 | - | - | - |
| 신명 신신명조 | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 신명 신문명조 | 1 | 0% | HFT | 상용 | (주)한글과컴퓨터 | (c) Copyright 1994,1995 Hangul & Computer Co., Ltd. | [한컴 서체 라이선스](sources/licenses/hancom-fonts_license_2026-09-24.md) |
| 나눔스퀘어 ExtraBold | 1 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://hangeul.naver.com/font) |
| Microsoft Sans Serif | 1 | 0% | TTF | 상용 | Microsoft / Monotype | © 2006 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |
| KoPubWorld바탕체 Medium | 1 | 0% | TTF | 자유 | - | 한국출판인회의 무료 배포 | [원문](https://www.kopus.org/biz-01-02/) |
| Arial Unicode MS | 1 | 0% | TTF | 상용 | Monotype | Digitized data copyright (C) 1993-2000 Agfa Monotype Corporation. All  | [폰트 내장 고지](findings-licenses.md) |
| Traditional Arabic | 1 | 0% | TTF | 불명 | - | - | - |
| Noto Sans CJK DemiLight | 1 | 0% | TTF | 자유 | - | SIL Open Font License 1.1 | [원문](https://fonts.google.com/noto) |
| -윤고딕110-WinCharSetFFFF-H | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| -윤고딕110 | 1 | 0% | TTF | 상용 | (주)윤디자인연구소 | - | [FONCO 사용범위](https://font.co.kr/policy/license) |
| 맑은 고딕 Semilight | 1 | 0% | TTF | 상용 | Microsoft / Monotype | © 2015 Microsoft Corporation. All Rights Reserved. | [폰트 내장 고지](findings-licenses.md) |

## 라이선스 원문 보존 사본

| 문서 | 사본 | 원 출처 |
|---|---|---|
| 한컴 서체 라이선스 | [사본](sources/licenses/hancom-fonts_license_2026-09-24.md) | https://font.hancom.com/pc/sub/sub3_1.php |
| 한컴 FAQ 2681 (Windows 기본 글꼴) | [사본](sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md) | https://www.hancom.com/support/faqCenter/faq/detail/2681 |
| (주)한양정보통신 EULA | 발췌 인용 — [clause-matrix.md](clause-matrix.md) | https://www.hanyang.co.kr/license_20131011.php |
| 윤디자인 FONCO 사용범위 | 발췌 인용 — [clause-matrix.md](clause-matrix.md) | https://font.co.kr/policy/license |
| 함초롬체 안내 | 발췌 인용 — [findings-openness.md](findings-openness.md) | https://noonnu.cc/font_page/654 |
| 한컴오피스 제품 EULA | 발췌 인용 — [clause-matrix.md](clause-matrix.md) | 설치본 `Contents/Resources/Readme/eula_ko.pdf` |

## 한계

- 표본은 2026-09-21~23 게시분 450건이다. 다른 시기·기관에서는 구성이 다를 수 있다
- 폰트 테이블 등재가 곧 본문 사용을 뜻하지 않는다
- 권리자가 `-`인 항목은 이 컴퓨터에 설치되어 있지 않아 파일 저작권을 확인하지 못한 것이다
- 이름 계열 추정(`HY*` → 한양정보통신 등)이 섞여 있으며, 개별 폰트의 실제 권리 귀속과 다를 수 있다
- 라이선스 요약은 공개 고지를 옮긴 것이며, 개별 구매·계약 조건과 다를 수 있다

# 폰트 파일 1,862종의 내장 라이선스 전수 조사

- 조사일: 2026-09-24
- 도구: [`tools/dump_font_licenses.py`](tools/dump_font_licenses.py)
- 원자료: [`data/font-license-census_2026-09-24.json`](data/font-license-census_2026-09-24.json) · 오픈소스분: [`data/oss-font-license_2026-09-24.json`](data/oss-font-license_2026-09-24.json)

## 가. 방법

TrueType/OpenType의 `name` 테이블과 `OS/2` 테이블은 공개 표준(OpenType 사양)이 정한 위치·형식에 따라 기록되어 있다. 이 조사는 규격에 따라 해당 필드를 읽어 표로 만들었을 뿐, 목적 코드를 원시 코드로 환원하는 과정을 포함하지 않는다.

| 추출 항목 | 내용 |
|---|---|
| name ID 0 | Copyright notice |
| name ID 7 | Trademark |
| **name ID 13** | **License Description — 파일에 내장된 라이선스 문구** |
| name ID 14 | License Info URL |
| OS/2 fsType | 임베딩 제한 비트 |

> 방법론상 유의: **name ID 13을 읽는 행위는 `hmtx`(advance width)를 읽는 행위와 기술적으로 완전히 동일하다.** 둘 다 규격이 정한 오프셋에서 값을 읽는 것이다. 라이선스를 확인하기 위한 판독을 역설계라 부르지 않는다면, 메트릭 판독도 같은 취급을 받아야 한다는 논증이 성립한다.

## 나. 조사 대상

| 출처 | 폰트 수 | 내장 문구 보유 | 고유 문구 수 |
|---|---:|---:|---:|
| Microsoft Office (Word/Excel/PowerPoint 번들) | 906 | 549 (60%) | 15 |
| macOS (System/Library/Fonts + Supplemental) | 769 | 281 (36%) | 26 |
| 한컴오피스 한/글 12.30.0 번들 | 187 | 30 (16%) | 14 |
| **합계** | **1,862** | **860 (46%)** | **49** |

별도로 오픈소스·MCF 폰트 27종을 같은 방식으로 조사했다(라. 참조).

## 다. 핵심 결과 — 금지 키워드 검색

내장 라이선스 문구 **860건(고유 49종)** 전체에 대한 키워드 검색 결과.

| 분류 | 검색어 | 해당 폰트 | 고유 문구 |
|---|---|---:|---:|
| **A 메트릭·수치 추출** | metric, kerning, advance width, side bearing, spacing, 자간, 장평, 간격, 수치 | **0** | **0** |
| **B 역설계** | reverse engineer, decompile, disassemble, 역설계, 디컴파일, 리버스 | **0** | **0** |
| C 수정·개작 | modify, alter, adapt, derivative, 개작, 수정, 변형 | 87 | 4 |
| E 복제·배포 | copy, distribute, redistribute, 복제, 배포 | 362 | 30 |

### 관찰 1 — A와 B가 모두 0이다

- 1,862종의 폰트 파일 어디에도 메트릭 추출을 금지하는 문구가 없다
- **역설계 금지 문구도 단 한 건도 없다.** 소프트웨어 EULA에서 표준 조항으로 통하는 문구가 폰트 파일 내장 라이선스에는 존재하지 않는다

### 관찰 2 — "modify"가 나오는 4건은 전부 금지가 아니라 허용이다

| 문구 | 폰트 수 | 성격 |
|---|---:|---|
| ParaType Free Font License | 16 | "grants you the right to use, copy, **modify** this font and distribute modified and unmodified copies" — **명시적 허용** |
| STIX Fonts (OFL 기반) | 29 | 파생물 작성을 허용하되 **이름을 바꿀 것**을 요구 |
| Microsoft supplied font (Hebrew Layout Logic 포함본) | 42 | "modify"는 본문이 아니라 첨부된 **MIT 라이선스** 부분에 등장 |

즉 조사 대상 폰트 파일에서 "수정"이라는 단어는 **오직 권리를 부여하는 맥락에서만** 나타났다.

## 라. 실제로 존재하는 조항은 어떤 것인가

고유 문구 49종 중 상위 유형.

| 문구 유형 | 폰트 수 | 금지 범위 |
|---|---:|---|
| Microsoft/일반 "use scope" 형 | 199 | 표시·인쇄, 임베딩(파일 내 제한 범위), 프린터 임시 다운로드 — **"Any other use is prohibited"** |
| SIL Open Font License 1.1 | 146 | 개방형. 사용·수정·재배포 허용 |
| Microsoft supplied font | 112 | 위 use scope 형과 동일 구조 |
| "Please contact the vendor to learn more about license restrictions." | 69 | **내용 없음** — 사실상 백지 |
| Monotype NOTIFICATION OF LICENSE AGREEMENT | 61 | "You may not copy or distribute this software" |
| Microsoft app and services font | 36 | 특정 제품·서비스 전용 |

`Any other use is prohibited` 를 포함하는 폰트는 **208종**이다.

### 관찰

- 폰트 라이선스의 규율 구조는 일관되게 **"어디에 쓸 수 있는가"(사용 매체·범위)** 중심이다
- **"파일을 어떻게 다룰 수 있는가"(분석·판독·개변)** 는 규율 대상으로 등장하지 않는다
- 다만 Microsoft 계열의 `Any other use is prohibited` 는 열거되지 않은 모든 행위를 포괄적으로 금지하는 형태여서, 메트릭 판독이 여기에 포섭되는지는 문언만으로 단정할 수 없다 (→ 변호사 검토 필요 사항)

## 마. 임베딩 제한 비트(OS/2 fsType) 분포

| 값 | 의미 | macOS | MS Office | 한컴 | 합계 |
|---|---|---:|---:|---:|---:|
| 8 | Editable | 120 | 795 | 29 | 944 |
| 0 | Installable (제한 없음) | 437 | 93 | 78 | 608 |
| 4 | Preview & Print | 188 | 12 | 32 | 232 |
| 2 | **Restricted License** | 3 | 0 | **47** | 50 |
| 기타 | | 21 | 6 | 1 | 28 |

### 관찰 — 한컴 번들의 Restricted License 47종

- 47종의 내역: **Bitstream 영문 장식체 39종** + **서울시스템 8종**
- 서울시스템 8종은 모두 **문체부 명의 서체**다

| 폰트 | fsType |
|---|---|
| 문체부 제목 바탕체 / 돋음체 / 제목 돋음체 / 바탕체 | 2 Restricted License |
| 문체부 궁체 정자체 / 궁체 흘림체 / 쓰기 정체 / 쓰기 흘림체 | 2 Restricted License |
| 문체부 훈민정음체 | 4 Preview & Print |

- **정부 부처 명의로 배포되는 서체가, 조사 대상 한글 폰트 중 가장 제한적인 임베딩 비트를 달고 있다**
- 경위는 확인하지 못했다. 문체부가 정한 것인지, 제작사(서울시스템)의 기본값인지 별도 확인 필요

## 바. 공문서 본문 폰트일수록 문구가 없다

[공문서 450건 조사](findings-gov-docs.md)에서 확인된 상위 폰트의 내장 라이선스.

| 폰트 | 공문서 등장률 | 내장 문구(ID 13) | fsType |
|---|---:|---|---|
| 함초롬바탕·함초롬돋움 | 98% / 96% | `YoonDesign Inc.` (상호만) | 8 Editable |
| 굴림·굴림체·바탕체·돋움체·궁서·궁서체 | 71~95% | **없음** | **0 Installable** |
| 한컴바탕·한컴돋움 | 71% | **없음** | **0 Installable** |
| HY 계열 다수 | 62~85% | **없음** | **0 Installable** |
| 맑은 고딕 | 92% | Monotype 표준문구 | 4 Preview & Print |

- **공문서 본문에 가장 많이 쓰이는 한글 폰트일수록 파일 안에 라이선스 문구가 없고 임베딩 제한도 0이다**
- 함초롬 계열의 ID 13은 `YoonDesign Inc.` 라는 **상호 문자열 하나**이며, 어떤 조건도 기술하지 않는다

## 사. 오픈소스 폰트 및 MCF 선례 27종

| 폰트군 | 종수 | 내장 라이선스 | fsType |
|---|---:|---|---|
| **Liberation** (Arial/Times/Courier 대응 MCF) | 12 | SIL Open Font License 1.1 | **0 Installable** |
| **Carlito** (Calibri 대응 MCF) | 4 | SIL Open Font License 1.1 | **0 Installable** |
| **Caladea** (Cambria 대응 MCF) | 4 | SIL Open Font License 1.1 | **0 Installable** |
| 고딕 A1 | 2 | SIL Open Font License 1.1 | 0 Installable |
| 나눔 계열 | 3 | `NHN Corporation` | 0 Installable |

### 관찰

- **MCF 선례 3종은 모두 OFL 1.1 + fsType 0**이다. 배포 조건에 아무런 제약을 두지 않았다
- 주목할 점: **고딕 A1은 저작권 표시가 `HanYang I&C` 이면서 OFL 1.1로 배포된다.** 역설계 금지 조항을 둔 바로 그 회사가, 다른 폰트는 자유 라이선스로 내놓고 있다
- 나눔 계열은 ID 13이 `NHN Corporation` 상호 문자열뿐이며 조건을 기술하지 않는다 (실제 라이선스는 별도 문서로 배포)

## 아. 한계

- 이 조사는 **폰트 파일에 내장된 문구**만 대상으로 한다. 제품 EULA·권리자 약관은 [`clause-matrix.md`](clause-matrix.md)에서 별도로 다룬다
- 내장 문구가 없다는 사실이 곧 제한이 없다는 뜻은 아니다. 제한이 다른 문서에 있을 수 있다
- 반대로 내장 문구가 있어도 그것이 계약상 구속력 있는 조건인지는 별개 문제다
- 키워드 검색은 영어·한국어 표현을 대상으로 했다. 다른 언어의 라이선스 문구는 탐지되지 않았을 수 있다
- 조사 대상은 이 컴퓨터(macOS 24.6.0)에 설치된 판본이며, 제품·버전에 따라 다를 수 있다

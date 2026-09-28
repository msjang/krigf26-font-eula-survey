# 폰트 파일 2,073종의 내장 라이선스 전수 조사

- 조사일: 2026-09-24 (Windows 10 분 2026-09-29 추가)
- 도구: [`tools/dump_font_licenses.py`](tools/dump_font_licenses.py) · [`tools/scan_license_keywords.py`](tools/scan_license_keywords.py)
- 원자료: [`data/font-license-census_2026-09-24.json`](data/font-license-census_2026-09-24.json) · 오픈소스분: [`data/oss-font-license_2026-09-24.json`](data/oss-font-license_2026-09-24.json) · Windows 분: [`data/win10-font-license-census_2026-09-29.json`](data/win10-font-license-census_2026-09-29.json)

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
| **Windows 10 시스템 글꼴 (OS 기본)** | **189** | **189 (100%)** | **5** |
| 한컴오피스 한/글 12.30.0 번들 (macOS) | 187 | 30 (16%) | 14 |
| 한컴오피스 2024 설치분 (Windows) | 22 | 8 (36%) | 2 |
| **합계** | **2,073** | **1,057 (51%)** | **49** |

별도로 오픈소스·MCF 폰트 27종을 같은 방식으로 조사했다(아. 참조).

> **Windows 분을 왜 나눠 적었나.** 조사한 PC 의 `C:\Windows\Fonts` 는 순정이 아니다. 한컴오피스 2024 가 자기 글꼴 22개를 같은 폴더에 설치해 두었다. 파일 생성일이 갈라 준다 — OS 기본분은 2019-03-19(141개)와 2019-10-07(5개), 한컴 설치분은 2023-03-28(22개)이다. 구분 없이 세면 "Windows 글꼴" 통계가 오염된다. 확장자가 `.fon`/`.fnt` 인 옛 비트맵 글꼴 192개는 OpenType 이 아니어서 제외했다.

## 다. 핵심 결과 — 금지 키워드 검색

내장 라이선스 문구 **1,057건(고유 49종)** 전체에 대한 키워드 검색 결과.

| 분류 | 검색어 | 해당 폰트 | 고유 문구 |
|---|---|---:|---:|
| **A 메트릭·수치 추출** | metric, kerning, advance width, side bearing, spacing, 자간, 장평, 간격, 수치 | **0** | **0** |
| **B 역설계** | reverse engineer, decompile, disassemble, 역설계, 디컴파일, 리버스 | **0** | **0** |
| C 수정·개작 | modify, alter, adapt, derivative, 개작, 수정, 변형 | 113 | 4 |
| E 복제·배포 | copy, distribute, redistribute, 복제, 배포 | 387 | 29 |

Windows 10 분만 따로 세도 같다. **A 0건, B 0건**이다.

> (정정) 이 표는 처음에 Windows 분을 뺀 1,862종 기준이었고, E 행을 `362 / 30` 으로 적었다. [`tools/scan_license_keywords.py`](tools/scan_license_keywords.py) 로 재현 가능하게 만들어 같은 범위를 다시 세니 `360 / 29` 다. A·B·C 는 처음 값과 같았다. 위 표는 Windows 10 분을 더한 2,073종 기준이다.

### 관찰 1 — A와 B가 모두 0이다

- 2,073종의 폰트 파일 어디에도 메트릭 추출을 금지하는 문구가 없다
- **역설계 금지 문구도 단 한 건도 없다.** 소프트웨어 EULA에서 표준 조항으로 통하는 문구가 폰트 파일 내장 라이선스에는 존재하지 않는다

### 관찰 2 — "modify"가 나오는 4건은 전부 금지가 아니라 허용이다

| 문구 | 폰트 수 | 성격 |
|---|---:|---|
| ParaType Free Font License | 16 | "grants you the right to use, copy, **modify** this font and distribute modified and unmodified copies" — **명시적 허용** |
| STIX Fonts (OFL 기반) | 29 | 파생물 작성을 허용하되 **이름을 바꿀 것**을 요구 |
| Microsoft supplied font (Hebrew Layout Logic 포함본) | 68 | "modify"는 본문이 아니라 첨부된 **MIT 라이선스** 부분에 등장 |

즉 조사 대상 폰트 파일에서 "수정"이라는 단어는 **오직 권리를 부여하는 맥락에서만** 나타났다.

## 라. 실제로 존재하는 조항은 어떤 것인가

고유 문구 49종 중 상위 유형. **이 표의 폰트 수는 Windows 분을 더하기 전 1,862종 기준**이다 (집계 방식을 그대로 두기 위해 갱신하지 않았다). Windows 분은 아래 마. 에서 따로 본다.

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

## 마. Windows 10 시스템 글꼴 189종 — 이 조사에서 가장 균질한 집단

공문서의 46~84% 가 쓰는 글꼴이 여기서 나온다. 한컴이 번들한 사본이 아니라 **OS 가 제공하는 원본**을 읽었다.

| 항목 | 값 |
|---|---|
| face 수 | 189 (파일 146개, TTC 전개) |
| 내장 라이선스 문구 보유 | **189 (100%)** |
| 고유 문구 수 | **5** |
| fsType | **189종 전부 8 Editable** — 예외 없음 |
| `Any other use is prohibited` 포함 | **188 / 189** |
| 라이선스 URL(name 14) 보유 | 127 |
| 메트릭 금지 문구 (분류 A) | **0** |
| 역설계 금지 문구 (분류 B) | **0** |

### 관찰 1 — 문구가 다섯 개뿐이고, 전부 이미 본 것이다

- 189종이 공유하는 라이선스 문구는 **5종**이다. 가장 많은 것 하나가 153종을 덮는다
- 그리고 **그 5종 모두가 앞서 조사한 1,862종에도 이미 등장한 문구다.** Windows 분을 더해도 고유 문구 총수는 49 그대로다
- (추론) 폰트 라이선스 문언의 세계는 생각보다 좁다. 플랫폼과 공급사가 달라도 같은 몇 개의 틀을 돌려쓴다

### 관찰 2 — 이 조사 전체에서 가장 일관된 규율

macOS 는 36%, 한컴 번들은 16% 만 문구를 달고 있고 fsType 도 제각각이다. Windows 는 **100% 가 문구를 달고 있고 fsType 이 하나로 통일**되어 있다.

- (사실) 그런데 그 일관된 문구 189건 어디에도 **메트릭 판독이나 역설계를 금지하는 말은 없다**
- (추론) 가장 촘촘하게 규율된 집단에서도 A·B 가 0 이라는 것은, 이 두 행위가 **누락된 것이 아니라 애초에 규율 대상이 아니었음**을 시사한다
- (유의) 대신 188종에 `Any other use is prohibited` 가 붙는다. 열거되지 않은 행위를 포괄 금지하는 형태이므로, 메트릭 판독이 여기 포섭되는지는 문언만으로 단정할 수 없다. 이 조사가 확인한 것은 **명시적 금지가 없다**는 사실까지다

### 관찰 3 — 한글 글꼴 8종의 저작권자

- (사실) 189종 중 저작권 표시가 `HanYang I&C` 인 것이 **8종**이다. 바탕·바탕체·궁서·궁서체·굴림·굴림체·돋움·돋움체가 여기 해당한다
- 상표는 Microsoft, 배포 라이선스도 Microsoft 문구다. 권리가 셋으로 갈리는 구조는
  [Windows 판 대조](findings-windows.md)에서 따로 다룬다

## 바. 임베딩 제한 비트(OS/2 fsType) 분포

| 값 | 의미 | macOS | MS Office | Windows 10 | 한컴(Mac) | 한컴(Win) | 합계 |
|---|---|---:|---:|---:|---:|---:|---:|
| 8 | Editable | 120 | 795 | **189** | 29 | 14 | 1,147 |
| 0 | Installable (제한 없음) | 437 | 93 | 0 | 78 | 2 | 610 |
| 4 | Preview & Print | 188 | 12 | 0 | 32 | 5 | 237 |
| 2 | **Restricted License** | 3 | 0 | 0 | **47** | 0 | 50 |
| 기타 | | 21 | 6 | 0 | 1 | 1 | 29 |

Windows 10 열이 한 칸에 몰려 있는 것이 눈에 띈다. **189종 전부가 8 Editable 이다.**

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

## 사. 공문서 본문 폰트일수록 문구가 없다

[공문서 조사](findings-gov-docs.md)에서 확인된 상위 폰트의 내장 라이선스. **아래 값은 한컴 번들본 기준이다.**

| 폰트 | 공문서 등장률 | 내장 문구(ID 13) | fsType |
|---|---:|---|---|
| 함초롬바탕·함초롬돋움 | 98% / 96% | `YoonDesign Inc.` (상호만) | 8 Editable |
| 굴림·굴림체·바탕체·돋움체·궁서·궁서체 | 71~95% | **없음** | **0 Installable** |
| 한컴바탕·한컴돋움 | 71% | **없음** | **0 Installable** |
| HY 계열 다수 | 62~85% | **없음** | **0 Installable** |
| 맑은 고딕 | 92% | Monotype 표준문구 | 4 Preview & Print |

- **공문서 본문에 가장 많이 쓰이는 한글 폰트일수록 파일 안에 라이선스 문구가 없고 임베딩 제한도 0이다**
  - (정정) 이 문장은 **한컴이 번들한 사본**에 대해서만 참이다. 위 표의 `없음`·`0 Installable` 은 한컴 번들본의 값이다
  - **Windows 원본은 정반대다.** 2026-09-29 에 OS 기본 글꼴 189종을 전수 판독하니 **189종 전부가 라이선스 문구를 갖고 있고 fsType 도 전부 8(Editable)** 이었다 (마. 참조). 같은 이름의 굴림·바탕 계열이라도 버전이 2.24 대 5.02/5.03 으로 다른 빌드다 → [findings-windows.md](findings-windows.md)
- 함초롬 계열의 ID 13은 `YoonDesign Inc.` 라는 **상호 문자열 하나**이며, 어떤 조건도 기술하지 않는다

## 아. 오픈소스 폰트 및 MCF 선례 27종

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

## 자. 한계

- 이 조사는 **폰트 파일에 내장된 문구**만 대상으로 한다. 제품 EULA·권리자 약관은 [`clause-matrix.md`](clause-matrix.md)에서 별도로 다룬다
- 내장 문구가 없다는 사실이 곧 제한이 없다는 뜻은 아니다. 제한이 다른 문서에 있을 수 있다
- 반대로 내장 문구가 있어도 그것이 계약상 구속력 있는 조건인지는 별개 문제다
- 키워드 검색은 영어·한국어 표현을 대상으로 했다. 다른 언어의 라이선스 문구는 탐지되지 않았을 수 있다
- 조사 대상은 macOS 24.6.0 과 Windows 10 (10.0.18363) 두 대에 설치된 판본이며, 제품·버전에 따라 다를 수 있다
- Windows 는 10 만 보았다. Windows 11 의 기본 글꼴은 구성과 버전이 다를 수 있다
- `.fon`/`.fnt` 옛 비트맵 글꼴 192종은 OpenType 이 아니어서 판독 대상에서 빠졌다

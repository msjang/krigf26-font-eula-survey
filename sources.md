# 출처 목록

- 수집일: 2026-09-24 (별도 표기 없는 경우)
- 원칙: 약관 원문은 전문 전재 대신 조항 분석에 필요한 범위에서 발췌 인용하고, 출처 URL·수집일·수집 방법을 함께 기록한다

## 가. 제품 EULA·권리자 약관

| 문서 | 출처 | 비고 |
|---|---|---|
| 한컴오피스 한/글 for Mac 12.30.0 제품 EULA | 설치본 내 `Contents/Resources/Readme/eula_ko.pdf` | 국문 5쪽. 설치본이 있으면 누구나 동일 경로에서 확인 가능 |
| 한컴오피스 한/글 for Mac 사용권 도움말 | 설치본 내 `Contents/Resources/Help/rights/rights.htm` | |
| 한컴오피스 2020 한/글 사용권 | https://help.hancom.com/hoffice110/ko-KR/Hwp/rights/rights.htm | |
| 한컴오피스 2022 한/글 사용권 | https://help.hancom.com/hoffice120/ko-KR/Hwp/rights/rights.htm | |
| (주)한양정보통신 EULA | https://www.hanyang.co.kr/license_20131011.php | 2013-10-10 시행 |
| 윤디자인 FONCO 사용범위 | https://font.co.kr/policy/license | |
| 윤디자인 FONCO 이용약관 | https://font.co.kr/policy/service | 전자상거래 표준약관 |

### 수집 방법

- 웹 문서: `curl` 로 HTML을 받아 태그 제거 후 텍스트 추출
- PDF: `pypdf` 로 텍스트 추출
- 로컬 사본은 조사자 작업 디렉터리에 보관하며, 이 레포에는 분석에 사용한 조항만 발췌해 수록

## 나. 폰트 파일

| 출처 | 경로 | 폰트 수 |
|---|---|---:|
| macOS 24.6.0 | `/System/Library/Fonts`, `/System/Library/Fonts/Supplemental`, `/Library/Fonts` | 769 |
| Microsoft Office for Mac | `/Applications/Microsoft {Word,Excel,PowerPoint}.app/Contents/Resources/DFonts` | 906 |
| 한컴오피스 한/글 12.30.0 | `.../Hnc/Shared/TTF/{Install,All,Hwp}` | 187 |
| 한컴오피스 HFT (한컴 고유 포맷) | `.../Hnc/Shared/Fonts/*.HFT` + `hftinfo.dat` | 387 |

### 오픈소스·MCF 폰트

| 폰트 | 출처 |
|---|---|
| Liberation 2.1.5 | https://github.com/liberationfonts/liberation-fonts (릴리스 첨부 TTF) |
| Carlito | https://github.com/googlefonts/carlito · https://github.com/google/fonts/tree/main/ofl/carlito |
| Caladea | https://github.com/huertatipografica/Caladea · https://github.com/google/fonts/tree/main/ofl/caladea |
| Pretendard / PretendardGOV 1.3.9 | https://github.com/orioncactus/pretendard |
| 나눔 계열, 고딕 A1, 고운바탕, IBM Plex Sans KR, Noto Sans KR | https://github.com/google/fonts |

## 다. 공문서

| 항목 | 내용 |
|---|---|
| 출처 | 정책브리핑 보도자료 https://www.korea.kr/briefing/pressReleaseList.do |
| 대상 | 첨부 HWPX 450건 (2026-09-21 ~ 2026-09-23 게시분) |
| robots.txt | `User-agent: *` / `Allow: /` — 2026-09-24 확인 |
| 수집 방식 | 순차 요청, 요청 간 0.35초 지연. 본문 내용은 저장하지 않고 폰트 테이블과 파일명만 추출 |
| 도구 | [`tools/harvest_gov_doc_fonts.py`](tools/harvest_gov_doc_fonts.py) |

### robots.txt 확인 결과 (2026-09-24)

| 사이트 | robots | 수집 여부 |
|---|---|---|
| www.korea.kr (정책브리핑) | `User-agent: *` `Allow: /` | 수집함 |
| www.prism.go.kr (정책연구관리시스템) | `Disallow:` 비어 있음 | 미수집 (이번 범위 밖) |
| **www.open.go.kr (정보공개포털)** | **`Disallow: /`** | **수집하지 않음** |
| **www.ntis.go.kr** | **`Disallow: /`** | **수집하지 않음** |
| www.data.go.kr | 일부 경로만 제한 | 미수집 |

원문 공문서(기안문)가 있는 정보공개포털이 가장 적합한 자료이나 robots.txt가 전면 금지이므로 수집 대상에서 제외했다.

## 다-2. 라이선스 고지 보존 사본

| 문서 | 사본 | 원 출처 |
|---|---|---|
| 한컴 서체 라이선스 | [`sources/licenses/hancom-fonts_license_2026-09-24.md`](sources/licenses/hancom-fonts_license_2026-09-24.md) | https://font.hancom.com/pc/sub/sub3_1.php |
| 한컴 FAQ 2681 (Windows 기본 글꼴 라이선스 고지) | [`sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md`](sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md) | https://www.hancom.com/support/faqCenter/faq/detail/2681 |
| 함초롬체 안내 | 발췌 인용 — [findings-openness.md](findings-openness.md) | https://noonnu.cc/font_page/654 |

폰트별 권리자·라이선스·출처는 [font-registry.md](font-registry.md)에 전수 정리했다.

## 라. 판례

| 사건 | 출처 | 상태 |
|---|---|---|
| 대법원 1996. 8. 23. 선고 94누5632 | https://casenote.kr/대법원/94누5632 | 전문 확인 |
| 대법원 2001. 6. 29. 선고 99다23246 | https://casenote.kr/대법원/99다23246 | 전문 확인 |
| 서울중앙지법 2014. 1. 23. 선고 2013가합23162 | https://www.copyright.or.kr/information-materials/trend/precedents/view.do?brdctsno=16476 | 해설 확인 |
| **대법원 2014. 10. 27. 선고 2013다74998, 2013다75007** | — | **확인 실패** (open-questions.md 참조) |

## 마. 법령

| 조문 | 출처 |
|---|---|
| 저작권법 제101조의3 (프로그램의 저작재산권의 제한) | https://casenote.kr/법령/저작권법/제101조의3 |
| 저작권법 제101조의4 (프로그램코드역분석) | https://casenote.kr/법령/저작권법/제101조의4 |
| 저작권법 제101조의5 | https://casenote.kr/법령/저작권법/제101조의5 |
| Directive 2009/24/EC Art. 6, Art. 8 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32009L0024 |

기준: 저작권법 [시행 2023. 8. 8.] [법률 제19592호, 2023. 8. 8., 타법개정]

## 바. 이력 조회

| 항목 | 출처 |
|---|---|
| hanyang.co.kr 스냅샷 이력 | https://web.archive.org/cdx/search/cdx?url=hanyang.co.kr&matchType=domain |
| license_20131011.php 스냅샷 | 2015-12-11 ~ 2026-01-11, 11건 확인 |

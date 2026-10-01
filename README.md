# 폰트 EULA 조항 조사

**폰트의 메트릭을 재는 것을 금지하는 조항이 실제로 있는가**

- 작성일: 2026.09.
- 작성자: 장민석 (msjang@kisti.re.kr)

> [!WARNING]
> 본 문서는 발표자 개인의 조사 결과이며 소속 기관의 공식 입장이 아닙니다. 법률 의견이 아닙니다. 변호사 검토를 대체하지 않습니다.
>
> 이 저장소의 문서는 Claude Opus 5(Anthropic)를 사용하여 작성했습니다. 검수를 하였지만 실수가 있을 수 있습니다. 수정이 필요한 경우 레포의 [Issue](https://github.com/msjang/krigf26-font-eula-survey/issues)에 남겨주세요.
>
> 수집·측정에 쓴 도구는 [`tools/`](tools/)에, 원자료는 [`data/`](data/)에 두어 누구나 재현할 수 있게 했습니다.

## 작성 방식

이 조사는 Claude Opus 5(Anthropic)를 자료 수집·판독·집계 도구로 사용했습니다. 무엇을 조사할지, 어떤 표본을 쓸지, 어떤 주장을 세울지는 작성자가 정했고, AI가 쓴 서술은 작성자의 검토를 거쳤습니다.

그 검토가 실제로 작동했다는 근거를 커밋 로그로 공개합니다. **`correct`로 시작하는 커밋은 이미 공개한 주장을 철회하거나 축소한 기록**입니다. 2026-10-01 기준 **18건**이며, 그중 **15건은 작성자의 지적에서 비롯되었습니다.**

- "한컴 EULA 파일이 설치본에 존재하지 않는다"는 서술은 작성자가 검색 범위를 문제 삼아 **철회**되었습니다
- 함초롬체를 상용으로 분류한 판정은 작성자가 제시한 근거로 **뒤집혔습니다** (개방성 점수 1.2 → 14.3)
- Linux를 대표하던 폰트가 배포판이 실제로 쓰는 파일이 아니라는 지적으로 **교체**되었습니다
- "윤곽선 좌표가 0% 일치"라는 측정을 "달라 보인다"로 읽히게 둔 서술은, "전부 1유닛씩 밀어도 0%가 된다"는 지적을 받고 **형태 겹침 측정을 추가**해 정정했습니다
- "PRISM은 서버가 자동 접근을 거부한다"는 서술은, 거부의 원인이 사이트가 아니라 **이 조사의 접근 방법**이었음이 드러나 정정했습니다 (작성자 지적 아님 — 스스로 발견)
- 말줄임표를 두고 "유니코드 이름 그대로 바닥 기준인데 한국 글꼴이 관행적으로 올려 그렸다"고 쓴 서술은, **국어 규정에서 가운데가 원칙**이고 **`U+2026`의 이름에는 높이가 없다**는 지적으로 두 차례 정정했습니다

정정 18건 중 **라틴·유니코드를 기본값으로 놓고 한국 쪽을 예외로 서술한 것**이 3건입니다. 조사 주제가 정확히 그 비대칭인데 서술이 반대로 간 경우라, 따로 세어 둡니다.

정정은 커밋에만 남기지 않고 **본문에도 남깁니다.** 조용히 고치지 않습니다. 규칙은 [`PROCESS.md`](PROCESS.md)에 적어 두었습니다.

## 웹에서 읽으세요

문서가 길고 표가 많습니다. 목차와 문서 간 이동이 붙은 웹 페이지가 훨씬 읽기 편합니다.

**→ [msjang.github.io/krigf26-font-eula-survey](https://msjang.github.io/krigf26-font-eula-survey/)**

저장소에는 마크다운 원본과 도구·데이터만 둡니다. HTML은 GitHub Pages가 만듭니다.

## 무엇을 조사했나

KrIGF 2026 세션 [공익적 상호운용성을 위한 사전 법적 확신 메커니즘](https://msjang.github.io/krigf26-no-action-letter)(2026-07-02, [오픈넷 세션 정리](https://www.opennet.or.kr/27856)) 직후, 법률 패널로 참여한 박경신 교수(고려대 법학전문대학원·오픈넷)가 물었습니다.

> 실제로 EULA에 font metric 추출을 명시적으로 금지하는 조항이 있는가요? 보통은 reverse engineering 금지조항만 있는 것으로 알고 있습니다.

그 질문에 인상이 아니라 원문과 실측으로 답하려는 기록입니다.

| | 대상 | 규모 |
|---|---|---|
| 1 | 제품 EULA·권리자 약관 문언 | 7종 |
| 2 | 폰트 파일 내장 라이선스 전수 | 2,073종 |
| 3 | 실제 공문서의 폰트 사용 실태 | 표본 두 벌 — 1,906건·3,200건 (2010~2026년, 64개 부처) |
| 4 | 해외 MCF 선례 메트릭 실측 | 7쌍 |
| 5 | 한컴 고유 포맷(HFT) 레지스트리 | 387종 |
| 6 | 공문서 서식 글꼴을 정하는 법령 | 시행규칙 별표 4·5 |
| 7 | Windows 10 기본 글꼴 원본 대조 | 189종 (한글 11종) |
| 8 | 정책연구 산출물의 폰트 사용 실태 | 9,159파일 (72개 기관, 14개 문서 종류) |
| 9 | **법령 서식 전수** | **28,639건** (소관부처 98곳) |

## 답

**메트릭 추출을 금지하는 조항은 0건입니다.** 그리고 전제하셨던 역설계 금지 조항조차 일반적이지 않았습니다 — 폰트 파일 내장 라이선스 860건 중 **0건**, 약관 7종 중 **1건**뿐입니다.

다만 결론은 양면적입니다. **금지 조항이 없으니 위반을 특정할 수 없지만, 허용 조항도 없으니 적법을 확인받을 경로도 없습니다.**

근거와 자세한 내용은 [조사 리포트](report.md)와 웹 페이지에 있습니다.

## 문서

| 문서 | 내용 |
|---|---|
| [조사 리포트](report.md) | 조사 범위·방법, 쟁점별 분석, 한계 |
| [조항 매트릭스](clause-matrix.md) | 약관 7종의 조항별 분류와 원문 발췌 |
| [**상위 폰트 20종**](font-top20.md) | 가장 많이 쓰이는 20종의 권리자·라이선스·**MCF 판정** |
| [공문서 폰트 목록](font-registry.md) | 폰트 415종 전수의 권리자·라이선스·출처 링크 |
| [내장 라이선스 전수 조사](findings-licenses.md) | 폰트 2,073종 |
| [연도·부처별 추세](findings-trend.md) | 공문서 1,906건, 2010~2026년 |
| [대체 폰트 메트릭](findings-substfont.md) | 대체 지정이 조판을 보존하지 않는다는 실측 |
| [메트릭 실측](findings-metrics.md) | MCF 선례 7쌍, 한글 폰트 구조 |
| [개방성 점검](findings-openness.md) | 문서 단위 채점 도구와 결과 |
| [HFT 레지스트리](findings-hft.md) | 한컴 고유 포맷 387종, 1993~1999년 빌드 |
| [Windows 판 대조](findings-windows.md) | 한글 글꼴 11종의 권리 구조, 공문서 96%가 걸린 병목, 한컴 번들본과의 차이 |
| [OS 간 조판 차이](findings-crossos.md) | Windows·macOS·Ubuntu 26.04·Android 13 대조. 문단 폭이 최대 13.9% 달라지고 줄 수가 바뀐다 |
| [CSS 메트릭 재정의](findings-css-metrics.md) | 폰트를 만들지 않고 CSS 로 어디까지 맞출 수 있나. 웹 한정 과도기 수단 |
| [투명도화지 폰트](findings-blankfont.md) | 글리프 없이 조판 수치만 담은 폰트. 제어점 0개로 조판이 완전히 일치한다 |
| [글꼴 이름과 상표](findings-trademark.md) | `바탕`·`돋움`은 1992년 국가가 정한 순화 용어인데 등록상표로 표시되어 있다 |
| [법령 조사](findings-regulation.md) | 시행규칙 별표 4·5의 글꼴 지정 |
| [**대체 연쇄**](findings-substchain.md) | 글꼴이 없을 때 조판이 어디서 깨지나. 한자는 0%, 한글은 73%가 깨진다. 깨짐의 83%가 한 지점으로 모인다 |
| [**법령 서식 전수**](findings-lawforms.md) | 28,639건 전수. HWPX 0건, 글꼴 여덟 종을 넘기면 한컴 고유 포맷을 피해 간 서식이 **0건**이다 |
| [정책연구 보고서](findings-prism.md) | PRISM 9,159파일, 72개 기관. 문서 장르별로 갈라 보면 중앙 배포 서식만 96%가 자유 글꼴이다 |
| [공문서 실태](findings-gov-docs.md) | 사흘치 표본 450건 |
| [출처 목록](sources.md) · [남은 질문](open-questions.md) | |

## 개방성 점검 도구

HWP·HWPX 문서를 넣으면 **자유 소프트웨어만으로 같은 레이아웃을 재현할 수 있는지** 채점합니다.

```bash
pip install fonttools olefile
python3 tools/openness_check.py 문서.hwpx    # HWPX
python3 tools/openness_check.py 문서.hwp     # HWP 5.0 바이너리도 지원
```

위법 여부를 판정하지 않습니다. 경고문도 "금지되어 있다"가 아니라 **"적법한지 사전에 확인받을 경로가 없다"** 로 씁니다.

## 재현

```bash
# 폰트 내장 라이선스 전수 추출
python3 tools/dump_font_licenses.py "macOS=/System/Library/Fonts" ... > census.json

# 한컴 고유 포맷(HFT) 레지스트리
python3 tools/dump_hft_registry.py > hft-registry.json

# 공문서 폰트 수집 — 연도·부처 층화 (korea.kr robots.txt Allow 확인 후, 요청 간 지연)
python3 tools/harvest_gov_doc_fonts.py --years 2010-2026 --weeks 8 --per-year 60 > gov.json
python3 tools/harvest_gov_doc_fonts.py --list-agencies      # 부처 코드 57개

# MCF 메트릭 대조 / 대체 폰트 영향
python3 tools/metric_compat.py <원본.ttf> <MCF.ttf>
python3 tools/measure_subst_metrics.py
python3 tools/simulate_linebreak.py

# 개방성 판정 DB와 폰트 대조표 생성
python3 tools/build_openness_db.py > data/font-openness-db.json
python3 tools/build_font_registry.py > font-registry.md
```

## 조사가 하지 않은 것

- MCF 제작이 적법하다는 결론을 내리지 않았습니다. 조사한 약관에 해당 금지 조항이 **없다는 사실**을 확인했을 뿐입니다.
- 특정 기업·기관의 정책을 평가하지 않았습니다. 확인된 문언과 수치만 기술했습니다.
- 약관 원문은 전문 전재 대신 발췌 인용하고, 출처 URL·수집일·수집 방법을 함께 적었습니다.
- 원본 폰트를 개변하지 않았습니다. 규격이 정한 위치의 값을 읽어 대조했을 뿐입니다.
- robots.txt가 수집을 막는 곳(정보공개포털·NTIS·정부24)은 수집하지 않았습니다. PRISM은 서버가 자동 접근을 거부해 중단했습니다.

## 관련 자료

- KrIGF 2026 세션 개요 — <https://igf.or.kr/4095>
- 세션 발제 자료 — <https://msjang.github.io/krigf26-no-action-letter>
- 세션 영상 — <https://www.youtube.com/live/c7Ok_kNfgjI>
- Polaris MCFG — <https://github.com/PolarisOffice/polaris_mcfg>
- pypandoc-hwpx — <https://github.com/msjang/pypandoc-hwpx>

## 라이선스

조사 문서·도구·추출 데이터는 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ko). 인용한 약관 문언의 권리는 각 권리자에게 있습니다.

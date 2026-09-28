# Windows 판 대조 — 기본 글꼴의 권리 구조와 한컴 번들의 차이

- 조사일: 2026-09-29
- 대상: Windows 10 (10.0.18363) + 한컴오피스 2024 (HWP 13.0.0.1053)
- 방법: SSH 로 원격 접속해 폰트 파일과 설치 구조를 판독. 파일은 읽기만 했다
- 원자료: [`data/win10-system-fonts_2026-09-29.json`](data/win10-system-fonts_2026-09-29.json)

## 가. 왜 확인했나

이 조사는 그동안 **macOS 판 한컴오피스 12.30.0** 설치본만 보았다. 두 가지가 남아 있었다.

1. [한컴오피스 Windows 판 제품 EULA 원문](open-questions.md) — 도움말 "사용권" 페이지가 *"제품 패키지에 포함된 (주)한컴 소프트웨어 사용 계약서"* 라는 **별도 문서를 지칭**하고 있어, Mac 판과 조항 구성이 다를 가능성이 있었다. 이 조사의 핵심 근거가 "한컴 제품 EULA 에 역설계 금지 조항이 없다" 이므로, Windows 판에 있으면 결론이 흔들린다
2. **Windows 기본 글꼴 9종의 원본** — 공문서의 46~84% 가 쓰는데, 그동안 본 것은 한컴이 번들한 사본이었다

## 나. Windows 판 설치본에는 제품 EULA 파일이 없다

- (사실) `C:\Program Files (x86)\Hnc` 전체를 뒤져 `eula`·`licen`·`agree`·`readme` 패턴에 걸리는 파일을 모두 확인했다. 나온 것은 **하이픈 사전(HncHyphen)의 오픈소스 라이선스 파일들뿐**이다
- (사실) `C:\` 전체에서 `*eula*` 를 찾으면 Java 와 Windows 자체 EULA 만 나온다. 한컴 것은 없다
- (사실) Mac 판에는 `Contents/Resources/Readme/eula_ko.pdf` (국문 5쪽) 가 있다. **Windows 판 `Readme` 폴더에는 설치 안내문(`hoffice_2024.html`)만 있고 EULA 가 없다**
- (사실) Mac 판에 있던 `Help/rights/rights.htm` 같은 사용권 고지 페이지도 Windows 설치본에서 찾지 못했다

### 관찰

- (추론) Windows 판 제품 EULA 는 **설치 과정에서만 표시되고 설치본에는 남지 않는** 것으로 보인다
- 따라서 이 조사가 확보한 한컴 제품 EULA 는 여전히 **Mac 판 12.30.0 하나**다. Windows 판 문언이 같은지는 확인하지 못했다
- (유의) 다만 Windows 판 설치본에 EULA 파일이 없다는 사실 자체가, 사용자가 사후에 자신이 동의한 조건을 확인하기 어렵다는 뜻이기도 하다

## 다. Windows 기본 글꼴 9종 — 권리가 셋으로 갈린다

`batang.ttc`(4 face)·`gulim.ttc`(4 face)·`malgun.ttf` 에서 name table 을 읽었다.

| 폰트 | 저작권 (name 0) | 상표 (name 7) | 라이선스 (name 13) | fsType |
|---|---|---|---|---|
| 바탕·바탕체·궁서·궁서체 | **HanYang I&C Co.,LTD. 2000** | *registered trademark of the **Microsoft Corporation*** | Microsoft supplied font | 8 Editable |
| 굴림 | **HanYang I&C Co., LTD. 2009** | 〃 | 〃 | 8 Editable |
| 굴림체·돋움·돋움체 | **HanYang I&C Co.,LTD. 2000** | 〃 | 〃 | 8 Editable |
| 맑은 고딕 | Microsoft Corporation 2016 | Microsoft | 〃 | 8 Editable |

라이선스 문구 전문은 이렇다.

> Microsoft supplied font. You may use this font to create, display, and print content as permitted by the license terms or terms of use, of the Microsoft product, service, or content in which this font was included. You may only (i) embed this font in content as permitted by the embedding restrictions included in this font; and (ii) temporarily download this font to a printer or other output device to help print content. **Any other use is prohibited.**

### 관찰 — 이것이 "권리불명" 의 실체다

한컴은 이 9종에 대해 [FAQ 2681](sources/licenses/hancom-faq2681_windows-fonts_2026-09-24.md)에서 *"(주)한글과컴퓨터와 해당 글꼴 저작권자 간의 계약을 통해 라이선스를 보유한 것은 아닙니다"* 라고 공지한다. 파일을 열어 보니 그 말의 구조가 드러난다.

- **저작권자는 (주)한양정보통신이다.** 이 조사에서 **유일하게 역설계 금지 조항을 둔** 바로 그 회사다
- **상표권자는 Microsoft 다.** `바탕`·`굴림` 같은 이름 자체가 Microsoft 의 등록상표로 표시되어 있다
- **배포 라이선스는 Microsoft 가 관리한다.** `Any other use is prohibited` 라는 포괄 금지가 붙는다

(추론) 따라서 이 9종을 대상으로 MCF 를 만들려는 사람은 **세 갈래를 동시에 마주한다** — 저작권자의 EULA 문언, Microsoft 의 포괄 금지, 그리고 이름에 걸린 상표. 한컴에 물어도 답이 없는 이유이기도 하다. 한컴은 이 사슬의 어느 고리도 아니다.

(유의) 상표는 **이름**에 걸리는 것이므로, MCF 를 만들 때 원본과 다른 이름을 쓰면 상표 쟁점은 피할 수 있다. 해외 MCF 선례가 `Arial → Liberation Sans`, `Calibri → Carlito` 처럼 **모두 다른 이름을 쓴 것**과 일관된다.

## 라. 한컴 번들본은 Windows 원본과 다른 파일이다

같은 이름의 폰트인데 파일이 다르다.

| 폰트 | | 버전 | fsType | 내장 라이선스 | 저작권 |
|---|---|---|---|---|---|
| 굴림 | Windows | 5.03 | Editable | **있음** (Microsoft) | HanYang I&C 2009 |
| | 한컴 Mac 번들 | **2.24** | **Installable(제한 없음)** | **없음** | HanYang I&C 1995-2013 |
| 궁서 | Windows | 5.02 | Editable | 있음 | HanYang I&C 2000 |
| | 한컴 Mac 번들 | **2.24** | **Installable** | **없음** | HanYang I&C 1995-2013 |
| 맑은 고딕 | Windows | 6.68 | Editable | 있음 | Microsoft 2016 |
| | 한컴 Mac 번들 | 6.50M | **Preview & Print** | 있음 | Microsoft 2013 |

굴림체·돋움체·바탕체·궁서체도 같은 양상이다.

### 플랫폼에 따라 다르다

- (사실) **Windows 판 한컴오피스 2024 는 굴림·바탕·돋움·궁서·맑은 고딕을 번들하지 않는다.** `Shared\TTF` 에 있는 것은 `HBATANG.TTF`(한컴바탕)·`HDOTUM.TTF`(한컴돋움)뿐이다. OS 가 제공하는 것을 쓴다
- (사실) **Mac 판 한컴오피스는 자체 빌드(2.24)를 번들한다.** macOS 에는 이 글꼴들이 없기 때문으로 보인다
- (추론) 그래서 한컴의 FAQ 2681 공지는 Windows 환경을 전제한 것으로 읽힌다. Mac 판에서 한컴이 번들하는 2.24 빌드의 권리 근거는 이 조사로 확인하지 못했다

### 앞선 서술의 정정

[내장 라이선스 전수 조사](findings-licenses.md)에서 이렇게 적었다.

> 공문서 본문에 가장 많이 쓰이는 한글 폰트일수록 파일 안에 라이선스 문구가 없고 임베딩 제한도 0이다

이는 **한컴이 번들한 사본에 대해 참**이고, **Windows 원본에 대해서는 거짓**이다. Windows 원본에는 Microsoft 라이선스 문구가 있고 fsType 도 8(Editable)이다. 해당 문서에 이 구분을 추가했다.

## 마. 메트릭은 같다

파일이 달라도 배치 수치는 일치한다.

| 폰트 | upem (Win/한컴) | 한글 폭 | `A` | `0` | 공백 | |
|---|---|---|---|---|---|---|
| 굴림 | 1024/1024 | 1000/1000 | 646/646 | 574/574 | 333/333 | 동일 |
| 굴림체 | 1024/1024 | 1000/1000 | 500/500 | 500/500 | 500/500 | 동일 |
| 돋움체 | 1024/1024 | 1000/1000 | 500/500 | 500/500 | 500/500 | 동일 |
| 바탕체 | 1024/1024 | 1000/1000 | 500/500 | 500/500 | 500/500 | 동일 |
| 궁서 | 1024/1024 | 1000/1000 | 688/688 | 583/583 | 333/333 | 동일 |

- (사실) 다섯 쌍 전부에서 한글 전각 폭·라틴 폭·공백 폭이 일치한다
- (추론) 따라서 **같은 문서를 Windows 와 Mac 에서 열어도 이 글꼴들 때문에 조판이 달라지지는 않는다.** 파일은 다르지만 MCF 가 맞춰야 할 수치는 같다
- (실무적 함의) MCF 의 기준값은 어느 쪽 빌드를 재도 같다

## 바. 폰트 레지스트리는 플랫폼이 공유한다

`hftinfo.dat`(폰트명 → 파일 → 공급사 색인)을 두 플랫폼에서 비교했다.

```
Mac 한컴오피스 12.30.0 : f1462ff6e78c4dab…  65,696 B
Win 한컴오피스 2024     : f1462ff6e78c4dab…  65,696 B
                         → SHA-256 동일, 바이트 단위로 같은 파일
```

- (사실) [HFT 레지스트리 조사](findings-hft.md)가 Mac 판에서 읽은 폰트명·공급사 매핑은 **Windows 판에도 그대로 적용된다**
- (추론) 한컴이 플랫폼과 무관하게 같은 폰트 레지스트리를 유지한다는 뜻이다

## 사. 한계

- **Windows 판 제품 EULA 문언을 확인하지 못했다.** 설치본에 파일이 없어, 설치 과정에서 표시되는 문언과 Mac 판 문언이 같은지는 여전히 미확인이다
- 조사한 Windows 는 10 (10.0.18363, 1909) 이다. Windows 11 의 기본 글꼴은 버전이 다를 수 있다
- 한컴오피스 2024 (13.0.0.1053) 번들 폰트 152종·HFT 390종의 전수 조사는 하지 않았다. Mac 판(TTF 187·HFT 387)과 구성이 다르므로 별도 과제다
- 메트릭 비교는 한글 1자·라틴 3자 표본이다. 전수 비교는 하지 않았다
- 상표에 관한 서술은 폰트 파일의 `name` ID 7 표기를 옮긴 것이며, 상표권의 실제 등록 상태나 효력 범위를 확인한 것이 아니다

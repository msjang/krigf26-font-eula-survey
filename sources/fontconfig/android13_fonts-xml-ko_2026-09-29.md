# Android 13 — `/system/etc/fonts.xml` 의 한국어 선언

- 수집일: 2026-09-29
- 출처: `budtmo/docker-android:emulator_13.0` 안의 `system-images/android-33/google_apis/x86_64/system.img`
- 판독: GPT → `super` 동적 파티션 → ext4 논리 파티션 → `debugfs` (마운트·부팅 없이 읽기만 했다)
- 버전 확인 (`/system/build.prop`)

```
ro.build.version.sdk=33
ro.build.version.release=13
```

## `<family lang="ko">` 원문

```xml
<family lang="ko">
        <font weight="400" style="normal" index="1" postScriptName="NotoSansCJKjp-Regular">
            NotoSansCJK-Regular.ttc
        </font>
        <font weight="400" style="normal" index="1" fallbackFor="serif"
              postScriptName="NotoSerifCJKjp-Regular">NotoSerifCJK-Regular.ttc
        </font>
    </family>
```

## 읽는 법

- `index="1"` 은 `NotoSansCJK-Regular.ttc` 안의 두 번째 face 를 가리키며, 그 face 의
  PostScript 이름은 `NotoSansCJKkr-Regular` 다. 즉 **한국어 기본 글꼴은 Noto Sans CJK KR** 이다
- `postScriptName` 속성에 `jp` 가 적혀 있으나 이는 TTC 파일의 대표 이름이고,
  실제 선택은 `index` 가 결정한다

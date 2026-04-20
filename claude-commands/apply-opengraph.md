# Apply OpenGraph Image (Next.js App Router)

현재 Next.js(app router) 프로젝트를 분석해서 OpenGraph 이미지를 생성하고, 파일을 적절한 위치에 배치한 뒤 메타데이터까지 자동으로 적용합니다.

이 커맨드는 `skills/opengraph-image` 스킬을 내부적으로 사용합니다.

사용자 입력: $ARGUMENTS

`$ARGUMENTS`로 받을 수 있는 힌트(모두 선택):

- `title="..."` — 제목을 강제 지정
- `subtitle="..."` — 부제를 강제 지정
- `prompt="..."` — 배경 프롬프트(영문 권장) 직접 지정
- `align=bottom-left|bottom-center|center|...` — 텍스트 정렬
- `route=/blog/my-post` — 특정 경로의 라우트 전용 OG 이미지 생성
- `skip-bg` — AI 배경 없이 단색으로
- `dry-run` — 파일을 쓰지 않고 계획만 보고

---

## 실행 단계

### 1. 프로젝트 검증

1. 현재 디렉토리(또는 사용자가 지정한 디렉토리)에서 다음을 확인합니다.
   - `package.json`에 `"next"` 의존성이 있는지
   - `app/` 디렉토리가 존재하는지 (app router 사용 중인지)
   - TypeScript 여부 확인 (`tsconfig.json` 존재 여부로 판단, 파일 확장자 `.tsx`/`.jsx` 결정)

2. app router가 아니거나 Next.js가 아니면, 사용자에게 알리고 `pages router` 또는 일반 웹사이트 적용 방법을 간단히 안내한 뒤 중단합니다. 계속 진행할지 묻습니다.

### 2. 메타데이터 수집

다음 우선순위로 **제목**과 **부제/설명**을 추출합니다 (사용자 입력이 최우선):

1. `$ARGUMENTS`의 `title=`, `subtitle=`
2. `app/layout.tsx`(또는 `.ts`/`.js`/`.jsx`) 안의 `export const metadata`에서 `title`, `description`
3. `app/page.tsx`의 metadata
4. `package.json`의 `name`, `description`
5. `README.md` 최상단의 `# 제목` 과 첫 단락

TypeScript의 `title`은 `string | { default, template, absolute }` 객체일 수 있으니 객체면 `default` 또는 `absolute`를 사용합니다.

특정 라우트용(`route=/blog/xxx`)이면 해당 라우트의 `page.tsx` 옆에 있는 metadata를 우선 사용합니다.

### 3. 배경 프롬프트 결정

1. `$ARGUMENTS`에 `prompt=`가 있으면 그대로 사용합니다.
2. 없으면 프로젝트 성격을 추론해 영문 프롬프트를 구성합니다.
   - `package.json`의 keywords, description, dependencies를 참고해서 분위기 결정
     - AI/LLM 관련이면 tech/dark/neon
     - 블로그/콘텐츠면 warm/editorial
     - 디자인/포트폴리오면 minimal/pastel
     - 기본값은 "modern abstract gradient, cinematic lighting, leaving space for overlay text"
   - 프롬프트에는 **항상 `leaving space for overlay text` / `minimal subject` 류 문구**를 포함해 텍스트 가독성을 확보합니다.
3. 사용자가 확인할 수 있도록 결정된 `title`, `subtitle`, `prompt`를 요약해서 보여줍니다.

### 4. 스킬 호출

`skills/opengraph-image/scripts/generate_og_image.py`를 호출합니다.

- **출력 경로 규칙**:
  - `route` 인자가 없으면 → `app/opengraph-image.png` (사이트 전체 기본값)
  - `route=/blog/[slug]` 처럼 라우트 지정 시 → `app/blog/[slug]/opengraph-image.png`
  - `app/` 디렉토리가 src 하위에 있으면 (`src/app/`) 그쪽에 저장합니다.
- `skip-bg` 힌트가 있으면 `--skip-bg`로 호출합니다.

실행 예:

```bash
export REPLICATE_API_TOKEN="${REPLICATE_API_TOKEN:?REPLICATE_API_TOKEN 환경변수가 필요합니다}"

python "$(git rev-parse --show-toplevel 2>/dev/null || echo "$HOME/git/clever-chip")/skills/opengraph-image/scripts/generate_og_image.py" \
  --title "$TITLE" \
  --subtitle "$SUBTITLE" \
  --prompt "$PROMPT" \
  --output "$OUTPUT_PATH" \
  --align bottom-left
```

`REPLICATE_API_TOKEN`이 설정돼 있지 않으면 사용자에게 안내하고, `--skip-bg`로 폴백할지 묻습니다.

### 5. 대체 텍스트 파일 생성

같은 디렉토리에 `opengraph-image.alt.txt`를 만들어 대체 텍스트(제목 + 부제)를 저장합니다. 이미 있으면 덮어쓸지 묻습니다.

### 6. metadata 적용 및 검증

`app/layout.tsx`의 `export const metadata`를 확인해 다음이 설정돼 있는지 점검합니다.

1. **`metadataBase`**: 없다면 `package.json`의 `homepage` 또는 README에서 URL을 추정해 추가 제안.
   ```tsx
   metadataBase: new URL("https://example.com"),
   ```
   URL을 결정할 수 없으면 placeholder(`https://your-domain.com`)로 두고 사용자에게 수정하도록 안내합니다.

2. **`openGraph`** / **`twitter`** 설정: 파일 기반 규칙(`app/opengraph-image.png`)을 쓰면 Next.js가 자동 주입하므로 **명시 설정이 없어도 동작**합니다. 다만 `twitter.card`를 `summary_large_image`로 지정하는 게 좋아서 없으면 추가 제안합니다.

3. 수정 전에 항상 변경사항을 사용자에게 미리 보여주고 동의를 구합니다 (diff 형태 권장).

`dry-run`이 있으면 실제 파일 변경은 생략하고 계획만 출력합니다.

### 7. 결과 리포트

아래 형식으로 한국어 요약을 제공합니다.

```
OpenGraph 이미지 적용 완료 ✅

- 생성 파일: app/opengraph-image.png (1200x630, PNG)
- 대체 텍스트: app/opengraph-image.alt.txt
- 제목: {title}
- 부제: {subtitle}
- 배경 프롬프트: {prompt_summary}
- 변경된 파일: app/layout.tsx (metadata 보강)

확인 링크
- Facebook Debugger: https://developers.facebook.com/tools/debug/?q={site_url}
- X Card Validator: https://cards-dev.twitter.com/validator
- LinkedIn Inspector: https://www.linkedin.com/post-inspector/

⚠️ 소셜 플랫폼은 OG 이미지를 강하게 캐시합니다. 교체 후 위 링크에서 재스크랩 해야 즉시 반영됩니다.
```

---

## 에러 처리

- **Pillow 미설치**: `pip install pillow --break-system-packages` 안내 후 자동 설치 제안.
- **REPLICATE_API_TOKEN 없음**: 사용자에게 토큰을 입력받거나 `--skip-bg` 폴백 제안. 절대 토큰을 파일에 기록하지 않습니다.
- **app/ 없음**: pages router 사용 가능성을 알리고, `public/og-image.png` 저장 + `_document.tsx`에 meta 추가하는 대안을 제안합니다(사용자 확인 후 진행).
- **기존 opengraph-image.png 존재**: 덮어쓸지, 백업(`.bak`)할지, 취소할지 선택지를 제시합니다.

## 모노레포 대응

`clever-chip` 같은 모노레포에서는 현재 작업 디렉토리(cwd)를 기준으로 가장 가까운 `package.json`을 찾아 그 프로젝트에만 적용합니다. 여러 Next.js 프로젝트가 있다면 어느 프로젝트에 적용할지 사용자에게 먼저 확인합니다.

## 참고

- 스킬 본체: `skills/opengraph-image/SKILL.md`
- OG 이미지 스펙: https://ogp.me/
- Next.js 파일 기반 메타데이터: https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image

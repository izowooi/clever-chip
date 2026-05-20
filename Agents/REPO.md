# 저장소 운영 방식

사용자는 `/Users/izowooi/git` 아래에서 여러 저장소를 운영한다.
이 파일은 작업 요청이 들어왔을 때 "어느 저장소를 먼저 볼지" 판단하기 위한 짧은 색인이다.

## 판단 원칙

- 요청의 제품명, 폴더명, 배포 URL, 기술 스택이 특정 저장소와 맞으면 그 저장소에서 시작한다.
- 저장소가 모호하면 추측해서 바로 수정하지 말고 사용자에게 먼저 확인한다.
- 각 저장소 안에 `AGENTS.md`, `CLAUDE.md`, `README.md`가 있으면 해당 파일의 지침을 우선 확인한다.
- `crispy-web`, `creative-plate`, `learning-cake`, `p2`, `t1`은 내부 프로젝트가 많은 묶음 저장소다.
- `crispy-web/employparty`처럼 상위 저장소 안에 별도 `.git`이 있는 중첩 저장소는 독립 저장소처럼 다룬다.

## 주요 저장소

- `crispy-web`
  - Next.js / Cloudflare Pages 기반 웹앱 묶음 저장소.
  - 예: `snapmany`, `gen-password`, `ductcanvas`, `photokeep`, `qrcode`, `podplay`, `clipplay`, `awesome-cut`, `seedance-studio`, `redraw`, `colorpick`, `imgblend`, `hero-showcase`.

- `clever-chip`
  - AI 프롬프트, 스킬, 에이전트 지침, 자동화 템플릿 저장소.

- `creative-plate`
  - 실험적 R&D 프로젝트 묶음 저장소.
  - 예: `pixel-palette`, `pixel-parfait`, `crawl-video`, `youtube-to-srt`, `aesthetics_score`, `social-syrup`.

- `learning-cake`
  - 학습/소규모 웹앱 묶음 저장소.
  - 예: 영어/일본어/중국어 학습 앱, 메모 공유, 사다리타기, 마니또, 반응속도, 일정 관리.

- `t1`
  - 금융 자동화 저장소. 주식 신호, Streamlit 대시보드, Polymarket 봇과 일일 리포트가 있다.

- `p2`
  - 크롤링/모니터링 자동화 저장소.
  - 예: ARCA 이미지 수집기, 토렌트 검색 결과 모니터링, 레거시 크롤러.

## 저장소 색인

- `NAIA2.0_origiin`
  - NAI/Stable Diffusion/ComfyUI 이미지 생성 자동화 도구의 원본 또는 외부 기반 저장소.

- `RisuAI`
  - 외부 AI 채팅 앱 저장소. Svelte/Tauri 기반 크로스플랫폼 채팅 클라이언트.

- `anime-toast`
  - NAI 기반 스토리북 제작 프로젝트. 프롬프트 박스, 팬 갤러리, 보조 스크립트가 있다.

- `cake-watch`
  - 서버 모니터링 Android 위젯 앱.

- `clever-lemon`
  - AI 시 창작 도우미 모바일 앱.

- `curious-cookie`
  - AI 이미지/지문 생성 실험성 앱. Flutter, Midjourney/OpenAI/Firebase 관련 코드가 섞여 있다.

- `dark-corn`
  - 식량 배급을 소재로 한 게임 프로젝트.

- `fish-bun`
  - 쿠키 클리커류 게임 기획 문서 저장소.

- `fresh-mint`
  - 이미지 업로드, 프롬프트 추출, 웹 스크래핑, Cloud Run 등 Python 실험 묶음.

- `fruit-combination`
  - Flutter 앱 및 배포/키 관리 관련 저장소. 세부 목적은 작업 전 확인 필요.

- `hell-timer`
  - Diablo 4 월드 이벤트 타이머 앱. Android, iOS, 스크린샷 리사이즈 도구가 있다.

- `infinite-girl`
  - Next.js 기반 이미지/캐릭터 생성 계열 웹앱으로 보이는 저장소.

- `jolly-jelly`
  - 오늘의 꽃말 등 일일 콘텐츠 생성/관리 저장소.

- `learning-roblo`
  - Roblox 학습 프로젝트 묶음. Rojo 기반 `collect-coin`, `tycoon` 등이 있다.

- `math_problems`
  - Project Euler와 React 학습용 미니 프로젝트 저장소.

- `memory-muffin`
  - 캘린더 PDF 등 개인 기록/자료성 산출물 저장소.

- `mini-muffin`
  - JavaScript/TypeScript 게임 학습용 미니 프로젝트 저장소.

- `mystic-cocoa`
  - AI 타로 카드 모바일 앱.

- `playground`
  - Next.js 기본 실험/연습용 저장소.

- `smart-sandwich`
  - AI 기반 퀴즈/학습 콘텐츠 생성 자동화 계열 저장소.

- `spicy-bullet`
  - 모바일 또는 게임성 UI 프로젝트로 보이는 저장소. 세부 목적은 작업 전 확인 필요.

- `story-soup`
  - 게임북/인터랙티브 스토리 멀티에이전트 하네스 저장소.

- `wake-coffee`
  - 알람/기상 보조 앱 계열 저장소.

## 중첩 독립 저장소

- `crispy-web/employparty`
  - `crispy-web` 내부에 있지만 별도 `.git`이 있는 Next.js 저장소. 현재는 기본 템플릿 성격이 강하다.

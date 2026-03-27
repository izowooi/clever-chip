# README 생성기

현재 프로젝트를 분석하여 **한국어 README.md**, **영어 README_EN.md**, **중국어 README_ZH.md**를 자동 생성합니다.

사용자 입력: $ARGUMENTS

## 분석 단계

1. **프로젝트 구조 파악**: 소스 코드, 설정 파일, 디렉토리 구조를 분석합니다.
2. **기술 스택 탐지**: 아래 설정 파일들에서 사용 기술을 추출합니다.
   - **JavaScript/TypeScript**: `package.json`, `tsconfig.json`, `bun.lockb`, `pnpm-lock.yaml`, `yarn.lock`
   - **Python**: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`
   - **Rust**: `Cargo.toml`
   - **Go**: `go.mod`
   - **JVM**: `build.gradle`, `build.gradle.kts`, `pom.xml`
   - **.NET**: `*.csproj`, `*.sln`, `Directory.Build.props`
   - **Swift**: `Package.swift`, `*.xcodeproj`
   - **Flutter/Dart**: `pubspec.yaml`
   - **기타**: `Dockerfile`, `docker-compose.yml`, `Makefile`, `Procfile`, `wrangler.toml`, `vercel.json`, `netlify.toml`
3. **패키지 매니저 감지**: lock 파일 기반으로 `npm`/`yarn`/`pnpm`/`bun` 중 실제 사용 매니저를 판별하고, 명령어 예시에 반영합니다.
4. **기존 문서 확인**: `docs/`, `prd.md`, `prd.txt`, `CHANGELOG.md`, `CONTRIBUTING.md` 등 기존 문서가 있으면 참고합니다.
5. **라이선스 확인**: `LICENSE`, `LICENSE.md` 파일이 있으면 해당 라이선스를 사용합니다. 없으면 MIT를 기본값으로 합니다.
6. **작성자 정보 추출**: `package.json`의 `author`, `git config user.name`, 또는 기존 README에서 작성자 정보를 추출합니다. 확인 불가 시 `$ARGUMENTS`에서 받거나 placeholder로 남깁니다.
7. **모노레포 형제 프로젝트 README 참고**: 같은 모노레포 내 다른 프로젝트의 README가 있으면 스타일을 맞춥니다.

## 생성할 파일

### 1. `README.md` (한국어 - 메인)
### 2. `README_EN.md` (영어)
### 3. `README_ZH.md` (중국어 간체)

## README 필수 포함 섹션 (순서대로)

아래 섹션을 **반드시** 포함하되, 프로젝트 성격에 맞게 내용을 채워 넣으세요.

### 헤더 영역
```markdown
# {이모지} {프로젝트명} - {한줄 설명}

<div align="center">

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-{배포URL}-{색상코드}?style=for-the-badge)]({배포URL})
[![{프레임워크}](https://img.shields.io/badge/{프레임워크}-{버전}-{색상}?style=for-the-badge&logo={로고})]({URL})
... (기술 스택 배지들)

**{프로젝트 핵심 가치를 담은 한 줄 설명}** ✨

[🎯 주요 기능](#-주요-기능) | [💻 로컬 실행](#-로컬에서-실행하기) | [🚀 배포하기](#-배포하기)

</div>
```

### 본문 섹션 (순서 준수)

1. **🎯 프로젝트 소개**
   - 프로젝트가 무엇인지, 누구를 위한 것인지 흥미롭게 설명
   - `### ✨ 주요 기능` 서브섹션에 이모지 + 기능 리스트

2. **📸 스크린샷** (가능한 경우)
   - `docs/` 폴더에 스크린샷이 있으면 테이블로 배치
   - 없으면 placeholder 주석으로 안내

3. **🎮 사용 방법**
   - **반드시 mermaid `graph TD` 플로우차트** 포함 (사용자 여정)
   - `### 📝 단계별 가이드` 서브섹션
   - 테이블이나 번호 목록으로 구체적인 사용법 설명

4. **🏗️ 기술 스택**
   - `<div align="center">` 안에 테이블 (카테고리 | 기술 | 용도)
   - `### 🎨 아키텍처` 서브섹션에 **mermaid 다이어그램** (시스템 구조)

5. **📁 프로젝트 구조**
   - 트리 형태 + 각 파일/폴더에 이모지와 한줄 설명

6. **💻 로컬에서 실행하기**
   - `### 📋 사전 준비물` (런타임 버전, API 키 등 — 프로젝트에 맞게)
   - `### 🔧 환경 변수 설정` (.env 예시, 민감 정보는 placeholder)
   - `### 🚀 실행 방법` (git clone → cd → 의존성 설치 → 실행)
     - 감지된 패키지 매니저에 맞는 명령어 사용 (npm/yarn/pnpm/bun/pip/cargo 등)
   - `### ⚙️ 사용 가능한 명령어` (테이블)

7. **🚀 배포하기**
   - 프로젝트 설정 파일에서 배포 대상을 추론하여 해당 플랫폼 가이드 작성
   - `wrangler.toml` → Cloudflare Pages/Workers
   - `vercel.json` 또는 Next.js → Vercel
   - `netlify.toml` → Netlify
   - `Dockerfile` → Docker 기반 배포 (AWS ECS, GCP Cloud Run, Railway, Fly.io 등)
   - `Procfile` → Heroku
   - 추론 불가 시 프로젝트 성격에 맞는 일반적인 배포 가이드

8. **추가 기술 섹션** (해당하는 경우)
   - AI 모델 사용 시: 모델 설명 + API 문서 링크
   - 알고리즘이 핵심이면: 알고리즘 설명 + mermaid 다이어그램
   - 보안 설계가 중요하면: 보안 아키텍처 설명
   - DB 스키마가 중요하면: ERD 다이어그램
   - API 서버라면: 주요 엔드포인트 요약 테이블

9. **🎯 향후 개선 사항** (선택)
   - 체크리스트 형태로 TODO 항목

10. **🤝 기여하기**
    - Fork → Branch → Commit → Push → PR 가이드
    - `CONTRIBUTING.md`가 있으면 링크 안내

11. **📄 라이선스**
    - 프로젝트의 `LICENSE` 파일 기반. 없으면 MIT 기본값.

12. **👨‍💻 만든 사람**
    - 분석 단계에서 추출한 작성자 정보 사용
    - Issue 안내

13. **푸터**
    ```markdown
    <div align="center">

    **⭐ 이 프로젝트가 마음에 드셨다면 Star를 눌러주세요! ⭐**

    Made with ❤️ using {주요기술}

    [{이모지} 지금 사용하기]({배포URL})

    </div>
    ```

## 스타일 가이드

- **이모지 사용**: 헤더, 기능 목록, 섹션 제목에 적극 사용
- **mermaid 다이어그램**: 최소 2개 (사용자 플로우 + 아키텍처), 가능하면 3개 이상
- **mermaid 스타일링**: `style` 속성으로 노드에 색상 지정 (fill, color)
- **테이블 활용**: 기술 스택, 명령어, 환경 변수 등은 테이블로 정리
- **코드 블록**: 실행 명령어, 환경 변수, 데이터 모델 등에 사용
- **톤**: 친근하고 흥미진진하게, 기술 문서지만 읽는 재미가 있도록
- **배지**: shields.io 배지로 Live Demo + 주요 기술 스택 표시

### 언어별 규칙

| 파일 | 언어 규칙 |
|------|-----------|
| `README.md` | 한국어. 전문용어(API, Edge Runtime 등)는 영어 그대로 사용 |
| `README_EN.md` | 영어. 한국어 README와 동일한 구조, 자연스러운 영어로 작성 |
| `README_ZH.md` | 중국어 간체. 한국어 README와 동일한 구조, 자연스러운 중국어로 작성. 전문용어(API, Edge Runtime 등)는 영어 그대로 사용 |

### 언어 간 상호 링크

- **한국어 README** 최상단 배지 영역:
  ```markdown
  > 🇺🇸 [English](./README_EN.md) | 🇨🇳 [中文](./README_ZH.md)
  ```
- **영어 README** 최상단:
  ```markdown
  > 🇰🇷 [한국어](./README.md) | 🇨🇳 [中文](./README_ZH.md)
  ```
- **중국어 README** 최상단:
  ```markdown
  > 🇰🇷 [한국어](./README.md) | 🇺🇸 [English](./README_EN.md)
  ```

## 실행 규칙

1. 먼저 프로젝트 루트의 모든 설정 파일과 소스 구조를 읽으세요.
2. `docs/` 폴더에 PRD나 기획 문서가 있으면 반드시 참고하세요.
3. 상위 디렉토리(`../`)에 형제 프로젝트의 README가 있으면 스타일을 맞추세요.
4. 배포 URL은 아래 우선순위로 추론하세요:
   - 기존 README나 설정 파일에 명시된 URL
   - `package.json`의 `homepage` 필드
   - `vercel.json`, `wrangler.toml` 등 배포 설정에서 추론
   - 확실하지 않으면 `{your-project-url}` placeholder 사용
5. `LICENSE` 파일을 확인하고 실제 라이선스를 반영하세요.
6. README.md → README_EN.md → README_ZH.md 순서로 생성하세요.
7. 이미 README 파일이 존재하면 덮어쓰기 전에 사용자에게 확인하세요.
8. `$ARGUMENTS`에 추가 지시사항이 있으면 우선 반영하세요.
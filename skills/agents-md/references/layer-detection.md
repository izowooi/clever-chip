# 계층 판별 휴리스틱

Analyst와 메인 스레드(Phase 1.5)가 사용하는 L1/L2/L3/L4 자동 판별 규칙.

## 신호별 정의

### `.git` 존재 신호

- **자체**: `target_path/.git`가 디렉토리
- **상위**: 상위 경로를 거슬러 올라 발견되는 git root, 거리 N단계 기록
- **부재**: 자체도 상위도 미발견

### 자식 git 저장소 수

- `target_path`의 직속 자식 디렉토리 중 `.git`를 가진 폴더 개수
- 2개 이상 → workspace 후보 신호 (L1/L2)

### 모노레포 신호 (최소 2개 충족)

1. 자식 디렉토리 중 자체 package 파일을 가진 폴더 ≥2개
2. 루트에 workspace 정의 파일 존재:
   - `pnpm-workspace.yaml`
   - `lerna.json`
   - `nx.json`
   - `turbo.json`
   - `pyproject.toml`의 path 의존성 다수
   - `Cargo.toml`의 `[workspace]` 섹션
   - `go.work`
3. 루트에 `apps/`, `packages/`, `services/` 같은 다중 프로젝트 컨벤션 디렉토리 + 그 아래 ≥2개 프로젝트
4. `.git submodule` 정의 다수

### 단일 프로젝트 신호

- package 파일 1개만 루트에 존재
- `src/` 같은 단일 entrypoint 폴더
- README가 프로젝트 단위 (저장소 단위 아님)

### 부모 AGENTS.md 신호

- 상위 경로에 AGENTS.md 발견 → 현재 위치는 자식 계층 (L1 부모 → L2 또는 L3 자식, L3 부모 → L4 자식)

## 계층별 판단 기준

### L1 신호

- **강한 신호**:
  - `target_path`가 사용자 홈 직속 또는 `~/git`, `~/dev`, `~/workspace` 같은 통상 dev root
  - `.git` 미존재 (자체)
  - 자식 git 저장소 수 ≥3개
- **약한 신호**:
  - `target_path` 이름이 `git`, `dev`, `code`, `workspace` 등
  - 부모 AGENTS.md 없음

### L2 신호

- **강한 신호**:
  - L1과 동일한 신호 + 사용자가 명시적으로 "workspace 규칙·인덱싱·REPOS.md"를 언급
  - 또는 L1과 같은 경로지만 사용자가 "L2만 분리"를 명시
- **모호 케이스**: L1과 동일 경로 — 합본 옵션 제공

### L3 신호

- **강한 신호**:
  - `target_path/.git` 존재 (대상 자체가 git root)
  - 부모 AGENTS.md 없음 또는 부모는 L1/L2
- **모노레포 L3**: 모노레포 신호 ≥2개 충족
- **단일 프로젝트 L3 (=최하위)**: 모노레포 신호 0~1개, 자식 폴더에 package 파일 1개씩만

비모노레포 단일 프로젝트 저장소는 L3가 최하위 — Writer가 L4 수준의 실행/테스트/빌드/배포 명령까지 포함.

### L4 신호

- **강한 신호**:
  - 상위 경로에 `.git` 존재 (대상은 git root가 아님)
  - 상위 경로에 부모 AGENTS.md 존재 (L3 또는 L2)
  - `target_path`에 package 파일 1개 + scripts/entrypoint 존재
  - 같은 부모 디렉토리에 형제 프로젝트 폴더가 있음

## 모호 케이스 처리

### L1 vs L2 (같은 경로)

같은 물리 경로에서 둘 다 가능. 사용자에게 AskUserQuestion으로 선택:
- A. L1 단독 (개발 철학만)
- B. L2 단독 (저장소 인덱싱만)
- C. L1+L2 합본 (한 파일에 둘 다)

### L3 vs L4 (애매한 폴더)

대상이 git root는 아니지만 package 파일이 여럿 있어 마치 L3처럼 보이는 경우 — 보통 L3 안의 sub-monorepo. 사용자에게 확인.

### L3 단일 프로젝트 vs L4

대상이 git root이면 무조건 L3 (단일 프로젝트면 L3가 최하위 — L4로 분류 안 함). L4는 git root가 아닌 서브 폴더에만 적용.

## 신뢰도 평가

Analyst 리포트에 `confidence` 표시:
- **high**: 강한 신호 ≥2개 모두 충족 + 모호 케이스 아님
- **medium**: 강한 신호 1~2개 충족, 약한 신호로 보완
- **low**: 모호 케이스 또는 강한 신호 충돌

신뢰도 low면 Phase 1.5에서 무조건 사용자 확인.

## 사용자 override

사용자가 자연어 호출에서 명시적으로 계층을 언급한 경우(`/agents-md L3 ~/git/build_ops`) 자동 판별 결과와 비교:
- 일치: 그대로 진행
- 불일치: AskUserQuestion으로 둘 다 제시하고 사용자 선택

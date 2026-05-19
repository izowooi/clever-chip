---
name: agents-md
description: AGENTS.md 또는 REPOS.md 파일을 L1/L2/L3/L4 계층에 맞게 생성·개선한다. 인터뷰 기반(한 번에 하나씩 + 추천 답변 + 출처)으로 사용자 정책을 수집하고 코드베이스를 분석해 한국어 본문 + 영문 기술 용어로 작성한다. 다음 상황에 반드시 사용 — "AGENTS.md 만들어줘 / 작성 / 생성 / 업데이트 / 개선 / 리뷰 / 수정", "L1/L2/L3/L4 AGENTS.md", "이 프로젝트 AGENTS.md", "REPOS.md 만들어줘", "에이전트 가이드 문서 작성", "/agents-md [경로]".
---

# AGENTS.md 빌더 (L1~L4 디스패처)

이 스킬은 사용자가 정의한 L1~L4 계층(가이드: `docs/AGENTS_MD_L1_L4_Guide.md`)에 맞춰 AGENTS.md를 자동 판별하고, 인터뷰·분석·작성·검토를 거쳐 안전하게 디스크에 저장한다.

## 트리거 시점

다음 중 하나라도 해당하면 이 스킬을 사용한다:
- 사용자가 AGENTS.md 또는 REPOS.md 작성/개선/업데이트를 명시적으로 요청
- 사용자가 `/agents-md [경로]` 슬래시 명령으로 호출
- 새 프로젝트 셋업 시 "이 프로젝트에 에이전트 가이드 문서 추가" 요청
- 기존 AGENTS.md에 대해 "이 부분 개선해줘" 요청 (improvement-mode)

다음은 트리거하지 않는다:
- 단순히 AGENTS.md 내용을 읽거나 보여달라는 요청 (Read 도구 직접)
- "agents" 디렉토리 생성 같은 무관 요청
- 디렉토리 구조 설명 같은 질의응답

## 계층 개요

| 계층 | 위치 예시 | 목적 |
|---|---|---|
| L1 | `/Users/{user}/git/AGENTS.md` 또는 더 위 | 사용자 전체 개발 철학·안전 규칙 |
| L2 | 저장소 모음 폴더 | 저장소 인덱싱·workspace 운영 |
| L3 | git 저장소 루트 | 저장소 구조·서브폴더 인덱싱 (모노레포면 인덱싱만, 비모노레포면 실행 명령까지) |
| L4 | 모노레포 안의 서브 프로젝트 | 실행·테스트·빌드·배포 등 운영 디테일 |

L1↔L2 합본 운영 가능 — 같은 물리 경로에 둘 다 두는 경우 인터뷰에서 사용자 확인.

---

## 워크플로우 (Phase 단위)

### Phase 0 — 컨텍스트 확인

1. 인자 파싱
   - 슬래시 호출: `/agents-md [경로]` — 경로 생략 시 현재 작업 디렉토리
   - 자연어 호출: 메시지에서 경로 추론, 모호하면 사용자에게 확인 (AskUserQuestion)
   - 옵션: 사용자가 명시적으로 `L1` `L2` `L3` `L4`를 언급하면 Phase 1 자동 판별 결과의 사전 후보로 기록 (단, 자동 판별과 충돌 시 사용자에게 확인)

2. 기존 AGENTS.md 존재 여부 확인
   - 존재: `mode = improve` — Phase 0.5로 분기
   - 미존재: `mode = create` — Phase 1로 진행

3. 워크스페이스 디렉토리 생성
   ```bash
   # 슬러그 = target 경로의 마지막 디렉토리명 (공백·특수문자는 -)
   mkdir -p ~/.claude/_workspace/agents-md/{YYYY-MM-DD_HHMM}_{slug}
   ```
   이 경로를 `workspace_dir`로 이후 단계에 전달.

4. 사용자에게 시작 알림 (한 줄): `"AGENTS.md 빌더를 시작합니다. 대상: {경로}, 모드: {create|improve}."`

### Phase 0.5 — improve 모드 진입 (해당 시)

`references/improvement-mode.md` 로딩 후 그 흐름을 따른다.

핵심:
1. 기존 AGENTS.md 읽고 섹션별 파싱
2. 사용자에게 plain text 질문: "AI 작업 중 마음에 들지 않았던 행동이 있나요? 또는 추가/수정하고 싶은 규칙이 있나요?"
3. 답변을 기반으로 어느 섹션을 어떻게 고칠지 제안 → Writer는 diff 단위 변경만
4. 사용자가 "전체 새로 작성"을 명시적으로 요청하면 `mode = create`로 전환하고 백업 표시 ON

### Phase 1 — 분석

`references/layer-detection.md` 로딩.

**Agent 호출 (model: opus):**
```
Agent(
  subagent_type: "general-purpose",
  description: "AGENTS.md analyst scan",
  model: "opus",
  prompt: <agents-md-analyst.md의 입력 형식에 맞춰 target_path, mode, workspace_dir 전달>
)
```

에이전트 정의는 `~/.claude/agents/agents-md-analyst.md` 참조. 호출 시 prompt 본문에 "너는 ~/.claude/agents/agents-md-analyst.md에 정의된 에이전트다. 해당 파일을 먼저 읽고 명세에 따라 동작하라" 명시.

산출물: `{workspace_dir}/01_analyst_report.md`.

### Phase 1.5 — 계층 확인

Analyst 리포트의 계층 후보(1순위 + 신뢰도)를 사용자에게 AskUserQuestion으로 확인.

```
질문: "분석 결과 이 경로는 {L?}로 판단됩니다. 근거: {짧은 요약}. 계속 진행할까요?"
옵션:
  A. L? (자동 판별 결과 — 추천)
  B. {2순위 또는 다른 계층} (override)
  C. L1+L2 합본 (모호 케이스에서만)
```

확정된 계층을 `layer`로 이후 단계에 사용. L1+L2 합본을 선택하면 Writer가 두 계층 내용을 단일 파일로 통합 작성.

### Phase 2 — 계층별 references 로딩

확정된 계층의 references 파일만 읽는다 (progressive disclosure):
- L1 → `references/l1.md`
- L2 → `references/l2.md`
- L3 → `references/l3.md`
- L4 → `references/l4.md`
- L1+L2 합본 → 두 파일 모두

references 파일에는 해당 계층의 인터뷰 질문 목록, 추천 답변 출처 규칙, 템플릿 경로가 정의되어 있다.

### Phase 3 — 인터뷰

메인 스레드에서 references에 정의된 질문을 **한 번에 하나씩** 진행.

**각 질문마다 다음 형식 출력:**

```markdown
## 질문 N — {항목명}

{질문 본문}

### 추천 답변

{한 줄 또는 짧은 문단}

### 출처

{코드 / 가이드 / LLM} — {구체적 근거: package.json scripts.test, 가이드 N행, 일반 권장}

### 왜 이걸 추천하는가

{짧은 설명}

### 선택지

A. {보수적 또는 추천 옵션}
B. {균형}
C. {적극적}
```

**도구 선택:**
- 정형 질문 (자율성 수준, push 정책, 모노레포 여부, 응답 스타일 등) → AskUserQuestion (A/B/C 또는 Yes/No 선택지)
- 자유 서술 질문 (프로젝트 목적, 위험 영역, 자주 깨지는 부분) → plain text 출력 후 사용자 응답 대기

**추천 답변 우선순위 (가이드 + Analyst 기반):**
1. Analyst가 코드에서 직접 확인한 사실 (예: `scripts.test`의 실제값) — 출처: "코드"
2. 가이드 문서의 권장 기본값 (예: 자율성 수준 균형 모드) — 출처: "가이드"
3. LLM 일반 판단 — 출처: "LLM"

답변을 받을 때마다 `{workspace_dir}/02_interview_answers.md`에 누적 저장 (Q/A 쌍 + 출처).

**모든 질문이 끝나면** 사용자에게 짧게 알림: "인터뷰 완료. 작성 단계로 넘어갑니다."

### Phase 4 — 작성 (라운드 1)

**Agent 호출:**
```
Agent(
  subagent_type: "general-purpose",
  description: "AGENTS.md writer draft v1",
  model: "opus",
  prompt: <agents-md-writer.md의 입력 형식에 맞춰 workspace_dir, analyst_report_path, interview_answers_path, layer, template_path, round=1 전달>
)
```

산출물: `{workspace_dir}/03_writer_draft_v1.md`.

사용자에게 한 줄 알림: "초안 작성 완료. 검토 단계로 넘어갑니다."

### Phase 5 — 검토 자동 루프 (최대 2회)

**라운드 1:**
```
Agent(
  subagent_type: "general-purpose",
  description: "AGENTS.md reviewer round 1",
  model: "opus",
  prompt: <draft_path=v1, target_code_path, analyst_report_path, layer, round=1 전달>
)
```

산출물: `{workspace_dir}/04_reviewer_report_v1.md`.

리포트의 "라운드 결정" 섹션 확인:
- **통과**: Phase 6으로 진행
- **Writer 재호출 필요**: 라운드 2로

**라운드 2 (필요 시):**

사용자에게 알림: "1차 검토에서 {N}건 발견, 자동 재작성 중..."

```
Agent(
  subagent_type: "general-purpose",
  description: "AGENTS.md writer draft v2",
  model: "opus",
  prompt: <round=2, prev_review_path=04_reviewer_report_v1.md 추가>
)
```

산출물: `03_writer_draft_v2.md`.

```
Agent(
  subagent_type: "general-purpose",
  description: "AGENTS.md reviewer round 2",
  model: "opus",
  prompt: <draft_path=v2, round=2, 라운드 1 리포트도 입력에 포함>
)
```

산출물: `04_reviewer_report_v2.md`.

라운드 2 결과에 상관없이 Phase 6으로 진행 (자동 루프 강제 종료).

**최종 draft 결정:**
- 마지막 라운드의 draft를 `final_draft_path`로 결정
- (선택) `cp` 또는 심볼릭 링크로 `03_writer_draft_final.md` 별칭 생성 — 디버깅 편의용

### Phase 6 — 승인 및 출력

사용자에게 다음을 한 화면에 노출:

1. **최종 draft 본문** (전체 마크다운)
2. **최종 Reviewer 리포트** (라운드 1만 또는 라운드 1+2 요약)
3. **AskUserQuestion**:
   ```
   질문: "이대로 저장할까요?"
   옵션:
     A. 저장 (추천)
     B. 수정 요청 (추가 인터뷰 후 Writer 재호출, 수동 루프)
     C. 취소 (워크스페이스만 보존, 최종 파일 변경 없음)
   ```

**A. 저장 선택 시:**
```bash
# 기존 파일 백업 (있다면)
[ -f {target_path}/AGENTS.md ] && cp {target_path}/AGENTS.md {target_path}/AGENTS.md.bak.{YYYY-MM-DD_HHMM}

# 최종 draft 이동
cp {final_draft_path} {target_path}/AGENTS.md
```

L2이고 사용자가 REPOS.md 생성도 동의했다면 같은 절차로 `{target_path}/REPOS.md`도 함께 출력.

**B. 수정 요청 선택 시:**
- 사용자에게 plain text: "어떤 부분을 수정할까요?" → 답변 받음
- 추가 답변을 `02_interview_answers.md`에 추가 누적
- Writer를 새 라운드 번호로 재호출 (자동 루프 카운트 리셋, 라운드 번호는 계속 증가 v3, v4...)
- 새 draft → Reviewer 라운드 1만 실행 → Phase 6 재진입

**C. 취소 선택 시:**
- 워크스페이스는 보존
- 사용자에게 알림: "취소되었습니다. 워크스페이스: {workspace_dir}"

### Phase 7 — 후속 가이드

저장 완료 후 사용자에게 다음 안내 (짧게):
- 저장 경로: `{target_path}/AGENTS.md` (백업: `.bak.{timestamp}`)
- 워크스페이스: `{workspace_dir}` (감사 추적용 보존)
- 이 파일은 글로벌 정책 문서이므로 `git commit` 전 한 번 더 검토 권장
- 자동 커밋은 사용자 CLAUDE.md 정책에 위임 — 스킬은 파일 생성/이동까지만 수행

---

## 데이터 흐름

```
사용자 호출
  ↓
Phase 0 (컨텍스트, mode 결정, workspace 생성)
  ↓
Phase 1 (Analyst Agent) → 01_analyst_report.md
  ↓
Phase 1.5 (계층 확인 AskUserQuestion)
  ↓
Phase 2 (계층별 references 로딩)
  ↓
Phase 3 (인터뷰 반복) → 02_interview_answers.md
  ↓
Phase 4 (Writer Agent v1) → 03_writer_draft_v1.md
  ↓
Phase 5 (Reviewer Agent v1) → 04_reviewer_report_v1.md
  ↓
{수정 필요 ≥1?}
  → Yes: Writer v2 → Reviewer v2
  → No: 종료
  ↓
Phase 6 (사용자 승인)
  ↓
{A. 저장 / B. 수정 / C. 취소}
  ↓
Phase 7 (후속 가이드)
```

데이터 전달은 **파일 기반**. 에이전트 호출 시 큰 마크다운을 prompt에 넣지 않고, 워크스페이스 파일 경로만 전달한다.

---

## 에러·엣지 케이스

- **계층 모호 (L1↔L2)**: 자동 판별 신뢰도 low → Phase 1.5에서 AskUserQuestion으로 명시 선택, 합본 옵션 제공
- **부모 AGENTS.md 미존재**: L3·L4 작업 시 부모 없으면 Analyst가 "부모 없음 — 모든 규칙 명시 필요" 플래그 → Writer가 그에 따라 작성
- **자동 루프 후 잔존 이슈**: 라운드 2 종료 후 Reviewer가 여전히 "수정 필요" 표시해도 강제 종료, 사용자에게 그대로 노출
- **사용자 취소**: 워크스페이스 보존, 최종 파일 변경 없음
- **워크스페이스 디스크 부족**: Phase 0에서 `df` 확인 (선택), 실패 시 사용자에게 정리 권장
- **민감 파일 처리**: Analyst가 존재만 보고, Writer는 절대 내용 출력 안 함, Reviewer는 출력 시 차단
- **자동 커밋 충돌**: 스킬은 `git add` / `git commit` 직접 호출하지 않음 — CLAUDE.md 정책에 위임

---

## 호출 시 사용할 에이전트 정의

- `~/.claude/agents/agents-md-analyst.md` (Phase 1)
- `~/.claude/agents/agents-md-writer.md` (Phase 4, 5 라운드 2, Phase 6 수정 요청)
- `~/.claude/agents/agents-md-reviewer.md` (Phase 5)

모든 Agent 호출에 `model: "opus"` 명시.

## references 인덱스

- `references/layer-detection.md` — 계층 판별 휴리스틱
- `references/l1.md` — L1 워크플로우·질문
- `references/l2.md` — L2 워크플로우·질문 + REPOS.md 옵션
- `references/l3.md` — L3 워크플로우·질문 (모노레포/비모노레포 분기)
- `references/l4.md` — L4 워크플로우·질문
- `references/improvement-mode.md` — 기존 파일 개선 흐름
- `references/templates/l1-template.md`
- `references/templates/l2-template.md`
- `references/templates/l3-template.md`
- `references/templates/l4-template.md`
- `references/templates/repos-template.md`

## 테스트 시나리오

### 정상 흐름 (L4 새 프로젝트)
1. 사용자: "이 프로젝트에 AGENTS.md 만들어줘" (Python 프로젝트 디렉토리에서)
2. Phase 0: mode=create, workspace 생성
3. Phase 1: Analyst가 `pyproject.toml` 발견, `pytest` 명령 추출, 부모 L3 AGENTS.md 발견
4. Phase 1.5: "L4로 판단됩니다 (근거: 부모 L3 존재, 단일 프로젝트)" — 사용자 A 선택
5. Phase 2: `references/l4.md` 로딩
6. Phase 3: 4개 질문 진행 (목적·외부 API·자주 깨지는 부분·README 외 관례)
7. Phase 4: Writer가 템플릿 기반 draft 작성
8. Phase 5: Reviewer 라운드 1 통과
9. Phase 6: 사용자 A 선택 → 저장
10. Phase 7: 완료 알림

### 에러 흐름 (Reviewer 2회 잔존)
1. Phase 5 라운드 1: Reviewer가 "명령어 미존재 1건, TODO 6개" → 수정 필요
2. Writer 라운드 2: 명령어 보정 시도, TODO는 정보 부족으로 그대로
3. Reviewer 라운드 2: 명령어는 통과, TODO 6개 잔존 → 수정 필요지만 강제 종료
4. Phase 6: 사용자에게 "TODO가 많아 인터뷰가 더 필요할 수 있습니다" 안내와 함께 draft 노출
5. 사용자가 B. 수정 요청 선택 → 추가 인터뷰 → Writer v3 → Reviewer 다시 → Phase 6 재진입

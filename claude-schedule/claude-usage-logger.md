---
name: claude-usage-logger
description: Claude 사용량을 브라우저(claude.ai)와 CLI(/usage)로 확인하여 텍스트 로그에 기록
---

## 목적
Claude의 주간 한도 사용량을 브라우저로 확인하고, 결과를 텍스트 로그 파일에 append 형태로 기록한다.

## 실행 순서

### Step 1: 브라우저 탭 준비
1. `tabs_context_mcp`로 현재 탭 그룹을 확인한다. 탭이 없으면 `createIfEmpty: true`로 생성한다.
2. 사용 가능한 탭 ID를 확보한다.

### Step 2: claude.ai 사용량 페이지 접속
1. 탭에서 `https://claude.ai/settings/usage` 로 navigate 한다.
2. 2초 대기 후 `get_page_text`로 페이지 텍스트를 읽는다.
3. 페이지 텍스트에서 **주간 한도** 정보만 파싱한다:
   - 주간 한도 사용 퍼센트 (예: "45% 사용됨")
   - 재설정 시점 (예: "(월) 오후 2:00에 재설정")
   - 마지막 업데이트 시각
4. 현재 세션 한도는 무시한다. 주간 한도만 기록한다.
5. 만약 로그인이 안 되어 있거나 페이지 로드 실패 시, 에러를 기록한다.

### Step 3: 로그 파일에 기록
1. 로그 파일 경로: `~/claude/claude-usage-logger/outputs/claude-usage-log.txt` (현재 작업 디렉토리의 outputs/claude-usage-log.txt )
2. bash 명령어로 현재 시각(KST)을 구하고, 다음 형식으로 append 한다:

```
[YYYY-MM-DD HH:MM KST] 주간 한도: XX% 사용됨 (재설정: X요일 오후 X:XX)
```

3. bash의 `echo >> file` 방식으로 append 한다.
4. 파일이 존재하지 않으면 새로 생성한다.

### Step 4: 완료 확인
- 로그 파일의 마지막 줄을 읽어서 기록이 정상적으로 추가되었는지 확인한다.

## 주의사항
- CLI의 `/usage` 명령은 interactive 전용이므로 사용하지 않는다.
- 현재 세션 한도는 기록하지 않는다. 주간 한도만 기록한다.
- 타임존은 KST(Asia/Seoul, UTC+9)를 사용한다.
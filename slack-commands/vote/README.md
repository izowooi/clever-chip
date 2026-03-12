# Slack 투표 봇

Slack에서 `/투표` 또는 `/vote` 명령어로 투표를 생성하는 봇입니다.

## 기능

- 쉼표로 구분된 선택지를 버튼으로 표시
- 여러 개 선택 가능 (다중 투표)
- 누가 투표했는지 @mention으로 표시
- 같은 버튼 다시 클릭 시 투표 취소

## 사용법

```
/투표 옵션1, 옵션2, 옵션3
```

예시:
```
/투표 짜장면, 짬뽕, 탕수육
/투표 월요일, 화요일, 수요일
/vote apple, banana, melon
```

---

## 배포 가이드

### 1. 사전 준비

- [Firebase CLI](https://firebase.google.com/docs/cli) 설치
- Firebase 프로젝트 생성
- Python 3.12 이상

### 2. Firebase 프로젝트 설정

```bash
# Firebase CLI 로그인
firebase login

# 프로젝트 디렉토리로 이동
cd slack-commands/vote

# .firebaserc 파일에서 프로젝트 ID 수정
# "default": "YOUR_PROJECT_ID" → 실제 프로젝트 ID로 변경
```

### 3. 환경 변수 설정

Slack App에서 다음 값을 가져와 Firebase Secrets에 저장:

```bash
# Slack App > Basic Information > App Credentials > Signing Secret
firebase functions:secrets:set SLACK_SIGNING_SECRET

# Slack App > OAuth & Permissions > Bot User OAuth Token (xoxb-로 시작)
firebase functions:secrets:set SLACK_BOT_TOKEN
```

### 4. 배포

```bash
# Functions 배포
firebase deploy --only functions
```

배포 완료 후 출력되는 URL 확인:
```
✔ functions[slack_vote(asia-northeast3)]: https://asia-northeast3-YOUR_PROJECT_ID.cloudfunctions.net/slack_vote
✔ functions[slack_vote_interactive(asia-northeast3)]: https://asia-northeast3-YOUR_PROJECT_ID.cloudfunctions.net/slack_vote_interactive
```

---

## Slack App 설정 가이드

### 1. Slash Commands 설정

[Slack API](https://api.slack.com/apps) > 앱 선택 > **Slash Commands**

**기존 `/투표` 커맨드 수정:**
- Command: `/투표`
- Request URL: `https://asia-northeast3-YOUR_PROJECT_ID.cloudfunctions.net/slack_vote`
- Short Description: 투표 생성
- Usage Hint: `옵션1, 옵션2, 옵션3`

**`/vote` 커맨드 추가 (선택):**
- Command: `/vote`
- Request URL: `https://asia-northeast3-YOUR_PROJECT_ID.cloudfunctions.net/slack_vote`
- Short Description: Create vote
- Usage Hint: `option1, option2, option3`

### 2. Interactivity 설정 (필수!)

[Slack API](https://api.slack.com/apps) > 앱 선택 > **Interactivity & Shortcuts**

1. **Interactivity** 토글 → **ON**
2. **Request URL** 입력:
   ```
   https://asia-northeast3-YOUR_PROJECT_ID.cloudfunctions.net/slack_vote_interactive
   ```
3. **Save Changes** 클릭

### 3. OAuth Scopes 확인

[Slack API](https://api.slack.com/apps) > 앱 선택 > **OAuth & Permissions**

**Bot Token Scopes**에 다음이 있는지 확인:
- `chat:write` - 메시지 전송/수정 (필수)
- `commands` - 슬래시 커맨드 (필수)

없으면 **Add an OAuth Scope** 클릭하여 추가 후 앱 재설치

### 4. 앱 재설치 (권한 변경 시)

권한을 변경했다면:
1. **OAuth & Permissions** > **Reinstall to Workspace** 클릭
2. 권한 승인

---

## 테스트 가이드

### 1. 테스트 채널 준비

1. Slack에서 테스트용 채널 생성 (예: `#test-vote`)
2. 봇을 채널에 초대:
   ```
   /invite @vote bot
   ```
   또는 채널 설정 > 통합 > 앱 추가

### 2. 기본 기능 테스트

#### 테스트 1: 투표 생성
```
/투표 사과, 바나나, 멜론
```

**예상 결과:**
- 3개의 버튼이 있는 투표 메시지 표시
- 각 버튼에 "투표 (0)" 표시
- "아직 투표 없음" 텍스트 표시

#### 테스트 2: 투표하기
1. "사과" 버튼 클릭

**예상 결과:**
- 버튼이 "투표 (1)"로 변경
- 자신의 이름이 @mention으로 표시

#### 테스트 3: 투표 취소
1. 같은 "사과" 버튼 다시 클릭

**예상 결과:**
- 버튼이 "투표 (0)"로 변경
- 자신의 이름이 사라짐
- "아직 투표 없음"으로 복귀

#### 테스트 4: 복수 투표
1. "사과" 버튼 클릭
2. "바나나" 버튼 클릭

**예상 결과:**
- 두 항목 모두에 자신의 이름 표시
- 각각 "투표 (1)"로 표시

#### 테스트 5: 여러 사용자 투표
1. 다른 팀원에게 같은 투표에 참여 요청
2. 같은 항목 또는 다른 항목 클릭

**예상 결과:**
- 투표한 모든 사용자의 이름이 @mention으로 표시
- 투표 수가 정확히 증가

### 3. 에러 케이스 테스트

#### 테스트 6: 옵션 없이 입력
```
/투표
```

**예상 결과:**
- 에러 메시지: "사용법: `/투표 옵션1, 옵션2, 옵션3`"

#### 테스트 7: 옵션 1개만 입력
```
/투표 사과
```

**예상 결과:**
- 에러 메시지: "최소 2개 이상의 옵션이 필요합니다"

#### 테스트 8: 옵션 11개 이상 입력
```
/투표 1,2,3,4,5,6,7,8,9,10,11
```

**예상 결과:**
- 에러 메시지: "최대 10개까지 옵션을 입력할 수 있습니다"

### 4. 문제 해결

#### 봇이 응답하지 않는 경우

1. **Firebase Functions 로그 확인:**
   ```bash
   firebase functions:log --only slack_vote
   firebase functions:log --only slack_vote_interactive
   ```

2. **Slack App 설정 확인:**
   - Request URL이 정확한지 확인
   - Interactivity가 ON인지 확인

3. **권한 확인:**
   - `chat:write` 권한이 있는지 확인
   - 봇이 채널에 초대되어 있는지 확인

#### 버튼 클릭 후 업데이트 안 되는 경우

1. **Interactivity URL 확인:**
   - `slack_vote_interactive` 함수 URL이 설정되어 있는지 확인

2. **SLACK_BOT_TOKEN 확인:**
   ```bash
   firebase functions:secrets:access SLACK_BOT_TOKEN
   ```
   - `xoxb-`로 시작하는 올바른 토큰인지 확인

---

## 프로젝트 구조

```
vote/
├── functions/
│   ├── main.py              # Firebase Functions 진입점
│   ├── vote_service.py      # 투표 로직
│   ├── slack_utils.py       # Slack 유틸리티
│   └── requirements.txt     # Python 의존성
├── firebase.json            # Firebase 설정
├── .firebaserc              # 프로젝트 연결
├── .gitignore               # Git 제외 파일
└── README.md                # 이 파일
```

---

## 제한 사항

- 최대 10개 옵션
- 옵션당 최대 약 150명 투표 가능 (Slack 버튼 value 2000자 제한)
- 서버 재시작 시에도 투표 데이터 유지 (메시지 자체에 저장)

---

## 라이선스

Internal Use Only

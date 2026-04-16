# 🚀 비개발자를 위한 바이브코딩 핵심 개념 가이드 - Part 2

> **Part 1**에서 프론트엔드/백엔드, API, 에러, 프레임워크/라이브러리, 데이터베이스를 배웠습니다.  
> **Part 2**에서는 실제 서비스 런칭에 필요한 Storage, 인증, Git/GitHub, 배포를 다룹니다.

---

## 📚 목차

6. [Storage (파일 저장소)](#6-storage-파일-저장소)
7. [인증 (Authentication)](#7-인증-authentication)
8. [Git & GitHub (형상관리)](#8-git--github-형상관리)
9. [배포 (Deployment)](#9-배포-deployment)

---

## 6. Storage (파일 저장소)

### 📦 비유: 창고 vs 서류 캐비닛

```
Database = 서류 캐비닛 (정리된 문서, 폼 형식)
Storage = 창고 (박스, 가구, 자전거... 뭐든 보관)
```

```mermaid
flowchart LR
    subgraph Database["🗄️ Database"]
        D1["이름: 홍길동"]
        D2["나이: 25"]
        D3["이메일: hong@..."]
    end
    
    subgraph Storage["📦 Storage"]
        S1["🖼️ 프로필사진.jpg"]
        S2["🎬 영상.mp4"]
        S3["📄 계약서.pdf"]
    end
    
    APP["🖥️ 내 앱"] --> Database
    APP --> Storage
```

### Database vs Storage

| 구분 | Database | Storage |
|------|----------|---------|
| 저장 대상 | 정형화된 데이터 (텍스트, 숫자) | 비정형화된 파일 (이미지, 영상, 문서) |
| 예시 | 유저 이름, 가격, 날짜 | 프로필 사진, 첨부파일, 동영상 |
| 조회 방법 | SQL 쿼리 | URL 링크 |
| 비유 | 엑셀 표 | 구글 드라이브 |

### Storage에 저장하는 것들

```mermaid
flowchart TB
    STORAGE["📦 Storage"]
    
    STORAGE --> IMG["🖼️ 이미지<br/>프로필, 썸네일, 배너"]
    STORAGE --> VIDEO["🎬 동영상<br/>강의, 광고, UGC"]
    STORAGE --> DOC["📄 문서<br/>PDF, 엑셀, 계약서"]
    STORAGE --> AUDIO["🎵 오디오<br/>음악, 팟캐스트, 음성"]
    STORAGE --> ETC["📁 기타<br/>ZIP, 백업 파일"]
```

---

### ☁️ Cloudflare R2

**"AWS S3보다 저렴한 클라우드 저장소"**

Cloudflare가 만든 오브젝트 스토리지입니다. AWS S3와 호환되면서 **전송 비용(Egress)이 무료**입니다.

```mermaid
flowchart LR
    subgraph R2["☁️ Cloudflare R2"]
        B1["📁 Bucket: my-app-images"]
        B2["📁 Bucket: my-app-videos"]
    end
    
    APP["🖥️ 내 앱"] -->|"업로드"| R2
    R2 -->|"다운로드 (무료!)"| USER["👤 사용자"]
```

#### R2 핵심 개념

| 용어 | 설명 | 비유 |
|------|------|------|
| **Bucket** | 파일을 담는 최상위 폴더 | 창고 하나 |
| **Object** | 저장된 개별 파일 | 창고 안의 물건 |
| **Key** | 파일의 경로/이름 | 물건의 위치 라벨 |

#### R2 파일 구조 예시

```
my-app-bucket/                    ← Bucket (창고)
├── profiles/                     ← 폴더
│   ├── user_001.jpg             ← Object (파일)
│   └── user_002.jpg
├── posts/
│   ├── post_001/
│   │   ├── thumbnail.jpg
│   │   └── video.mp4
│   └── post_002/
│       └── image.png
└── documents/
    └── terms.pdf
```

#### R2 사용 흐름

```mermaid
sequenceDiagram
    participant User as 👤 사용자
    participant App as 🖥️ 앱
    participant R2 as ☁️ R2
    
    User->>App: 프로필 사진 선택
    App->>R2: 파일 업로드 요청
    R2-->>App: 저장 완료! URL 반환
    App->>App: DB에 URL 저장
    App-->>User: 업로드 완료!
    
    Note over User,R2: 나중에 이미지 볼 때
    
    User->>App: 프로필 페이지 접속
    App->>App: DB에서 URL 조회
    App-->>User: 이미지 URL 전달
    User->>R2: 이미지 직접 로드
```

#### Cloudflare R2 설정하기

**1단계: Cloudflare 대시보드 접속**
- [dash.cloudflare.com](https://dash.cloudflare.com) 접속
- 좌측 메뉴에서 **R2 Object Storage** 클릭

**2단계: Bucket 생성**
```
Bucket 이름: my-app-storage
위치: APAC (아시아 태평양) 선택
```

**3단계: API 토큰 생성**
- R2 → Manage R2 API Tokens
- Create API Token 클릭
- 권한: Object Read & Write

**4단계: 앱에서 사용**
```javascript
// 환경변수 설정 필요
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=my-app-storage
R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
```

---

### 🔥 Firebase Storage

**"Firebase 생태계와 완벽 통합된 저장소"**

Firebase 프로젝트 안에서 파일을 쉽게 저장하고 관리할 수 있습니다.

```mermaid
flowchart TB
    subgraph Firebase["🔥 Firebase"]
        AUTH["🔐 Auth"]
        DB["🗄️ Realtime DB"]
        STORAGE["📦 Storage"]
    end
    
    APP["📱 내 앱"] --> Firebase
    
    AUTH -.->|"인증된 유저만<br/>업로드 허용"| STORAGE
    DB -.->|"파일 URL 저장"| STORAGE
```

#### Firebase Storage 특징

| 특징 | 설명 |
|------|------|
| **Firebase Auth 연동** | 로그인한 유저만 업로드 가능하게 설정 |
| **보안 규칙** | 누가 어떤 파일에 접근 가능한지 세밀하게 제어 |
| **자동 CDN** | 전 세계 어디서든 빠른 다운로드 |
| **간편한 SDK** | 웹, Android, iOS 모두 쉽게 연동 |

#### Firebase Storage 경로 구조

```
gs://my-app.appspot.com/          ← Storage 루트
├── users/
│   ├── uid_001/
│   │   └── profile.jpg           ← 유저별 프로필
│   └── uid_002/
│       └── profile.jpg
├── posts/
│   └── post_001/
│       ├── image_1.jpg
│       └── image_2.jpg
└── public/
    └── banner.jpg                ← 누구나 접근 가능
```

#### Firebase Storage 보안 규칙 예시

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // 유저 본인 폴더만 읽기/쓰기 가능
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null 
                         && request.auth.uid == userId;
    }
    
    // public 폴더는 누구나 읽기 가능
    match /public/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

#### Firebase Storage 사용 예시 (웹)

```javascript
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";

// 파일 업로드
const storage = getStorage();
const storageRef = ref(storage, `users/${userId}/profile.jpg`);

await uploadBytes(storageRef, file);  // 파일 업로드
const url = await getDownloadURL(storageRef);  // URL 받기

console.log("다운로드 URL:", url);
// https://firebasestorage.googleapis.com/v0/b/my-app.appspot.com/...
```

---

### Cloudflare R2 vs Firebase Storage

| 항목 | Cloudflare R2 | Firebase Storage |
|------|--------------|-----------------|
| **비용** | 전송(Egress) 무료! | 전송량에 따라 과금 |
| **설정 난이도** | 중간 (API 키 설정) | 쉬움 (Firebase 통합) |
| **인증 연동** | 직접 구현 필요 | Firebase Auth 자동 연동 |
| **CDN** | Cloudflare 글로벌 | Google 글로벌 |
| **추천 상황** | 대용량, 비용 중요 | Firebase 이미 사용 중 |

### 💡 바이브코딩 팁

```
❌ "이미지 업로드 기능 만들어줘"

✅ "프로필 이미지 업로드 기능 만들어줘.
    - Storage: Cloudflare R2 사용
    - Bucket: user-profiles
    - 경로: users/{userId}/profile.jpg
    - 업로드 후 URL을 Supabase users 테이블에 저장해줘"
```

---

## 7. 인증 (Authentication)

### 🎫 비유: 놀이공원 입장

```
인증 = 놀이공원 입구에서 신분증 확인하고 팔찌 받기
인가 = 팔찌 종류에 따라 탈 수 있는 놀이기구가 다름
```

```mermaid
flowchart LR
    subgraph 입구["🚪 입구 (인증)"]
        A["신분증 확인"]
        B["팔찌 발급"]
    end
    
    subgraph 내부["🎢 놀이공원 (인가)"]
        C["일반 팔찌 → 일반 기구만"]
        D["VIP 팔찌 → 모든 기구"]
    end
    
    USER["👤 방문객"] --> 입구
    입구 --> 내부
```

### 인증(Authentication) vs 인가(Authorization)

| 구분 | 인증 (Authentication) | 인가 (Authorization) |
|------|---------------------|---------------------|
| 질문 | "너 누구야?" | "너 이거 해도 돼?" |
| 목적 | 신원 확인 | 권한 확인 |
| 예시 | 로그인 | 관리자만 삭제 가능 |
| 비유 | 신분증 검사 | VIP 팔찌 확인 |

---

### 🔐 인증 흐름 이해하기

#### 기본 로그인 흐름

```mermaid
sequenceDiagram
    participant User as 👤 사용자
    participant App as 🖥️ 앱
    participant Auth as 🔐 인증 서버
    participant DB as 🗄️ DB

    User->>App: 1. 이메일/비밀번호 입력
    App->>Auth: 2. 로그인 요청
    Auth->>DB: 3. 회원 정보 확인
    DB-->>Auth: 4. 확인 완료
    Auth-->>App: 5. 토큰(Token) 발급 🎫
    App->>App: 6. 토큰 저장
    App-->>User: 7. 로그인 성공!
    
    Note over User,DB: 이후 API 호출할 때마다
    
    User->>App: 내 정보 보기
    App->>Auth: 토큰과 함께 요청 🎫
    Auth-->>App: 토큰 유효! 정보 반환
    App-->>User: 정보 표시
```

#### 토큰(Token)이란?

```
토큰 = 디지털 신분증 = 놀이공원 팔찌
```

한번 로그인하면 받는 **"통행증"** 입니다. 이후에는 이 토큰만 보여주면 다시 로그인할 필요 없이 서비스를 이용할 수 있습니다.

```javascript
// 토큰 예시 (JWT - JSON Web Token)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VySWQiOiJ1c2VyXzAwMSIsImVtYWlsIjoiaG9uZ0BlbWFpbC5jb20ifQ.
abc123signature...

// 이 안에 담긴 정보 (디코딩하면):
{
  "userId": "user_001",
  "email": "hong@email.com",
  "exp": 1699999999  // 만료 시간
}
```

---

### ⚡ Supabase Auth

**PostgreSQL 기반의 강력한 인증 시스템**

```mermaid
flowchart TB
    subgraph SupabaseAuth["⚡ Supabase Auth"]
        EMAIL["📧 이메일/비밀번호"]
        SOCIAL["🔗 소셜 로그인"]
        MAGIC["✨ Magic Link"]
        PHONE["📱 전화번호"]
    end
    
    SOCIAL --> GOOGLE["Google"]
    SOCIAL --> GITHUB["GitHub"]
    SOCIAL --> KAKAO["Kakao"]
    SOCIAL --> APPLE["Apple"]
    
    APP["🖥️ 내 앱"] --> SupabaseAuth
```

#### Supabase Auth 특징

| 특징 | 설명 |
|------|------|
| **다양한 로그인 방식** | 이메일, 소셜, Magic Link, 전화번호 |
| **Row Level Security** | DB 테이블과 연동해서 권한 제어 |
| **JWT 토큰** | 표준 JWT 사용 |
| **쉬운 설정** | 대시보드에서 클릭 몇 번으로 설정 |

#### Supabase Auth 설정하기

**1단계: 대시보드에서 Provider 활성화**

```
Supabase Dashboard → Authentication → Providers
```

**2단계: 소셜 로그인 설정 (예: Google)**

```
1. Google Cloud Console에서 OAuth 클라이언트 생성
2. Client ID, Client Secret 복사
3. Supabase에 붙여넣기
4. Redirect URL 설정: https://[project].supabase.co/auth/v1/callback
```

#### Supabase Auth 사용 예시

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// 📧 이메일 회원가입
const { data, error } = await supabase.auth.signUp({
  email: 'hong@email.com',
  password: 'securepassword123'
})

// 📧 이메일 로그인
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'hong@email.com',
  password: 'securepassword123'
})

// 🔗 Google 로그인
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google'
})

// 👤 현재 로그인한 유저 정보
const { data: { user } } = await supabase.auth.getUser()

// 🚪 로그아웃
await supabase.auth.signOut()
```

#### Row Level Security (RLS) 예시

**"로그인한 유저만 자기 데이터 접근"**

```sql
-- posts 테이블에 RLS 활성화
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 본인 게시글만 조회 가능
CREATE POLICY "유저는 본인 글만 볼 수 있음" ON posts
  FOR SELECT USING (auth.uid() = user_id);

-- 본인만 게시글 작성 가능
CREATE POLICY "유저는 본인 이름으로만 글 작성" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

---

### 🔥 Firebase Auth

**Google의 강력한 인증 서비스**

```mermaid
flowchart TB
    subgraph FirebaseAuth["🔥 Firebase Auth"]
        EMAIL["📧 이메일/비밀번호"]
        SOCIAL["🔗 소셜 로그인"]
        PHONE["📱 전화번호 인증"]
        ANON["👻 익명 로그인"]
    end
    
    SOCIAL --> GOOGLE["Google"]
    SOCIAL --> FACEBOOK["Facebook"]
    SOCIAL --> APPLE["Apple"]
    SOCIAL --> TWITTER["Twitter"]
    
    APP["📱 내 앱"] --> FirebaseAuth
```

#### Firebase Auth 특징

| 특징 | 설명 |
|------|------|
| **모바일 최적화** | Android, iOS SDK 완벽 지원 |
| **익명 로그인** | 가입 없이 먼저 사용, 나중에 계정 연결 |
| **전화번호 인증** | SMS 인증 기본 제공 |
| **Firebase 통합** | Firestore, Storage와 자동 연동 |

#### Firebase Auth 설정하기

**1단계: Firebase Console에서 활성화**

```
Firebase Console → Authentication → Sign-in method
→ 원하는 로그인 방식 Enable
```

**2단계: 앱에 Firebase SDK 추가**

```javascript
// firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "...",
  authDomain: "my-app.firebaseapp.com",
  projectId: "my-app",
  // ...
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
```

#### Firebase Auth 사용 예시

```javascript
import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut 
} from 'firebase/auth';
import { auth } from './firebase';

// 📧 이메일 회원가입
const userCredential = await createUserWithEmailAndPassword(
  auth, 
  'hong@email.com', 
  'securepassword123'
);
const user = userCredential.user;

// 📧 이메일 로그인
await signInWithEmailAndPassword(auth, 'hong@email.com', 'password');

// 🔗 Google 로그인
const provider = new GoogleAuthProvider();
await signInWithPopup(auth, provider);

// 👤 현재 유저 확인
const currentUser = auth.currentUser;
console.log(currentUser.email);

// 🚪 로그아웃
await signOut(auth);
```

#### Firebase Security Rules 예시

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 로그인한 유저만 자기 데이터 접근
    match /users/{userId} {
      allow read, write: if request.auth != null 
                         && request.auth.uid == userId;
    }
    
    // 게시글은 누구나 읽기, 작성자만 수정/삭제
    match /posts/{postId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth.uid == resource.data.authorId;
    }
  }
}
```

---

### 인증 흐름 전체 그림

```mermaid
flowchart TB
    subgraph Client["📱 클라이언트 (프론트엔드)"]
        LOGIN["로그인 화면"]
        APP["앱 메인"]
    end
    
    subgraph Auth["🔐 인증 서비스"]
        SUPA["⚡ Supabase Auth"]
        FIRE["🔥 Firebase Auth"]
    end
    
    subgraph Backend["⚙️ 백엔드"]
        API["API 서버"]
        DB["데이터베이스"]
    end
    
    LOGIN -->|"1. 로그인 요청"| Auth
    Auth -->|"2. 토큰 발급 🎫"| LOGIN
    LOGIN -->|"3. 토큰 저장"| APP
    APP -->|"4. 토큰과 함께 API 호출"| API
    API -->|"5. 토큰 검증"| Auth
    Auth -->|"6. 유효함!"| API
    API -->|"7. DB 조회"| DB
    DB -->|"8. 데이터"| API
    API -->|"9. 응답"| APP
```

---

### Supabase Auth vs Firebase Auth

| 항목 | Supabase Auth | Firebase Auth |
|------|--------------|---------------|
| **데이터베이스** | PostgreSQL (SQL) | Firestore (NoSQL) |
| **권한 제어** | Row Level Security | Security Rules |
| **소셜 로그인** | ✅ 다양하게 지원 | ✅ 다양하게 지원 |
| **익명 로그인** | ❌ 미지원 | ✅ 지원 |
| **전화번호 인증** | ✅ 지원 | ✅ 지원 (더 쉬움) |
| **MCP 연동** | ✅ 지원 | ❌ 미지원 |
| **추천 상황** | SQL 선호, 웹 중심 | 모바일 앱, Google 생태계 |

### 💡 바이브코딩 팁

```
❌ "로그인 기능 만들어줘"

✅ "Supabase Auth로 로그인 기능 만들어줘.
    - 이메일/비밀번호 로그인
    - Google 소셜 로그인
    - 로그인 후 users 테이블에 프로필 정보 저장
    - 비로그인 유저는 /login으로 리다이렉트
    - RLS로 본인 데이터만 접근 가능하게"
```

---

## 8. Git & GitHub (형상관리)

### 📖 비유: 요리 레시피 노트

```
Git = 요리 레시피를 버전별로 기록하는 노트
GitHub = 그 노트를 보관하는 클라우드 서재
```

요리를 할 때 레시피를 조금씩 개선해 나간다고 상상해보세요. "소금을 조금 줄여봤다", "마늘을 추가해봤다" 같은 변경 사항을 매번 노트에 기록하면, 나중에 "저번에 맛있었던 버전"으로 언제든 돌아갈 수 있습니다. **Git**이 바로 이 "레시피 변경 노트"이고, **GitHub**는 이 노트를 인터넷에 올려두는 "클라우드 서재"입니다.

```mermaid
flowchart LR
    subgraph Local["🏠 내 컴퓨터 (Git)"]
        WORK["📝 레시피 수정"]
        SAVE["💾 변경 기록 저장<br/>(Commit)"]
    end
    
    subgraph Remote["☁️ GitHub (원격 저장소)"]
        REPO["📚 레시피 보관소<br/>(Repository)"]
        SHARE["👥 다른 사람과 공유"]
    end
    
    WORK --> SAVE
    SAVE -->|"Push (업로드)"| REPO
    REPO -->|"Pull (다운로드)"| WORK
    REPO --> SHARE
```

---

### 형상관리란?

형상관리(Version Control)는 **"파일의 변경 이력을 추적하고 관리하는 것"** 입니다.

아마 한 번쯤 이런 경험이 있을 겁니다:

```
📁 내 프로젝트/
├── 보고서_최종.docx
├── 보고서_최종_수정.docx
├── 보고서_최종_수정_진짜최종.docx
├── 보고서_최종_수정_진짜최종(2).docx
└── 보고서_최종_수정_진짜최종_이게진짜.docx   ← 어느 게 최신...? 😱
```

Git을 쓰면 이런 혼란이 사라집니다. **파일은 하나만 있고, 변경 이력은 Git이 전부 기억**해줍니다.

```
📁 내 프로젝트/
├── 보고서.docx          ← 파일은 하나뿐!
└── .git/                ← Git이 모든 변경 이력을 여기에 보관
     ├── ver 1: 초안 작성
     ├── ver 2: 서론 수정
     ├── ver 3: 데이터 추가
     └── ver 4: 최종 검토 반영   ← 지금 상태
```

---

### 핵심 용어 하나씩 알아보기

#### 📦 저장소 (Repository)

```
저장소 = 프로젝트 폴더 + 변경 이력 전체
```

레스토랑 비유로 돌아가면, 저장소는 **레시피북 한 권**입니다. 레시피(소스 코드)뿐 아니라, "언제 뭘 바꿨는지" 기록까지 전부 담고 있습니다.

저장소는 두 곳에 존재할 수 있습니다:

| 구분 | 위치 | 비유 |
|------|------|------|
| **로컬 저장소** | 내 컴퓨터 | 내 책상 위의 레시피 노트 |
| **원격 저장소** | GitHub 서버 | 구글 드라이브에 백업해둔 사본 |

---

#### 📥 클론 (Clone)

```
클론 = 원격 저장소를 통째로 내 컴퓨터에 복사하기
```

다른 요리사가 만들어둔 레시피북이 GitHub에 있을 때, **그 책을 통째로 복사해서 내 책상에 가져오는 것**이 클론입니다.

```mermaid
flowchart LR
    GITHUB["☁️ GitHub<br/>원격 저장소"] -->|"git clone"| LOCAL["🏠 내 컴퓨터<br/>로컬 저장소"]
    
    style GITHUB fill:#f5f5f5,stroke:#333
    style LOCAL fill:#e8f5e9,stroke:#333
```

```bash
# 클론 명령어 예시
git clone https://github.com/사용자이름/프로젝트이름.git

# 실행하면 내 컴퓨터에 "프로젝트이름" 폴더가 생기고,
# 그 안에 모든 코드 + 변경 이력이 복사됩니다!
```

**바이브코딩에서 클론이 필요한 순간:**
- Cursor/VS Code에서 남의 프로젝트를 가져와서 수정할 때
- 오픈소스 템플릿을 기반으로 내 프로젝트를 시작할 때
- 다른 컴퓨터에서 내 프로젝트를 이어서 작업할 때

---

#### 💾 커밋 (Commit)

```
커밋 = "지금 상태를 저장!" (게임의 세이브 포인트)
```

요리하다가 "여기까지는 잘 됐다!" 싶으면, 그 시점의 레시피를 노트에 기록하는 것이 커밋입니다. 나중에 실패하더라도 **이 세이브 포인트로 돌아올 수 있습니다.**

```mermaid
gitGraph
    commit id: "init project"
    commit id: "add login UI"
    commit id: "connect DB"
    commit id: "add board"
    commit id: "fix design"
```

> 각 동그라미가 하나의 커밋(세이브 포인트)입니다.  
> init project → 로그인 화면 추가 → DB 연결 → 게시판 기능 완성 → 디자인 수정

```bash
# 1. 변경된 파일을 "저장할 목록"에 추가 (재료 준비)
git add .

# 2. 현재 상태를 저장! (세이브!)
git commit -m "로그인 화면 UI 완성"
```

커밋할 때 **메시지**를 함께 남깁니다. 이건 레시피 노트에 "이번에 뭘 바꿨는지" 메모를 적는 것과 같습니다.

**좋은 커밋 메시지 예시:**
```
✅ "회원가입 이메일 인증 기능 추가"
✅ "메인 페이지 로딩 속도 개선"
✅ "장바구니 수량 버그 수정"

❌ "수정"
❌ "asdf"
❌ "뭔가 바꿈"
```

---

#### 🚀 푸시 (Push)

```
푸시 = 내 컴퓨터의 커밋을 GitHub에 업로드
```

내 책상에서 레시피를 수정하고 기록(커밋)했으면, 그걸 **클라우드 서재(GitHub)에 올리는 것**이 푸시입니다.

```mermaid
flowchart LR
    LOCAL["🏠 내 컴퓨터<br/>커밋 3개 완료!"] -->|"git push 📤"| GITHUB["☁️ GitHub<br/>원격 저장소에 반영"]
```

```bash
# GitHub에 내 변경사항 업로드!
git push
```

**왜 푸시가 중요한가요?**
- 내 컴퓨터가 고장나도 **GitHub에 백업**이 있습니다
- 다른 사람(또는 다른 컴퓨터)에서 **내 코드를 받을** 수 있습니다
- Vercel, Cloudflare Pages 같은 배포 서비스가 **GitHub를 보고 자동 배포**합니다

> 💡 커밋은 "세이브", 푸시는 "클라우드 동기화"라고 생각하면 됩니다.  
> 게임에서 세이브만 하고 클라우드 동기화 안 하면, 다른 기기에선 이어하기가 안 되는 것과 같습니다!

---

#### 📥 풀 (Pull)

```
풀 = GitHub에 있는 최신 변경사항을 내 컴퓨터로 가져오기
```

```mermaid
flowchart RL
    GITHUB["☁️ GitHub<br/>누군가 새로운 커밋을 올림"] -->|"git pull 📥"| LOCAL["🏠 내 컴퓨터<br/>최신 상태로 업데이트"]
```

```bash
# GitHub에서 최신 변경사항 가져오기
git pull
```

---

#### 🌿 브랜치 (Branch)

```
브랜치 = 원본 레시피를 건드리지 않고, 복사본에서 실험하는 것
```

파스타 레시피가 지금 완벽하다고 칩시다. 그런데 "크림소스 대신 토마토소스를 써볼까?" 하는 실험을 하고 싶습니다. 원본 레시피를 직접 고치면 실패했을 때 돌아가기 어렵겠죠? 그래서 **원본은 그대로 두고, 복사본을 만들어서 실험**하는 것이 브랜치입니다.

```mermaid
gitGraph
    commit id: "main recipe"
    commit id: "base done"
    branch feature/tomato-sauce
    checkout feature/tomato-sauce
    commit id: "try tomato"
    commit id: "adjust amount"
    checkout main
    merge feature/tomato-sauce id: "merge experiment"
    commit id: "next task"
```

> main(공식 레시피)에서 feature/tomato-sauce(실험 브랜치)를 만들어 토마토소스를 시도하고,  
> 성공하면 다시 main에 합칩니다(merge). 실패하면? 브랜치만 버리면 원본은 무사!

| 용어 | 설명 | 비유 |
|------|------|------|
| **main** (기본 브랜치) | 완성된 안정 버전 | 현재 식당 메뉴에 올라간 공식 레시피 |
| **feature 브랜치** | 새 기능을 만들 때 | 주방에서 몰래 실험 중인 신메뉴 |
| **merge** (병합) | 실험이 성공하면 합치기 | 신메뉴를 공식 메뉴에 추가 |

```bash
# 새 브랜치 만들고 이동
git checkout -b feature/login-page

# 작업하고 커밋...
git add .
git commit -m "로그인 페이지 추가"

# GitHub에 올리기
git push -u origin feature/login-page

# 작업 끝나면 main에 합치기 (보통 GitHub에서 Pull Request로 진행)
```

**브랜치가 바이브코딩에서 중요한 이유:**

AI에게 새로운 기능을 시킬 때, 브랜치를 만들어두면 실험이 실패해도 안전합니다. "AI가 코드를 이상하게 바꿔버렸다!" 해도 **main 브랜치는 무사**하니까요.

---

### Git 전체 흐름 한눈에 보기

```mermaid
flowchart TB
    subgraph Local["🏠 내 컴퓨터"]
        direction TB
        WORK["📝 작업 공간<br/>(코드 수정)"]
        STAGE["📋 스테이징<br/>(저장할 목록)"]
        LOCAL_REPO["💾 로컬 저장소<br/>(커밋 이력)"]
    end
    
    subgraph Remote["☁️ GitHub"]
        REMOTE_REPO["📚 원격 저장소"]
    end
    
    WORK -->|"git add<br/>(변경 파일 선택)"| STAGE
    STAGE -->|"git commit<br/>(세이브!)"| LOCAL_REPO
    LOCAL_REPO -->|"git push<br/>(업로드)"| REMOTE_REPO
    REMOTE_REPO -->|"git pull<br/>(다운로드)"| WORK
    REMOTE_REPO -->|"git clone<br/>(최초 복사)"| Local
```

**요리 비유로 정리하면:**

| Git 명령어 | 요리 비유 | 설명 |
|-----------|----------|------|
| `git clone` | 다른 셰프의 레시피북 복사 | 원격 저장소를 내 컴퓨터로 가져오기 |
| `git add` | 오늘 바꾼 레시피 재료 목록 정리 | 저장할 파일 선택 |
| `git commit` | 레시피 노트에 기록 (세이브!) | 변경사항을 이력으로 저장 |
| `git push` | 레시피를 클라우드 서재에 업로드 | GitHub에 올리기 |
| `git pull` | 클라우드 서재에서 최신 레시피 받기 | GitHub에서 받아오기 |
| `git branch` | 실험용 레시피 사본 만들기 | 새 브랜치 생성 |
| `git merge` | 실험 성공한 레시피를 공식 채택 | 브랜치 합치기 |

---

### 🔗 GitHub 기본 사용법

#### GitHub 저장소 만들기

```
1. github.com 접속 & 로그인
2. 오른쪽 상단 "+" → "New repository"
3. 저장소 이름 입력 (예: my-vibe-project)
4. "Create repository" 클릭
5. 끝!
```

#### Cursor / VS Code에서 GitHub 연동

AI 코딩 도구(Cursor 등)에서 작업한 코드를 GitHub에 올리는 흐름:

```mermaid
flowchart LR
    CURSOR["💻 Cursor에서<br/>AI와 코딩"] --> COMMIT["💾 커밋<br/>(세이브)"]
    COMMIT --> PUSH["🚀 푸시<br/>(GitHub 업로드)"]
    PUSH --> DEPLOY["🌐 자동 배포<br/>(Vercel 등)"]
```

대부분의 코드 에디터에는 Git 기능이 내장되어 있어서, 터미널에 명령어를 입력하지 않고도 **버튼 클릭만으로** 커밋과 푸시가 가능합니다.

---

### 💡 바이브코딩 팁

```
❌ "코드 저장해줘"

✅ "이 프로젝트를 GitHub 저장소에 올려줘.
    - 저장소 이름: my-blog-app
    - 커밋 메시지: '초기 프로젝트 설정'
    - main 브랜치에 푸시해줘"
```

```
❌ "새 기능 추가해줘"

✅ "feature/dark-mode 브랜치 만들어서 다크모드 추가해줘.
    작업 끝나면 main에 머지할 수 있게 PR 만들어줘"
```

---

## 9. 배포 (Deployment)

### 🚀 비유: 음식 배달

```
개발 = 집에서 요리하기
배포 = 요리를 손님에게 배달하기
```

아무리 맛있는 요리를 만들어도, 손님에게 **전달**하지 않으면 의미가 없습니다!

```mermaid
flowchart LR
    subgraph Dev["🏠 개발 환경"]
        CODE["💻 내 컴퓨터"]
    end
    
    subgraph Deploy["🚀 배포"]
        WEB["🌐 웹 배포"]
        MOBILE["📱 앱 배포"]
    end
    
    subgraph Users["👥 사용자"]
        BROWSER["🖥️ 브라우저"]
        PHONE["📱 스마트폰"]
    end
    
    CODE -->|"배포"| Deploy
    WEB --> BROWSER
    MOBILE --> PHONE
```

### 배포의 종류

| 플랫폼 | 배포 방식 | 도구 |
|--------|----------|------|
| **웹** | 호스팅 서비스에 업로드 | Vercel, Cloudflare Pages |
| **Android** | Play Store 심사 | Google Play Console |
| **iOS** | App Store 심사 | App Store Connect |

---

### 🌐 웹 배포

#### Vercel

**"Next.js 만든 회사의 배포 서비스"**

Next.js를 만든 회사라서 **Next.js와 궁합이 최고**입니다.

```mermaid
flowchart LR
    subgraph GitHub["📂 GitHub"]
        REPO["저장소"]
    end
    
    subgraph Vercel["▲ Vercel"]
        BUILD["빌드"]
        CDN["글로벌 CDN"]
    end
    
    REPO -->|"Push"| BUILD
    BUILD --> CDN
    CDN --> USER["👤 전세계 사용자"]
```

**Vercel 특징:**

| 특징 | 설명 |
|------|------|
| **자동 배포** | GitHub Push하면 자동으로 배포 |
| **Preview 배포** | PR마다 테스트용 URL 생성 |
| **글로벌 CDN** | 전세계 어디서든 빠름 |
| **무료 티어** | 개인 프로젝트 무료 |

**Vercel 배포 방법:**

```bash
# 방법 1: CLI 사용
npm install -g vercel
vercel

# 방법 2: GitHub 연동 (더 쉬움!)
# 1. vercel.com 접속
# 2. GitHub로 로그인
# 3. 저장소 선택
# 4. Deploy 클릭
# 끝!
```

**배포 후 URL 예시:**
```
https://my-app.vercel.app          ← 기본 도메인
https://my-custom-domain.com       ← 커스텀 도메인 연결 가능
```

---

#### Cloudflare Pages

**"빠르고 저렴한 정적 사이트 호스팅"**

Cloudflare의 글로벌 네트워크를 활용한 초고속 배포 서비스입니다.

```mermaid
flowchart LR
    subgraph GitHub["📂 GitHub"]
        REPO["저장소"]
    end
    
    subgraph CF["☁️ Cloudflare"]
        PAGES["Pages"]
        EDGE["Edge Network<br/>(전세계 300+)"]
    end
    
    REPO -->|"Push"| PAGES
    PAGES --> EDGE
    EDGE --> USER["👤 사용자"]
```

**Cloudflare Pages 특징:**

| 특징 | 설명 |
|------|------|
| **무제한 요청** | 트래픽 걱정 없음 (무료!) |
| **초고속** | 전세계 300+ 데이터센터 |
| **Workers 연동** | 서버리스 함수 연동 가능 |
| **R2 연동** | 스토리지와 쉬운 연동 |

**Cloudflare Pages 배포 방법:**

```bash
# 1. Cloudflare Dashboard → Pages
# 2. Create a project
# 3. Connect to Git → GitHub 선택
# 4. 저장소 선택
# 5. Build settings 설정:

Framework preset: Next.js
Build command: npm run build
Build output directory: .next
```

**환경 변수 설정:**
```
Settings → Environment variables
→ NEXT_PUBLIC_SUPABASE_URL = https://xxx.supabase.co
→ NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJxx...
```

---

#### Vercel vs Cloudflare Pages

| 항목 | Vercel | Cloudflare Pages |
|------|--------|-----------------|
| **Next.js 지원** | ⭐ 최고 (공식) | 좋음 |
| **무료 범위** | 월 100GB 대역폭 | 무제한! |
| **빌드 시간** | 월 6,000분 (무료) | 월 500회 (무료) |
| **서버리스 함수** | Vercel Functions | Workers |
| **추천 상황** | Next.js 프로젝트 | 정적 사이트, 비용 절감 |

### 💡 바이브코딩 팁 (웹 배포)

```
❌ "배포해줘"

✅ "Vercel로 배포 설정해줘.
    - GitHub 저장소: my-app
    - 환경변수: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY
    - 커스텀 도메인: myapp.com 연결
    - main 브랜치 push하면 자동 배포되게"
```

---

### 📱 모바일 앱 배포

#### 모바일 배포 전체 흐름

```mermaid
flowchart TB
    subgraph Dev["💻 개발"]
        CODE["코드 작성"]
        BUILD["앱 빌드"]
        SIGN["서명 (Signing)"]
    end
    
    subgraph Review["📋 심사"]
        SUBMIT["스토어 제출"]
        WAIT["심사 대기<br/>(1~7일)"]
        RESULT["승인/거절"]
    end
    
    subgraph Release["🎉 출시"]
        STORE["스토어 등록"]
        USER["사용자 다운로드"]
    end
    
    CODE --> BUILD --> SIGN --> SUBMIT --> WAIT --> RESULT
    RESULT -->|"승인"| STORE --> USER
    RESULT -->|"거절"| CODE
```

---

#### 🤖 Google Play Store (Android)

**Play Console에서 앱을 등록하고 관리합니다.**

```mermaid
flowchart LR
    subgraph Prepare["📦 준비물"]
        APK["APK/AAB 파일"]
        ICON["앱 아이콘<br/>(512x512)"]
        SCREEN["스크린샷<br/>(최소 2장)"]
        DESC["앱 설명"]
    end
    
    subgraph Console["🎮 Play Console"]
        UPLOAD["앱 업로드"]
        INFO["스토어 정보"]
        PRICE["가격 설정"]
        SUBMIT["심사 제출"]
    end
    
    Prepare --> Console
```

**Android 배포 준비물:**

| 항목 | 설명 | 규격 |
|------|------|------|
| **APK/AAB** | 앱 설치 파일 | AAB 권장 (2021년부터 필수) |
| **앱 아이콘** | 스토어에 표시되는 아이콘 | 512 x 512 PNG |
| **스크린샷** | 앱 미리보기 | 최소 2장, 폰/태블릿별 |
| **피처 그래픽** | 스토어 배너 이미지 | 1024 x 500 |
| **앱 설명** | 앱 소개 텍스트 | 최대 4,000자 |
| **개인정보처리방침** | 필수 (URL) | 웹페이지 링크 |

**Android 배포 절차:**

```
1. Google Play Console 가입 (등록비 $25, 1회)
   → play.google.com/console

2. 앱 만들기
   → 앱 이름, 기본 언어, 앱/게임 여부 선택

3. 앱 서명 키 설정
   → Google이 관리하는 서명 권장

4. 스토어 등록 정보 입력
   → 아이콘, 스크린샷, 설명 등

5. 콘텐츠 등급 설문
   → 폭력성, 성인 콘텐츠 여부 답변

6. 가격 및 배포 국가 설정

7. AAB 파일 업로드
   → 내부 테스트 → 비공개 테스트 → 프로덕션

8. 심사 제출
   → 보통 1~3일 소요 (첫 앱은 7일까지)
```

**테스트 트랙 종류:**

```mermaid
flowchart LR
    INTERNAL["🔒 내부 테스트<br/>(100명)"] --> CLOSED["🔐 비공개 테스트<br/>(초대된 사람만)"]
    CLOSED --> OPEN["🔓 공개 테스트<br/>(누구나 참여)"]
    OPEN --> PROD["🚀 프로덕션<br/>(정식 출시)"]
```

---

#### 🍎 App Store (iOS)

**App Store Connect에서 앱을 등록하고 관리합니다.**

```mermaid
flowchart LR
    subgraph Prepare["📦 준비물"]
        IPA["IPA 파일"]
        ICON["앱 아이콘<br/>(1024x1024)"]
        SCREEN["스크린샷<br/>(기기별)"]
        DESC["앱 설명"]
    end
    
    subgraph Connect["🍎 App Store Connect"]
        UPLOAD["앱 업로드<br/>(Xcode/Transporter)"]
        INFO["스토어 정보"]
        REVIEW["앱 심사"]
    end
    
    Prepare --> Connect
```

**iOS 배포 준비물:**

| 항목 | 설명 | 규격 |
|------|------|------|
| **IPA** | 앱 설치 파일 | Xcode로 Archive |
| **앱 아이콘** | 스토어 아이콘 | 1024 x 1024 PNG |
| **스크린샷** | 기기별 필요 | iPhone 6.9", 6.5", iPad 등 |
| **앱 설명** | 앱 소개 | 최대 4,000자 |
| **개인정보처리방침** | 필수 | URL 링크 |
| **앱 미리보기** | 동영상 (선택) | 15~30초 |

**iOS 배포 절차:**

```
1. Apple Developer 가입 (연 $99 = 약 13만원)
   → developer.apple.com

2. App Store Connect에서 앱 등록
   → appstoreconnect.apple.com

3. 인증서 & 프로비저닝 프로파일 설정
   → Xcode에서 자동 관리 가능

4. Xcode에서 Archive 생성
   → Product → Archive

5. App Store Connect에 업로드
   → Xcode → Distribute App → App Store Connect

6. 스토어 정보 입력
   → 스크린샷, 설명, 카테고리 등

7. 앱 심사 제출
   → 보통 24~48시간 (거절되면 더 오래)

8. 승인 후 출시
   → 즉시 출시 or 예약 출시 선택
```

**iOS 심사 주요 거절 사유:**

| 거절 사유 | 설명 |
|----------|------|
| **버그/크래시** | 앱이 죽거나 기능이 안 됨 |
| **불완전한 정보** | 스크린샷, 설명 부족 |
| **가이드라인 위반** | 결제 정책, 콘텐츠 규정 |
| **개인정보** | 개인정보 수집 고지 누락 |
| **메타데이터** | 앱 이름, 설명의 오해 소지 |

**TestFlight (iOS 베타 테스트):**

```mermaid
flowchart LR
    DEV["개발자"] -->|"빌드 업로드"| TF["🛩️ TestFlight"]
    TF -->|"초대 링크"| INTERNAL["내부 테스터<br/>(100명)"]
    TF -->|"공개 링크"| EXTERNAL["외부 테스터<br/>(10,000명)"]
```

---

### 모바일 배포 비교

| 항목 | Google Play Store | App Store |
|------|------------------|-----------|
| **등록 비용** | $25 (1회) | $99/년 |
| **심사 기간** | 1~7일 | 24~48시간 |
| **심사 엄격도** | 상대적 느슨 | 매우 엄격 |
| **업데이트 심사** | 빠름 | 동일하게 심사 |
| **테스트 배포** | 내부/비공개/공개 | TestFlight |
| **결제 수수료** | 15~30% | 15~30% |

---

### 배포 전 체크리스트

```mermaid
flowchart TB
    subgraph Web["🌐 웹 체크리스트"]
        W1["✅ 환경변수 설정"]
        W2["✅ 빌드 에러 없음"]
        W3["✅ 도메인 연결"]
        W4["✅ HTTPS 적용"]
    end
    
    subgraph Mobile["📱 모바일 체크리스트"]
        M1["✅ 아이콘/스크린샷"]
        M2["✅ 앱 서명 완료"]
        M3["✅ 개인정보처리방침"]
        M4["✅ 테스트 완료"]
        M5["✅ 버전 번호 증가"]
    end
```

### 💡 바이브코딩 팁 (모바일 배포)

```
❌ "앱스토어 올려줘"

✅ "iOS 앱스토어 배포 준비해줘.
    - 앱 이름: My App
    - 번들 ID: com.mycompany.myapp
    - 버전: 1.0.0
    - 카테고리: 생산성
    - Xcode에서 Archive 하는 방법이랑
    - App Store Connect 설정 방법 알려줘"
```

---

## 📝 Part 2 정리: 바이브코딩 체크리스트

| 개념 | 지시할 때 명시하면 좋은 것 |
|------|-------------------------|
| **Storage** | "R2/Firebase Storage 사용", "버킷 이름", "폴더 구조" |
| **인증** | "Supabase/Firebase Auth", "소셜 로그인 종류", "권한 규칙" |
| **Git/GitHub** | "브랜치 이름", "커밋 메시지", "저장소 이름", "PR 만들어줘" |
| **웹 배포** | "Vercel/Cloudflare Pages", "환경변수", "도메인" |
| **앱 배포** | "스토어 종류", "버전", "테스트 트랙" |

---

## 🎯 전체 아키텍처 한눈에 보기

```mermaid
flowchart TB
    subgraph Client["📱 클라이언트"]
        WEB["🌐 웹<br/>(Next.js)"]
        ANDROID["🤖 Android"]
        IOS["🍎 iOS"]
    end
    
    subgraph Auth["🔐 인증"]
        SUPA_AUTH["Supabase Auth"]
        FIRE_AUTH["Firebase Auth"]
    end
    
    subgraph Backend["⚙️ 백엔드"]
        API["FastAPI"]
        FUNC["Cloud Functions"]
    end
    
    subgraph Data["🗄️ 데이터"]
        SUPA_DB["Supabase DB"]
        FIRE_DB["Firebase DB"]
    end
    
    subgraph Storage["📦 저장소"]
        R2["Cloudflare R2"]
        FIRE_STORAGE["Firebase Storage"]
    end
    
    subgraph Deploy["🚀 배포"]
        VERCEL["Vercel"]
        CF_PAGES["CF Pages"]
        PLAY["Play Store"]
        APPSTORE["App Store"]
    end
    
    Client --> Auth
    Client --> Backend
    Backend --> Data
    Backend --> Storage
    
    WEB --> VERCEL
    WEB --> CF_PAGES
    ANDROID --> PLAY
    IOS --> APPSTORE
```

---

## 📚 추천 조합

| 용도 | 추천 스택 |
|------|----------|
| **웹 서비스 (빠른 개발)** | Next.js + Supabase + Vercel |
| **웹 서비스 (비용 절감)** | Next.js + Supabase + Cloudflare Pages + R2 |
| **모바일 앱 (실시간)** | Flutter + Firebase 전체 |
| **풀스택 (바이브코딩)** | Next.js + Supabase (MCP) + Vercel |

---

> 📌 **이 문서는 GitHub에서 관리됩니다.**  
> 피드백이나 추가 요청은 Issue로 남겨주세요!
> 
> **Part 1 보러가기:** [프론트엔드/백엔드, API, 에러, 프레임워크, 데이터베이스](./vibe-coding-guide-for-non-developers.md)

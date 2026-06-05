# SQL Injection 취약점 분석 및 시큐어 코딩 로그인 시스템

## 📋 프로젝트 개요

Python Flask 기반 SQL Injection 취약점 학습용 애플리케이션입니다. 
같은 기능을 구현한 **취약한 방식**과 **안전한 방식**을 비교하여 시큐어 코딩의 중요성을 학습할 수 있습니다.

## 🎯 프로젝트 목표

- **F-01**: 회원가입 (SHA256 비밀번호 해싱)
- **F-02**: 취약한 로그인 (SQL Injection 공격 가능)
- **F-03**: 안전한 로그인 (Prepared Statement 방식)
- **F-04**: 결과 화면 (실행된 SQL 쿼리 시각화)

## 📁 프로젝트 구조

```
Vibe_Coding/
├── secure.py              # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── security_demo.db       # SQLite 데이터베이스 (자동 생성)
└── templates/
    └── index.html         # 웹 UI
```

## 🚀 설치 및 실행

### 1. 필수 요구사항
- Python 3.7 이상
- pip (Python 패키지 관리자)

### 2. 설치 단계

```bash
# 1. 프로젝트 디렉토리로 이동
cd c:\Users\test\문서\Vibe_Coding

# 2. Python 가상환경 생성 (선택사항이지만 권장)
python -m venv venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# 4. 필수 패키지 설치
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
python secure.py
```

### 4. 웹 브라우저에서 접속

```
http://localhost:5000
```

## 💡 사용 방법

### 회원가입
1. "회원가입" 섹션에서 아이디(3자 이상), 비밀번호(4자 이상) 입력
2. "회원가입" 버튼 클릭
3. 데이터베이스에 해시된 비밀번호로 저장됨

### 테스트 계정 사용
"테스트 계정 & 공격 페이로드 보기" 버튼을 클릭하면 미리 생성된 계정 정보가 표시됩니다:
- admin / admin123
- user1 / pass1234
- user2 / password
- test / test1234
- demo / demo123

### 취약한 로그인 테스트 (SQL Injection)

#### 정상 로그인:
- 아이디: `admin`
- 비밀번호: `admin123`
- 결과: ✓ 로그인 성공

#### SQL Injection 공격:
- 아이디: `admin' --`
- 비밀번호: (아무거나)
- 결과: ✓ 로그인 성공 (비밀번호 우회!)

- 아이디: `' OR '1'='1`
- 비밀번호: `' OR '1'='1`
- 결과: ✓ 로그인 성공 (모든 계정으로 접근 가능!)

### 안전한 로그인 테스트 (Prepared Statement)

#### 정상 로그인:
- 아이디: `admin`
- 비밀번호: `admin123`
- 결과: ✓ 로그인 성공

#### SQL Injection 공격 시도:
- 아이디: `admin' --`
- 비밀번호: (아무거나)
- 결과: ❌ 로그인 실패 (공격 방어됨!)

- 아이디: `' OR '1'='1`
- 비밀번호: `' OR '1'='1`
- 결과: ❌ 로그인 실패 (공격 방어됨!)

## 🔒 보안 개념

### 취약한 방식 (문자열 포맷팅)
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password_hash}'"
cursor.execute(query)
```
**문제점**: 사용자 입력이 SQL 구문으로 해석될 수 있음

### 안전한 방식 (Prepared Statement)
```python
query = "SELECT * FROM users WHERE username = ? AND password_hash = ?"
cursor.execute(query, (username, password_hash))
```
**장점**: 입력값이 데이터로만 처리되어 SQL 구문으로 해석되지 않음

## 🛠️ 기술 스택

| 기술 | 용도 |
|------|------|
| Python 3 | 백엔드 언어 |
| Flask | 웹 프레임워크 |
| SQLite3 | 데이터베이스 |
| SHA256 | 비밀번호 해싱 |
| HTML5/CSS3/JavaScript | 프론트엔드 |

## 📊 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎓 학습 목표

1. **SQL Injection의 원리** 이해
2. **취약한 코딩 패턴** 인식
3. **Prepared Statement의 필요성** 체감
4. **시큐어 코딩 관행** 학습
5. **실제 공격 벡터** 체험

## ⚠️ 주의사항

- 이 애플리케이션은 **교육용**입니다
- **실제 프로덕션 환경**에서는 사용하지 마세요
- 더 강화된 보안 조치 필요 (암호화, SSL/TLS 등)
- 개발 모드(`debug=True`)는 로컬 개발용만 사용

## 📝 라이선스

개인 학습용으로 자유롭게 사용 가능합니다.

## 🔗 참고 자료

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Python SQLite3 안전한 쿼리](https://docs.python.org/3/library/sqlite3.html#how-to-write-portable-sql-code)
- [Prepared Statements](https://en.wikipedia.org/wiki/Prepared_statement)

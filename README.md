# 웹 시큐어 코딩 인터랙티브 학습 스튜디오 (Stitch Security Academy)

> **Python Flask & Tailwind CSS v3 기반의 4대 핵심 웹 보안 취약점 시각화 및 시큐어 코딩 아카데미**

---

## 📋 프로젝트 개요

**Stitch Security Academy**는 웹 애플리케이션의 4대 주요 취약점(**SQL Injection, XSS, CSRF, IDOR**)을 실시간으로 시연하고, **취약한 백엔드 방식 vs 안전한 시큐어 코딩 방식**을 1:1로 비교 분석하는 인터랙티브 교육용 스튜디오입니다.

눈이 편안한 **Soft Warm White (Tailwind CSS v3)** 디자인과 직관적인 **1-Click 자동 제출(Auto-Submit)** 기능, **백엔드 쿼리/DOM 시각화 도구**를 통해 보안 원리를 부드럽고 명확하게 체득할 수 있습니다.

---

## 🎯 4대 핵심 학습 모듈 (04 Core Modules)

| 모듈 | 주제 | 주요 학습 내용 | 접속 라우트 |
| :--- | :--- | :--- | :--- |
| **Module 01** | **SQL Injection & DB 보안** | f-string 문자열 결합 쿼리의 취약점 분석 및 `Prepared Statement` 파라미터 바인딩 방어 | `/sqli` |
| **Module 02** | **XSS & 클라이언트 보안** | Reflected 및 Event XSS 스크립트 주입 시연 및 서버측 `HTML Entity Escape` (Sanitization) 방어 | `/xss` |
| **Module 03** | **CSRF & 세션 보안** | 자동 쿠키 전송을 도용한 위조 송금 공격 관찰 및 `Anti-CSRF Token` & `SameSite` 쿠키 검증 방어 | `/csrf` |
| **Module 04** | **인증/인가 & IDOR 방어** | 식별자 파라미터 조작(IDOR)을 통한 타인 데이터 무단 열람 시연 및 `서버 세션 인가(RBAC)` 검증 방어 | `/auth` |

---

## 📁 프로젝트 구조

```
Vibe_Coding/
├── secure.py                 # Flask 백엔드 메인 애플리케이션 (API & 라우터)
├── security_demo.db          # SQLite 데이터베이스 (최초 실행 시 자동 생성)
├── requirements.txt          # Python 패키지 의존성 (Flask 등)
├── HOW_TO_USE.md             # 세부 사용자 매뉴얼
├── README.md                 # 프로젝트 종합 명서
└── templates/                # Soft Warm White Tailwind CSS v3 템플릿
    ├── hub.html              # 보안 아카데미 메인 포털 허브 (/)
    ├── sqli.html             # Module 01: SQL Injection 스튜디오 (/sqli)
    ├── xss.html              # Module 02: XSS 스튜디오 (/xss)
    ├── csrf.html             # Module 03: CSRF 스튜디오 (/csrf)
    ├── auth.html             # Module 04: 인증/인가 & IDOR 스튜디오 (/auth)
    └── index.html            # SQLi 메인 백업 템플릿
```

---

## 🚀 설치 및 실행 방법

### 1. 필수 요구사항
- **Python 3.7 이상**
- **pip** (파이썬 패키지 관리자)

### 2. 패키지 설치
```bash
# 필수 패키지 설치 (Flask)
pip install -r requirements.txt
```

### 3. 애플리케이션 구동
```bash
python secure.py
```

### 4. 웹 브라우저 접속
- **메인 포털 허브**: [http://localhost:5000/](http://localhost:5000/)
- **SQL Injection 스튜디오**: [http://localhost:5000/sqli](http://localhost:5000/sqli)
- **XSS 스튜디오**: [http://localhost:5000/xss](http://localhost:5000/xss)
- **CSRF 스튜디오**: [http://localhost:5000/csrf](http://localhost:5000/csrf)
- **IDOR 스튜디오**: [http://localhost:5000/auth](http://localhost:5000/auth)

---

## ✨ 특장점 & UX 개선 사항

1. **1-Click Auto-Submit 원스톱 실행**
   - 튜토리얼 프리셋 칩이나 샌드박스 버튼을 클릭하면 **자동 입력 + API 호출 + 결과 시각화**가 원스톱으로 즉시 처리됩니다.
2. **팝업(confirm) 없는 부드러운 단계 이동**
   - 상단 Step 타임라인 클릭 시 팝업 차단 걱정 없이 원하는 단계로 즉시 부드럽게 전환됩니다.
3. **실시간 시각화 Inspector**
   - **SQL Visualizer**: 백엔드에서 조합된 최종 SQL 문법 하이라이팅
   - **DOM Render Window**: 주입된 자바스크립트 스크립트/이벤트 동적 실행 시각화
   - **HTTP Packet Visualizer**: HTTP Header, Cookie, Anti-CSRF Token 검증 패킷 표시
4. **Soft Warm White Design Standard**
   - Tailwind CSS v3 기반의 눈이 편안한 Slate/Warm White 테마 및 Glassmorphism 헤더 네비게이션 적용.

---

## 🔒 핵심 시큐어 코딩 요약

### 1. SQL Injection 방어 (Prepared Statement)
```python
# ❌ 취약한 코드 (f-string)
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# ✅ 안전한 코드 (파라미터 바인딩)
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

### 2. XSS 방어 (HTML Entity Escape)
```python
# ❌ 취약한 코드 (Raw Output)
return f"<div>검색어: {content}</div>"

# ✅ 안전한 코드 (html.escape)
escaped = html.escape(content)
return f"<div>검색어: {escaped}</div>"
```

### 3. CSRF 방어 (Anti-CSRF Token & SameSite)
```python
# ✅ X-CSRF-Token 헤더 검증
csrf_token = request.headers.get('X-CSRF-Token')
if csrf_token != 'VALID_TOKEN':
    return jsonify({'error': 'Invalid CSRF Token'}), 403
```

### 4. IDOR 방어 (서버 세션 인가 대조)
```python
# ✅ 요청 ID와 로그인 세션 ID 상호 검증
if str(session.get('user_id')) != str(request_user_id):
    return jsonify({'error': 'Forbidden'}), 403
```

---

## ⚠️ 주의사항

- 본 애플리케이션은 보안 및 시큐어 코딩 학습을 위한 **교육용 시뮬레이터**입니다.
- 웹사이트 공격 및 악용 목적으로 사용하실 수 없으며, 로컬 개발 환경(`localhost`)에서 실습용으로만 활용하세요.

---

## 📝 라이선스

개인 학습 및 보안 교육용으로 자유롭게 사용 가능합니다.

"""
=================================================================
🔐 보안 교육용 Flask 애플리케이션
=================================================================
이 프로그램은 SQL Injection 공격을 시연하고 방어 방법을 보여줍니다.

📚 학습 목표:
  1. SQL Injection이 무엇인지 이해하기
  2. 취약한 코드 vs 안전한 코드 비교
  3. Prepared Statement의 중요성 학습

🚀 빠른 시작:
  1. 이 파일을 실행: python secure.py
  2. 브라우저에서 http://localhost:5000 접속
  3. "테스트 계정" 버튼에서 샘플 계정 확인
  4. 취약한 로그인과 안전한 로그인 비교해보기

=================================================================
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'security_demo.db'

# =================================================================
# 1️⃣ 데이터베이스 설정 함수들
# =================================================================

def init_db():
    """
    데이터베이스 초기화 함수
    
    역할:
    - 'security_demo.db' 파일 생성
    - users 테이블 생성
    - 테스트용 샘플 계정 5개 추가
    
    호출 시점: 프로그램 시작할 때 한 번만 실행됨
    """
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 👤 사용자 테이블 생성
        # id: 자동 증가 번호
        # username: 사용자 아이디 (중복 불가)
        # password_hash: 암호화된 비밀번호
        # created_at: 가입 날짜
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 📝 테스트 계정 정보 (교육용)
        test_users = [
            ('admin', hash_password('admin123')),
            ('user1', hash_password('pass1234')),
            ('user2', hash_password('password')),
            ('test', hash_password('test1234')),
            ('demo', hash_password('demo123')),
        ]
        
        # 반복문으로 각 계정을 데이터베이스에 추가
        for username, password_hash in test_users:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                         (username, password_hash))
        
        # 변경사항을 데이터베이스에 저장
        conn.commit()
        conn.close()
        print("✓ 데이터베이스 초기화 완료")

def hash_password(password):
    """
    비밀번호를 암호화하는 함수
    
    매개변수:
    - password (문자열): 원본 비밀번호
    
    반환값:
    - 암호화된 비밀번호 (64자 문자열)
    
    예시:
    - hash_password('admin123')
    - → '240be518....' (매우 긴 문자열)
    
    중요: 같은 비밀번호는 항상 같은 해시값이 나옵니다!
    """
    return hashlib.sha256(password.encode()).hexdigest()

# =================================================================
# 2️⃣ 회원가입 함수
# =================================================================

def register_user(username, password):
    """
    새로운 사용자를 등록하는 함수
    
    매개변수:
    - username (문자열): 새로운 아이디
    - password (문자열): 새로운 비밀번호
    
    반환값:
    - (성공여부, 메시지) 튜플
    - 예: (True, "회원가입 성공") 또는 (False, "이미 존재하는 아이디입니다")
    
    동작 과정:
    1. 비밀번호를 해시 함수로 암호화
    2. 데이터베이스에 아이디와 암호화된 비밀번호 저장
    3. 성공/실패 메시지 반환
    
    주의: 비밀번호는 암호화되어 저장되므로 원본 비밀번호는 알 수 없습니다
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                     (username, password_hash))
        conn.commit()
        conn.close()
        return True, "회원가입 성공"
    except sqlite3.IntegrityError:
        # 같은 아이디가 이미 존재하면 이 에러 발생
        return False, "이미 존재하는 아이디입니다"
    except Exception as e:
        # 예상치 못한 다른 에러 처리
        return False, f"오류: {str(e)}"

# =================================================================
# 3️⃣ 로그인 함수 - 취약한 방식 (공격 가능!) ⚠️
# =================================================================

def vulnerable_login(username, password):
    """
    ⚠️ 취약한 로그인 함수 - SQL Injection 공격에 노출됨!
    
    문제점:
    - 사용자 입력을 검증 없이 SQL 쿼리에 직접 넣음
    - 입력된 문장이 그대로 SQL 코드가 될 수 있음
    - 특수 문자(예: ' 또는 --)로 공격자가 조건을 바꿀 수 있음
    
    공격 예시:
    - 아이디: admin' --
      설명: 비밀번호 검사 부분을 주석 처리해 우회함
    - 아이디: ' OR '1'='1
      설명: 항상 참이 되는 조건을 넣어 로그인 성공시킴
    
    매개변수:
    - username (문자열): 입력받은 아이디
    - password (문자열): 입력받은 비밀번호
    
    반환값:
    - (성공여부, 메시지, 실제_SQL_쿼리)
    - 쿼리는 사용자가 공격을 이해하도록 보여줌
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        # ❌ 이 방식이 문제! 문자열 조합으로 쿼리 만들어짐
        # 사용자가 입력한 값이 그대로 쿼리에 들어감
        query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password_hash}'"
        
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, f"로그인 성공: {result[1]}", query
        else:
            return False, "아이디 또는 비밀번호가 틀렸습니다", query
    except Exception as e:
        return False, f"오류: {str(e)}", ""

# =================================================================
# 4️⃣ 로그인 함수 - 안전한 방식 (추천!) ✅
# =================================================================

def secure_login(username, password):
    """
    ✅ 안전한 로그인 함수 - Prepared Statement 사용
    
    장점:
    - SQL 인젝션 공격으로부터 완벽하게 보호됨
    - 사용자 입력이 데이터로 취급되어 절대 코드로 실행 안 됨
    - 프로덕션(실제 서비스)에서 반드시 사용해야 함!
    
    안전한 원리:
    - "?" 기호를 사용해 데이터 영역을 명시적으로 표시
    - 튜플 (username, password_hash)의 값들을 안전하게 전달
    - 데이터베이스가 SQL과 데이터를 구분해서 처리
    
    결과적으로:
    - ' OR '1'='1 같은 공격 입력도 그냥 일반 텍스트로 처리됨
    
    매개변수:
    - username (문자열): 입력받은 아이디
    - password (문자열): 입력받은 비밀번호
    
    반환값:
    - (성공여부, 메시지, 안전한_SQL_쿼리_패턴)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        # ✅ 안전한 방식! Prepared Statement 사용
        # "?"는 매개변수 자리를 나타냄
        # 두 번째 매개변수 (username, password_hash)를 안전하게 전달
        query = "SELECT * FROM users WHERE username = ? AND password_hash = ?"
        cursor.execute(query, (username, password_hash))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, f"로그인 성공: {result[1]}", query
        else:
            return False, "아이디 또는 비밀번호가 틀렸습니다", query
    except Exception as e:
        return False, f"오류: {str(e)}", ""

# =================================================================
# 5️⃣ 웹 페이지 라우트들 (Flask 웹 서버)
# =================================================================
# 라우트란? 특정 URL 주소로 접속할 때 실행되는 함수

@app.route('/')
def index():
    """
    메인 페이지를 보여주는 함수
    
    URL: http://localhost:5000/
    역할: index.html 파일을 브라우저에 표시
    """
    return render_template('index.html')

# =================================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """
    회원가입 API 엔드포인트
    
    URL: http://localhost:5000/api/register
    메서드: POST (데이터를 보낼 때 사용)
    
    받는 데이터 (JSON 형식):
    {
        "username": "새로운아이디",
        "password": "새로운비밀번호"
    }
    
    반환 데이터 (JSON 형식):
    {
        "success": true/false,
        "message": "결과 메시지"
    }
    """
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    # 입력값 검증 (값이 비어있는지 확인)
    if not username or not password:
        return jsonify({'success': False, 'message': '아이디와 비밀번호를 입력해주세요'}), 400
    
    # 입력값 검증 (최소 길이 확인)
    if len(username) < 3 or len(password) < 4:
        return jsonify({'success': False, 'message': '아이디는 3자 이상, 비밀번호는 4자 이상이어야 합니다'}), 400
    
    success, message = register_user(username, password)
    return jsonify({'success': success, 'message': message})

# =================================================================

@app.route('/api/vulnerable-login', methods=['POST'])
def api_vulnerable_login():
    """
    취약한 로그인 API (SQL Injection 데모용)
    
    URL: http://localhost:5000/api/vulnerable-login
    메서드: POST
    
    목적:
    - SQL Injection 공격 원리를 교육하기 위한 엔드포인트
    - 실제 서비스에서는 절대 사용하면 안 됨!
    - 학습용으로만 사용해야 함!
    """
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    success, message, query = vulnerable_login(username, password)
    
    return jsonify({
        'success': success,
        'message': message,
        'query': query,  # 쿼리를 보여주는 것은 교육용일 때만!
        'is_vulnerable': True
    })

# =================================================================

@app.route('/api/secure-login', methods=['POST'])
def api_secure_login():
    """
    안전한 로그인 API (Prepared Statement 사용)
    
    URL: http://localhost:5000/api/secure-login
    메서드: POST
    
    목적:
    - SQL Injection 공격으로부터 안전한 로그인 구현
    - 프로덕션 서비스에서 반드시 이 방식을 사용해야 함!
    
    안전성:
    - 특수 문자(' -- 등)가 포함된 입력도 안전하게 처리됨
    - 데이터베이스 레벨에서 SQL 코드와 데이터를 구분함
    """
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    success, message, query = secure_login(username, password)
    
    return jsonify({
        'success': success,
        'message': message,
        'query': query,
        'is_vulnerable': False
    })

# =================================================================

@app.route('/api/test-accounts', methods=['GET'])
def api_test_accounts():
    """
    테스트 계정 정보 및 공격 예시를 제공하는 API
    
    URL: http://localhost:5000/api/test-accounts
    메서드: GET (데이터를 받기만 함)
    
    사용 방법:
    1. "테스트 계정" 버튼을 클릭
    2. 제공되는 아이디/비밀번호로 로그인해보기
    3. "공격 예시" 섹션의 특수 문자를 입력해서 비교하기
    
    📚 학습 포인트:
    - 취약한 로그인: 특수 문자로 공격 성공
    - 안전한 로그인: 같은 입력으로 공격 실패
    """
    return jsonify({
        'accounts': [
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'user1', 'password': 'pass1234'},
            {'username': 'user2', 'password': 'password'},
            {'username': 'test', 'password': 'test1234'},
            {'username': 'demo', 'password': 'demo123'},
        ],
        'injection_examples': [
            {
                'payload': "' OR '1'='1",
                'description': "💥 모든 계정으로 로그인 가능 (취약한 방식에서만 성공!)"
            },
            {
                'payload': "admin' --",
                'description': "💥 비밀번호 우회 (취약한 방식에서만 성공!)"
            },
            {
                'payload': "' OR '1'='1' /*",
                'description': "💥 또 다른 공격 방식 (취약한 방식에서만 성공!)"
            }
        ]
    })

# =================================================================
# 🚀 프로그램 시작 지점
# =================================================================

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════╗
║        🔐 보안 교육용 Flask 애플리케이션 시작됨                ║
╚════════════════════════════════════════════════════════════════╝

📌 다음 단계:
1. 브라우저에서 이 주소 열기: http://localhost:5000
2. "테스트 계정" 버튼에서 샘플 아이디/비밀번호 확인
3. 취약한 로그인과 안전한 로그인 비교해보기
4. SQL Injection 공격 예시를 입력해서 차이 관찰

💡 학습 팁:
- 취약한 로그인에서 ' OR '1'='1 를 입력해보세요
- 안전한 로그인에서 같은 입력을 해보세요
- 결과의 차이를 보세요!

🔗 주소: http://localhost:5000
⏹️ 종료: 터미널에서 Ctrl+C 누르기

════════════════════════════════════════════════════════════════
    """)
    
    init_db()
    app.run(debug=True, host='localhost', port=5000)


from flask import Flask, render_template, request, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'security_demo.db'

# 데이터베이스 초기화
def init_db():
    """데이터베이스 및 테이블 생성"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 사용자 테이블 생성
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 테스트 데이터 삽입 (5명)
        test_users = [
            ('admin', hash_password('admin123')),
            ('user1', hash_password('pass1234')),
            ('user2', hash_password('password')),
            ('test', hash_password('test1234')),
            ('demo', hash_password('demo123')),
        ]
        
        for username, password_hash in test_users:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                         (username, password_hash))
        
        conn.commit()
        conn.close()
        print("✓ 데이터베이스 초기화 완료")

# 비밀번호 해시 함수
def hash_password(password):
    """SHA256을 사용하여 비밀번호 해싱"""
    return hashlib.sha256(password.encode()).hexdigest()

# 회원가입
def register_user(username, password):
    """사용자 회원가입"""
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
        return False, "이미 존재하는 아이디입니다"
    except Exception as e:
        return False, f"오류: {str(e)}"

# 취약한 로그인 (SQL Injection 가능)
def vulnerable_login(username, password):
    """
    취약한 로그인 - SQL Injection 공격에 노출됨
    사용자 입력을 검증 없이 쿼리에 직접 포함
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        # 문자열 포맷팅 방식 (취약함)
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

# 안전한 로그인 (Prepared Statement)
def secure_login(username, password):
    """
    안전한 로그인 - Prepared Statement 방식
    사용자 입력을 쿼리 매개변수로 안전하게 전달
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        # Prepared Statement 방식 (안전함)
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

# 라우트: 메인 페이지
@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

# 라우트: 회원가입
@app.route('/api/register', methods=['POST'])
def api_register():
    """회원가입 API"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'message': '아이디와 비밀번호를 입력해주세요'}), 400
    
    if len(username) < 3 or len(password) < 4:
        return jsonify({'success': False, 'message': '아이디는 3자 이상, 비밀번호는 4자 이상이어야 합니다'}), 400
    
    success, message = register_user(username, password)
    return jsonify({'success': success, 'message': message})

# 라우트: 취약한 로그인
@app.route('/api/vulnerable-login', methods=['POST'])
def api_vulnerable_login():
    """취약한 로그인 API (SQL Injection 데모)"""
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    success, message, query = vulnerable_login(username, password)
    
    return jsonify({
        'success': success,
        'message': message,
        'query': query,
        'is_vulnerable': True
    })

# 라우트: 안전한 로그인
@app.route('/api/secure-login', methods=['POST'])
def api_secure_login():
    """안전한 로그인 API (Prepared Statement)"""
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

# 라우트: 테스트 계정 정보
@app.route('/api/test-accounts', methods=['GET'])
def api_test_accounts():
    """테스트 계정 정보"""
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
                'description': "모든 계정으로 로그인 가능 (취약함)"
            },
            {
                'payload': "admin' --",
                'description': "비밀번호 우회 (취약함)"
            }
        ]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=5000)

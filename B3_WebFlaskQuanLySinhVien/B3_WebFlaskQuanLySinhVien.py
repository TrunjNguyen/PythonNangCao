from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import psycopg2
from psycopg2 import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = 'http://localhost:5000 '  

# Cấu hình database
DB_CONFIG = {
    "database": "TestDB",
    "user": "postgres",
    "password": "123456",
    "host": "localhost",
    "port": "5432"
}

# Decorator để kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Kết nối database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "Thanhtrung" and password == "123456":
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Sai tài khoản hoặc mật khẩu!")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# API endpoints
@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM sinh_vien")
        students = cursor.fetchall()
        return jsonify([{"ma_sv": row[0], "ho_ten": row[1]} for row in students])
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students', methods=['POST'])
@login_required
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sinh_vien (ma_sv, ho_ten) VALUES (%s, %s)",
            (data['ma_sv'], data['ho_ten'])
        )
        conn.commit()
        return jsonify({"message": "Thêm sinh viên thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students/<ma_sv>', methods=['PUT'])
@login_required
def update_student(ma_sv):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE sinh_vien SET ho_ten = %s WHERE ma_sv = %s",
            (data['ho_ten'], ma_sv)
        )
        conn.commit()
        return jsonify({"message": "Cập nhật sinh viên thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/api/students/<ma_sv>', methods=['DELETE'])
@login_required
def delete_student(ma_sv):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM sinh_vien WHERE ma_sv = %s", (ma_sv,))
        conn.commit()
        return jsonify({"message": "Xóa sinh viên thành công"})
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
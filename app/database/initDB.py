import sqlite3
import os

def initDB(db_path="app/database/db/emotion_system.db"):
    conn = None  # 提前定义 conn，防止 finally 中引用报错

    try:
        # 创建数据库目录（如果不存在）
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        is_new_db = not os.path.exists(db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ 数据库连接成功！")

        if is_new_db:
            print("📦 检测到数据库首次创建，正在初始化表结构...")

            # 创建表结构
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    account TEXT UNIQUE,
                    email TEXT UNIQUE,
                    phone TEXT UNIQUE,
                    password_hash TEXT,
                    gender TEXT,
                    age INTEGER,
                    user_type TEXT,
                    work_unit TEXT,
                    created_at DATETIME
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Children (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    nickname TEXT,
                    birthday DATE,
                    notes TEXT,
                    created_at DATETIME,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ChildGuardians (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_id INTEGER,
                    guardian_id INTEGER,
                    relation TEXT,
                    FOREIGN KEY (child_id) REFERENCES Children(id),
                    FOREIGN KEY (guardian_id) REFERENCES Users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ChildTherapists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_id INTEGER,
                    therapist_id INTEGER,
                    assigned_at DATETIME,
                    FOREIGN KEY (child_id) REFERENCES Children(id),
                    FOREIGN KEY (therapist_id) REFERENCES Users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS EmotionRecords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_id INTEGER,
                    source_type TEXT,
                    recognized_emotion TEXT,
                    timestamp DATETIME,
                    confidence REAL,
                    raw_data_path TEXT,
                    notes TEXT,
                    FOREIGN KEY (child_id) REFERENCES Children(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS MultimodalResults (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_id INTEGER,
                    face_emotion TEXT,
                    audio_emotion TEXT,
                    text_emotion TEXT,
                    final_emotion TEXT,
                    timestamp DATETIME,
                    fusion_strategy TEXT,
                    confidence REAL,
                    FOREIGN KEY (child_id) REFERENCES Children(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TreatmentSessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_id INTEGER,
                    therapist_id INTEGER,
                    start_time DATETIME,
                    end_time DATETIME,
                    total_questions INTEGER,
                    correct_answers INTEGER,
                    notes TEXT,
                    FOREIGN KEY (child_id) REFERENCES Children(id),
                    FOREIGN KEY (therapist_id) REFERENCES Users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS EmotionQuestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    question_text TEXT,
                    expected_emotion TEXT,
                    child_answer TEXT,
                    is_correct BOOLEAN,
                    created_at DATETIME,
                    FOREIGN KEY (session_id) REFERENCES TreatmentSessions(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Message (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    receiver_id INTEGER,
                    content TEXT,
                    sent_at DATETIME,
                    FOREIGN KEY (sender_id) REFERENCES Users(id),
                    FOREIGN KEY (receiver_id) REFERENCES Users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loginLogs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    login_time DATETIME,
                    ip_address TEXT,
                    device_info TEXT,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            ''')

            conn.commit()
            print("✅ 数据库初始化完成！")
        else:
            print("ℹ️ 数据库已存在，跳过表结构初始化。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        if conn:
            conn.close()
            print("🔒 数据库连接已关闭！")

# 调用初始化
initDB()

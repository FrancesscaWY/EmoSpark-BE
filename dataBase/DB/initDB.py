import sqlite3

def initDB(db_path="emotion_system.db"):
    try:
        # 创建数据库连接
        conn = sqlite3.connect('./DB/emotion_system.db')
        cursor = conn.cursor()

        print("数据库连接成功！")
        # 创建 Users 表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
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

        # 创建 Children 表
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

        # 创建 ChildGuardians 表
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

        # 创建 ChildTherapists 表
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

        # 创建 EmotionRecords 表
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

        # 创建 MultimodalResults 表
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

        # 创建 TreatmentSessions 表
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

        # 创建 EmotionQuestions 表
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

        # 创建 Message 表
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

        # 创建 loginLogs 表
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

        # 提交所有更改
        conn.commit()
        print("✅ 数据库初始化完成！")

    except Exception as e:
        print(f"发生错误: {e}")  # 捕获并打印错误信息
    finally:
        # 关闭连接
        if conn:
            conn.close()
            print("数据库连接已关闭！")

# 调用函数进行初始化
initDB()

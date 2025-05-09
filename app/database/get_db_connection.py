# app/database/db.py
import sqlite3
import os

def get_db_connection():
    """
    创建并返回数据库连接对象
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'db', 'emotion_system.db')
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 将查询结果以字典的形式返回
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise  # 抛出异常，供调用处捕获

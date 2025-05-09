from datetime import datetime

from charset_normalizer.md__mypyc import exports
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import sqlite3
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from starlette.responses import Response
import os
import logging
from app.database.get_db_connection import get_db_connection
# from typing_extensions import deprecated

# from test.demoTest import response

# app = FastAPI()
router = APIRouter()
# def init_routes(app: FastAPI):
#     @app.get("/spark/api/check_account")
#     async def check_account():
#         return {"message": "Account checked"}
# 密码加密
pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

# def get_db_connection():
#     db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'db', 'emotion_system.db')
#     try:
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row
#         return conn
#     except Exception as e:
#         print(f"Database connection error: {e}")
#         raise

# 注册请求数据模型
class RegisterRequest(BaseModel):
    username: str
    age: int
    gender: str
    userType: str
    phone: str
    email: str
    account: str
    password: str
    work_unit: Optional[str] = None

# 检查账号是否已存在
@router.post("/check_account")
async def check_account(account: str):
    # 手动设置 CORS 响应头
    # response.headers["Access-Control-Allow-Origin"] = "http://localhost:3004"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

    # 查询账号是否存在
        cursor.execute('SELECT 1 FROM Users WHERE account = ?', (account,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return JSONResponse(content={"exists":True})
        else:
            return JSONResponse(content={"exists":False})

    except sqlite3.DatabaseError as e:
        # 如果是数据库错误，记录日志并返回更明确的错误信息
        logging.error(f"Database error: {str(e)}")
        return JSONResponse(content={"error": "Database connection failed"}, status_code=500)

    except Exception as e:
        # 处理其他类型的错误
        logging.error(f"Unexpected error: {str(e)}")
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)

# 注册 API
@router.post("/register")
async def register_user(request: RegisterRequest):
    # 密码加密
    hashed_password = pwd_context.hash(request.password)

    try:
        # 连接到数据库并插入数据
        conn = get_db_connection()
        cursor = conn.cursor()

        # 插入注册用户数据

        cursor.execute('''
            INSERT INTO Users (username, account, email, phone, password_hash, gender, age, user_type, work_unit, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.username,
            request.account,
            request.email,
            request.phone,
            hashed_password,
            request.gender,
            request.age,
            request.userType,
            request.work_unit,
            datetime.now()
        ))

        conn.commit()
        conn.close()

        return JSONResponse(content={"success": True, "message":"注册成功"},status_code=200)
    #
    # except sqlite3.IntegrityError as e:
    #     return JSONResponse(content={"success": False, "message": "用户名、邮箱或手机号已存在"},status_code=500)
    #
    # except Exception as e:
    #     return JSONResponse(content={"success": False, "message": str(e)},status_code=500)
    except sqlite3.IntegrityError as e:
        logging.error(f"Database integrity error: {e}")
        return JSONResponse(content={"success": False, "message": "用户名、邮箱或手机号已存在"}, status_code=400)

    except sqlite3.DatabaseError as e:
        logging.error(f"Database error: {e}")
        return JSONResponse(content={"success": False, "message": "数据库错误"}, status_code=500)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return JSONResponse(content={"success": False, "message": f"服务器内部错误: {str(e)}"}, status_code=500)

class LoginRequest(BaseModel):
    userAccount: str
    userType: str
    password: str

@router.post("/login")
async def login_user(data: LoginRequest):
    user_account = data.userAccount
    user_type = data.userType
    password = data.password

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM Users WHERE (account = ? OR phone = ? OR email = ?) AND user_type = ?''',(user_account,user_account,user_account,user_type))
        user = cursor.fetchone()
        conn.close()

        if user:
            if pwd_context.verify(password, user['password_hash']):
                return JSONResponse(content={"success":True,"message":"登录成功"},status_code=200)
            else:
                return JSONResponse(content={"success":False,"message":"密码错误"},status_code=400)
        else:
            return JSONResponse(content={"success":False,"message":"用户不存在"},status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": f"内部错误: {str(e)}"}, status_code=500)

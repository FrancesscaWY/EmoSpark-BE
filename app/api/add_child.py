from audeer import deprecated
from fastapi import FastAPI, HTTPException,Depends,APIRouter
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime
from passlib.context import CryptContext
from app.database.get_db_connection import get_db_connection
from fastapi.responses import JSONResponse
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
# def hash_password(password:str)->str:
#     return pwd_context.hash(password)
# def verify_password(plain_password: str,hash_password:str)->bool:
#     return pwd_context.verify(plain_password,hash_password)

class AddChildRequest(BaseModel):
    parent_id: int
    name: str
    nickname: str
    gender: int
    birthday: Optional[int]
    account: str
    password: str
    note: Optional[str]=None
    relation: Optional[str] = "家长"

@router.post('/parents/add_child')
def add_child(req: AddChildRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        birthday_date = (
            datetime.utcfromtimestamp(req.birthday / 1000).date().isoformat()
            if req.birthday else None
        )
        try:
            hashed_password = pwd_context.hash(req.password)

            cursor.execute('''
                INSERT INTO Users(username,account,password_hash,gender,user_type,created_at)
                VALUES(?,?,?,?,?,?)
            ''',(
                req.name,
                req.account,
                hashed_password,
                '男' if req.gender == 1 else '女',
                'child',
                now
            ))

            user_id = cursor.lastrowid
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise HTTPException(status_code=400,detail=f"账号冲突或缺失字段：{e}")
        try:
            cursor.execute('''
            INSERT INTO Children(user_id, nickname, birthday,notes,created_at)
            VALUES(?,?,?,?,?)
            ''',(
                user_id,
                req.nickname,
                birthday_date,
                req.note,
                now
            ))
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"儿童信息保存失败:{e}")

        try:
            cursor.execute('''
                INSERT INTO ChildGuardians(child_id, guardian_id,relation)
                VALUES(?,?,?)
                ''',(
                    user_id,
                    req.parent_id,
                    req.relation or "家长"
                ))
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise HTTPException(status_code=400,detail=f"关联保存失败：{e}")
        # 提交事务
        conn.commit()
        # 返回标准 JSON
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "儿童账号及关联创建成功",
                "child_id": user_id,
                "guardian_id": req.parent_id,
                "relation": req.relation or "家长",
            },
        )
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="用户名已存在或字段冲突")
    finally:
        conn.close()


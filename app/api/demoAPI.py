from fastapi import FastAPI
from pydantic import BaseModel
from app.database import get_db_connection
app = FastAPI()

# 定义请求体格式
class Number(BaseModel):
    value: int

@app.post("/check_even")
async def check_even(number: Number):
    # 判断是否为偶数
    if number.value % 2 == 0:
        return {"number": number.value, "is_even": True}
    else:
        return {"number": number.value, "is_even": False}


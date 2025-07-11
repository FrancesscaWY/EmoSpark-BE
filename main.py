from sys import prefix

from fastapi import FastAPI
from app.api import register  # 确保正确导入 register.py 中的 router（APIRouter 实例）
from app.api import  add_child
from app.api import recognize_emotion
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 允许的来源
# origins = [
#     "http://localhost:3004",  # 你前端的端口
#     "http://127.0.0.1:3004"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3004"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router, prefix="/spark/api")
app.include_router(add_child.router, prefix="/spark/api")
app.include_router(recognize_emotion.router,prefix="/spark/api")

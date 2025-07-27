# 从 fastapi 库中导入 FastAPI 类
from dotenv import load_dotenv
from fastapi import FastAPI
from src.test import router

# 加载 .env 文件中存储的密钥
load_dotenv()

# 创建 FastAPI 实例
app = FastAPI()


app.include_router(router, prefix="/api/v1")

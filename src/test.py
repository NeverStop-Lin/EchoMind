from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read_root():
    print("--- 正在处理根路径 / 的请求 ---")
    return {"message": "Hello, FastAPI222!"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # 打印一些有用的信息
    print(f"请求已进入 read_item 函数")
    print(f"接收到的路径参数 item_id: {item_id} (类型: {type(item_id)})")
    print(f"接收到的查询参数 q: {q} (类型: {type(q)})")

    if q:
        print("参数 q 存在，准备返回...")
    else:
        print("参数 q 不存在")

    # 在返回前打印一条最终信息
    print("--- 请求处理完毕，即将发送响应 ---")

    return {"item_id": item_id, "q": q}

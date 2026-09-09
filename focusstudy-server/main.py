import json
import os
import time
from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ===== 应用初始化 =====
app = FastAPI(title="FocusStudy API", version="1.0.0")

# 跨域配置：允许本地前端开发服务器访问
# （部署到线上后，把线上前端域名也加进 allow_origins）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 数据存储：JSON 文件（无需数据库） =====
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def read_json(filename: str, default: list):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filename: str, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def new_id() -> int:
    return int(time.time() * 1000)


# ===== Pydantic 模型：校验前端传来的数据 =====
class TaskIn(BaseModel):
    name: str
    subject: str = "未分类"
    priority: str = "medium"
    deadline: str = "未设置"


class RecordIn(BaseModel):
    taskName: str = "未绑定任务"
    subject: str = "未分类"
    minutes: int
    date: str = ""


# ===== 任务接口 =====
@app.get("/api/tasks")
def get_tasks():
    return read_json("tasks.json", [])


@app.post("/api/tasks")
def create_task(task: TaskIn):
    tasks = read_json("tasks.json", [])
    new_task = task.model_dump()
    new_task["id"] = new_id()
    new_task["done"] = False
    tasks.append(new_task)
    write_json("tasks.json", tasks)
    return new_task


# ===== 专注记录接口 =====
@app.get("/api/records")
def get_records():
    return read_json("records.json", [])


@app.post("/api/records")
def create_record(record: RecordIn):
    records = read_json("records.json", [])
    new_record = record.model_dump()
    new_record["id"] = new_id()
    if not new_record["date"]:
        new_record["date"] = date.today().isoformat()
    records.append(new_record)
    write_json("records.json", records)
    return new_record


# ===== 统计接口 =====
@app.get("/api/stats")
def get_stats():
    records = read_json("records.json", [])

    total_minutes = sum(r.get("minutes", 0) for r in records)

    # 按科目分组
    subject_map = {}
    for r in records:
        s = r.get("subject", "未分类")
        subject_map[s] = subject_map.get(s, 0) + r.get("minutes", 0)

    # 按日期分组
    day_map = {}
    for r in records:
        d = r.get("date", "未知")
        day_map[d] = day_map.get(d, 0) + r.get("minutes", 0)

    return {
        "total_minutes": total_minutes,
        "total_count": len(records),
        "by_subject": subject_map,
        "by_date": day_map,
    }


# ===== 根路径：健康检查 =====
@app.get("/")
def root():
    return {"message": "FocusStudy API 运行中", "docs": "/docs"}

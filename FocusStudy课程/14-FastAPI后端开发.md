# 第 14 课：FastAPI 后端开发

> 目标：创建 focusstudy-server 后端项目，用 FastAPI 实现任务和统计的 API 接口，数据存 JSON 文件。
> 耗时：约 2 天
> 完成后你的项目就是"有前有后"的全栈项目了！

---

## 📌 这节课你会学到

1. 后端 / API / 接口 到底是干什么的
2. 虚拟环境（venv）是什么、为什么必须用
3. FastAPI 项目结构 + 第一个接口
4. GET / POST 接口写法 + Pydantic 数据校验
5. 用 JSON 文件做存储
6. 用浏览器 / curl 测试接口

---

## 🧠 概念讲解

### 1. API 是什么？（复习餐厅比喻）

**API（应用程序接口）** = 后厨的"取餐窗口"：
- 前端（大堂服务员）对窗口喊："给我一份今日任务"（**GET 请求**）
- 后厨（后端）把菜端出来：返回 JSON 数据
- 前端也可以喊："新增一个任务"（**POST 请求**，带着要加的数据）

```
前端 Vue  ──GET /api/tasks──►  后端 FastAPI  ──读文件──►  records.json
   ▲                             │
   └───────── JSON 数据 ◄────────┘
```

**HTTP 方法**：
- `GET`：取数据（不改变服务器状态）
- `POST`：提交新数据（创建）
- `PUT` / `PATCH`：更新
- `DELETE`：删除

### 2. 虚拟环境 venv：给每个项目一个"独立 Python 房间"

不同项目需要不同版本的依赖包，直接在系统里装会互相打架。**venv** 给每个项目开一个独立房间：

```powershell
cd "E:\本科\Beginner's-Paradise‑FirstCommit"
python -m venv focusstudy-server/.venv        # 创建虚拟环境（在项目文件夹里）
```

以后要装依赖、运行项目，都先"激活"这个房间：
- PowerShell：`.venv\Scripts\Activate.ps1`
- 激活后终端前缀会出现 `(.venv)`，表示你在这个房间里

### 3. FastAPI 最小示例（先看懂再动手）

```python
from fastapi import FastAPI

app = FastAPI()          # 创建应用

@app.get("/hello")       # 装饰器：注册一个 GET 接口
def hello():
    return {"message": "你好，FocusStudy"}
```

`@app.get("/hello")` 是**装饰器**——它"装饰"了下面的函数，告诉 FastAPI："当有人访问 /hello 时，执行这个函数"。

启动：`uvicorn main:app --reload`（`--reload` 改代码自动重启）

---

## 🛠 动手做

### 第一步：创建项目骨架

```powershell
cd "E:\本科\Beginner's-Paradise‑FirstCommit"
python -m venv focusstudy-server/.venv
cd focusstudy-server
.venv\Scripts\Activate.ps1        # 激活虚拟环境（终端出现 (.venv)）
pip install fastapi uvicorn       # 安装两个包（装进虚拟环境）
```

> 如果激活报"禁止运行脚本"，在 PowerShell 里执行一次：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，选 Y。

### 第二步：项目结构

```
focusstudy-server/
├── .venv/               # 虚拟环境（git 已忽略，别提交）
├── main.py              # FastAPI 应用 + 所有接口
├── data/
│   ├── tasks.json       # 任务数据（自动生成）
│   └── records.json     # 专注记录（自动生成）
└── requirements.txt     # 依赖清单（pip freeze 生成）
```

### 第三步：写 main.py（亲手敲！）

```python
import json
import os
from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ===== 应用初始化 =====
app = FastAPI(title="FocusStudy API", version="1.0.0")

# 跨域配置：允许前端 (http://localhost:5173) 调用（第 15 课细讲）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 数据存储：读写 JSON 文件 =====
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

# ===== Pydantic 模型：校验前端传来的数据 =====
class TaskIn(BaseModel):
    name: str                      # 必填
    subject: str = "未分类"         # 可选，带默认值
    priority: str = "medium"
    deadline: str = "未设置"

class RecordIn(BaseModel):
    taskName: str = "未绑定任务"
    subject: str = "未分类"
    minutes: int                   # 必填
    date: str = ""

# ===== 任务接口 =====
@app.get("/api/tasks")
def get_tasks():
    return read_json("tasks.json", [])

@app.post("/api/tasks")
def create_task(task: TaskIn):
    tasks = read_json("tasks.json", [])
    new_task = task.model_dump()          # 校验过的数据转成字典
    new_task["id"] = int(__import__("time").time() * 1000)   # 生成唯一 id
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
    new_record["id"] = int(__import__("time").time() * 1000)
    if not new_record["date"]:
        new_record["date"] = date.today().isoformat()
    records.append(new_record)
    write_json("records.json", records)
    return new_record

# ===== 统计接口（复用第 13 课的逻辑） =====
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
```

### 第四步：启动并测试

```powershell
uvicorn main:app --reload
```

看到 `Uvicorn running on http://127.0.0.1:8000` 就成功了。

**测试方式 1（浏览器）**：打开 http://127.0.0.1:8000/docs —— **FastAPI 自带交互式接口文档**！你可以直接在里面点"Try it out"测试每个接口。这也是 Demo 视频的好素材。

**测试方式 2（curl）**：另开一个终端：

```powershell
# 获取任务列表
curl http://127.0.0.1:8000/api/tasks

# 新增任务
curl -X POST http://127.0.0.1:8000/api/tasks -H "Content-Type: application/json" -d "{\"name\":\"测试任务\",\"subject\":\"数学\"}"

# 查看统计
curl http://127.0.0.1:8000/api/stats
```

**测试方式 3（POSTMAN / 浏览器扩展）**：装个 Postman 图形化测试更直观（可选）。

### 第五步：生成 requirements.txt + 提交

```powershell
pip freeze > requirements.txt
```

```powershell
git add .
git commit -m "feat: FastAPI 后端完成（任务/记录/统计接口 + JSON存储）"
git push
```

---

## ✅ 本节验收标准

- [ ] `uvicorn main:app --reload` 能启动
- [ ] /docs 页面能打开，5 个接口都能测试通过
- [ ] 新增任务后，`data/tasks.json` 里出现数据
- [ ] /api/stats 返回正确的 total_minutes / by_subject / by_date
- [ ] 能解释 venv 是干什么的、为什么用
- [ ] 能说出 GET 和 POST 的区别

---

## ⚠️ 常见坑

- **坑 1**：pip 安装很慢/失败 → 用国内镜像：`pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple`
- **坑 2**：`uvicorn` 不是内部命令 → 没激活虚拟环境。先 `.venv\Scripts\Activate.ps1`。
- **坑 3**：改代码不生效 → 确认启动时带了 `--reload`。
- **坑 4**：Pydantic 校验报错（422）→ 前端传的字段名和模型定义不一致，检查拼写。
- **坑 5**：前端访问接口被 CORS 拦截 → 第 15 课专门解决，先记住"跨域"这个词。

---

## 📝 学习日志打卡

```
今天：完成了后端全部接口，/docs 里能直接测试，很有成就感。
困难：uvicorn 找不到命令，发现是没激活虚拟环境，激活后就好了。
明天：前后端联调，让 Vue 页面真正调用这些接口。
```

---

## 🔜 下一课预告

**第 15 课**：前后端联调！解决跨域问题，在 Vue 里用 fetch 调用后端接口，打通数据流。

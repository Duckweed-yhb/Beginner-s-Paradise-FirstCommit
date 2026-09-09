# 第 13 课：Python 基础 — 后端语言

> 目标：掌握 Python 核心语法（变量 / 类型 / 条件 / 循环 / 函数 / 列表 / 字典 / JSON 读写），并写一个"统计专注记录"的命令行脚本。
> 耗时：约 1 天
> 好消息：你已经会 JavaScript 了，Python 的语法逻辑几乎一样，只是"换了个写法"。

---

## 📌 这节课你会学到

1. Python 和 JavaScript 的"对照表"（最快的学法！）
2. 列表 / 字典（对应 JS 的数组 / 对象）
3. 函数定义（缩进是 Python 的灵魂）
4. 读写 JSON 文件（后端存储的核心）
5. 动手：统计脚本——读取专注记录 JSON，算出总时长和科目排行

---

## 🧠 概念讲解

### 1. Python vs JavaScript 对照表（重点！）

| 概念 | JavaScript | Python |
|---|---|---|
| 定义变量 | `let x = 1` | `x = 1`（直接写，无关键字） |
| 常量 | `const x = 1` | 约定全大写 `X = 1`（无强制） |
| 字符串 | `"abc"` / `'abc'` | `"abc"` / `'abc'` 一样 |
| 注释 | `// 注释` | `# 注释` |
| 数组/列表 | `[1,2,3]` | `[1,2,3]`（叫 list） |
| 对象/字典 | `{name:"小明"}` | `{"name": "小明"}`（叫 dict） |
| 条件 | `if (a > 0) { }` | `if a > 0:` |
| 循环 | `for (let i=0; i<n; i++)` / `for (const x of arr)` | `for i in range(n)` / `for x in arr` |
| 函数 | `function f(a) { return a*2 }` | `def f(a): return a * 2` |
| 布尔 | `true / false / null` | `True / False / None` |

**Python 的特殊之处：用缩进（空格）表示代码块**，不用花括号：

```python
score = 85
if score >= 90:
    print("优秀")      # 缩进 4 个空格 = 属于 if 的代码块
    print("继续保持")
else:
    print("加油")
print("这句话在 if 外面")   # 缩进回到顶格 = 不属于 if
```

> ⚠️ 缩进错了程序直接报错。VSCode 里 Tab 键会自动转成缩进，很省心。

### 2. 列表与字典（后端数据处理的主角）

```python
# 列表（对应 JS 数组）
subjects = ["数学", "英语", "物理"]
print(subjects[0])        # 数学
subjects.append("化学")   # 末尾追加
print(len(subjects))      # 4

# 字典（对应 JS 对象）
task = {"id": 1, "name": "写数学作业", "done": False}
print(task["name"])       # 写数学作业
task["done"] = True       # 修改
```

### 3. 读写 JSON 文件（后端存储核心）

后端要把数据存到文件里（比赛用 JSON 文件，不搞数据库）：

```python
import json

# ===== 写入 =====
data = [
    {"subject": "数学", "minutes": 25, "date": "2026-09-08"},
    {"subject": "英语", "minutes": 25, "date": "2026-09-08"},
]

with open("records.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# ensure_ascii=False 让中文正常显示；indent=2 让文件易读

# ===== 读取 =====
with open("records.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded[0]["subject"])   # 数学
```

> `with open(...) as f:` 是 Python 的"用完自动关闭文件"写法，养成习惯。

---

## 🛠 动手做：专注记录统计脚本

### 第一步：准备数据文件

在项目根目录新建 `practice/python/` 文件夹，在里面新建 `records.json`：

```json
[
  {"subject": "数学", "minutes": 25, "date": "2026-09-06"},
  {"subject": "数学", "minutes": 50, "date": "2026-09-07"},
  {"subject": "英语", "minutes": 25, "date": "2026-09-07"},
  {"subject": "物理", "minutes": 25, "date": "2026-09-08"},
  {"subject": "英语", "minutes": 25, "date": "2026-09-08"}
]
```

### 第二步：写统计脚本 `stats.py`（亲手敲！）

```python
import json

# ===== 1. 读取 JSON 文件 =====
with open("records.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# ===== 2. 统计总时长 =====
total_minutes = 0
for r in records:
    total_minutes += r["minutes"]
print(f"总专注时长：{total_minutes} 分钟（{total_minutes / 60:.1f} 小时）")

# ===== 3. 按科目分组求和（对应第 12 课 JS 的 groupBySubject） =====
subject_map = {}          # 字典当"分组桶"
for r in records:
    subject = r["subject"]
    if subject not in subject_map:
        subject_map[subject] = 0
    subject_map[subject] += r["minutes"]

# ===== 4. 排序并输出排行（sorted 按值降序） =====
ranking = sorted(subject_map.items(), key=lambda item: item[1], reverse=True)
print("\n科目专注排行：")
for subject, minutes in ranking:
    print(f"  {subject}: {minutes} 分钟")

# ===== 5. 找出专注最多的一天 =====
day_map = {}
for r in records:
    day_map[r["date"]] = day_map.get(r["date"], 0) + r["minutes"]
best_day = max(day_map.items(), key=lambda item: item[1])
print(f"\n最专注的一天：{best_day[0]}，专注了 {best_day[1]} 分钟")
```

### 第三步：运行

```powershell
cd "E:\本科\Beginner's-Paradise‑FirstCommit\practice\python"
python stats.py
```

**预期输出**：
```
总专注时长：150 分钟（2.5 小时）

科目专注排行：
  数学: 75 分钟
  英语: 50 分钟
  物理: 25 分钟

最专注的一天：2026-09-07，专注了 75 分钟
```

### 改一改

1. 往 `records.json` 加两条数据，重跑脚本，所有数字应该自动更新
2. 把排序改成升序（`reverse=False`）
3. 用 `f-string` 格式化：试试 `print(f"你好，{name}")` 这种写法（Python 3.6+ 最推荐）

---

## ✅ 本节验收标准

- [ ] 脚本正确统计总时长 / 科目排行 / 最专注的一天
- [ ] 能说出 JS 和 Python 的 3 个语法差异
- [ ] 会读写 JSON 文件（json.dump / json.load）
- [ ] 能解释 `with open(...) as f` 的作用
- [ ] 遇到缩进报错（IndentationError）能自己修好

---

## ⚠️ 常见坑

- **坑 1**：`IndentationError`（缩进错误）→ 检查代码块是否统一用 4 空格缩进。
- **坑 2**：中文字符在文件里乱码 → 打开文件一律加 `encoding="utf-8"`。
- **坑 3**：`json.load` 报错 → 确认 JSON 文件格式正确（双引号、无尾逗号）。
- **坑 4**：`print(f"...")` 里花括号写错 → f-string 里用 `{}` 包变量名，`{{` 才是字面花括号。

---

## 📝 学习日志打卡

```
今天：用 Python 写出了统计脚本，感觉和 JS 很像，就是写法不同。
困难：第一次缩进报错，改成统一 4 空格就好了。
明天：学 FastAPI，把统计逻辑变成网页能调用的接口。
```

---

## 🔜 下一课预告

**第 14 课**：FastAPI 后端开发！创建 focusstudy-server，写任务和统计的 API 接口，浏览器和前端都能调用。

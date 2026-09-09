# 第 17 课：README 与线上部署

> 目标：写出专业的英文 README（评委第一眼看的文档），把前端部署上线生成可访问链接（比赛推荐加分项）。
> 耗时：约 2 天

---

## 📌 这节课你会学到

1. README 为什么重要、专业 README 的结构
2. 英文 README 的写法（用模板填空）
3. AI 使用声明怎么写（比赛规则强制）
4. 部署方案对比：Vercel / Netlify / GitHub Pages
5. 部署流程实操

---

## 🧠 概念讲解

### 1. README 为什么重要

README 是评委打开你 GitHub 仓库**第一眼看到**的东西。Presentation & Communication 占 20%，README 是其中的大头。**写不清楚运行步骤 = 评委跑不起来 = 白做。**

一个专业的 README 结构：

```
1. 项目名 + 一句话简介 + Logo/截图
2. 功能特性（Features）—— 用列表 + emoji
3. 技术栈（Tech Stack）
4. 截图（Screenshots）—— 强烈建议放！
5. 本地运行步骤（Getting Started）—— 评委照着能跑
6. 项目结构（Project Structure）
7. AI 使用声明（AI Usage Disclosure）—— 比赛要求
8. 学习收获（What I Learned）—— 学习成长 30% 的加分点
9. License / 联系方式
```

### 2. 部署方案对比（选一个就行）

| 平台 | 适合 | 优点 | 免费额度 |
|---|---|---|---|
| **Vercel** | 前端项目 | 一键部署、自动 HTTPS、和 GitHub 联动 | 个人免费 |
| **Netlify** | 前端项目 | 拖拽部署、简单 | 个人免费 |
| **GitHub Pages** | 纯静态 | 不用注册新账号 | 免费 |

> 本课用 **Vercel**（最简单，还能给评委演示自动部署）。后端部署（Render）可选做，见"进阶"。

---

## 🛠 动手做

### 第一步：准备截图

1. 启动项目，分别截 3 张图：任务页 / 计时器页 / 统计页
2. 存到 `focusstudy-web/src/assets/screenshots/`（或项目根目录 `screenshots/`）
3. 图片命名：`tasks.png`、`timer.png`、`stats.png`

### 第二步：写英文 README

在 **focusstudy-web 项目根目录**新建 `README.md`，用下面的模板填（**不要直接抄，改成你自己的话**，评委看得出来）：

```markdown
# 🍅 FocusStudy

A lightweight student focus study management system with a Pomodoro timer,
task management, and learning data visualization — helping students plan,
focus, and understand where their study time goes.

## ✨ Features

- 📋 **Task Management**: add tasks with subject, priority and deadline;
  mark as done, edit or delete
- ⏱️ **Pomodoro Focus Timer**: customizable focus/break sessions with
  start / pause / reset, and a completion notification
- 📊 **Data Visualization**: daily & weekly focus duration bar chart,
  subject share pie chart, completion summary (ECharts)
- 💾 **Local-first storage**: tasks & focus records saved in browser
  localStorage, with a FastAPI backend as the data service

## 🛠 Tech Stack

- Frontend: Vue 3 + Vite + Element Plus + ECharts
- Backend: Python + FastAPI
- Storage: localStorage + JSON files (no database required)

## 🚀 Getting Started

### Prerequisites
- Node.js >= 18
- Python >= 3.10

### 1. Run the frontend
```bash
cd focusstudy-web
npm install
npm run dev
# open http://localhost:5173
```

### 2. Run the backend (optional, for full-stack mode)
```bash
cd focusstudy-server
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# API docs: http://127.0.0.1:8000/docs
```

> The app also works without the backend (localStorage fallback).

## 📁 Project Structure
```
focusstudy-web/     # Vue 3 frontend
focusstudy-server/  # FastAPI backend
```

## 🤖 AI Usage Disclosure

This project was built as a learning project. AI tools were used for:
- Explaining concepts and debugging errors
- Code review suggestions
The core business logic (task management, timer, statistics) was written
and understood by me during this hackathon.

## 🌱 What I Learned

- How the web works: frontend / backend / API / storage
- Building a real app with Vue 3, Element Plus and ECharts
- Writing and testing a FastAPI backend
- Debugging with browser DevTools
- Version control with Git & GitHub
```

### 第三步：部署到 Vercel

1. 注册/登录 https://vercel.com （推荐用 GitHub 账号登录）
2. 点 **Add New → Project**
3. **Import** 你的 GitHub 仓库 `focusstudy`
4. 框架选 **Vite**（Vercel 会自动识别）
5. Build Command 保持默认（`npm run build`），Output Directory 保持默认（`dist`）
6. 点 **Deploy**，等 1~2 分钟
7. 部署完成，你会得到一个网址：`https://focusstudy-xxxx.vercel.app`

**验证**：用手机浏览器打开这个网址，能访问、能操作！

### 第四步：把部署链接写进 GitHub 仓库简介

GitHub 仓库页面 → 右上 **Settings** → 左侧 **General** 拉到 **About** → 点 ✏️ 编辑 → Website 填部署链接 → Save。

### 第五步：提交 README

```powershell
git add .
git commit -m "docs: 添加英文 README"
git push
```

### 🔥 进阶（可选，加分）：后端也部署

用 **Render**（https://render.com）免费部署 FastAPI：
1. 新建 Web Service，连 GitHub 仓库
2. Root Directory 填 `focusstudy-server`，Build Command 填 `pip install -r requirements.txt`，Start Command 填 `uvicorn main:app --host 0.0.0.0 --port 10000`
3. 部署后把 CORS 的 `allow_origins` 改成你的前端部署地址

---

## ✅ 本节验收标准

- [ ] focusstudy-web/README.md 存在且是英文、结构完整
- [ ] README 里有 3 张截图
- [ ] AI 使用声明已写
- [ ] Vercel 部署成功，手机能打开
- [ ] GitHub 仓库简介里有部署链接
- [ ] 按 README 的步骤，在一个干净环境能跑起来（或明确写了依赖）

---

## ⚠️ 常见坑

- **坑 1**：Vercel 构建失败 → 看构建日志（Build Logs），常见是 node 版本问题，在 Vercel 项目设置里把 Node 版本调到 20+。
- **坑 2**：部署后页面空白 → 路由用了 `createWebHistory`，刷新子路径 404。Vercel 需要加 `vercel.json` 重写配置（或改用 hash 路由）。**快速方案**：Vercel 部署的 Vite 项目一般会自动处理，若 404 再加：
  ```json
  { "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
  ```
  保存为 `focusstudy-web/vercel.json` 重新部署。
- **坑 3**：截图路径不对显示裂图 → 用相对路径 `./screenshots/tasks.png`，且确认图片已 push。
- **坑 4**：README 里代码块格式错乱 → 嵌套代码块注意缩进，用 4 个空格。

---

## 📝 学习日志打卡

```
今天：写了英文 README，项目部署上线了，手机都能打开！
困难：第一次部署构建失败，看日志发现是 Node 版本问题，调高后成功。
明天：录 Demo 视频，准备提交比赛！
```

---

## 🔜 下一课预告

**第 18 课**：Demo 视频与比赛提交！写视频脚本、录制 3-5 分钟演示、填 Devpost 提交表单、完成所有收尾检查。

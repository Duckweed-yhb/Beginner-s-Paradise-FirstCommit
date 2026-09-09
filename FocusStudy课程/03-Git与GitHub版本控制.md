# 第 3 课：Git 与 GitHub 版本控制

> 目标：学会 Git 三连招（add / commit / push），建立你的公开 GitHub 仓库。
> 耗时：约 1 天
> 为什么重要：黑客松要求"公开 GitHub 仓库 + 全程提交记录"，提交记录就是证明"代码是比赛期间写的"的铁证。评委真的会看！

---

## 📌 这节课你会学到

1. Git 和 GitHub 的区别（一个是工具，一个是网站）
2. 工作区 → 暂存区 → 仓库 的"三棵树"模型
3. Git 三连招：`git add` / `git commit` / `git push`
4. 在 GitHub 上建公开仓库并关联本地
5. `.gitignore` 是什么、为什么需要

---

## 🧠 概念讲解

### 1. Git 和 GitHub 是什么关系？

- **Git**：装在你电脑上的**版本管理工具**。它给你的代码拍"快照"，每拍一次，以后都能回到那一刻。**快照 = commit（提交）**。
- **GitHub**：一个**存放代码的网站**。你把本地的快照传到 GitHub 上，代码就有了"公开的家"，评委和其他人都能看到。

> **类比**：Git 是你的"游戏存档系统"，GitHub 是把存档同步到"云端服务器"。

### 2. 三棵树模型（最重要的概念）

```
你的代码变更
     │
     ▼
┌────────────┐   git add   ┌────────────┐   git commit   ┌────────────┐
│  工作区     │ ──────────► │  暂存区     │ ────────────► │  本地仓库    │
│ (你改的文件) │             │ (准备打包的) │               │ (存档记录)   │
└────────────┘             └────────────┘               └────────────┘
                                                               │
                                                  git push      ▼
                                                          ┌────────────┐
                                                          │ GitHub 远程 │
                                                          └────────────┘
```

- **工作区**：你正在编辑的文件
- **暂存区**：你告诉 Git "这些文件我要打包"（`git add`）
- **仓库**：真正存下快照的地方（`git commit`）

**每天的习惯**：改了代码 → `git add .` → `git commit -m "描述"` →（晚上）`git push`。

---

## 🛠 动手做

### 第一步：设置你的"签名"（只做一次）

打开终端，输入（把名字邮箱换成你自己的，用 GitHub 注册邮箱）：

```powershell
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的邮箱@example.com"
```

### 第二步：在 GitHub 网页上创建公开仓库

1. 登录 https://github.com
2. 右上角 **+** → **New repository**
3. 填写：
   - Repository name：`focusstudy`（简短即可）
   - 选择 **Public**（比赛要求公开！）
   - **不要**勾选 "Add a README file"（我们本地已经有内容，避免冲突）
4. 点击 **Create repository**
5. 创建后页面会显示一串命令，**先别关页面**，记下你的仓库地址（形如 `https://github.com/你的用户名/focusstudy.git`）

### 第三步：把本地项目连上 GitHub

在 VSCode 终端里，进入你的项目文件夹（如果不在）：

```powershell
cd "E:\本科\Beginner's-Paradise‑FirstCommit"
```

然后依次执行：

```powershell
git init                        # 1. 在这个文件夹里初始化 Git
git add .                       # 2. 把所有文件加入暂存区
git commit -m "first commit: 项目文档与课程"   # 3. 拍下第一张快照
git branch -M main              # 4. 把主分支改名为 main（GitHub 默认叫 main）
git remote add origin https://github.com/你的用户名/focusstudy.git   # 5. 关联远程仓库（换成你的地址）
git push -u origin main         # 6. 推送到 GitHub
```

**第一次 push 会弹出登录窗口**：用浏览器登录 GitHub 授权即可。如果要求输入密码，用 **Personal Access Token**（见"常见坑 2"）。

### 第四步：验证

1. 打开 `https://github.com/你的用户名/focusstudy`
2. 你应该能看到 README.md、课程文件夹等所有文件
3. 点进文件夹，能看到你写的 `学习日志模板.md` 等

**成功了！你有了一个公开的 GitHub 仓库，这就是参赛的"证据仓库"。** 🎉

### 第五步：创建 .gitignore（现在养成好习惯）

新建文件 `.gitignore`（注意开头有个点，文件名就是 `.gitignore`），内容：

```
# 忽略临时文件与系统文件
node_modules/
dist/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
```

> `node_modules` 是以后安装的依赖包，非常大，**绝对不能传到 GitHub**。`.gitignore` 就是"黑名单"，告诉 Git 这些文件不用管。

然后把这次修改提交：

```powershell
git add .
git commit -m "add .gitignore"
git push
```

---

## ✅ 本节验收标准

- [ ] GitHub 上有公开仓库 `focusstudy`，能看到全部文件
- [ ] 会用三连招：`git add .` → `git commit -m "说明"` → `git push`
- [ ] `.gitignore` 已创建并提交
- [ ] 会看 `git status` 和 `git log`（自己试试这两个命令，看看输出）

---

## ⚠️ 常见坑

- **坑 1**：`git push` 报 "failed to push some refs" → 远程仓库有本地没有的文件（比如你勾选了 README）。解决：`git pull origin main --allow-unrelated-histories` 再 push。
- **坑 2**：push 时要求输密码但密码不对 → GitHub 已不支持密码 push，需要 **Personal Access Token**：GitHub → Settings → Developer settings → Personal access tokens → Generate new token，勾选 `repo` 权限，复制那串 token 当密码用。
- **坑 3**：`git commit` 后才发现写错字 → 用 `git commit --amend -m "新的说明"` 改最后一次提交说明。
- **坑 4**：不小心把 node_modules 传上去了 → 加进 `.gitignore` 后，用 `git rm -r --cached node_modules` 从 Git 里移除（本地文件还在）。

---

## 📝 学习日志打卡

```
今天：学会了 Git 三连招，我的代码第一次"上云"了。
困难：第一次 push 弹出登录，按提示用浏览器授权就成功了。
明天：开始学 HTML，给 FocusStudy 搭页面骨架。
```

---

## 🔜 下一课预告

**第 4 课**：HTML 基础。你将用 HTML 画出 FocusStudy 页面的"骨架"——标题、任务区、计时器区、统计区。

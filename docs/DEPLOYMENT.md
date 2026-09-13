# 🚀 线上部署方案

> 比赛里"线上可访问版本"是**加分项**（推荐但非强制）。
> 但做得好能明显提升 reviewers 的体验 —— 他们可能懒得本地跑，但一定会点开链接看。

---

## 先想清楚一件事：你要部署什么？

这个项目有两种部署形态，**选第一种就够**：

| 方案 | 部署内容 | 难度 | 数据能保存吗 | 推荐度 |
|---|---|---|---|---|
| **A. 只部署前端** | `focusstudy-web/dist` 静态文件 | ⭐ 很简单 | ✅ 保存在访问者自己的浏览器里 | ✅ **推荐** |
| B. 前后端都部署 | 前端 + FastAPI 常驻服务 | ⭐⭐⭐ 麻烦 | ✅ 保存到服务器 | 时间充裕再考虑 |

**为什么推荐 A？**
因为 FocusStudy 本来就是"离线优先"设计：`localStorage` 是权威数据源，后端只是同步目标。
所以只部署前端，**功能是完整的** —— 评委能建任务、跑计时器、看图表，数据也会留在他的浏览器里。
反而是方案 B 的免费后端方案通常有休眠、限流、冷启动问题，评委点开链接转圈 30 秒，比不部署还糟。

> README 里已经把"后端可选"写成明确的设计决策，所以只部署前端完全站得住脚，不是偷懒。

---

## 方案 A：部署前端（15 分钟搞定）

### 步骤 1：本地确认构建没问题

```powershell
cd focusstudy-web
npm run build
npm run preview      # 本地打开 http://localhost:4173 检查一遍
```

### 步骤 2：把仓库推到 GitHub（应该已经做了）

### 步骤 3A：用 Vercel（最推荐，对 Vue 支持最好）

1. 打开 <https://vercel.com> → 用 GitHub 账号登录
2. **Add New → Project** → 选中你的 `Beginner-s-Paradise-FirstCommit` 仓库
3. 关键配置（Vercel 不一定能自动识别子目录）：
   - **Root Directory**：`focusstudy-web` ← **必须改，否则找不到 package.json**
   - **Framework Preset**：`Vite`
   - **Build Command**：`npm run build`
   - **Output Directory**：`dist`
4. 点 **Deploy**，等 1 分钟
5. 拿到形如 `https://xxx.vercel.app` 的链接

### 步骤 3B：用 Netlify（备选）

1. <https://app.netlify.com> → **Add new site → Import an existing project**
2. 选 GitHub 仓库
3. 配置：
   - **Base directory**：`focusstudy-web`
   - **Build command**：`npm run build`
   - **Publish directory**：`focusstudy-web/dist`
4. Deploy

### 步骤 3C：用 GitHub Pages（你已经有 `Duckweed-yhb.github.io`，可以复用经验）

静态站最简单的做法是手动推 `dist`：

```powershell
cd focusstudy-web
npm run build

# 把 dist 内容推到 gh-pages 分支
cd dist
git init
git add -A
git commit -m "deploy: FocusStudy 线上版本"
git branch -M gh-pages
git remote add origin https://github.com/Duckweed-yhb/Beginner-s-Paradise-FirstCommit.git
git push -f origin gh-pages
```

然后到仓库 **Settings → Pages**，Source 选 `gh-pages` 分支。

> ⚠️ **注意**：如果部署在子路径（例如 `用户名.github.io/仓库名/`），
> `vite.config.js` 需要加 `base: "/仓库名/"`，否则资源 404、页面白屏。
> 用 Vercel/Netlify 部署在根路径则不需要改。

### 步骤 4：验证部署成功

打开链接，逐项确认：

- [ ] 页面能打开，顶部导航是番茄橙主题
- [ ] 能新增一个任务，刷新后任务还在
- [ ] 计时器能开始倒计时（可以先手动把时长改成 1 分钟来测）
- [ ] 统计页能画出图表
- [ ] 按 F12 看 Console，**没有红色报错**

> 部署后 `/api` 请求会 404，这是**预期行为**：任务页会显示
> "后端未启动：数据仅保存在本机浏览器，功能完全正常"。
> 这个提示是我刻意加的 —— 让评委一眼看懂"这不是坏了，是设计如此"。

---

## 方案 B：连后端一起部署（可选）

如果时间充裕，想让数据存在服务器上。

**前置改动**：后端目前把数据写在 `data/*.json`，很多免费平台的文件系统是临时的，
重启就丢。真要长期部署，得换成真实数据库或对象存储 —— 这超出本次参赛范围，
所以**建议只在前端加一行说明就好**。

真要试，可以看这些（都需要信用卡验证或付费，免费的会休眠）：

- **Render**：支持 Python Web Service，免费实例 15 分钟无访问会休眠
- **Railway**：部署简单，免费额度有限
- **PythonAnywhere**：有免费层，但需要手动配置 WSGI

部署后端后，还要改前端让它指向线上后端：
`build` 时通过环境变量注入 API 地址，或者在后端开好 CORS 允许你的 Vercel 域名。

> **我的建议**：本次比赛**不做方案 B**。把省下来的时间用来写好项目描述和录好 Demo 视频，
> 那两项（Presentation 20% + 项目描述）的收益远比多一个后端链接高。

---

## 附：部署前检查清单

- [ ] `npm run build` 本地成功，无报错
- [ ] `npm run preview` 页面功能正常
- [ ] 根目录 `README.md` 里的部署步骤与实际一致
- [ ] 仓库是 **public**（比赛要求公开仓库）
- [ ] `focusstudy-server/data/`、`node_modules/`、`.venv/` 没有被提交进仓库
- [ ] 部署完成后把链接填到 Devpost 的 "Try it out" 一栏

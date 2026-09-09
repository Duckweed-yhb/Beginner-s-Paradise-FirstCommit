# 第 9 课：Vite + Element Plus — 搭建项目框架

> 目标：创建 FocusStudy 的正式前端项目（focusstudy-web），理解项目结构，接入 Element Plus 组件库，搭出三页面的框架。
> 耗时：约 1 天
> 🎉 从这一课开始，你进入"正式开发"阶段！之前的都是练手。

---

## 📌 这节课你会学到

1. Vite 是什么、为什么用它
2. 用 Vite 创建 Vue3 项目、看懂项目目录
3. 单文件组件（SFC）的完整结构
4. 安装并接入 Element Plus 组件库
5. 用 Vue Router 搭出三个页面：任务 / 计时器 / 统计

---

## 🧠 概念讲解

### 1. Vite 是什么？

**Vite** 是前端项目的"开发服务器 + 打包工具"：
- 开发时：你改代码，浏览器**秒级刷新**（热更新 HMR）
- 上线时：把所有代码**打包**成浏览器能直接跑的文件

> 类比：Vite 是"工地总管"——开发时盯着你改的每一块砖实时刷新，完工时把所有材料打包成可交付的房子。

### 2. 单文件组件（SFC）长什么样

一个 `.vue` 文件 = 一个组件（页面的一块积木），三个部分：

```vue
<template>
  <!-- ① 页面结构（HTML + Vue 指令） -->
  <h1>{{ title }}</h1>
</template>

<script setup>
// ② 逻辑（JavaScript，setup 语法糖：不用写 return）
import { ref } from "vue";
const title = ref("FocusStudy");
</script>

<style scoped>
/* ③ 样式（scoped = 只对本组件生效，不污染全局） */
h1 { color: #ff6b35; }
</style>
```

### 3. Vue Router：多页面切换

一个网站要有"任务页 / 计时器页 / 统计页"，用 **Vue Router** 管"地址 → 页面"的映射：

```
http://localhost:5173/          → 首页（重定向到 /tasks）
http://localhost:5173/tasks     → 任务管理页
http://localhost:5173/timer     → 番茄计时器页
http://localhost:5173/stats     → 数据统计页
```

---

## 🛠 动手做

### 第一步：创建项目（在终端执行）

```powershell
cd "E:\本科\Beginner's-Paradise‑FirstCommit"
npm create vite@latest focusstudy-web -- --template vue
```

如果询问安装 create-vite，输入 `y` 回车。创建完成后：

```powershell
cd focusstudy-web
npm install
```

**验证**：`npm run dev` 启动，浏览器打开终端显示的地址（通常是 http://localhost:5173），看到 Vite + Vue 的默认欢迎页就成功了。按 `Ctrl + C` 停掉。

### 第二步：安装 Element Plus 和 Vue Router

```powershell
npm install element-plus @element-plus/icons-vue
npm install vue-router@4
```

### 第三步：看懂项目结构（重点！）

```
focusstudy-web/
├── index.html              # 入口 HTML（浏览器先加载它）
├── package.json            # 项目"清单"：依赖和命令
├── vite.config.js          # Vite 配置（后面要改，加代理）
└── src/
    ├── main.js             # 入口 JS：创建应用、挂载
    ├── App.vue             # 根组件（所有页面的"壳"）
    ├── router/
    │   └── index.js        # 路由配置（地址→页面）
    ├── components/         # 可复用小组件
    ├── views/              # 页面级组件（三页放这）
    │   ├── TasksView.vue   # 任务管理页
    │   ├── TimerView.vue   # 计时器页
    │   └── StatsView.vue   # 统计页
    └── assets/             # 静态资源（图片、全局样式）
```

### 第四步：配置 main.js（接入 Element Plus）

把 `src/main.js` 内容**替换**为：

```javascript
import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

// 注册 Element Plus 所有图标组件（图标名变成全局组件，如 <Edit />）
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(ElementPlus);
app.use(router);
app.mount("#app");
```

### 第五步：创建路由

新建文件 `src/router/index.js`：

```javascript
import { createRouter, createWebHistory } from "vue-router";
import TasksView from "../views/TasksView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/tasks" },          // 访问根路径 → 跳去任务页
    { path: "/tasks", component: TasksView },   // 任务管理
    { path: "/timer", component: () => import("../views/TimerView.vue") },  // 懒加载写法
    { path: "/stats", component: () => import("../views/StatsView.vue") },
  ],
});

export default router;
```

> `() => import(...)` 是**懒加载**：访问到该页面才加载代码，页面多时更快。

### 第六步：改造 App.vue（导航壳）

把 `src/App.vue` 内容**替换**为：

```vue
<template>
  <el-container class="layout">
    <!-- 顶栏：品牌 + 导航 -->
    <el-header class="header">
      <div class="brand">🍅 FocusStudy</div>
      <el-menu mode="horizontal" :default-active="activeMenu" router class="nav">
        <el-menu-item index="/tasks">任务管理</el-menu-item>
        <el-menu-item index="/timer">专注计时</el-menu-item>
        <el-menu-item index="/stats">数据统计</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 内容区：路由切换到这里 -->
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
// 当前地址 → 高亮对应的导航项
const activeMenu = computed(() => route.path);
</script>

<style>
body { margin: 0; background: #f5f7fa; }
.layout { min-height: 100vh; }
.header {
  display: flex; align-items: center; justify-content: space-between;
  background: white; border-bottom: 1px solid #eee;
}
.brand { font-size: 22px; font-weight: bold; color: #ff6b35; }
.nav { border-bottom: none !important; }
</style>
```

### 第七步：创建三个占位页面

`src/views/TasksView.vue`：

```vue
<template>
  <el-card>
    <h2>📋 任务管理</h2>
    <p>这里将实现任务的新增、列表、完成、删除（第 10 课完成）</p>
  </el-card>
</template>
```

`src/views/TimerView.vue`：

```vue
<template>
  <el-card>
    <h2>⏱️ 番茄专注计时器</h2>
    <p>这里将实现专注倒计时、开始/暂停/重置（第 11 课完成）</p>
  </el-card>
</template>
```

`src/views/StatsView.vue`：

```vue
<template>
  <el-card>
    <h2>📊 数据统计</h2>
    <p>这里将显示专注时长图表（第 12 课完成）</p>
  </el-card>
</template>
```

### 第八步：跑起来 + 提交

```powershell
npm run dev
```

浏览器打开，点顶部三个导航，页面能切换就成功了！

然后提交到 GitHub（形成比赛期间的提交记录）：

```powershell
git add .
git commit -m "feat: 初始化 FocusStudy 前端项目，接入 Element Plus 与路由"
git push
```

---

## ✅ 本节验收标准

- [ ] `npm run dev` 能启动，页面显示顶栏 + 三个导航
- [ ] 点击三个导航能切换到对应页面
- [ ] 能说出 `main.js / App.vue / router/index.js / views/` 各自的作用
- [ ] 能独立创建一个 `.vue` 文件并说出三部分结构
- [ ] 提交记录已 push 到 GitHub

---

## ⚠️ 常见坑

- **坑 1**：`npm run dev` 报端口占用 → 终端提示 `Port 5173 is in use`，按提示按 `y` 换个端口即可。
- **坑 2**：页面白屏 / 控制台报错 → 看 F12 Console，最常见是路由路径写错或组件没导出。
- **坑 3**：Element Plus 组件不生效（样式是原生的）→ 确认 main.js 里引入了 CSS：`import "element-plus/dist/index.css"`。
- **坑 4**：改代码没反应 → Vite 热更新一般秒级，偶尔需要重启 `npm run dev`。

---

## 📝 学习日志打卡

```
今天：创建了正式的 focusstudy-web 项目，接入了 Element Plus 和路由，三个页面能切换了。
困难：刚开始不知道 main.js 和 App.vue 是干嘛的，对照课程一步步配好的。
明天：开发任务管理模块，让任务真的能增删改查。
```

---

## 🔜 下一课预告

**第 10 课**：任务管理模块！这是 FocusStudy 的第一块核心功能——用 Element Plus 的表格、表单、标签做出完整任务管理，并把数据存进 localStorage。

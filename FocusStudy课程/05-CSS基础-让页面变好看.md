# 第 5 课：CSS 基础 — 让页面变好看

> 目标：学会 CSS 核心语法（选择器 / 盒模型 / Flexbox），把第 4 课的骨架"装修"成好看的界面。
> 耗时：约 1 天

---

## 📌 这节课你会学到

1. CSS 是什么、怎么"挂"到 HTML 上（三种引入方式）
2. 选择器：怎么选中要装修的元素
3. 盒模型：margin / border / padding / content
4. Flexbox 布局：让元素排队、居中
5. 常用美化属性：颜色、字体、圆角、阴影

---

## 🧠 概念讲解

### 1. CSS 是什么？

**CSS（层叠样式表）** 控制网页的"长相"：颜色、大小、间距、位置。HTML 定骨架，CSS 做装修。

**三种引入方式**（今天用第 3 种）：

```html
<!-- 方式1：写在标签里（不推荐，难维护） -->
<div style="color: red;">文字</div>

<!-- 方式2：写在 <style> 里（练习用可以） -->
<style>
  p { color: blue; }
</style>

<!-- 方式3：外部文件（项目标准做法，推荐） -->
<link rel="stylesheet" href="style.css">
```

### 2. 选择器：CSS 怎么"找到"元素

```css
/* 标签选择器：选中所有 <p> */
p { color: gray; }

/* 类选择器：选中所有 class="card" 的元素（用 . 开头） */
.card { background: white; }

/* id 选择器：选中 id="timer" 的元素（用 # 开头，只能一个） */
#timer { font-size: 48px; }

/* 后代选择器：选中 .card 里面的所有 button */
.card button { border-radius: 8px; }
```

> **记住口诀**：`标签直接写，类用点，id 用井号`。

### 3. 盒模型：每个元素都是一个"盒子"

```
┌────────────────────────── margin 外边距（盒子与外界的距离）
│  ┌────────────────────── border 边框
│  │  ┌────────────────── padding 内边距（内容与边框的距离）
│  │  │  ┌────────────── content 内容
│  │  │  │   文字/图片
│  │  │  └──────────────
│  │  └──────────────────
│  └──────────────────────
└──────────────────────────
```

```css
.card {
  width: 300px;                 /* 内容宽度 */
  padding: 20px;                /* 内边距：内容四周留 20px 空 */
  border: 1px solid #ddd;       /* 1px 实线浅灰边框 */
  border-radius: 12px;          /* 圆角 */
  margin: 16px auto;            /* 外边距：上下16px，左右auto（水平居中） */
}
```

### 4. Flexbox：一学就会的布局神器

想让一排按钮"排队并居中"？用 flex：

```css
.btn-group {
  display: flex;          /* 开启 flex 布局，子元素自动横排 */
  gap: 10px;              /* 子元素间距 */
  justify-content: center;/* 主轴居中（水平） */
  align-items: center;    /* 交叉轴居中（垂直） */
}
```

> **类比**：`display: flex` 像把元素们放进一条"可伸缩的排队通道"，`justify-content` 管横着怎么排，`align-items` 管竖着怎么对齐。

### 5. 常用美化速查

```css
color: #333;                /* 文字颜色（可以用 #hex、rgb()、英文单词） */
background-color: #f5f7fa;  /* 背景色 */
font-size: 16px;            /* 字号 */
font-weight: bold;          /* 加粗 */
letter-spacing: 1px;        /* 字间距 */
box-shadow: 0 4px 12px rgba(0,0,0,0.1);  /* 阴影，让卡片有立体感 */
```

---

## 🛠 动手做：给 FocusStudy 装修

### 第一步：建文件

在 `practice/html/` 下新建 `style.css`，并在 `index.html` 的 `<head>` 里加上：

```html
<link rel="stylesheet" href="style.css">
```

### 第二步：写 style.css（亲手敲！）

```css
/* ===== 全局 ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", sans-serif;
  background: #f5f7fa;
  color: #333;
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;            /* 页面整体居中 */
}

/* ===== 顶部标题 ===== */
header { text-align: center; margin-bottom: 24px; }
header h1 { color: #ff6b35; font-size: 36px; }
header p { color: #888; margin-top: 6px; }

/* ===== 三个模块卡片 ===== */
section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
section h2 { font-size: 18px; margin-bottom: 14px; color: #333; }

/* ===== 任务输入区 ===== */
.task-input { display: flex; gap: 8px; margin-bottom: 14px; }
.task-input input {
  flex: 1;                    /* 输入框自动撑满剩余空间 */
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.task-input button {
  padding: 10px 18px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.task-input button:hover { background: #e85a26; }  /* 悬停变色 */

/* ===== 任务列表 ===== */
ul { list-style: none; }
li {
  display: flex;
  justify-content: space-between;  /* 两端对齐 */
  padding: 10px 12px;
  border-bottom: 1px solid #f0f0f0;
}

/* ===== 计时器区 ===== */
.timer-display {
  font-size: 56px;
  font-weight: bold;
  text-align: center;
  color: #ff6b35;
  letter-spacing: 2px;
  margin: 12px 0;
}
.btn-group { display: flex; justify-content: center; gap: 12px; }
.btn-group button {
  padding: 10px 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}
.btn-group button:first-child { background: #ff6b35; color: white; border: none; }

/* ===== 统计区 ===== */
.stats { display: flex; justify-content: space-around; text-align: center; }
.stats p { font-size: 14px; color: #888; }
.stats .num { font-size: 28px; font-weight: bold; color: #333; }
```

### 第三步：改 index.html，给结构加上 class

把 `<div>` 输入区改成 `<div class="task-input">`，计时按钮区改成 `<div class="btn-group">`，倒计时 `<p>` 改成 `<p class="timer-display">`，统计区的两个 `<p>` 按下面结构改：

```html
<div class="stats">
  <p>今日专注<span class="num">0</span>分钟</p>
  <p>本周专注<span class="num">0</span>分钟</p>
</div>
```

保存后用 Live Server 刷新（或直接刷新浏览器），对比一下装修前后！

### 第四步：改一改

1. 把主题色 `#ff6b35` 换成一个你喜欢的颜色（比如 `#4caf50` 绿色），全站颜色跟着变
2. 把卡片圆角 `12px` 改成 `4px` 再改回 `50px`，观察不同风格
3. 给 `li` 加 `border-radius: 8px` 和 `margin-bottom: 6px`，列表变卡片风格

---

## ✅ 本节验收标准

- [ ] 页面有主题色、卡片阴影、圆角，不再是白底黑字
- [ ] 任务输入框和按钮在一行（flex 生效）
- [ ] 计时器数字居中放大显示
- [ ] 会改颜色变量并看到全局变化
- [ ] 能用一句话解释盒模型的四层结构

---

## ⚠️ 常见坑

- **坑 1**：CSS 改了没反应 → 检查 `<link>` 的 `href` 路径对不对、浏览器有没有刷新（按 F5 或 Ctrl+F5 强刷）
- **坑 2**：样式"打架" → 同样优先级后写的生效；不同选择器，`id` > `class` > `标签`。写不出效果时先检查是不是被覆盖。
- **坑 3**：`margin: 0 auto` 不居中 → 它只对**有固定宽度**的块级元素生效。
- **坑 4**：中文乱码/字体奇怪 → `font-family` 里保留 `sans-serif` 兜底。

---

## 📝 学习日志打卡

```
今天：用 CSS 把页面装修成了像样的产品界面，学会 flex 布局和盒模型。
困难：按钮不在一行，后来发现是忘记给父容器加 display: flex。
明天：学 JavaScript，让页面真正"动"起来。
```

---

## 🔜 下一课预告

**第 6 课**：JavaScript 基础。页面现在只是"静态展板"，学了 JS 它才有大脑——能算、能判断、能响应你的点击。

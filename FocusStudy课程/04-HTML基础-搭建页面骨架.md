# 第 4 课：HTML 基础 — 搭建页面骨架

> 目标：学会 HTML 常用标签，画出 FocusStudy 首页的"骨架"。
> 耗时：约 1 天

---

## 📌 这节课你会学到

1. HTML 是什么、网页是怎么组成的
2. 最常用的标签：标题 / 段落 / 列表 / 输入框 / 按钮
3. 标签的"属性"（id / class / placeholder）
4. 动手做 FocusStudy 的静态页面骨架

---

## 🧠 概念讲解

### 1. HTML 是什么？

**HTML（超文本标记语言）** 是网页的"骨架"——它用一套标签来描述"这里放一个标题、那里放一个输入框"。

浏览器读 HTML 文件，就知道怎么把内容显示出来。

```html
<!-- 一个最小网页 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>我的网页</title>
</head>
<body>
  <h1>你好，世界</h1>
  <p>这是我的第一个网页。</p>
</body>
</html>
```

结构解读：
- `<!DOCTYPE html>`：告诉浏览器"我是 HTML5"
- `<html>`：整个页面的根，里面装所有东西
- `<head>`：页面的"后台信息"（标题、编码），不显示在页面上
- `<body>`：页面的"正文"，用户能看到的一切都在这里

> **类比**：HTML 是房子的钢筋骨架。骨架定好了，第 5 课的 CSS 来刷墙装修，第 6 课起的 JavaScript 来装水电（让房子"活"起来）。

### 2. 常用标签速查表（今天用到的）

| 标签 | 作用 | 示例 |
|---|---|---|
| `<h1>` ~ `<h6>` | 标题（1 最大，6 最小） | `<h1>FocusStudy</h1>` |
| `<p>` | 段落 | `<p>专注学习，从现在开始</p>` |
| `<div>` | 一块区域（万能容器） | `<div class="timer">...</div>` |
| `<ul>` / `<li>` | 无序列表 | `<ul><li>数学作业</li></ul>` |
| `<input>` | 输入框 | `<input placeholder="输入任务名">` |
| `<button>` | 按钮 | `<button>开始专注</button>` |
| `<select>` / `<option>` | 下拉选择 | `<select><option>数学</option></select>` |
| `<img>` | 图片 | `<img src="logo.png" alt="logo">` |
| `<br>` | 换行 | `第一行<br>第二行` |

### 3. 属性：给标签"补充说明"

标签可以有属性，写在标签名后面：

```html
<input type="text" placeholder="请输入任务名称" id="taskInput" class="my-input">
```

- `type="text"`：输入框的类型（text 文本、date 日期、number 数字）
- `placeholder="..."`：输入框里的灰色提示文字
- `id`：给元素一个唯一编号（页面里只能有一个）
- `class`：给元素一个分类名（可以很多个共用）——CSS 主要靠这个来"找"元素

---

## 🛠 动手做：FocusStudy 页面骨架

### 第一步：创建文件

在项目根目录新建文件夹 `practice/html/`（前 8 课练手代码都放这），在里面新建 `index.html`。

### 第二步：写代码（亲手敲！）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>FocusStudy - 学生专注学习系统</title>
</head>
<body>

  <!-- 顶部：标题区 -->
  <header>
    <h1>🍅 FocusStudy</h1>
    <p>管理任务 · 专注计时 · 数据统计</p>
  </header>

  <!-- 模块一：任务管理区 -->
  <section>
    <h2>📋 我的任务</h2>
    <!-- 新增任务的输入区 -->
    <div>
      <input placeholder="任务名称">
      <input placeholder="科目">
      <button>添加任务</button>
    </div>
    <!-- 任务列表（以后用代码动态生成） -->
    <ul>
      <li>数学作业 - 今天 24:00 前</li>
      <li>背英语单词 - 明天</li>
    </ul>
  </section>

  <!-- 模块二：番茄计时器区 -->
  <section>
    <h2>⏱️ 专注计时器</h2>
    <div>
      <!-- 倒计时显示，先写死一个时间 -->
      <p>25:00</p>
      <button>开始</button>
      <button>暂停</button>
      <button>重置</button>
    </div>
  </section>

  <!-- 模块三：数据统计区（以后放图表） -->
  <section>
    <h2>📊 学习统计</h2>
    <p>今日专注：0 分钟</p>
    <p>本周专注：0 分钟</p>
  </section>

</body>
</html>
```

### 第三步：在浏览器里看效果

方式 A（简单）：双击 `index.html` 用浏览器打开
方式 B（推荐，以后用得上）：右键 VSCode 里的 `index.html` → **Open with Live Server**（第 2 课装的插件），浏览器会打开一个本地地址 `http://127.0.0.1:5500/...`

### 第四步：改一改（"改坏"学习法）

试着做这些改动，观察变化：
1. 把 `<h1>` 改成 `<h3>`，标题变什么了？
2. 把 `placeholder="任务名称"` 里的字改掉，输入框提示变什么了？
3. 加一个 `<li>物理作业 - 后天</li>`，列表多一行
4. 删掉一个 `</section>`，页面会怎样？（故意删错 → 再补回来，感受结构的重要性）

---

## ✅ 本节验收标准

- [ ] 浏览器能打开 `practice/html/index.html`，看到 3 大模块
- [ ] 能说出 5 个以上常用标签的作用
- [ ] 知道 `id` 和 `class` 的区别
- [ ] 完成了"改一改"的 4 个小练习

---

## ⚠️ 常见坑

- **坑 1**：标签忘写闭合斜杠（如只写 `<div>` 不写 `</div>`）→ 页面错乱。成对标签一定要闭合。
- **坑 2**：中文字符串用了中文引号 → 代码里一律用英文引号 `""`。
- **坑 3**：文件编码乱码 → 确保 `<head>` 里有 `<meta charset="UTF-8">`。
- **坑 4**：Live Server 没反应 → 确认右下角状态栏显示端口号，或右键重新 Open with Live Server。

---

## 📝 学习日志打卡

```
今天：用 HTML 搭出了 FocusStudy 的页面骨架，三块功能区都立起来了。
困难：有时候忘写闭合标签，页面就乱了，现在养成了先写闭合再写内容。
明天：学 CSS，把骨架装修得好看一点。
```

---

## 🔜 下一课预告

**第 5 课**：CSS 基础。给今天的骨架"刷墙装修"——配色、布局、间距，让它从一个简陋页面变成像样的产品界面。

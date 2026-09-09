# 第 7 课：DOM 与 localStorage — 做迷你任务清单

> 目标：学会操作网页元素（DOM）和浏览器本地存储（localStorage），亲手做一个"刷新不丢数据"的迷你任务清单。
> 耗时：约 1.5 天
> 意义：这是 FocusStudy **任务管理 + 本地存储** 的原型预演，做完这节课，第 10 课你会用 Vue 把它重写一遍，感受框架的威力。

---

## 📌 这节课你会学到

1. DOM 是什么、怎么选中 / 修改 / 添加元素
2. 事件监听：响应用户点击、输入
3. `localStorage`：把数据存进浏览器，刷新不丢
4. `JSON.stringify` / `JSON.parse`：对象和字符串互转
5. 动手：完整的迷你任务清单（增 / 显 / 删 / 存）

---

## 🧠 概念讲解

### 1. DOM 是什么？

**DOM（文档对象模型）** 是浏览器把 HTML 变成的一棵"元素树"。JS 可以通过这棵树**找到、修改、增删**页面元素。

```
document（整棵树）
 └── body
      ├── h1（标题）
      ├── div#taskInput（输入区）
      │    ├── input
      │    └── button
      └── ul#taskList（任务列表）
           ├── li
           └── li
```

**最常用的 4 个 DOM 操作**：

```javascript
// 1. 找到元素
const input = document.getElementById("taskInput");   // 按 id 找（最常用）
const btns = document.querySelectorAll(".btn");       // 按 class 找，返回数组
const btn = document.querySelector(".btn");           // 按选择器找第一个

// 2. 改内容
h1.textContent = "新标题";            // 改文字
div.innerHTML = "<p>新内容</p>";      // 改内部 HTML（拼接多元素时用）

// 3. 创建 + 添加元素
const li = document.createElement("li");
li.textContent = "新任务";
list.appendChild(li);                // 加到列表末尾

// 4. 删除元素
li.remove();                         // 把自己从树上摘掉
```

### 2. 事件：响应用户操作

```javascript
btn.addEventListener("click", function () {
  // 用户点击按钮时，这里的代码会执行
});
```

常见事件：`click`（点击）、`input`（输入时）、`change`（输入框内容变化）、`keydown`（按键）、`submit`（表单提交）。

### 3. localStorage：浏览器里的"小仓库"

`localStorage` 是浏览器自带的**键值对存储**，数据存在你的电脑上，**刷新页面、关掉浏览器都还在**。

```javascript
// 存数据（key-value）
localStorage.setItem("username", "小明");

// 取数据
const name = localStorage.getItem("username");   // "小明"

// 删数据
localStorage.removeItem("username");
```

**重要限制**：localStorage 只能存**字符串**。存对象/数组要先转成字符串（JSON），取出来再转回对象：

```javascript
// 存一个数组
const tasks = [{ id: 1, name: "数学作业" }, { id: 2, name: "背单词" }];
localStorage.setItem("tasks", JSON.stringify(tasks));   // 对象 → JSON字符串

// 取出来
const saved = localStorage.getItem("tasks");
const taskList = JSON.parse(saved);    // JSON字符串 → 对象/数组
console.log(taskList[0].name);         // 数学作业
```

> **JSON** 是一种"用文字描述数据"的格式：`{"name":"小明","age":17}`。`JSON.stringify` 是"打包"，`JSON.parse` 是"拆包"。

---

## 🛠 动手做：迷你任务清单

在 `practice/html/` 下新建 `todo.html`，敲入下面完整代码（**这是本节核心，请亲手敲并逐行理解**）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>迷你任务清单</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: "Microsoft YaHei", sans-serif; max-width: 500px; margin: 40px auto; padding: 0 16px; }
    h1 { text-align: center; margin-bottom: 20px; }
    .input-row { display: flex; gap: 8px; margin-bottom: 16px; }
    .input-row input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
    .input-row button { padding: 10px 16px; background: #ff6b35; color: white; border: none; border-radius: 8px; cursor: pointer; }
    ul { list-style: none; }
    li {
      display: flex; justify-content: space-between; align-items: center;
      padding: 12px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 8px;
    }
    li.done { opacity: 0.5; text-decoration: line-through; }
    .del { color: #e74c3c; cursor: pointer; border: none; background: none; font-size: 16px; }
  </style>
</head>
<body>
  <h1>📋 迷你任务清单</h1>

  <div class="input-row">
    <input id="taskInput" placeholder="输入任务名称，回车添加">
    <button id="addBtn">添加</button>
  </div>

  <ul id="taskList"></ul>

  <script>
    // ===== 数据层：所有任务存在这个数组里，并同步到 localStorage =====
    const STORAGE_KEY = "mini_tasks";

    // 从 localStorage 读取初始数据（第一次为空数组）
    let tasks = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

    function saveTasks() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));   // 数组 → 字符串 → 存起来
    }

    // ===== 视图层：把 tasks 数组渲染成页面上的 <li> =====
    function render() {
      const list = document.getElementById("taskList");
      list.innerHTML = "";                       // 清空旧列表（避免重复渲染）

      for (const task of tasks) {
        // 创建 li
        const li = document.createElement("li");
        li.textContent = task.name;
        if (task.done) li.classList.add("done"); // 已完成 → 加灰色删除线样式

        // 点击 li 切换完成状态
        li.addEventListener("click", function () {
          task.done = !task.done;
          saveTasks();
          render();
        });

        // 删除按钮
        const delBtn = document.createElement("button");
        delBtn.textContent = "✕";
        delBtn.className = "del";
        delBtn.addEventListener("click", function (event) {
          event.stopPropagation();               // 阻止事件冒泡（避免同时触发上面的切换）
          tasks = tasks.filter(t => t.id !== task.id);   // 过滤掉该任务
          saveTasks();
          render();
        });

        li.appendChild(delBtn);
        list.appendChild(li);
      }
    }

    // ===== 添加任务 =====
    function addTask() {
      const input = document.getElementById("taskInput");
      const name = input.value.trim();           // 去掉首尾空格
      if (name === "") return;                   // 空输入不处理

      tasks.push({ id: Date.now(), name: name, done: false });   // Date.now() 生成唯一id
      saveTasks();
      render();
      input.value = "";                          // 清空输入框
    }

    document.getElementById("addBtn").addEventListener("click", addTask);
    document.getElementById("taskInput").addEventListener("keydown", function (e) {
      if (e.key === "Enter") addTask();          // 回车也能添加
    });

    // 首次加载渲染
    render();
  </script>
</body>
</html>
```

### 验证（重要！）

1. 添加 3 个任务 → 页面显示 3 行
2. 点击某行 → 变灰 + 删除线（完成状态）
3. 点 ✕ → 该行删除
4. **按 F5 刷新页面 → 数据还在！**（localStorage 生效）
5. 打开 F12 → Application → Local Storage，能看到 `mini_tasks` 的 JSON 数据

### 改一改

1. 把 `event.stopPropagation()` 删掉，点删除按钮，观察发生了什么（学会"事件冒泡"这个坑）
2. 给任务加一个 `subject`（科目）字段，页面上显示"数学：写作业"
3. 加一个"清空所有"按钮

---

## ✅ 本节验收标准

- [ ] 增 / 删 / 完成状态切换全部可用
- [ ] 刷新页面后数据不丢（localStorage 生效）
- [ ] 能解释 `JSON.stringify` 和 `JSON.parse` 各在什么时候用
- [ ] 能说出 `getElementById` / `createElement` / `appendChild` / `remove` 的作用
- [ ] 在 F12 里亲眼看到存储的数据

---

## ⚠️ 常见坑

- **坑 1**：刷新后数据没了 → 检查是不是忘了 `saveTasks()`，或存的时候没 `JSON.stringify`。
- **坑 2**：`JSON.parse` 报错 → 存进去的是空字符串/非法 JSON。安全写法：`JSON.parse(localStorage.getItem(KEY)) || []`。
- **坑 3**：点删除按钮，任务却变完成 → 事件冒泡。用 `event.stopPropagation()` 阻止。
- **坑 4**：重复渲染内容重复 → 每次 render 先 `list.innerHTML = ""` 清空。

---

## 📝 学习日志打卡

```
今天：做出了刷新不丢数据的迷你任务清单，掌握 DOM 操作和 localStorage。
困难：点删除按钮会同时触发切换完成状态，查资料学到的 stopPropagation 解决了。
明天：学 Vue3，用框架重写这个清单，体验"数据驱动视图"。
```

---

## 🔜 下一课预告

**第 8 课**：Vue3 入门。你会发现用框架写同样的功能，代码量减少一半、逻辑更清晰——这正是 FocusStudy 正式前端要用的技术。

# 第 6 课：JavaScript 基础 — 让页面会思考

> 目标：掌握 JavaScript 核心语法（变量 / 类型 / 条件 / 循环 / 函数 / 数组 / 对象），并写一个"专注时长计算器"练手。
> 耗时：约 1.5 天

---

## 📌 这节课你会学到

1. JavaScript 在网页里扮演什么角色
2. 变量与数据类型
3. 条件判断 `if / else` 和循环 `for`
4. 函数：把逻辑打包成"小工具"
5. 数组与对象：JS 里最重要的两种数据结构
6. 动手：写一个"专注时长计算器"

---

## 🧠 概念讲解

### 1. JavaScript 是什么？

**JavaScript（简称 JS）** 是让网页"活起来"的语言：能算数、能判断、能响应点击、能读写数据。浏览器天生就能执行它。

> 注意：JavaScript 和 Java **没有任何关系**，就像"老婆饼"和"老婆"没关系 😄

### 2. 变量：给数据起名字

```javascript
// let：可以重新赋值的变量（最常用）
let score = 0;
score = 10;          // 可以改

// const：常量，赋值后不能改（推荐优先用）
const appName = "FocusStudy";
// appName = "xxx";  ← 这行会报错

// 命名规则：驼峰命名（myFocusTime），不能以数字开头，区分大小写
```

### 3. 数据类型（记住这 5 种就够起步）

```javascript
const name = "小明";        // 字符串 String（文本，用引号）
const age = 17;             // 数字 Number
const isStudent = true;     // 布尔 Boolean（true/false）
const subjects = ["数学", "英语", "物理"];   // 数组 Array（列表）
const task = {              // 对象 Object（键值对集合）
  id: 1,
  name: "写数学作业",
  done: false
};
```

**数组**就是"有序列表"，用下标访问（**从 0 开始**）：

```javascript
const subjects = ["数学", "英语", "物理"];
console.log(subjects[0]);   // 数学
console.log(subjects.length); // 3（长度）
subjects.push("化学");       // 末尾追加 → ["数学","英语","物理","化学"]
```

**对象**就是"带名字的数据包"，用 `.` 访问：

```javascript
const task = { id: 1, name: "写数学作业", done: false };
console.log(task.name);      // 写数学作业
task.done = true;            // 修改属性
```

### 4. 条件判断：让程序"做选择"

```javascript
let focusMinutes = 25;

if (focusMinutes >= 25) {
  console.log("完成了一个番茄！休息一下");
} else if (focusMinutes >= 10) {
  console.log("坚持住，快完成了");
} else {
  console.log("刚起步，加油");
}
```

### 5. 循环：让程序"重复干活"

```javascript
// 遍历数组（最常用）
const subjects = ["数学", "英语", "物理"];
for (let i = 0; i < subjects.length; i++) {
  console.log("科目：" + subjects[i]);
}

// 更简洁的写法（for...of，推荐）
for (const s of subjects) {
  console.log("科目：" + s);
}
```

### 6. 函数：把逻辑打包成"小工具"

```javascript
// 定义函数：计算两个时间点之间的分钟数
function calcMinutes(startHour, startMin, endHour, endMin) {
  const start = startHour * 60 + startMin;   // 把时间换算成"从0点起的分钟数"
  const end = endHour * 60 + endMin;
  return end - start;                        // return = 把结果"交出去"
}

// 箭头函数（现代写法，等价于上面）
const calcMinutes = (startHour, startMin, endHour, endMin) => {
  const start = startHour * 60 + startMin;
  const end = endHour * 60 + endMin;
  return end - start;
};

// 调用
const minutes = calcMinutes(9, 0, 9, 25);
console.log(minutes);   // 25
```

> 函数三要素：**输入（参数）→ 加工（函数体）→ 输出（return）**。

---

## 🛠 动手做：专注时长计算器

在 `practice/html/` 下新建 `calculator.html`，把下面的完整代码敲进去，用 Live Server 打开：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>专注时长计算器</title>
</head>
<body>
  <h1>⏱️ 专注时长计算器</h1>

  <p>
    开始时间：
    <input id="startHour" type="number" placeholder="时" min="0" max="23" value="9">
    :
    <input id="startMin" type="number" placeholder="分" min="0" max="59" value="0">
  </p>
  <p>
    结束时间：
    <input id="endHour" type="number" placeholder="时" min="0" max="23" value="10">
    :
    <input id="endMin" type="number" placeholder="分" min="0" max="59" value="0">
  </p>
  <button id="calcBtn">计算专注分钟数</button>

  <h2 id="result">结果会显示在这里</h2>

  <script>
    // 1. 先写好"计算逻辑"函数（今天学的重点）
    function calcMinutes(startHour, startMin, endHour, endMin) {
      const start = startHour * 60 + startMin;
      const end = endHour * 60 + endMin;
      return end - start;
    }

    // 2. 给按钮绑定点击事件（DOM 操作，第 7 课细讲）
    const btn = document.getElementById("calcBtn");
    btn.addEventListener("click", function () {
      // 3. 从输入框取值（注意要转成数字）
      const sh = Number(document.getElementById("startHour").value);
      const sm = Number(document.getElementById("startMin").value);
      const eh = Number(document.getElementById("endHour").value);
      const em = Number(document.getElementById("endMin").value);

      // 4. 调用函数，显示结果
      const minutes = calcMinutes(sh, sm, eh, em);
      const result = document.getElementById("result");

      if (minutes >= 0) {
        result.textContent = "专注了 " + minutes + " 分钟（约 " + (minutes / 60).toFixed(1) + " 小时）";
      } else {
        result.textContent = "结束时间比开始早，请检查输入";
      }
    });
  </script>
</body>
</html>
```

**试试**：开始 9:00、结束 10:25 → 应该显示"专注了 85 分钟"。

### 进阶练习（做完会很有成就感）

1. 给计算器加一个"今日多次专注总时长"：用数组记录每次的分钟数，用 for 循环累加
2. 把 `calcMinutes` 改成箭头函数写法，确认功能不变
3. 故意把 `Number(...)` 去掉，输入 9 和 0，看结果变成什么（会发现"9"+"0"="90"，字符串拼接！）

---

## ✅ 本节验收标准

- [ ] 计算器能正确算出任意时间段的分钟数
- [ ] 结束早于开始时有友好提示（if/else 生效）
- [ ] 能独立写出：一个数组 + for 循环遍历 + 函数封装
- [ ] 能解释为什么 `"9" + "0"` 是 `"90"` 而不是 `9`

---

## ⚠️ 常见坑

- **坑 1**：`input.value` 拿到的是**字符串**，做数学运算前必须 `Number()` 转换。
- **坑 2**：拼字符串用 `+`，但数字相加也是 `+`，混用会出 bug——练习 3 就是让你踩这个坑。
- **坑 3**：函数名/变量名拼写不一致 → 报 `is not defined`，检查大小写。
- **坑 4**：`<script>` 标签忘写闭合 → 整个页面 JS 失效，控制台（F12）会有红色报错。

---

## 📝 学习日志打卡

```
今天：学会了 JS 的变量/条件/循环/函数/数组/对象，做出了专注时长计算器。
困难：忘了把输入转数字，9+0 变成了 90，明白字符串和数字的区别了。
明天：学 DOM 和 localStorage，做一个能增删任务、刷新不丢数据的迷你清单。
```

---

## 🔜 下一课预告

**第 7 课**：DOM 与 localStorage。今天已经碰了一下"操作网页元素"，明天正式学会它，还要学"本地存储"——刷新页面数据不丢，这是 FocusStudy 的核心存储方案。

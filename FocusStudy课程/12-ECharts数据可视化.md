# 第 12 课：ECharts 数据可视化

> 目标：把 localStorage 里的专注记录，画成"每日专注时长柱状图"和"科目占比饼图"。
> 耗时：约 1.5 天
> 这是 Demo 视频里最直观、最吸引评委的部分！

---

## 📌 这节课你会学到

1. ECharts 是什么、怎么在 Vue 里使用
2. 柱状图 / 饼图的基本配置（option 的结构）
3. 从记录数组**聚合统计**出图表数据（reduce / 分组）
4. 图表随窗口大小自适应（resize）

---

## 🧠 概念讲解

### 1. ECharts 是什么？

**ECharts** 是百度开源的图表库：给数据 + 配置，它画出漂亮的柱状图、饼图、折线图。

**核心三步**（记住这个流程）：
1. 准备一个放图表的 `<div>`
2. 初始化：`echarts.init(dom元素)`
3. 给配置：`chart.setOption({...})` —— 数据变了再 setOption 一次即可更新

```javascript
import * as echarts from "echarts";

// 1. 拿到容器
const chartDom = document.getElementById("myChart");
// 2. 初始化
const myChart = echarts.init(chartDom);
// 3. 配置 + 渲染
myChart.setOption({
  xAxis: { data: ["周一", "周二", "周三"] },
  yAxis: {},
  series: [{ type: "bar", data: [50, 80, 60] }]
});
```

### 2. 图表的灵魂：从数据到"option"

原始记录（localStorage 里的 focus_records）：

```javascript
[
  { subject: "数学", minutes: 25, date: "2026-09-08" },
  { subject: "英语", minutes: 25, date: "2026-09-08" },
  { subject: "数学", minutes: 50, date: "2026-09-09" },
]
```

要画"科目占比饼图"，需要加工成：

```javascript
[
  { name: "数学", value: 75 },
  { name: "英语", value: 25 },
]
```

**加工方法（分组求和）**——这是数据分析的基本功：

```javascript
function groupBySubject(records) {
  const map = {};                        // 用对象做"分组桶"
  for (const r of records) {
    if (!map[r.subject]) map[r.subject] = 0;
    map[r.subject] += r.minutes;         // 相同科目累加
  }
  // 转成 ECharts 要的格式
  return Object.entries(map).map(([name, value]) => ({ name, value }));
}
```

### 3. 最近 7 天柱状图的数据准备

```javascript
function last7Days(records) {
  // 生成最近 7 天的日期数组（今天往前）
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0, 10));
  }
  // 每天的专注分钟数
  const values = days.map(date =>
    records.filter(r => r.date === date).reduce((s, r) => s + r.minutes, 0)
  );
  // 日期显示为"09-08"样式
  const labels = days.map(d => d.slice(5));
  return { labels, values };
}
```

---

## 🛠 动手做

### 第一步：安装 ECharts

```powershell
npm install echarts
```

### 第二步：创建可复用的图表组件（推荐写法）

新建 `src/components/BaseChart.vue`（以后任何图表都用它）：

```vue
<template>
  <div ref="chartRef" class="base-chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import * as echarts from "echarts";

const props = defineProps({
  option: { type: Object, required: true },   // 图表配置（由父组件传入）
});

const chartRef = ref(null);
let chart = null;

onMounted(() => {
  chart = echarts.init(chartRef.value);
  chart.setOption(props.option);

  // 窗口变化时图表自适应（重要！）
  window.addEventListener("resize", () => chart && chart.resize());
});

// option 变了就重新渲染
watch(() => props.option, (newOption) => {
  chart && chart.setOption(newOption, true);   // true = 完全替换而非合并
}, { deep: true });

onUnmounted(() => {
  window.removeEventListener("resize", () => chart && chart.resize());
  chart && chart.dispose();   // 销毁图表，防内存泄漏
});
</script>

<style scoped>
.base-chart { width: 100%; height: 320px; }
</style>
```

### 第三步：写统计页面

把 `src/views/StatsView.vue` **完整替换**为：

```vue
<template>
  <div class="stats-page">
    <!-- 顶部汇总卡片 -->
    <el-row :gutter="16" class="summary-row">
      <el-col :span="8">
        <el-card><div class="num">{{ totalMinutes }}</div><div class="label">累计专注（分钟）</div></el-card>
      </el-col>
      <el-col :span="8">
        <el-card><div class="num">{{ totalCount }}</div><div class="label">完成番茄数</div></el-card>
      </el-col>
      <el-col :span="8">
        <el-card><div class="num">{{ subjectCount }}</div><div class="label">覆盖科目数</div></el-card>
      </el-col>
    </el-row>

    <!-- 最近 7 天柱状图 -->
    <el-card class="chart-card">
      <h2>📈 最近 7 天专注时长</h2>
      <BaseChart :option="barOption" />
    </el-card>

    <!-- 科目占比饼图 -->
    <el-card class="chart-card">
      <h2>🥧 各科目专注占比</h2>
      <BaseChart :option="pieOption" />
    </el-card>

    <el-empty v-if="records.length === 0" description="还没有专注记录，先去计时器完成一个番茄吧！" />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import BaseChart from "../components/BaseChart.vue";

// ===== 数据源（与第 11 课同 key） =====
const records = ref(JSON.parse(localStorage.getItem("focus_records")) || []);

// ===== 汇总卡片 =====
const totalMinutes = computed(() => records.value.reduce((s, r) => s + r.minutes, 0));
const totalCount = computed(() => records.value.length);
const subjectCount = computed(() => new Set(records.value.map(r => r.subject)).size);

// ===== 最近 7 天柱状图 =====
const barOption = computed(() => {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0, 10));
  }
  const values = days.map(date =>
    records.value.filter(r => r.date === date).reduce((s, r) => s + r.minutes, 0)
  );

  return {
    tooltip: { trigger: "axis" },
    grid: { left: 40, right: 20, top: 30, bottom: 30 },
    xAxis: { type: "category", data: days.map(d => d.slice(5)) },
    yAxis: { type: "value", name: "分钟" },
    series: [{
      name: "专注时长",
      type: "bar",
      data: values,
      itemStyle: { color: "#ff6b35", borderRadius: [6, 6, 0, 0] },
      barWidth: 32,
    }],
  };
});

// ===== 科目占比饼图 =====
const pieOption = computed(() => {
  const map = {};
  for (const r of records.value) {
    if (!map[r.subject]) map[r.subject] = 0;
    map[r.subject] += r.minutes;
  }
  const data = Object.entries(map).map(([name, value]) => ({ name, value }));

  return {
    tooltip: { trigger: "item", formatter: "{b}: {c} 分钟 ({d}%)" },
    legend: { bottom: 0 },
    series: [{
      name: "专注时长",
      type: "pie",
      radius: ["40%", "65%"],      // 环形饼图
      avoidLabelOverlap: true,
      label: { formatter: "{b}: {c}分" },
      data,
    }],
  };
});
</script>

<style scoped>
.stats-page { max-width: 960px; margin: 0 auto; }
.summary-row { margin-bottom: 20px; }
.summary-row .num { font-size: 32px; font-weight: bold; color: #ff6b35; text-align: center; }
.summary-row .label { text-align: center; color: #888; margin-top: 4px; font-size: 14px; }
.chart-card { margin-bottom: 20px; }
.chart-card h2 { margin-top: 0; font-size: 18px; }
</style>
```

### 验证清单

1. 先去计时器完成 1~2 个番茄（或临时造几条测试数据：F12 Console 里执行下面的代码造数据）
   ```javascript
   // 造测试数据（在浏览器 F12 控制台执行）
   const recs = [];
   for (let i = 0; i < 5; i++) {
     const d = new Date(); d.setDate(d.getDate() - i);
     recs.push({ id: Date.now()+i, taskName: "测试", subject: ["数学","英语","物理"][i%3], minutes: 25, date: d.toISOString().slice(0,10) });
   }
   localStorage.setItem("focus_records", JSON.stringify(recs));
   location.reload();
   ```
2. 统计页出现柱状图和环形饼图
3. 顶部三个汇总数字与记录一致
4. 拖拽浏览器窗口大小 → 图表自适应缩放
5. 清空 localStorage（F12 里删掉 focus_records 再刷新）→ 显示空状态提示

### 提交

```powershell
git add .
git commit -m "feat: 完成 ECharts 数据可视化统计页面"
git push
```

---

## ✅ 本节验收标准

- [ ] 最近 7 天柱状图正确显示每天的专注分钟
- [ ] 科目占比饼图正确显示各科目占比
- [ ] 汇总卡片数字与记录数据一致（可手动核对）
- [ ] 窗口缩放图表自适应
- [ ] 空数据时有友好提示
- [ ] 能解释 `groupBySubject` 分组求和的原理

---

## ⚠️ 常见坑

- **坑 1**：图表容器高度为 0 → 图表不显示。容器必须有确定高度（BaseChart 里设了 320px）。
- **坑 2**：`echarts.init` 时元素还没渲染 → 必须在 `onMounted` 里初始化。
- **坑 3**：`setOption` 第二次调用默认是"合并"，旧数据会残留 → 用 `setOption(option, true)` 完全替换。
- **坑 4**：组件销毁后图表还在监听 resize → `onUnmounted` 里 `dispose()`。
- **坑 5**：日期用 `new Date()` 的时区问题 → 用 `toISOString().slice(0,10)` 取 UTC 日期即可（本课统一口径）。

---

## 📝 学习日志打卡

```
今天：做出了柱状图和饼图，学会了把记录数据"分组求和"成图表需要的格式。
困难：图表第一次不显示，发现是容器没高度，设置 320px 解决。
明天：开始学 Python，为后端做准备。
```

---

## 🔜 下一课预告

**第 13 课**：Python 基础。后端要用 Python 写，今天学它的核心语法——你会发现和 JavaScript 很像，学起来很快。

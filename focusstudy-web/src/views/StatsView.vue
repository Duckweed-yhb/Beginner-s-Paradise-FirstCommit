<template>
  <div class="stats-page">
    <!-- 数据来源提示：让"这份数字从哪来"一目了然 -->
    <el-alert
      v-if="dataSource"
      :title="dataSource"
      :type="isRemote ? 'success' : 'info'"
      :closable="false"
      show-icon
      class="source-alert"
    />

    <!-- 顶部汇总卡片 -->
    <el-row :gutter="16" class="summary-row">
      <el-col :xs="12" :sm="6">
        <el-card>
          <div class="num">{{ totalMinutes }}</div>
          <div class="label">累计专注（分钟）</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card>
          <div class="num">{{ totalCount }}</div>
          <div class="label">完成番茄数</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card>
          <div class="num">{{ subjectCount }}</div>
          <div class="label">覆盖科目数</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card>
          <div class="num">{{ taskCompletionRate }}<span class="unit">%</span></div>
          <div class="label">任务完成率</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近 7 天柱状图 -->
    <el-card class="chart-card">
      <h2>📈 最近 7 天专注时长</h2>
      <BaseChart v-if="records.length > 0" :option="barOption" />
      <el-empty v-else description="暂无专注记录，先去计时器完成一个番茄吧！" />
    </el-card>

    <!-- 科目占比饼图 -->
    <el-card class="chart-card">
      <h2>🥧 各科目专注占比</h2>
      <BaseChart v-if="records.length > 0" :option="pieOption" />
      <el-empty v-else description="暂无专注记录，先去计时器完成一个番茄吧！" />
    </el-card>

    <!-- 明细表：比图表更细，方便自己复盘 -->
    <el-card v-if="records.length > 0">
      <h2>🗂 专注明细</h2>
      <el-table :data="recentRecords" stripe max-height="360">
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="taskName" label="任务" min-width="180" />
        <el-table-column label="科目" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.subject || "未分类" }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="时长" width="100" align="right">
          <template #default="{ row }">{{ row.minutes }} 分钟</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import BaseChart from "../components/BaseChart.vue";
import { fetchStats } from "../api";
import { loadRecords, loadTasks } from "../storage";
import { recentDates } from "../time";

// ===== 数据源说明 =====
const isRemote = ref(false);
const dataSource = ref("");

// 本地记录是明细最全的一份，优先使用
const records = ref(loadRecords());
// 任务列表只用来算完成率
const tasks = ref(loadTasks());

onMounted(async () => {
  try {
    const stats = await fetchStats();

    if (records.value.length > 0) {
      // 本地有明细 → 直接用本地，信息更全（后端只存聚合结果，没有明细）
      isRemote.value = false;
      dataSource.value = `数据来源：本机浏览器记录（共 ${records.value.length} 条明细）`;
    } else if (stats && stats.by_date && Object.keys(stats.by_date).length > 0) {
      // 本地为空但服务器有数据 → 用服务器汇总结果兜底展示
      useRemoteStats(stats);
    } else {
      isRemote.value = false;
      dataSource.value = "本机暂无专注记录";
    }
  } catch {
    isRemote.value = false;
    dataSource.value = "后端未启动：使用本机浏览器数据";
  }
});

/** 后端只返回聚合结果，没有明细，这里按天还原成图表能用的形状 */
function useRemoteStats(stats) {
  records.value = Object.entries(stats.by_date).map(([date, minutes]) => ({
    date,
    minutes,
    subject: "全部",
    taskName: "（来自服务器汇总）",
  }));
  isRemote.value = true;
  dataSource.value = "本地无明细，已回退到服务器汇总数据";
}

// ===== 汇总 =====
const totalMinutes = computed(() =>
  records.value.reduce((sum, r) => sum + (Number(r.minutes) || 0), 0)
);

const totalCount = computed(() => records.value.length);

const subjectCount = computed(
  () => new Set(records.value.map((r) => r.subject || "未分类")).size
);

const taskCompletionRate = computed(() => {
  if (tasks.value.length === 0) return 0;
  const done = tasks.value.filter((t) => t.done).length;
  return Math.round((done / tasks.value.length) * 100);
});

// ===== 最近 7 天柱状图 =====
// 用 recentDates() 生成的是**本地日期**，和记录里的日期口径一致。
// 之前直接 new Date().toISOString() 会在 UTC+8 的凌晨错位一天。
const barOption = computed(() => {
  const days = recentDates(7);
  const values = days.map((date) =>
    records.value
      .filter((r) => r.date === date)
      .reduce((sum, r) => sum + (Number(r.minutes) || 0), 0)
  );

  return {
    tooltip: { trigger: "axis" },
    grid: { left: 45, right: 20, top: 30, bottom: 30 },
    xAxis: { type: "category", data: days.map((d) => d.slice(5)) },
    yAxis: { type: "value", name: "分钟" },
    series: [
      {
        name: "专注时长",
        type: "bar",
        data: values,
        itemStyle: { color: "#ff6b35", borderRadius: [6, 6, 0, 0] },
        barWidth: 32,
      },
    ],
  };
});

// ===== 科目占比饼图 =====
const pieOption = computed(() => {
  const map = {};
  for (const r of records.value) {
    const subject = r.subject || "未分类";
    map[subject] = (map[subject] || 0) + (Number(r.minutes) || 0);
  }
  const data = Object.entries(map).map(([name, value]) => ({ name, value }));

  return {
    tooltip: { trigger: "item", formatter: "{b}: {c} 分钟 ({d}%)" },
    legend: { bottom: 0 },
    series: [
      {
        name: "专注时长",
        type: "pie",
        radius: ["40%", "65%"],
        avoidLabelOverlap: true,
        label: { formatter: "{b}: {c}分" },
        data,
      },
    ],
  };
});

// ===== 明细表：最近的记录排在最前 =====
const recentRecords = computed(() =>
  [...records.value]
    .sort((a, b) => {
      if (a.date === b.date) return (b.id || 0) - (a.id || 0);
      return a.date < b.date ? 1 : -1;
    })
    .slice(0, 50)
);
</script>

<style scoped>
.stats-page { max-width: 1080px; margin: 0 auto; }
.source-alert { margin-bottom: 16px; }
.summary-row { margin-bottom: 20px; }
.summary-row .num {
  font-size: 32px;
  font-weight: bold;
  color: #ff6b35;
  text-align: center;
}
.summary-row .num .unit { font-size: 16px; margin-left: 2px; }
.summary-row .label {
  text-align: center;
  color: #888;
  margin-top: 4px;
  font-size: 14px;
}
.chart-card { margin-bottom: 20px; }
.chart-card h2 { margin-top: 0; font-size: 18px; }
</style>

<template>
  <div class="stats-page">
    <!-- 顶部汇总卡片 -->
    <el-row :gutter="16" class="summary-row">
      <el-col :xs="24" :sm="8">
        <el-card>
          <div class="num">{{ totalMinutes }}</div>
          <div class="label">累计专注（分钟）</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card>
          <div class="num">{{ totalCount }}</div>
          <div class="label">完成番茄数</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card>
          <div class="num">{{ subjectCount }}</div>
          <div class="label">覆盖科目数</div>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import BaseChart from "../components/BaseChart.vue";
import { fetchStats } from "../api";

// ===== 数据源 =====
const records = ref(JSON.parse(localStorage.getItem("focus_records")) || []);

// 尝试从后端取统计（失败则使用本地 localStorage 数据）
onMounted(async () => {
  try {
    const stats = await fetchStats();
    if (stats && stats.by_date && Object.keys(stats.by_date).length > 0) {
      // 用后端数据生成等价记录：by_date / by_subject 无法还原明细，
      // 这里只用于兜底展示；本地记录存在时仍以本地为准（明细更全）
      if (records.value.length === 0) {
        useRemoteStats(stats);
      }
    }
  } catch (e) {
    // 后端未启动：使用本地数据
  }
});

function useRemoteStats(stats) {
  // 用 by_date 生成"按天"的记录用于柱状图展示
  const pseudo = Object.entries(stats.by_date).map(([date, minutes]) => ({
    date,
    minutes,
    subject: "全部",
    taskName: "（后端汇总）",
  }));
  records.value = pseudo;
  remoteOnly.value = true;
}

const remoteOnly = ref(false);

// ===== 汇总 =====
const totalMinutes = computed(() => records.value.reduce((s, r) => s + r.minutes, 0));
const totalCount = computed(() => records.value.length);
const subjectCount = computed(
  () => new Set(records.value.map((r) => r.subject || "未分类")).size
);

// ===== 最近 7 天柱状图 =====
const barOption = computed(() => {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0, 10));
  }
  const values = days.map((date) =>
    records.value.filter((r) => r.date === date).reduce((s, r) => s + r.minutes, 0)
  );

  return {
    tooltip: { trigger: "axis" },
    grid: { left: 40, right: 20, top: 30, bottom: 30 },
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
    const s = r.subject || "未分类";
    map[s] = (map[s] || 0) + r.minutes;
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
</script>

<style scoped>
.stats-page { max-width: 960px; margin: 0 auto; }
.summary-row { margin-bottom: 20px; }
.summary-row .num {
  font-size: 32px;
  font-weight: bold;
  color: #ff6b35;
  text-align: center;
}
.summary-row .label {
  text-align: center;
  color: #888;
  margin-top: 4px;
  font-size: 14px;
}
.chart-card { margin-bottom: 20px; }
.chart-card h2 { margin-top: 0; font-size: 18px; }
</style>

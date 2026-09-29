<template>
  <div class="timer-page">
    <el-card class="timer-card">
      <h2>🍅 番茄专注计时器</h2>

      <!-- 模式切换：专注 / 休息 -->
      <!-- 注意：Element Plus 2.6+ 已弃用 label 写法，必须用 value，
           否则升级后会失效并打印弃用警告 -->
      <el-radio-group v-model="mode" @change="handleModeChange">
        <el-radio-button value="focus">专注 {{ focusMinutes }} 分钟</el-radio-button>
        <el-radio-button value="break">休息 {{ breakMinutes }} 分钟</el-radio-button>
      </el-radio-group>

      <!-- 时长自定义（第 11 课要求的"自定义专注/休息时长"） -->
      <div class="duration-config">
        <div class="duration-item">
          <span class="duration-label">专注时长</span>
          <el-input-number
            v-model="focusMinutes"
            :min="MIN_MINUTES"
            :max="MAX_MINUTES"
            :step="5"
            size="small"
            :disabled="isRunning"
            @change="handleDurationChange"
          />
          <span class="duration-unit">分钟</span>
        </div>

        <div class="duration-item">
          <span class="duration-label">休息时长</span>
          <el-input-number
            v-model="breakMinutes"
            :min="MIN_MINUTES"
            :max="MAX_MINUTES"
            :step="1"
            size="small"
            :disabled="isRunning"
            @change="handleDurationChange"
          />
          <span class="duration-unit">分钟</span>
        </div>

        <el-button
          link
          type="primary"
          size="small"
          :disabled="isRunning"
          @click="resetDurations"
        >
          恢复默认（25 / 5）
        </el-button>
      </div>
      <p class="hint">计时进行中不能改时长，先重置再调。</p>

      <!-- 环形进度 + 倒计时 -->
      <div class="timer-body">
        <el-progress
          type="circle"
          :percentage="progressPercent"
          :width="220"
          :stroke-width="10"
          color="#ff6b35"
        >
          <template #default>
            <div class="time-text">{{ displayTime }}</div>
            <div class="mode-text">{{ statusText }}</div>
          </template>
        </el-progress>
      </div>

      <!-- 绑定当前任务（可选） -->
      <div class="task-bind">
        <el-select
          v-model="bindTaskId"
          placeholder="绑定当前任务（可选，完成时记录科目）"
          clearable
          style="width: 320px"
        >
          <el-option
            v-for="t in unfinishedTasks"
            :key="t.id"
            :label="t.name"
            :value="t.id"
          />
        </el-select>
      </div>

      <!-- 控制按钮 -->
      <div class="btn-group">
        <el-button
          v-if="status === 'idle' || status === 'paused'"
          type="primary"
          size="large"
          @click="startTimer"
        >
          ▶ {{ status === "paused" ? "继续" : "开始" }}
        </el-button>
        <el-button v-else type="warning" size="large" @click="pauseTimer">
          ⏸ 暂停
        </el-button>

        <el-button size="large" :disabled="status === 'idle'" @click="resetTimer">
          ↺ 重置
        </el-button>
      </div>

      <p v-if="lastRecordMessage" class="record-message">{{ lastRecordMessage }}</p>

      <!-- 今日汇总 -->
      <el-divider />
      <p class="today-summary">
        今日已专注：<b>{{ todayMinutes }}</b> 分钟（{{ todayCount }} 个番茄）
      </p>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import { ElNotification } from "element-plus";
import { createRecord, fetchRecords, syncSilently } from "../api";
import { loadRecords, saveRecords, loadTasks, loadSettings, saveSettings } from "../storage";
import { todayString, formatClock } from "../time";

// ===== 配置 =====
const DEFAULT_FOCUS_MINUTES = 25;
const DEFAULT_BREAK_MINUTES = 5;
const MIN_MINUTES = 1;
const MAX_MINUTES = 180;

// 时长从设置里恢复，用户改过一次以后就一直生效
const savedSettings = loadSettings();
const focusMinutes = ref(savedSettings.focusMinutes || DEFAULT_FOCUS_MINUTES);
const breakMinutes = ref(savedSettings.breakMinutes || DEFAULT_BREAK_MINUTES);

// ===== 计时器状态 =====
const mode = ref("focus"); // focus / break
const status = ref("idle"); // idle / running / paused
const totalSeconds = ref(focusMinutes.value * 60);
const remaining = ref(totalSeconds.value);
let timerId = null;
let endAt = 0; // 目标结束时刻（毫秒时间戳）：剩余秒数一律由墙钟反推，防 setInterval 漂移

const isRunning = computed(() => status.value === "running");

const bindTaskId = ref(null);
const lastRecordMessage = ref("");

// ===== 未完成任务（用于绑定选择） =====
const unfinishedTasks = ref([]);

function loadUnfinishedTasks() {
  unfinishedTasks.value = loadTasks().filter((t) => !t.done);

  // 绑定的任务如果被删掉/完成了，就自动解除绑定，避免记录到不存在的任务上
  if (
    bindTaskId.value !== null &&
    !unfinishedTasks.value.some((t) => t.id === bindTaskId.value)
  ) {
    bindTaskId.value = null;
  }
}

// ===== 专注记录 =====
const records = ref(loadRecords());

function persistRecords() {
  saveRecords(records.value);
}

// ===== 跨天处理 =====
// 【这里修掉了一个真实的 bug】
// 原来写的是 `const today = new Date().toISOString().slice(0, 10)`：
//   1) 只在组件挂载时算一次 —— 页面开过午夜，"今日汇总"就会一直显示前一天的数字
//   2) 用的是 UTC 日期 —— UTC+8 的凌晨 0~8 点会被算到前一天
// 现在改成每 30 秒重新取一次本地日期，跨天时自动刷新。
const currentDate = ref(todayString());
let dayTicker = null;

// ===== 显示 =====
const displayTime = computed(() => formatClock(remaining.value));

const progressPercent = computed(() => {
  if (totalSeconds.value <= 0) return 0;
  const done = totalSeconds.value - remaining.value;
  return Math.min(100, Math.round((done / totalSeconds.value) * 100));
});

const statusText = computed(() => {
  if (status.value === "paused") return "已暂停";
  if (status.value === "idle") return mode.value === "focus" ? "准备专注" : "准备休息";
  return mode.value === "focus" ? "专注中" : "休息中";
});

// ===== 核心逻辑 =====
function durationFor(m) {
  return (m === "focus" ? focusMinutes.value : breakMinutes.value) * 60;
}

function startTimer() {
  if (status.value === "idle") {
    totalSeconds.value = durationFor(mode.value);
    remaining.value = totalSeconds.value;
  }
  // 时间戳基准：记下"应该结束的时刻"，每次 tick 用墙钟反推剩余秒数。
  // 浏览器后台标签节流会让 setInterval 变慢（漂移），反推计算保证倒计时始终和真实时间一致。
  endAt = Date.now() + remaining.value * 1000;
  status.value = "running";

  clearInterval(timerId);
  timerId = setInterval(tick, 250);
}

/** 每次 tick：用墙钟反推剩余秒数，归零即结束 */
function tick() {
  const rest = Math.max(0, Math.round((endAt - Date.now()) / 1000));
  remaining.value = rest;
  if (rest <= 0) {
    finishTimer();
  }
}

function finishTimer() {
  clearInterval(timerId);
  timerId = null;
  status.value = "idle";
  onTimerComplete();
}

function pauseTimer() {
  clearInterval(timerId);
  timerId = null;
  // 暂停瞬间把剩余秒数固定下来，继续时以它为新的结束时刻基准
  remaining.value = Math.max(0, Math.round((endAt - Date.now()) / 1000));
  status.value = "paused";
}

function resetTimer() {
  clearInterval(timerId);
  timerId = null;
  endAt = 0;
  status.value = "idle";
  totalSeconds.value = durationFor(mode.value);
  remaining.value = totalSeconds.value;
}

function handleModeChange() {
  resetTimer();
}

/** 改时长时同步保存，并刷新当前剩余时间（未开始时） */
function handleDurationChange() {
  saveSettings({
    focusMinutes: focusMinutes.value,
    breakMinutes: breakMinutes.value,
  });
  if (status.value === "idle") {
    resetTimer();
  }
}

function resetDurations() {
  focusMinutes.value = DEFAULT_FOCUS_MINUTES;
  breakMinutes.value = DEFAULT_BREAK_MINUTES;
  handleDurationChange();
}

async function onTimerComplete() {
  status.value = "idle";
  lastRecordMessage.value = "";

  if (mode.value === "focus") {
    const bindTask = unfinishedTasks.value.find((t) => t.id === bindTaskId.value);

    // 用**本地日期**，不是 UTC 日期
    const record = {
      id: Date.now(),
      taskName: bindTask ? bindTask.name : "未绑定任务",
      subject: bindTask ? bindTask.subject : "未分类",
      minutes: focusMinutes.value,
      date: todayString(),
    };

    records.value.push(record);
    persistRecords();

    // 同步到后端；失败也无所谓，本地已经有这条记录了
    const ok = await syncSilently(createRecord(record));
    lastRecordMessage.value = ok
      ? `已记录 ${record.minutes} 分钟，并同步到服务器`
      : `已记录 ${record.minutes} 分钟（本地保存，服务器未连接）`;

    ElNotification({
      title: "🎉 专注完成！",
      message: `已完成 ${record.minutes} 分钟，休息 ${breakMinutes.value} 分钟吧`,
      type: "success",
      duration: 5000,
    });

    mode.value = "break";
  } else {
    ElNotification({
      title: "☕ 休息结束",
      message: "开始下一个番茄吧！",
      type: "info",
      duration: 5000,
    });
    mode.value = "focus";
  }

  resetTimer();
}

// ===== 今日汇总（用响应式的 currentDate，跨天会自动更新） =====
const todayMinutes = computed(() =>
  records.value
    .filter((r) => r.date === currentDate.value)
    .reduce((sum, r) => sum + (Number(r.minutes) || 0), 0)
);

const todayCount = computed(
  () => records.value.filter((r) => r.date === currentDate.value).length
);

// ===== 离开页面提醒（运行中切走会弹提示） =====
function beforeUnloadHandler(e) {
  e.preventDefault();
  e.returnValue = "";
}

watch(status, (val) => {
  if (val === "running") {
    window.addEventListener("beforeunload", beforeUnloadHandler);
  } else {
    window.removeEventListener("beforeunload", beforeUnloadHandler);
  }
});

// ===== 生命周期 =====
onMounted(() => {
  loadUnfinishedTasks();

  // 回到这个页面时刷新可选任务（在任务页改完再切回来）
  window.addEventListener("focus", loadUnfinishedTasks);

  // 本地有记录而后端是空的：把本地记录静默补推上去，让服务器成为真实镜像。
  // 幂等做法：只在"后端确实是空的"时才推，避免重复。
  (async () => {
    try {
      const remote = await fetchRecords();
      if (Array.isArray(remote) && remote.length === 0 && records.value.length > 0) {
        for (const r of records.value) {
          await syncSilently(
            createRecord({
              taskName: r.taskName,
              subject: r.subject,
              minutes: r.minutes,
              date: r.date,
            })
          );
        }
      }
    } catch {
      /* 后端未启动：本地数据照常可用，什么都不做 */
    }
  })();

  // 后台标签切回来时，立即用墙钟校准一次，不等下一次 tick
  document.addEventListener("visibilitychange", resyncOnVisible);

  // 每 30 秒检查一次是否跨天：跨了就刷新 currentDate，
  // 让"今日汇总"在午夜之后自动归零，而不是继续显示昨天
  dayTicker = setInterval(() => {
    const now = todayString();
    if (now !== currentDate.value) {
      currentDate.value = now;
    }
  }, 30000);
});

/** 页面从后台切回时校准剩余时间（后台节流可能让 tick 滞后） */
function resyncOnVisible() {
  if (status.value !== "running") return;
  const rest = Math.max(0, Math.round((endAt - Date.now()) / 1000));
  remaining.value = rest;
  if (rest <= 0) finishTimer();
}

onUnmounted(() => {
  window.removeEventListener("focus", loadUnfinishedTasks);
  window.removeEventListener("beforeunload", beforeUnloadHandler);
  document.removeEventListener("visibilitychange", resyncOnVisible);
  clearInterval(timerId);
  clearInterval(dayTicker);
});
</script>

<style scoped>
.timer-page { max-width: 680px; margin: 0 auto; }
.timer-card { text-align: center; padding: 24px; }
.duration-config {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}
.duration-item { display: flex; align-items: center; gap: 6px; }
.duration-label { color: #666; font-size: 14px; }
.duration-unit { color: #999; font-size: 13px; }
.hint { color: #bbb; font-size: 12px; margin: 8px 0 0; }
.timer-body { margin: 24px 0; display: flex; justify-content: center; }
.time-text { font-size: 44px; font-weight: bold; color: #333; letter-spacing: 2px; }
.mode-text { color: #888; margin-top: 4px; }
.task-bind { margin-bottom: 20px; }
.btn-group { display: flex; justify-content: center; gap: 12px; margin-top: 8px; }
.record-message { color: #67c23a; font-size: 13px; margin: 12px 0 0; }
.today-summary { color: #666; }
</style>

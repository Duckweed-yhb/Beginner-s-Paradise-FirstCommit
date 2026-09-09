<template>
  <div class="timer-page">
    <el-card class="timer-card">
      <h2>🍅 番茄专注计时器</h2>

      <!-- 模式切换：专注 / 休息 -->
      <el-radio-group v-model="mode" @change="resetTimer">
        <el-radio-button label="focus">专注 {{ focusMinutes }} 分钟</el-radio-button>
        <el-radio-button label="break">休息 {{ breakMinutes }} 分钟</el-radio-button>
      </el-radio-group>

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
            <div class="mode-text">{{ mode === "focus" ? "专注中" : "休息中" }}</div>
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
          <el-option v-for="t in unfinishedTasks" :key="t.id" :label="t.name" :value="t.id" />
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
          ▶ 开始
        </el-button>
        <el-button v-else type="warning" size="large" @click="pauseTimer">⏸ 暂停</el-button>

        <el-button size="large" :disabled="status === 'idle'" @click="resetTimer">
          ↺ 重置
        </el-button>
      </div>

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
import { createRecord } from "../api";

// ===== 配置 =====
const focusMinutes = 25;
const breakMinutes = 5;

// ===== 计时器状态 =====
const mode = ref("focus");
const status = ref("idle"); // idle / running / paused
const totalSeconds = ref(focusMinutes * 60);
const remaining = ref(totalSeconds.value);
let timerId = null;

const bindTaskId = ref(null);

// ===== 未完成任务（用于绑定选择） =====
const unfinishedTasks = ref([]);
onMounted(() => {
  loadUnfinishedTasks();
  // 每次回到页面刷新可选任务
  window.addEventListener("focus", loadUnfinishedTasks);
});
onUnmounted(() => {
  window.removeEventListener("focus", loadUnfinishedTasks);
  clearInterval(timerId);
  window.removeEventListener("beforeunload", beforeUnloadHandler);
});

function loadUnfinishedTasks() {
  const tasks = JSON.parse(localStorage.getItem("focus_tasks")) || [];
  unfinishedTasks.value = tasks.filter((t) => !t.done);
}

// ===== 专注记录 =====
const records = ref(JSON.parse(localStorage.getItem("focus_records")) || []);

function saveRecords() {
  localStorage.setItem("focus_records", JSON.stringify(records.value));
}

// ===== 显示 =====
const displayTime = computed(() => {
  const m = String(Math.floor(remaining.value / 60)).padStart(2, "0");
  const s = String(remaining.value % 60).padStart(2, "0");
  return `${m}:${s}`;
});

const progressPercent = computed(() =>
  Math.round(((totalSeconds.value - remaining.value) / totalSeconds.value) * 100)
);

// ===== 核心逻辑 =====
function startTimer() {
  if (status.value === "idle") {
    totalSeconds.value = mode.value === "focus" ? focusMinutes * 60 : breakMinutes * 60;
    remaining.value = totalSeconds.value;
  }
  status.value = "running";
  timerId = setInterval(() => {
    remaining.value--;
    if (remaining.value <= 0) {
      clearInterval(timerId);
      timerId = null;
      onTimerComplete();
    }
  }, 1000);
}

function pauseTimer() {
  clearInterval(timerId);
  timerId = null;
  status.value = "paused";
}

function resetTimer() {
  clearInterval(timerId);
  timerId = null;
  status.value = "idle";
  totalSeconds.value = mode.value === "focus" ? focusMinutes * 60 : breakMinutes * 60;
  remaining.value = totalSeconds.value;
}

async function onTimerComplete() {
  status.value = "idle";

  if (mode.value === "focus") {
    const bindTask = unfinishedTasks.value.find((t) => t.id === bindTaskId.value);
    const record = {
      id: Date.now(),
      taskName: bindTask ? bindTask.name : "未绑定任务",
      subject: bindTask ? bindTask.subject : "未分类",
      minutes: focusMinutes,
      date: new Date().toISOString().slice(0, 10),
    };
    records.value.push(record);
    saveRecords();

    // 同步一条到后端（失败不影响本地）
    try {
      await createRecord(record);
    } catch (e) {
      // 后端未启动：仅保存在本地
    }

    ElNotification({
      title: "🎉 专注完成！",
      message: "太棒了，休息 5 分钟吧",
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

// ===== 离开页面提醒（运行中切走会弹提示） =====
watch(status, (val) => {
  if (val === "running") {
    window.addEventListener("beforeunload", beforeUnloadHandler);
  } else {
    window.removeEventListener("beforeunload", beforeUnloadHandler);
  }
});

function beforeUnloadHandler(e) {
  e.preventDefault();
  e.returnValue = "";
}

// ===== 今日汇总 =====
const today = new Date().toISOString().slice(0, 10);
const todayMinutes = computed(() =>
  records.value.filter((r) => r.date === today).reduce((s, r) => s + r.minutes, 0)
);
const todayCount = computed(() => records.value.filter((r) => r.date === today).length);
</script>

<style scoped>
.timer-page { max-width: 640px; margin: 0 auto; }
.timer-card { text-align: center; padding: 24px; }
.timer-body { margin: 24px 0; display: flex; justify-content: center; }
.time-text { font-size: 44px; font-weight: bold; color: #333; letter-spacing: 2px; }
.mode-text { color: #888; margin-top: 4px; }
.task-bind { margin-bottom: 20px; }
.btn-group { display: flex; justify-content: center; gap: 12px; margin-top: 8px; }
.today-summary { color: #666; }
</style>

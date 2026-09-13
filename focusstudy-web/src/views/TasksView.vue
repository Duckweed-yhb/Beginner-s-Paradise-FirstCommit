<template>
  <div class="tasks-page">
    <!-- ① 新增任务表单 -->
    <el-card class="form-card">
      <h2>➕ 新增任务</h2>
      <el-form :inline="true" @submit.prevent>
        <el-form-item label="任务名称">
          <el-input
            v-model="form.name"
            placeholder="如：完成数学第五章习题"
            style="width: 240px"
            clearable
            maxlength="100"
            @keyup.enter="addTask"
          />
        </el-form-item>

        <el-form-item label="科目">
          <el-select v-model="form.subject" placeholder="选择科目" style="width: 130px">
            <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>

        <el-form-item label="优先级">
          <el-select v-model="form.priority" style="width: 110px">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>

        <el-form-item label="截止日期">
          <el-date-picker
            v-model="form.deadline"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择日期"
            style="width: 160px"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="adding" @click="addTask">
            添加任务
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 同步状态：诚实告诉用户数据在哪儿 -->
      <p class="sync-hint" :class="syncStateClass">{{ syncHint }}</p>
    </el-card>

    <!-- ② 任务列表 -->
    <el-card>
      <div class="list-header">
        <h2>📋 我的任务（{{ unfinishedCount }} 项未完成）</h2>
        <el-radio-group v-model="filter" size="small">
          <el-radio-button value="all">全部</el-radio-button>
          <el-radio-button value="active">未完成</el-radio-button>
          <el-radio-button value="done">已完成</el-radio-button>
        </el-radio-group>
      </div>

      <el-empty
        v-if="tasks.length === 0"
        description="还没有任务，先添加一个吧"
      />
      <el-empty
        v-else-if="visibleTasks.length === 0"
        :description="filter === 'active' ? '太棒了，没有未完成的任务！' : '还没有已完成的任务'"
      />

      <el-table v-else :data="visibleTasks" stripe>
        <el-table-column label="完成" width="70" align="center">
          <template #default="{ row }">
            <el-checkbox
              :model-value="row.done"
              @change="() => toggleTask(row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="任务名称" min-width="180">
          <template #default="{ row }">
            <span
              :style="{
                textDecoration: row.done ? 'line-through' : 'none',
                color: row.done ? '#bbb' : '#333',
              }"
            >
              {{ row.name }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="科目" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.subject }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="优先级" width="90">
          <template #default="{ row }">
            <el-tag :type="priorityType(row.priority)">
              {{ priorityText(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="截止日期" width="120">
          <template #default="{ row }">
            <span :class="{ overdue: isOverdue(row) }">
              {{ row.deadline }}
              <el-tooltip v-if="isOverdue(row)" content="已过期" placement="top">
                <el-icon><WarningFilled /></el-icon>
              </el-tooltip>
            </span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="editTask(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeTask(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- ③ 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑任务" width="420px">
      <el-form label-width="80px">
        <el-form-item label="任务名称">
          <el-input v-model="editing.name" maxlength="100" />
        </el-form-item>
        <el-form-item label="科目">
          <el-select v-model="editing.subject" style="width: 100%">
            <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="editing.priority" style="width: 100%">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="editing.deadline"
            type="date"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from "vue";
import { ElMessage } from "element-plus";
import {
  fetchTasks,
  createTask,
  updateTask,
  deleteTask,
  syncSilently,
} from "../api";
import { loadTasks, saveTasks } from "../storage";
import { todayString } from "../time";

// ===== 数据 =====
const subjects = [
  "数学", "英语", "语文", "物理", "化学",
  "生物", "历史", "地理", "政治", "编程",
];

const form = reactive({
  name: "",
  subject: "数学",
  priority: "medium",
  deadline: "",
});

// 本地 localStorage 是 UI 的权威数据源，服务器是同步目标
const tasks = ref(loadTasks());

// 防连点：添加按钮在请求进行中会转圈并禁用
const adding = ref(false);

const filter = ref("all");
const editDialogVisible = ref(false);
const editing = ref({});

// 同步状态提示：#7 修复 —— 现在编辑、完成、删除也会同步到后端
const syncOk = ref(null); // null=未探测, true=已连接, false=离线
const syncHint = computed(() => {
  if (syncOk.value === null) return "正在检测后端服务…";
  if (syncOk.value) return "已连接后端服务，改动会同步到服务器";
  return "后端未启动：数据仅保存在本机浏览器，功能完全正常";
});
const syncStateClass = computed(() => ({
  "sync-online": syncOk.value === true,
  "sync-offline": syncOk.value === false,
}));

// ===== 自动保存到 localStorage（本地数据兜底 + 即时可用） =====
watch(
  tasks,
  () => {
    saveTasks(tasks.value);
  },
  { deep: true }
);

// ===== 页面加载：尝试从后端同步 =====
onMounted(async () => {
  try {
    const remote = await fetchTasks();
    syncOk.value = true;

    // #6 修复：原来只有"后端非空"时才覆盖本地，导致后端为空时
    // 本地数据永远同步不上去。现在本地为空才用后端数据填充，
    // 两边都有数据时以本地为准（本地是用户实际在用的那份）。
    if (Array.isArray(remote) && remote.length > 0) {
      if (tasks.value.length === 0) {
        tasks.value = remote;
      }
    } else if (tasks.value.length > 0) {
      // 后端是空的但本地有数据：把本地已有的任务补推上去
      for (const task of tasks.value) {
        await syncSilently(
          createTask({
            name: task.name,
            subject: task.subject,
            priority: task.priority,
            deadline: task.deadline,
          })
        );
      }
    }
  } catch {
    // 后端未启动：使用本地 localStorage 数据
    syncOk.value = false;
  }
});

// ===== 新增 =====
async function addTask() {
  const name = form.name.trim();

  if (!name) {
    ElMessage.warning("请填写任务名称");
    return;
  }
  // 防连点 / 防重复任务
  if (adding.value) return;
  if (tasks.value.some((t) => t.name === name && !t.done)) {
    ElMessage.warning("已经有同名的未完成任务了");
    return;
  }

  adding.value = true;
  try {
    const newTask = {
      id: Date.now(),
      name,
      subject: form.subject,
      priority: form.priority,
      deadline: form.deadline || "未设置",
      done: false,
    };

    tasks.value.push(newTask);
    form.name = "";

    // 同步到后端（失败不影响本地使用）
    const ok = await syncSilently(
      createTask({
        name,
        subject: newTask.subject,
        priority: newTask.priority,
        deadline: newTask.deadline,
      })
    );
    if (ok) syncOk.value = true;
    saveTasks(tasks.value);
  } finally {
    adding.value = false;
  }
}

// ===== 切换完成状态 —— 现在会同步到后端 =====
async function toggleTask(row) {
  row.done = !row.done;
  saveTasks(tasks.value);

  // #7 修复：以前勾选完成只改本地，服务器上的 done 永远是 false。
  // 现在只把 done 这一个字段推上去，后端做的是局部更新，不会冲掉其他字段。
  await syncSilently(updateTask(row.id, { done: row.done }));
}

function removeTask(row) {
  tasks.value = tasks.value.filter((t) => t.id !== row.id);
  saveTasks(tasks.value);

  // 同步删除（id 对不上时后端返回 404，静默忽略即可）
  syncSilently(deleteTask(row.id));
}

function editTask(row) {
  editing.value = { ...row };
  editDialogVisible.value = true;
}

function saveEdit() {
  const target = tasks.value.find((t) => t.id === editing.value.id);
  if (!target) return;

  if (!editing.value.name || !editing.value.name.trim()) {
    ElMessage.warning("任务名称不能为空");
    return;
  }

  target.name = editing.value.name.trim();
  target.subject = editing.value.subject;
  target.priority = editing.value.priority;
  target.deadline = editing.value.deadline || "未设置";

  saveTasks(tasks.value);

  // 编辑也要同步到后端
  syncSilently(
    updateTask(target.id, {
      name: target.name,
      subject: target.subject,
      priority: target.priority,
      deadline: target.deadline,
    })
  );

  editDialogVisible.value = false;
  ElMessage.success("已保存");
}

// ===== 计算与工具 =====
const unfinishedCount = computed(() => tasks.value.filter((t) => !t.done).length);

const visibleTasks = computed(() => {
  if (filter.value === "active") return tasks.value.filter((t) => !t.done);
  if (filter.value === "done") return tasks.value.filter((t) => t.done);
  return tasks.value;
});

function priorityText(p) {
  return { high: "高", medium: "中", low: "低" }[p] || "中";
}

function priorityType(p) {
  return { high: "danger", medium: "warning", low: "info" }[p] || "info";
}

/** 截止日期早于今天且任务未完成 → 标记为过期 */
function isOverdue(row) {
  if (row.done) return false;
  if (!row.deadline || row.deadline === "未设置") return false;
  return row.deadline < todayString();
}
</script>

<style scoped>
.tasks-page { max-width: 1080px; margin: 0 auto; }
.form-card { margin-bottom: 20px; }
h2 { margin-top: 0; font-size: 18px; }
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}
.list-header h2 { margin: 0; }
.sync-hint { font-size: 12px; margin: 4px 0 0; }
.sync-online { color: #67c23a; }
.sync-offline { color: #e6a23c; }
.overdue { color: #f56c6c; }
</style>

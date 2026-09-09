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
          <el-button type="primary" @click="addTask">添加任务</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- ② 任务列表 -->
    <el-card>
      <h2>📋 我的任务（{{ unfinishedCount }} 项未完成）</h2>

      <el-empty v-if="tasks.length === 0" description="还没有任务，先添加一个吧" />

      <el-table v-else :data="tasks" stripe>
        <el-table-column label="完成" width="70" align="center">
          <template #default="{ row }">
            <el-checkbox :model-value="row.done" @change="toggleTask(row)" />
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

        <el-table-column prop="deadline" label="截止日期" width="120" />

        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="editTask(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeTask(row.id)">
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
          <el-input v-model="editing.name" />
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
import { fetchTasks, createTask } from "../api";

// ===== 数据 =====
const STORAGE_KEY = "focus_tasks";
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

const tasks = ref(JSON.parse(localStorage.getItem(STORAGE_KEY)) || []);

const editDialogVisible = ref(false);
const editing = ref({});

// ===== 自动保存到 localStorage（本地数据兜底 + 即时可用） =====
watch(
  tasks,
  () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks.value));
  },
  { deep: true }
);

// ===== 页面加载：尝试从后端同步（失败则安静地用本地数据） =====
onMounted(async () => {
  try {
    const remote = await fetchTasks();
    if (Array.isArray(remote) && remote.length > 0) {
      tasks.value = remote;
    }
  } catch (e) {
    // 后端未启动：使用本地 localStorage 数据
  }
});

// ===== 方法 =====
async function addTask() {
  const name = form.name.trim();
  if (!name) {
    alert("请填写任务名称");
    return;
  }
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

  // 尝试同步到后端（失败不影响本地使用）
  try {
    await createTask({
      name,
      subject: form.subject,
      priority: form.priority,
      deadline: form.deadline || "未设置",
    });
  } catch (e) {
    // 后端未启动：仅保存在本地
  }
}

function toggleTask(row) {
  row.done = !row.done;
}

function removeTask(id) {
  tasks.value = tasks.value.filter((t) => t.id !== id);
}

function editTask(row) {
  editing.value = { ...row };
  editDialogVisible.value = true;
}

function saveEdit() {
  const target = tasks.value.find((t) => t.id === editing.value.id);
  if (target) {
    target.name = editing.value.name;
    target.subject = editing.value.subject;
    target.priority = editing.value.priority;
    target.deadline = editing.value.deadline;
  }
  editDialogVisible.value = false;
}

// ===== 计算与工具 =====
const unfinishedCount = computed(() => tasks.value.filter((t) => !t.done).length);

function priorityText(p) {
  return { high: "高", medium: "中", low: "低" }[p] || "中";
}
function priorityType(p) {
  return { high: "danger", medium: "warning", low: "info" }[p] || "info";
}
</script>

<style scoped>
.tasks-page { max-width: 960px; margin: 0 auto; }
.form-card { margin-bottom: 20px; }
h2 { margin-top: 0; font-size: 18px; }
</style>

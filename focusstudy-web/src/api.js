// API 封装层：所有后端调用都走这里（第 15 课）
// 后端未启动时调用会失败，各页面已做 localStorage 容错

async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`请求失败: ${res.status}`);
  }
  return res.json();
}

// ===== 任务接口 =====
export const fetchTasks = () => request("/api/tasks");
export const createTask = (task) =>
  request("/api/tasks", { method: "POST", body: JSON.stringify(task) });

// ===== 专注记录接口 =====
export const fetchRecords = () => request("/api/records");
export const createRecord = (record) =>
  request("/api/records", { method: "POST", body: JSON.stringify(record) });

// ===== 统计接口 =====
export const fetchStats = () => request("/api/stats");

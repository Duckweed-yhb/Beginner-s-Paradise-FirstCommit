// API 封装层：所有后端调用都走这里（第 15 课）
//
// 设计原则：**后端是可选的**。
// 这个应用在完全离线、后端没启动的情况下也必须能正常用，
// 因为一个"网络一断就崩"的学习工具，本身就成了干扰源。
// 所以每个调用失败时都抛错，由页面决定怎么优雅降级到 localStorage。

const TIMEOUT_MS = 4000;

async function request(url, options = {}) {
  // 加超时：后端若挂起（不是拒绝连接而是卡住），没超时的话页面会一直转圈
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      ...options,
    });

    if (!res.ok) {
      throw new Error(`请求失败: ${res.status} ${res.statusText}`);
    }

    // DELETE 之类可能返回空响应体，这里做一下兼容
    const text = await res.text();
    return text ? JSON.parse(text) : null;
  } finally {
    clearTimeout(timer);
  }
}

// ===== 任务接口 =====
export const fetchTasks = () => request("/api/tasks");

export const createTask = (task) =>
  request("/api/tasks", { method: "POST", body: JSON.stringify(task) });

/** 局部更新任务：只传要改的字段，其余后端会保留 */
export const updateTask = (id, patch) =>
  request(`/api/tasks/${id}`, { method: "PUT", body: JSON.stringify(patch) });

export const deleteTask = (id) =>
  request(`/api/tasks/${id}`, { method: "DELETE" });

// ===== 专注记录接口 =====
export const fetchRecords = () => request("/api/records");

export const createRecord = (record) =>
  request("/api/records", { method: "POST", body: JSON.stringify(record) });

export const deleteRecord = (id) =>
  request(`/api/records/${id}`, { method: "DELETE" });

// ===== 统计接口 =====
export const fetchStats = () => request("/api/stats");

// ===== 工具：静默执行一个后端调用 =====
/**
 * 执行后端调用，失败时**安静地忽略**。
 * 页面的本地数据已经是权威来源，同步失败只影响服务器端副本，
 * 不应该给正在专注学习的用户弹任何错误提示。
 * @param {Promise} promise 后端调用
 * @returns {Promise<boolean>} 是否同步成功
 */
export async function syncSilently(promise) {
  try {
    await promise;
    return true;
  } catch {
    return false;
  }
}

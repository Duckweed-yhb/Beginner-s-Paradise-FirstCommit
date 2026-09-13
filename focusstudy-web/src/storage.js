// localStorage 数据层
//
// 为什么单独抽一个文件？
// 之前 "focus_tasks" 这个字符串在 TasksView 和 TimerView 里各写了一遍，
// 一旦哪边拼错，计时器就读不到任务列表，而且不会报错 —— 这种 bug 最难查。
// 现在 key 只定义一次，所有读写都走这里。

/** localStorage 的 key，集中管理，避免各处手写字符串拼错 */
export const KEYS = {
  TASKS: "focus_tasks",
  RECORDS: "focus_records",
  SETTINGS: "focus_settings",
};

/**
 * 安全读取 JSON。localStorage 里可能是 null，也可能被人为改成了非法 JSON，
 * 这两种情况都应该返回兜底值，而不是让整个页面白屏。
 * @param {string} key
 * @param {*} fallback 读不到或解析失败时返回的值
 */
export function readJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    if (raw === null) return fallback;
    const parsed = JSON.parse(raw);
    return parsed === null || parsed === undefined ? fallback : parsed;
  } catch {
    // 数据被改坏了：不要让它把页面搞崩
    return fallback;
  }
}

/**
 * 安全写入 JSON。
 * @param {string} key
 * @param {*} value
 * @returns {boolean} 是否写入成功（隐私模式 / 配额满时会失败）
 */
export function writeJSON(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    // 存储不可用（无痕模式、配额超限）时静默失败：
    // 页面仍然可用，只是刷新后数据会丢。
    return false;
  }
}

// ===== 任务 =====
export const loadTasks = () => readJSON(KEYS.TASKS, []);
export const saveTasks = (tasks) => writeJSON(KEYS.TASKS, tasks);

// ===== 专注记录 =====
export const loadRecords = () => readJSON(KEYS.RECORDS, []);
export const saveRecords = (records) => writeJSON(KEYS.RECORDS, records);

// ===== 设置（番茄时长等）=====
export const loadSettings = () => readJSON(KEYS.SETTINGS, {});
export const saveSettings = (settings) => writeJSON(KEYS.SETTINGS, settings);

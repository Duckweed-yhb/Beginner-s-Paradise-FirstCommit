// 时间与日期工具（第 16 课的跨天 bug 就是从这里修的）
//
// 为什么不能直接用 toISOString().slice(0, 10)？
// 因为 toISOString() 返回的是 **UTC** 时间。在中国（UTC+8），
// 本地 9 月 10 日凌晨 00:30 会被格式化成一个"还在 9 月 9 日"的 UTC 日期，
// 于是这个番茄就被记到了前一天 —— 而这恰恰是整个应用最核心的数据。
//
// 正确做法：用本地时区自己拼日期，不经过 UTC。

/**
 * 把 Date 对象格式化为本地时区的 YYYY-MM-DD。
 * @param {Date} [date] 默认取当前时间
 * @returns {string} 例如 "2026-09-10"
 */
export function toLocalDateString(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/**
 * 今天的本地日期字符串。
 * @returns {string}
 */
export function todayString() {
  return toLocalDateString(new Date());
}

/**
 * 取最近 n 天的本地日期字符串，按时间升序（最早的在前面）。
 * 用于"最近 7 天"柱状图的横轴。
 * @param {number} n
 * @returns {string[]}
 */
export function recentDates(n) {
  const dates = [];
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(toLocalDateString(d));
  }
  return dates;
}

/**
 * 把秒数格式化成 MM:SS。
 * @param {number} totalSeconds
 * @returns {string}
 */
export function formatClock(totalSeconds) {
  const safe = Math.max(0, Math.floor(totalSeconds));
  const m = String(Math.floor(safe / 60)).padStart(2, "0");
  const s = String(safe % 60).padStart(2, "0");
  return `${m}:${s}`;
}

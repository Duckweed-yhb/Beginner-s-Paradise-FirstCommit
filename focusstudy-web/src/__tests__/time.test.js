// time.js 的单元测试：本地时区日期是"最不能出错"的核心逻辑
import { describe, it, expect } from "vitest";
import { toLocalDateString, todayString, recentDates, formatClock } from "../time";

describe("time.js 本地日期工具", () => {
  it("toLocalDateString 用本地时区拼 YYYY-MM-DD，不经过 UTC", () => {
    // new Date(2026, 8, 10) 在本地时区就是 2026-09-10
    expect(toLocalDateString(new Date(2026, 8, 10))).toBe("2026-09-10");
    expect(toLocalDateString(new Date(2026, 0, 5))).toBe("2026-01-05");
  });

  it("todayString 返回 10 位日期", () => {
    expect(todayString()).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  it("recentDates(7) 返回 7 天、升序、最后一天是今天", () => {
    const dates = recentDates(7);
    expect(dates.length).toBe(7);
    expect(dates[dates.length - 1]).toBe(todayString());
    for (let i = 1; i < dates.length; i++) {
      expect(dates[i] > dates[i - 1]).toBe(true);
    }
  });

  it("formatClock 格式化与兜底", () => {
    expect(formatClock(90)).toBe("01:30");
    expect(formatClock(0)).toBe("00:00");
    expect(formatClock(-5)).toBe("00:00");
    expect(formatClock(25 * 60)).toBe("25:00");
  });
});

// storage.js 的单元测试：localStorage 读写的兜底行为
import { describe, it, expect, beforeEach } from "vitest";
import { KEYS, readJSON, writeJSON, loadTasks, saveTasks } from "../storage";

// node 环境没有 localStorage，这里给一个最小可用的内存替身
const store = new Map();
globalThis.localStorage = {
  getItem: (k) => (store.has(k) ? store.get(k) : null),
  setItem: (k, v) => store.set(k, String(v)),
  removeItem: (k) => store.delete(k),
  clear: () => store.clear(),
};

describe("storage.js localStorage 数据层", () => {
  beforeEach(() => store.clear());

  it("key 各不相同且含义清晰", () => {
    expect(KEYS.TASKS).toBe("focus_tasks");
    expect(KEYS.RECORDS).toBe("focus_records");
    expect(KEYS.SETTINGS).toBe("focus_settings");
    expect(new Set(Object.values(KEYS)).size).toBe(3);
  });

  it("保存后能读回同样的数据", () => {
    const tasks = [{ id: 1, name: "数学", done: false }];
    saveTasks(tasks);
    expect(loadTasks()).toEqual(tasks);
  });

  it("读不到时返回兜底值而不是报错", () => {
    expect(readJSON("not-exists", [])).toEqual([]);
  });

  it("localStorage 里是坏 JSON 时返回兜底值", () => {
    store.set(KEYS.TASKS, "{ this is not json");
    expect(loadTasks()).toEqual([]);
  });

  it("写失败（如配额满）时返回 false 而不是抛错", () => {
    globalThis.localStorage.setItem = () => {
      throw new Error("QuotaExceededError");
    };
    expect(writeJSON(KEYS.TASKS, [])).toBe(false);
  });
});

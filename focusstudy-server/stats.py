"""FocusStudy 专注数据统计核心逻辑。

这个模块刻意做成**纯函数、无副作用**：不读文件、不碰网络、不依赖 FastAPI。
好处是它可以被单元测试完整覆盖（见 tests/test_stats.py），
接口层 main.py 只负责"取数据 → 调这里 → 返回 JSON"。

负责人备注：把这些逻辑从接口里抽出来，是第 16 课"测试与打磨"里学到的
分层思想 —— 业务逻辑和传输层分开，才好单独验证。
"""

from typing import Dict, List, Optional

# 未指定科目时的兜底分类名
DEFAULT_SUBJECT = "未分类"


def total_minutes(records: List[dict]) -> int:
    """累计专注分钟数。

    对缺字段 / 非数字的脏数据做容错，避免一条坏记录让整个统计接口 500。
    """
    total = 0
    for record in records:
        minutes = record.get("minutes")
        if isinstance(minutes, bool):  # bool 是 int 的子类，要单独排除
            continue
        if isinstance(minutes, (int, float)):
            total += int(minutes)
    return total


def group_by_subject(records: List[dict]) -> Dict[str, int]:
    """按科目聚合专注分钟数。

    返回示例：{"数学": 75, "英语": 25}
    """
    result: Dict[str, int] = {}
    for record in records:
        subject = record.get("subject") or DEFAULT_SUBJECT
        minutes = record.get("minutes")
        if isinstance(minutes, bool) or not isinstance(minutes, (int, float)):
            continue
        result[subject] = result.get(subject, 0) + int(minutes)
    return result


def group_by_date(records: List[dict]) -> Dict[str, int]:
    """按日期聚合专注分钟数（日期形如 2026-09-10）。

    缺日期的记录统一归到"未知"，而不是丢弃 —— 数据宁可粗糙也不要凭空消失。
    """
    result: Dict[str, int] = {}
    for record in records:
        day = record.get("date") or "未知"
        minutes = record.get("minutes")
        if isinstance(minutes, bool) or not isinstance(minutes, (int, float)):
            continue
        result[day] = result.get(day, 0) + int(minutes)
    return result


def build_summary(records: List[dict]) -> dict:
    """汇总接口的完整返回体，前端 /api/stats 直接用这个。"""
    return {
        "total_minutes": total_minutes(records),
        "total_count": len(records),
        "by_subject": group_by_subject(records),
        "by_date": group_by_date(records),
    }


def find_by_id(items: List[dict], item_id: int) -> Optional[dict]:
    """按 id 查找一条记录，找不到返回 None。"""
    for item in items:
        if item.get("id") == item_id:
            return item
    return None

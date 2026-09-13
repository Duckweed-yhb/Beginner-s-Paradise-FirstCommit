"""stats.py 的单元测试。

运行：
    cd focusstudy-server
    python -m pytest -v

这些测试覆盖了我在开发中真实踩到的边界情况：
脏数据、缺字段、bool 混进数字、空列表。
"""

import stats


def test_total_minutes_normal():
    records = [
        {"minutes": 25},
        {"minutes": 50},
        {"minutes": 5},
    ]
    assert stats.total_minutes(records) == 80


def test_total_minutes_empty():
    assert stats.total_minutes([]) == 0


def test_total_minutes_ignores_dirty_data():
    """脏数据不能让统计崩掉，也不能算错。"""
    records = [
        {"minutes": 30},
        {"minutes": None},          # 缺值
        {"minutes": "25"},          # 字符串
        {},                          # 整个字段都没有
        {"minutes": True},          # bool 是 int 的子类，必须排掉
        {"minutes": 10.7},          # 浮点取整
    ]
    assert stats.total_minutes(records) == 40


def test_group_by_subject():
    records = [
        {"subject": "数学", "minutes": 25},
        {"subject": "数学", "minutes": 50},
        {"subject": "英语", "minutes": 25},
    ]
    assert stats.group_by_subject(records) == {"数学": 75, "英语": 25}


def test_group_by_subject_missing_goes_to_default():
    """科目缺失的记录归到"未分类"，不能丢。"""
    records = [{"minutes": 25}, {"subject": "", "minutes": 5}]
    assert stats.group_by_subject(records) == {stats.DEFAULT_SUBJECT: 30}


def test_group_by_date():
    records = [
        {"date": "2026-09-09", "minutes": 25},
        {"date": "2026-09-09", "minutes": 25},
        {"date": "2026-09-10", "minutes": 50},
    ]
    assert stats.group_by_date(records) == {"2026-09-09": 50, "2026-09-10": 50}


def test_group_by_date_missing_goes_to_unknown():
    records = [{"minutes": 25}]
    assert stats.group_by_date(records) == {"未知": 25}


def test_build_summary_shape():
    """汇总返回体的结构必须稳定，前端依赖这些 key。"""
    records = [
        {"subject": "数学", "minutes": 25, "date": "2026-09-09"},
        {"subject": "英语", "minutes": 30, "date": "2026-09-10"},
    ]
    summary = stats.build_summary(records)

    assert summary["total_minutes"] == 55
    assert summary["total_count"] == 2
    assert summary["by_subject"] == {"数学": 25, "英语": 30}
    assert summary["by_date"] == {"2026-09-09": 25, "2026-09-10": 30}


def test_find_by_id():
    items = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    assert stats.find_by_id(items, 2)["name"] == "b"
    assert stats.find_by_id(items, 999) is None
    assert stats.find_by_id([], 1) is None

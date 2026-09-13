"""接口层集成测试：用 FastAPI TestClient 打真实 HTTP 请求。

每个用例都把数据目录换到临时文件夹（monkeypatch），
所以跑测试**不会**污染你本地的 data/tasks.json。

运行：
    cd focusstudy-server
    python -m pytest -v
"""

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    """把后端的数据目录指向 pytest 的临时目录，保证测试互不干扰。"""
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    with TestClient(main.app) as c:
        yield c


def test_root_health(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "运行中" in res.json()["message"]


def test_tasks_start_empty(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.json() == []


def test_create_and_list_task(client):
    res = client.post(
        "/api/tasks",
        json={"name": "完成数学第五章", "subject": "数学", "priority": "high"},
    )
    assert res.status_code == 201
    created = res.json()
    assert created["name"] == "完成数学第五章"
    assert created["done"] is False
    assert isinstance(created["id"], int)

    listed = client.get("/api/tasks").json()
    assert len(listed) == 1
    assert listed[0]["id"] == created["id"]


def test_create_task_rejects_empty_name(client):
    """空名称必须被挡下来（第 16 课自测清单里的边界情况）。"""
    res = client.post("/api/tasks", json={"name": ""})
    assert res.status_code == 422


def test_create_task_rejects_bad_priority(client):
    res = client.post("/api/tasks", json={"name": "x", "priority": "urgent"})
    assert res.status_code == 422


def test_update_task_partial_patch_keeps_other_fields(client):
    """只传 done 时，名称/科目不能被冲掉 —— 这是勾选完成功能的关键。"""
    task_id = client.post(
        "/api/tasks", json={"name": "背单词", "subject": "英语"}
    ).json()["id"]

    res = client.put(f"/api/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    updated = res.json()
    assert updated["done"] is True
    assert updated["name"] == "背单词"
    assert updated["subject"] == "英语"


def test_update_missing_task_returns_404(client):
    res = client.put("/api/tasks/123456", json={"done": True})
    assert res.status_code == 404


def test_delete_task(client):
    task_id = client.post("/api/tasks", json={"name": "临时任务"}).json()["id"]

    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["remaining"] == 0
    assert client.get("/api/tasks").json() == []


def test_delete_missing_task_returns_404(client):
    assert client.delete("/api/tasks/999999").status_code == 404


def test_create_record_fills_local_date(client):
    """date 留空时后端用本地日期补上（不是 UTC）。"""
    res = client.post(
        "/api/records",
        json={"taskName": "数学作业", "subject": "数学", "minutes": 25},
    )
    assert res.status_code == 201
    record = res.json()
    assert record["date"] == main.local_today()
    assert len(record["date"]) == 10  # YYYY-MM-DD


def test_create_record_rejects_zero_or_negative_minutes(client):
    assert client.post("/api/records", json={"minutes": 0}).status_code == 422
    assert client.post("/api/records", json={"minutes": -25}).status_code == 422


def test_stats_aggregates_records(client):
    client.post("/api/records", json={"subject": "数学", "minutes": 25, "date": "2026-09-09"})
    client.post("/api/records", json={"subject": "数学", "minutes": 25, "date": "2026-09-10"})
    client.post("/api/records", json={"subject": "英语", "minutes": 50, "date": "2026-09-10"})

    data = client.get("/api/stats").json()
    assert data["total_minutes"] == 100
    assert data["total_count"] == 3
    assert data["by_subject"] == {"数学": 50, "英语": 50}
    assert data["by_date"] == {"2026-09-09": 25, "2026-09-10": 75}


def test_stats_empty_returns_zeros(client):
    data = client.get("/api/stats").json()
    assert data == {
        "total_minutes": 0,
        "total_count": 0,
        "by_subject": {},
        "by_date": {},
    }


def test_delete_record(client):
    record_id = client.post("/api/records", json={"minutes": 25}).json()["id"]
    assert client.delete(f"/api/records/{record_id}").status_code == 200
    assert client.get("/api/records").json() == []


def test_corrupted_data_file_does_not_crash(tmp_path, monkeypatch):
    """data 文件被改坏时接口应该退化成空数据，而不是 500。"""
    monkeypatch.setattr(main, "DATA_DIR", str(tmp_path))
    (tmp_path / "tasks.json").write_text("{ this is not json", encoding="utf-8")

    with TestClient(main.app) as c:
        assert c.get("/api/tasks").json() == []

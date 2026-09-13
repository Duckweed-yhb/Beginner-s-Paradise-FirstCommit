"""pytest 全局配置：把临时目录固定在项目内。

为什么需要这个文件：
pytest 默认把临时目录建在系统 %TEMP% 下，并在会话结束时遍历清理。
在某些受限环境（沙箱 / 权限收紧的机器）里，这一步会抛
`PermissionError: [WinError 5]`，让 **全部用例在 teardown 阶段报错**，
看起来像测试失败，其实用例本身是过的。

这里的做法是自己提供 tmp_path，把目录固定到 tests/.tmp/ 下，
完全绕开系统临时目录，同时覆盖掉 pytest 的清理钩子。
这样在任何机器上 `python -m pytest` 都能干净地跑完。
"""

import shutil
from pathlib import Path

import pytest

TMP_ROOT = Path(__file__).parent / ".tmp"


@pytest.fixture
def tmp_path(request):
    """给每个用例一个独立且可写的临时目录（项目内，不用系统 %TEMP%）。"""
    safe_name = request.node.name.replace("/", "_").replace("\\", "_")
    path = TMP_ROOT / safe_name
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)
    return path


def pytest_sessionfinish(session, exitstatus):
    """会话结束时清理测试临时文件。

    覆盖 pytest 自带的 basetemp 清理逻辑（它会在受限环境下报 WinError 5）。
    这里用 ignore_errors=True，清理失败也绝不影响测试结论。
    """
    shutil.rmtree(TMP_ROOT, ignore_errors=True)

"""
monitor.py — 变化监控模块
职责：对比当前内容和上次快照，检测变化
"""
from fetcher import fetch_page, save_snapshot, load_latest_snapshot


def check_change(url: str = None) -> dict:
    """
    检查目标网页是否发生变化。

    返回:
        {
            "changed": True/False,
            "current": "当前内容",
            "previous": "上次内容",
            "snapshot_path": "新快照路径"
        }
    """
    current = fetch_page(url)
    previous = load_latest_snapshot()

    result = {
        "current": current,
        "previous": previous,
    }

    if previous is None:
        # 第一次运行，没有历史快照
        path = save_snapshot(current)
        result["changed"] = True
        result["snapshot_path"] = path
        result["message"] = "首次快照已保存"
    elif current.strip() != previous.strip():
        # 内容发生了变化
        path = save_snapshot(current)
        result["changed"] = True
        result["snapshot_path"] = path
        result["message"] = "检测到网页内容变化"
    else:
        result["changed"] = False
        result["message"] = "内容无变化"

    return result


def get_diff(previous: str, current: str, max_length: int = 2000) -> str:
    """
    简单对比两段文本，找出新增和删除。
    返回变更摘要。
    """
    prev_set = set(previous.splitlines())
    curr_set = set(current.splitlines())

    added = curr_set - prev_set
    removed = prev_set - curr_set

    parts = []
    if added:
        parts.append(f"[新增内容 {len(added)} 行]:\n" + "\n".join(list(added)[:10]))
    if removed:
        parts.append(f"[删除内容 {len(removed)} 行]:\n" + "\n".join(list(removed)[:10]))

    result = "\n\n".join(parts)
    return result[:max_length]
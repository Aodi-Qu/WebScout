"""
fetcher.py — 网页抓取模块
职责：下载网页内容，提取纯文本
"""
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from config import SNAPSHOT_DIR, TARGET_URL

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def fetch_page(url: str = None) -> str:
    """
    抓取网页 HTML，提取正文文本。
    返回纯文本内容。
    """
    if url is None:
        url = TARGET_URL

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    # 去掉 script 和 style 标签
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text()
    # 清理多余空行
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def save_snapshot(content: str) -> str:
    """
    保存网页快照到 snapshots/ 目录。
    返回快照文件路径。
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SNAPSHOT_DIR, f"snapshot_{timestamp}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def load_latest_snapshot() -> str | None:
    """
    加载最近一次的快照内容。
    如果没有历史快照，返回 None。
    """
    files = sorted(os.listdir(SNAPSHOT_DIR))
    if not files:
        return None

    latest = files[-1]
    with open(os.path.join(SNAPSHOT_DIR, latest), "r", encoding="utf-8") as f:
        return f.read()
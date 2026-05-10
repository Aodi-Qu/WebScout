"""
reporter.py — 报告生成模块
职责：调用 LLM 总结网页变化，生成可读报告
"""
import os
from datetime import datetime
from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, REPORT_DIR

_client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
os.makedirs(REPORT_DIR, exist_ok=True)


def summarize_change(previous: str, current: str) -> str:
    """用 LLM 总结网页变化内容"""
    if not previous:
        return "首次监控，已保存快照。"

    prompt = f"""下面是一个网页的旧内容和新内容。请用1-3句话总结发生了什么变化。

旧内容片段：
{previous[:1500]}

新内容片段：
{current[:1500]}

请直接描述变化，不要多余的话。"""

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM 总结失败] {e}"


def save_report(summary: str, url: str) -> str:
    """保存监控报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORT_DIR, f"report_{timestamp}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"监控网址: {url}\n")
        f.write(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"变化摘要:\n{summary}\n")
    return filepath
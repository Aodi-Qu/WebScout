"""
main.py — 主入口（定时监控版）
"""
import time
from notifier import send_change_notification
from monitor import check_change
from reporter import summarize_change, save_report
from config import TARGET_URL


def run_once():
    """执行一次监控检查"""
    print(f"\n{'='*40}")
    print(f"  ⏰ {time.strftime('%H:%M:%S')} — 正在检查...")
    print(f"  目标: {TARGET_URL}")

    result = check_change(TARGET_URL)
    print(f"  📡 {result['message']}")

    if result["changed"]:
        summary = summarize_change(
            result.get("previous", ""),
            result["current"]
        )
        print(f"  📝 变化摘要: {summary}")
        report_path = save_report(summary, TARGET_URL)
        print(f"  📄 报告已保存: {report_path}")
        send_change_notification(TARGET_URL, summary)
    else:
        print("  ✅ 无变化")

    return result["changed"]


def main():
    INTERVAL = 180  # 检查间隔（秒），180 = 3分钟

    print("=" * 40)
    print("  WebScout — 定时网页监控 Agent")
    print(f"  目标: {TARGET_URL}")
    print(f"  间隔: 每 {INTERVAL} 秒检查一次")
    print("  按 Ctrl+C 停止")
    print("=" * 40)

    # 立即执行一次
    run_once()

    # 循环定时执行
    while True:
        try:
            print(f"\n💤 等待 {INTERVAL} 秒后进行下一次检查...")
            time.sleep(INTERVAL)
            run_once()
        except KeyboardInterrupt:
            print("\n\n👋 监控已停止")
            break


if __name__ == "__main__":
    main()
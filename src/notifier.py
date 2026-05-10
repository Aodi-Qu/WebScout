"""
notifier.py — 邮件通知模块
职责：检测到网页变化时发送邮件通知
"""
import smtplib
from email.mime.text import MIMEText
from config import SMTP_EMAIL, SMTP_PASSWORD, NOTIFY_EMAIL


def send_change_notification(url: str, summary: str) -> bool:
    """发送变化通知邮件"""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print("  ⚠️ 未配置邮件，跳过通知")
        return False

    subject = f"🔔 网页监控告警: {url[:50]}"
    body = f"""监控目标: {url}

变化摘要:
{summary}

请及时查看。
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = NOTIFY_EMAIL

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, [NOTIFY_EMAIL], msg.as_string())
        server.quit()
        print("  📧 邮件通知已发送")
        return True
    except Exception as e:
        print(f"  ❌ 邮件发送失败: {e}")
        return False
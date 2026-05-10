import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LLM_BASE_URL = "https://api.deepseek.com"
LLM_MODEL = "deepseek-chat"

SNAPSHOT_DIR = "snapshots"
REPORT_DIR = "reports"

# 监控目标（可以加多个网址）
TARGET_URL = "https://top.baidu.com/board?tab=realtime"


# 邮件通知配置
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")
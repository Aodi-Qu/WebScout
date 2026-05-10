# WebScout — 网页变化监控与智能摘要 Agent

定时抓取目标网页，检测内容变化，调用 LLM 生成变化摘要，并通过邮件自动推送告警。

## 功能演示

- 每 3 分钟自动检查目标网页
- 发现变化 → LLM 自动总结变化内容
- 发送邮件通知，秒收告警

## 技术栈

Python / Requests / BeautifulSoup / DeepSeek API / SMTP

## 核心模块

| 模块 | 功能 |
|:---|:---|
| `fetcher.py` | 网页抓取：Requests + BeautifulSoup，过滤噪音标签 |
| `monitor.py` | 变化检测：对比历史快照，集合运算定位新增/删除行 |
| `reporter.py` | LLM 智能摘要：新旧内容发给大模型，生成变化总结 |
| `notifier.py` | 邮件通知：SMTP 自动发送告警邮件 |
| `main.py` | 定时循环监控，间隔可配置 |

## 项目亮点

- 检测 → 摘要 → 通知，端到端闭环
- LLM 替代人工肉眼对比，自动生成变化报告
- 定时轮询机制，可配置检查间隔
- 快照存档，支持事后追溯

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/Aodi-Qu/WebScout.git
cd WebScout

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建 .env 文件
echo DEEPSEEK_API_KEY=你的Key > .env
echo SMTP_EMAIL=你的QQ邮箱@qq.com >> .env
echo SMTP_PASSWORD=QQ邮箱授权码 >> .env
echo NOTIFY_EMAIL=接收通知的邮箱 >> .env

# 4. 修改 src/config.py 中的 TARGET_URL

# 5. 运行
cd src
python main.py

# 快速开始

## 安装依赖

```bash
pip install requests
```

## 使用方法

### 1. 查询新股日历

```bash
python scripts/get_ipo_calendar.py
```

### 2. 查询中签率

```bash
python scripts/get_ipo_win_rate.py
```

### 3. 设置每日提醒

可以使用 cron 功能设置每日早上9点提醒：

```bash
# 使用 OpenClaw cron
openclaw cron add --name "打新提醒" --schedule "every 9:00" --payload "check_ipo_alert"
```

## 配置

复制 `assets/config.example.json` 为 `config.json` 并配置：

```json
{
  "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
}
```

## 在 OpenClaw 中使用

直接对话触发：
- "今天有哪些新股可以申购"
- "查看中签率"
- "设置打新提醒"

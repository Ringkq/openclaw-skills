---
name: stock-ipo-alert
description: A股打新提醒工具。提供新股申购日历、中签率提醒、新股上市提醒、打新收益统计等功能。使用场景：查询今日/近期可申购的新股、设置新股申购提醒、查看中签率数据、获取新股上市通知、统计打新收益。触发关键词：新股、打新、申购、IPO、中签、新股上市、打新收益。
---

# A股打新提醒 (stock-ipo-alert)

## 功能概览

本技能提供A股打新全流程服务，包括：

1. **新股申购日历** - 查看今日/本周/本月可申购的新股
2. **中签率查询** - 实时获取各新股中签率数据
3. **上市提醒** - 新股上市价格和收益提醒
4. **打新统计** - 历史打新收益汇总分析

## 数据来源

使用东方财富网API获取数据：
- 新股申购日历：`http://datacenter.eastmoney.com/api/data/v1/get`
- 中签率数据：同上

## 使用示例

### 查询今日可申购新股

```bash
curl "http://datacenter.eastmoney.com/api/data/v1/get?reportName=RPT_BONDLIST&columns=ALL&filter=..."
```

或使用本技能提供的脚本：
```bash
python scripts/get_ipo_calendar.py
```

### 查看中签率

```bash
python scripts/get_ipo_win_rate.py
```

### 设置打新提醒

使用cron功能设置每日打新提醒：
```bash
openclaw cron add --schedule "every 9:00" --payload "打新提醒"
```

## 脚本说明

### scripts/get_ipo_calendar.py

获取近期可申购新股列表。

输出字段：
- 股票代码
- 股票名称
- 申购代码
- 申购价格
- 申购上限
- 申购日期
- 上市日期

### scripts/get_ipo_win_rate.py

获取历史新股中签率数据。

输出字段：
- 股票代码
- 股票名称
- 中签率
- 申购人数
- 冻结资金

### scripts/check_ipo_alert.py

检查是否有新股即将上市，发送提醒通知。

## 配置说明

### 环境变量

可选配置：
- `IPO_ALERT_WEBHOOK`: 提醒推送的Webhook地址
- `IPO_ALERT_WECHAT`: 企业微信通知配置

### 通知方式

支持以下通知方式：
1. 企业微信消息 (wecom_mcp)
2. 飞书消息
3. Telegram bot
4. Webhook

## 扩展功能

### 打新收益计算

根据新股上市首日涨幅计算打新收益：

```python
def calculate_ipo_profit(stock_price, increase_rate):
    # 沪市一签1000股，深市一签500股
    shares = 1000 if stock_price.startswith('6') else 500
    profit = stock_price * shares * (increase_rate / 100)
    return profit
```

### 智能推荐

根据中签率和历史收益数据，推荐最优打新标的：

1. 优先选择主板新股
2. 关注发行价较低的新股
3. 考虑流通盘大小

## 注意事项

1. 打新需要市值配售，沪市每持有1万元市值可申购1签
2. 中签后需在T+1日16:00前存入足额资金
3. 新股申购可能破发，请理性投资

## 相关工具

- `stock` 技能：股票行情查询
- `stock-analysis` 技能：股票深度分析
- `wecom_mcp` 工具：企业微信消息发送

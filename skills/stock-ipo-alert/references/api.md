# A股打新数据接口参考

## 东方财富API

### 新股申购日历

接口地址：
```
http://datacenter.eastmoney.com/api/data/v1/get
```

参数：
```json
{
  "reportName": "RPT_BONDLIST",
  "columns": "ALL",
  "filter": "(XSGX='网下')(STOCKCODE='000001')",
  "pageNumber": "1",
  "pageSize": "50",
  "source": "WEB"
}
```

### 中签率查询

接口地址：
```
http://datacenter.eastmoney.com/api/data/v1/get
```

参数：
```json
{
  "reportName": "RPT_IPO_DETAIL",
  "columns": "ALL",
  "filter": "(IPO_DATE=2026-03-29)",
  "source": "WEB"
}
```

## 字段说明

### 新股日历字段
| 字段 | 说明 |
|------|------|
| STOCKCODE | 股票代码 |
| STOCKNAME | 股票名称 |
| SGCODE | 申购代码 |
| ISSUEPRICE | 发行价格 |
| MAXSUBSCRIBE | 申购上限 |
| SGGZR | 申购日期 |
| LISTINGDATE | 上市日期 |

### 中签率字段
| 字段 | 说明 |
|------|------|
| STOCKCODE | 股票代码 |
| STOCKNAME | 股票名称 |
| WINRATE | 中签率 |
| APPLYNUM | 申购人数 |
| FUNDS | 冻结资金 |

## 数据示例

### 新股申购日历响应
```json
{
  "data": [
    {
      "STOCKCODE": "603139",
      "STOCKNAME": "康瑞电梯",
      "SGCODE": "732139",
      "ISSUEPRICE": 15.80,
      "MAXSUBSCRIBE": 15000,
      "SGGZR": "2026-03-30",
      "LISTINGDATE": "2026-04-08"
    }
  ]
}
```

### 中签率响应
```json
{
  "data": [
    {
      "STOCKCODE": "603139",
      "STOCKNAME": "康瑞电梯",
      "WINRATE": 0.032,
      "APPLYNUM": 1234567,
      "FUNDS": 1234567890
    }
  ]
}
```

## 错误处理

- 网络超时：重试3次，每次间隔5秒
- 数据为空：返回提示"今日无新股申购"
- API错误：记录日志并返回降级数据

## 限流说明

东方财富API限流：
- 每分钟60次请求
- 建议缓存数据5分钟

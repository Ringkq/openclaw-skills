#!/usr/bin/env python3
"""
A股打新中签率查询
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def get_ipo_win_rate(date_range=30):
    """
    获取近期新股中签率数据
    
    Args:
        date_range: 查询天数范围
    
    Returns:
        list: 中签率数据列表
    """
    
    url = "http://datacenter.eastmoney.com/api/data/v1/get"
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=date_range)
    
    params = {
        "reportName": "RPT_IPO_DETAIL",
        "columns": "ALL",
        "filter": f"(IPO_DATE>='{start_date.strftime('%Y-%m-%d')}')",
        "pageNumber": "1",
        "pageSize": "50",
        "source": "WEB"
    }
    
    data = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                data_list = result.get('data', [])
                
                win_rates = []
                for item in data_list:
                    win_rate = item.get('WINRATE', 0)
                    if win_rate is None:
                        win_rate = 0
                    
                    win_rates.append({
                        'code': item.get('STOCKCODE', ''),
                        'name': item.get('STOCKNAME', ''),
                        'win_rate': float(win_rate) * 100,  # 转换为百分比
                        'apply_num': item.get('APPLYNUM', 0),
                        'funds': item.get('FUNDS', 0),
                        'ipo_date': item.get('IPO_DATE', '')
                    })
                
                return win_rates
            else:
                return []
                
    except Exception as e:
        print(f"Error fetching win rate: {e}")
        return []

def format_win_rate(win_rates):
    """格式化中签率输出"""
    
    if not win_rates:
        return "暂无中签率数据"
    
    # 按中签率排序
    win_rates.sort(key=lambda x: x['win_rate'], reverse=True)
    
    output = ["📊 近期新股中签率\n"]
    output.append("-" * 60)
    
    for i, item in enumerate(win_rates[:10], 1):
        output.append(f"\n{i}. {item['name']} ({item['code']})")
        output.append(f"   中签率: {item['win_rate']:.3f}%")
        output.append(f"   申购人数: {item['apply_num']:,}")
        output.append(f"   冻结资金: ¥{item['funds']/100000000:.2f}亿")
        output.append(f"   申购日期: {item['ipo_date']}")
    
    output.append("\n" + "-" * 60)
    
    # 统计
    avg_rate = sum(r['win_rate'] for r in win_rates) / len(win_rates)
    output.append(f"\n平均中签率: {avg_rate:.3f}%")
    output.append(f"总新股数: {len(win_rates)}")
    
    return "\n".join(output)

def main():
    """主函数"""
    print("正在获取中签率数据...")
    
    win_rates = get_ipo_win_rate(date_range=30)
    result = format_win_rate(win_rates)
    
    print(result)
    
    return result

if __name__ == "__main__":
    main()

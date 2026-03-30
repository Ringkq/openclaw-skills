#!/usr/bin/env python3
"""
A股打新日历 - 获取近期可申购新股列表
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def get_ipo_calendar(days=7):
    """
    获取近期可申购新股列表
    
    Args:
        days: 查询天数范围
    
    Returns:
        list: 新股列表
    """
    
    # 东方财富API - 新股申购日历
    url = "http://datacenter.eastmoney.com/api/data/v1/get"
    
    params = {
        "reportName": "RPT_BONDLIST",
        "columns": "ALL",
        "pageNumber": "1",
        "pageSize": "50",
        "source": "WEB"
    }
    
    # 构建请求
    data = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                ipo_list = result.get('data', [])
                
                # 过滤近期可申购的新股
                today = datetime.now()
                upcoming = []
                
                for ipo in ipo_list:
                    sg_date_str = ipo.get('SGGZR', '')
                    if sg_date_str:
                        try:
                            sg_date = datetime.strptime(sg_date_str, '%Y-%m-%d')
                            if (sg_date - today).days <= days:
                                upcoming.append({
                                    'code': ipo.get('STOCKCODE', ''),
                                    'name': ipo.get('STOCKNAME', ''),
                                    'sg_code': ipo.get('SGCODE', ''),
                                    'price': ipo.get('ISSUEPRICE', 0),
                                    'max_subscribe': ipo.get('MAXSUBSCRIBE', 0),
                                    'sg_date': sg_date_str,
                                    'listing_date': ipo.get('LISTINGDATE', '')
                                })
                        except:
                            continue
                
                return upcoming
            else:
                return []
                
    except Exception as e:
        print(f"Error fetching IPO calendar: {e}")
        return []

def format_ipo_list(ipo_list):
    """格式化新股列表输出"""
    
    if not ipo_list:
        return "今日暂无可申购的新股"
    
    output = ["📈 近期可申购新股\n"]
    output.append("-" * 60)
    
    for i, ipo in enumerate(ipo_list, 1):
        output.append(f"\n{i}. {ipo['name']} ({ipo['code']})")
        output.append(f"   申购代码: {ipo['sg_code']}")
        output.append(f"   发行价格: ¥{ipo['price']:.2f}")
        output.append(f"   申购上限: {ipo['max_subscribe']}股")
        output.append(f"   申购日期: {ipo['sg_date']}")
        output.append(f"   上市日期: {ipo['listing_date']}")
    
    output.append("\n" + "-" * 60)
    output.append(f"\n共 {len(ipo_list)} 只新股")
    
    return "\n".join(output)

def main():
    """主函数"""
    print("正在获取新股申购日历...")
    
    ipo_list = get_ipo_calendar(days=7)
    result = format_ipo_list(ipo_list)
    
    print(result)
    
    return result

if __name__ == "__main__":
    main()

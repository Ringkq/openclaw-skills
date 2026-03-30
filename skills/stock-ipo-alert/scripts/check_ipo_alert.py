#!/usr/bin/env python3
"""
A股打新提醒检查脚本
检查是否有新股即将申购或上市，发送提醒通知
"""

import json
import urllib.request
import urllib.parse
import os
from datetime import datetime, timedelta
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / "config.json"
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "webhook_url": os.environ.get("IPO_ALERT_WEBHOOK", ""),
        "wecom_webhook": os.environ.get("WECOM_WEBHOOK", "")
    }

def get_upcoming_ipo(days=3):
    """获取即将申购的新股"""
    
    url = "http://datacenter.eastmoney.com/api/data/v1/get"
    
    params = {
        "reportName": "RPT_BONDLIST",
        "columns": "ALL",
        "pageNumber": "1",
        "pageSize": "20",
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
                
                today = datetime.now()
                upcoming = []
                
                for item in data_list:
                    sg_date_str = item.get('SGGZR', '')
                    if sg_date_str:
                        try:
                            sg_date = datetime.strptime(sg_date_str, '%Y-%m-%d')
                            days_until = (sg_date - today).days
                            
                            if 0 <= days_until <= days:
                                upcoming.append({
                                    'name': item.get('STOCKNAME', ''),
                                    'code': item.get('STOCKCODE', ''),
                                    'price': item.get('ISSUEPRICE', 0),
                                    'sg_date': sg_date_str,
                                    'days_until': days_until,
                                    'listing_date': item.get('LISTINGDATE', '')
                                })
                        except:
                            continue
                
                return upcoming
    except Exception as e:
        print(f"Error: {e}")
    
    return []

def check_ipo_alert():
    """检查打新提醒"""
    
    print(f"正在检查打新提醒... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查今日/明日可申购的新股
    upcoming = get_upcoming_ipo(days=3)
    
    if not upcoming:
        print("暂无打新提醒")
        return
    
    # 生成提醒消息
    messages = ["📢 打新提醒\n"]
    messages.append("=" * 40)
    
    for ipo in upcoming:
        days_text = "今日" if ipo['days_until'] == 0 else f"明日" if ipo['days_until'] == 1 else f"{ipo['days_until']}日后"
        
        messages.append(f"\n{ipo['name']} ({ipo['code']})")
        messages.append(f"   申购日期: {days_text} ({ipo['sg_date']})")
        messages.append(f"   发行价格: ¥{ipo['price']:.2f}")
        messages.append(f"   上市日期: {ipo['listing_date']}")
    
    messages.append("\n" + "=" * 40)
    messages.append("\n记得准备好市值哦！")
    
    alert_msg = "\n".join(messages)
    print(alert_msg)
    
    # 发送通知
    send_notification(alert_msg)

def send_notification(message):
    """发送通知"""
    
    config = load_config()
    
    # 企业微信webhook
    if config.get("wecom_webhook"):
        try:
            import requests
            requests.post(
                config["wecom_webhook"],
                json={"msgtype": "text", "text": {"content": message}},
                timeout=5
            )
            print("✅ 已发送企业微信通知")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
    
    # 通用webhook
    elif config.get("webhook_url"):
        try:
            import requests
            requests.post(
                config["webhook_url"],
                json={"text": message},
                timeout=5
            )
            print("✅ 已发送Webhook通知")
        except Exception as e:
            print(f"❌ 发送失败: {e}")
    
    else:
        print("⚠️ 未配置通知渠道")

def main():
    """主函数"""
    check_ipo_alert()

if __name__ == "__main__":
    main()

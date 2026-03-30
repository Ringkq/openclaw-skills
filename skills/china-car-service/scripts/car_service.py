#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国车主服务助手
违章查询、车险计算、年检提醒、驾照积分
"""

import json
import sys
from datetime import datetime, timedelta

# 违章扣分标准（常见）
VIOLATION_RULES = {
    "12分": [
        "饮酒后驾车（血液酒精含量80mg/100ml以上）",
        "无证驾驶",
        "伪造、变造机动车牌证",
        "高速公路逆行",
        "造成交通事故后逃逸"
    ],
    "9分": [
        "驾驶与准驾车型不符的车辆",
        "高速公路超速50%以上",
        "高速公路倒车、逆行"
    ],
    "6分": [
        "超速20%-50%",
        "闯红灯",
        "不按规定让行",
        "违法占用应急车道"
    ],
    "3分": [
        "超速10%-20%",
        "不系安全带",
        "开车接打手机",
        "不按规定使用灯光"
    ],
    "1分": [
        "违反禁令标志",
        "违反禁止标线",
        "不按规定停车"
    ]
}

# 车险费用参考
def calc_car_insurance(car_value: float, car_age: int = 1, no_claim_years: int = 0):
    """
    估算车险费用
    car_value: 新车购置价（万元）
    car_age: 车龄（年）
    no_claim_years: 连续未出险年数
    """
    # 交强险（固定）
    jiaoquan = 950  # 6座以下家用车
    
    # 商业险基准费率
    # 车损险：新车购置价 * 费率
    base_rate = 0.0085  # 基准费率0.85%
    
    # 折旧系数
    depreciation = max(0.4, 1 - car_age * 0.1)
    insured_value = car_value * depreciation
    
    # 车损险
    chesun = insured_value * 10000 * base_rate
    
    # 三者险（100万）
    sanzhе = 1800
    
    # 驾乘险
    jiacheng = 300
    
    # 不计免赔
    bujimianpei = (chesun + sanzhе) * 0.2
    
    # 无赔款优待系数
    ncd_factors = {0: 1.0, 1: 0.9, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.5}
    ncd = ncd_factors.get(min(no_claim_years, 5), 0.5)
    
    commercial = (chesun + sanzhе + jiacheng + bujimianpei) * ncd
    total = jiaoquan + commercial
    
    return {
        "车辆信息": f"购置价{car_value}万元，车龄{car_age}年",
        "连续未出险": f"{no_claim_years}年（优惠系数{ncd}）",
        "交强险": f"{jiaoquan:.0f}元",
        "商业险明细": {
            "车损险": f"{chesun:.0f}元",
            "三者险（100万）": f"{sanzhе:.0f}元",
            "驾乘险": f"{jiacheng:.0f}元",
            "不计免赔": f"{bujimianpei:.0f}元",
            "优惠后合计": f"{commercial:.0f}元"
        },
        "预估总费用": f"{total:.0f}元",
        "说明": "实际费用以保险公司报价为准，各地费率有差异"
    }

# 年检周期
def get_inspection_schedule(registration_date: str, car_type: str = "private"):
    """
    获取年检周期
    registration_date: 注册日期 YYYY-MM
    car_type: private(私家车) / commercial(营运车)
    """
    try:
        reg = datetime.strptime(registration_date, "%Y-%m")
    except:
        return {"错误": "日期格式应为 YYYY-MM，如 2020-06"}
    
    now = datetime.now()
    car_age = (now - reg).days / 365
    
    if car_type == "private":
        if car_age < 6:
            schedule = "6年内免检（每2年提交交通安全技术检验合格证明）"
            next_inspection = "6年后开始年检"
        elif car_age < 10:
            schedule = "每年检验1次"
            next_inspection = f"每年{reg.month}月前"
        else:
            schedule = "每6个月检验1次"
            next_inspection = f"每年{reg.month}月和{(reg.month+6-1)%12+1}月前"
    else:
        schedule = "营运车辆每年检验1次"
        next_inspection = f"每年{reg.month}月前"
    
    return {
        "注册日期": registration_date,
        "车龄": f"{car_age:.1f}年",
        "年检规则": schedule,
        "下次年检": next_inspection,
        "年检流程": [
            "1. 提前预约检测站",
            "2. 携带行驶证、身份证",
            "3. 确保车辆外观完好、灯光正常",
            "4. 检测合格后领取合格标志"
        ],
        "查询入口": "交管12123 APP → 车辆业务 → 检验预约"
    }

def get_violation_query_guide(city: str = "全国"):
    """获取违章查询指南"""
    return {
        "官方查询": {
            "交管12123 APP": "最权威，支持全国违章查询和处理",
            "支付宝": "城市服务 → 交通违章",
            "微信": "城市服务 → 交通违章查询"
        },
        "查询所需信息": ["车牌号", "车辆识别代码（VIN）", "发动机号"],
        "处理方式": {
            "线上缴款": "交管12123 APP直接缴纳",
            "线下处理": "携带行驶证、驾驶证到交警队"
        },
        "注意事项": [
            "违章后15天内处理可享受折扣（部分城市）",
            "超过3个月未处理可能影响年检",
            "严重违章需本人到场处理"
        ]
    }

def get_license_points_info():
    """获取驾照积分规则"""
    return {
        "积分规则": "每年12分，扣完需参加学习考试",
        "常见违章扣分": VIOLATION_RULES,
        "消分方式": {
            "自然消分": "每年1月1日重置为12分",
            "满分学习": "扣满12分需参加7天学习+考试",
            "网上学习": "部分城市支持网上学习消分（1-6分）"
        },
        "查询方式": "交管12123 APP → 驾驶证业务 → 驾驶证信息"
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python car_service.py <功能> [参数]")
        print("功能: insurance(车险), inspection(年检), violation(违章), points(积分)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "insurance":
        value = float(sys.argv[2]) if len(sys.argv) > 2 else 15
        age = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        no_claim = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        result = calc_car_insurance(value, age, no_claim)
    elif func == "inspection":
        date = sys.argv[2] if len(sys.argv) > 2 else "2020-06"
        result = get_inspection_schedule(date)
    elif func == "violation":
        city = sys.argv[2] if len(sys.argv) > 2 else "全国"
        result = get_violation_query_guide(city)
    elif func == "points":
        result = get_license_points_info()
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

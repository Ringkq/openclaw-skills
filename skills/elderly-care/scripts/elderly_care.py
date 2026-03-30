#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
养老服务助手
提供养老金估算、养老机构指南、补贴政策等
"""

import json
import sys

# 养老机构类型
CARE_HOME_TYPES = {
    "公办养老院": {
        "特点": ["价格低廉（每月1500-3000元）", "床位紧张需排队", "政府监管严格", "适合低收入老人"],
        "申请方式": "向户籍所在地民政局申请",
        "等待时间": "通常需要等待1-3年"
    },
    "公建民营养老院": {
        "特点": ["政府建设、企业运营", "价格适中（每月3000-6000元）", "服务质量较好", "床位相对充足"],
        "申请方式": "直接联系机构"
    },
    "民办养老院": {
        "特点": ["价格较高（每月4000-15000元）", "服务个性化", "环境较好", "入住灵活"],
        "注意事项": ["查看营业执照和养老机构许可证", "了解护理等级和收费标准", "实地考察环境和服务"]
    },
    "医养结合机构": {
        "特点": ["配备医疗设施", "适合失能、半失能老人", "价格较高（每月5000-20000元）"],
        "适合人群": "患有慢性病、需要长期护理的老人"
    }
}

# 居家养老服务
HOME_CARE_SERVICES = {
    "生活照料": ["助餐服务", "助浴服务", "助洁服务", "助行服务", "代购代办"],
    "医疗护理": ["上门换药", "注射服务", "康复训练", "健康监测", "慢病管理"],
    "精神慰藉": ["心理疏导", "陪伴聊天", "文化娱乐活动"],
    "紧急救援": ["一键呼叫", "GPS定位", "跌倒检测"],
    "获取方式": ["拨打12345政务热线", "联系社区居委会", "通过养老服务平台预约"]
}

# 老年人补贴政策
ELDERLY_SUBSIDIES = {
    "高龄补贴": {
        "80-89岁": "每月50-200元（各地不同）",
        "90-99岁": "每月100-500元",
        "100岁以上": "每月300-1000元",
        "申请方式": "向户籍所在地民政局申请"
    },
    "失能老人补贴": {
        "条件": "经评估为失能或半失能",
        "金额": "每月200-600元",
        "申请方式": "向社区或民政局申请评估"
    },
    "养老服务补贴": {
        "条件": "低收入、失能、高龄老人",
        "内容": "购买居家养老服务的补贴",
        "申请方式": "向社区居委会申请"
    },
    "医疗救助": {
        "内容": "低收入老人医疗费用补助",
        "申请方式": "向民政局申请"
    }
}

# 养老金计算
def calculate_pension(monthly_salary: float, years: int, retirement_age: int = 60):
    """
    估算养老金
    简化公式：基础养老金 + 个人账户养老金
    """
    # 假设社平工资（各地不同，此处用全国平均）
    social_avg = 8000  # 元/月
    
    # 缴费指数（假设为1，即按社平工资缴费）
    contribution_index = monthly_salary / social_avg
    
    # 基础养老金
    base_pension = social_avg * (1 + contribution_index) / 2 * years * 0.01
    
    # 个人账户（个人缴费8%）
    personal_account_total = monthly_salary * 0.08 * 12 * years
    
    # 计发月数（60岁退休为139个月）
    months_map = {60: 139, 55: 170, 50: 195}
    payment_months = months_map.get(retirement_age, 139)
    
    personal_pension = personal_account_total / payment_months
    
    total = base_pension + personal_pension
    
    return {
        "月工资": f"{monthly_salary:.0f}元",
        "缴费年限": f"{years}年",
        "退休年龄": f"{retirement_age}岁",
        "预估月养老金": f"{total:.0f}元",
        "基础养老金": f"{base_pension:.0f}元",
        "个人账户养老金": f"{personal_pension:.0f}元",
        "个人账户累计": f"{personal_account_total:.0f}元",
        "说明": "此为简化估算，实际金额以社保局核算为准，各地社平工资不同"
    }

def get_care_home_guide(care_type: str = None):
    """获取养老机构指南"""
    if care_type and care_type in CARE_HOME_TYPES:
        return {care_type: CARE_HOME_TYPES[care_type]}
    return {
        "养老机构类型": CARE_HOME_TYPES,
        "选择建议": [
            "根据老人健康状况选择护理等级",
            "考虑地理位置（方便家人探视）",
            "了解收费标准和服务内容",
            "实地考察环境、卫生、餐饮",
            "查看资质证书和口碑评价"
        ]
    }

def get_home_care_info():
    """获取居家养老服务信息"""
    return HOME_CARE_SERVICES

def get_subsidy_info(age: int = None):
    """获取补贴政策"""
    if age and age >= 80:
        relevant = {"高龄补贴": ELDERLY_SUBSIDIES["高龄补贴"]}
        if age >= 80:
            relevant["高龄补贴"]["您的年龄段"] = ELDERLY_SUBSIDIES["高龄补贴"].get(
                "80-89岁" if age < 90 else ("90-99岁" if age < 100 else "100岁以上")
            )
        return relevant
    return ELDERLY_SUBSIDIES

def main():
    if len(sys.argv) < 2:
        print("用法: python elderly_care.py <功能> [参数]")
        print("功能: pension(养老金), care_home(养老机构), home_care(居家养老), subsidy(补贴)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "pension":
        salary = float(sys.argv[2]) if len(sys.argv) > 2 else 8000
        years = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        age = int(sys.argv[4]) if len(sys.argv) > 4 else 60
        result = calculate_pension(salary, years, age)
    elif func == "care_home":
        care_type = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_care_home_guide(care_type)
    elif func == "home_care":
        result = get_home_care_info()
    elif func == "subsidy":
        age = int(sys.argv[2]) if len(sys.argv) > 2 else None
        result = get_subsidy_info(age)
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

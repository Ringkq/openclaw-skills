#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国房贷计算器
支持等额本息、等额本金、公积金贷款、提前还款分析
"""

import json
import sys
import math

# 2024年最新利率
RATES = {
    "LPR_5Y": 3.95,          # 5年以上LPR
    "首套商业贷款": 3.50,      # LPR - 0.45%
    "二套商业贷款": 4.05,      # LPR + 0.10%
    "公积金5年以上": 3.10,
    "公积金5年以下": 2.60,
}

def calc_equal_payment(principal: float, annual_rate: float, years: int):
    """等额本息计算"""
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / n
    else:
        monthly_payment = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    
    total_payment = monthly_payment * n
    total_interest = total_payment - principal
    
    # 前12个月明细
    schedule = []
    remaining = principal
    for i in range(1, min(13, n+1)):
        interest = remaining * monthly_rate
        principal_payment = monthly_payment - interest
        remaining -= principal_payment
        schedule.append({
            "月份": i,
            "月供": round(monthly_payment, 2),
            "还本金": round(principal_payment, 2),
            "还利息": round(interest, 2),
            "剩余本金": round(max(0, remaining), 2)
        })
    
    return {
        "还款方式": "等额本息",
        "贷款金额": f"{principal/10000:.0f}万元",
        "贷款年限": f"{years}年（{n}期）",
        "年利率": f"{annual_rate}%",
        "每月还款": f"{monthly_payment:.2f}元",
        "还款总额": f"{total_payment:.2f}元",
        "支付利息": f"{total_interest:.2f}元",
        "利息占比": f"{total_interest/principal*100:.1f}%",
        "前12个月明细": schedule
    }

def calc_decreasing_payment(principal: float, annual_rate: float, years: int):
    """等额本金计算"""
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    monthly_principal = principal / n
    
    first_payment = monthly_principal + principal * monthly_rate
    last_payment = monthly_principal + monthly_principal * monthly_rate
    
    total_interest = 0
    remaining = principal
    schedule = []
    for i in range(1, n+1):
        interest = remaining * monthly_rate
        total_interest += interest
        payment = monthly_principal + interest
        remaining -= monthly_principal
        if i <= 12:
            schedule.append({
                "月份": i,
                "月供": round(payment, 2),
                "还本金": round(monthly_principal, 2),
                "还利息": round(interest, 2),
                "剩余本金": round(max(0, remaining), 2)
            })
    
    total_payment = principal + total_interest
    
    return {
        "还款方式": "等额本金",
        "贷款金额": f"{principal/10000:.0f}万元",
        "贷款年限": f"{years}年（{n}期）",
        "年利率": f"{annual_rate}%",
        "首月还款": f"{first_payment:.2f}元",
        "末月还款": f"{last_payment:.2f}元",
        "还款总额": f"{total_payment:.2f}元",
        "支付利息": f"{total_interest:.2f}元",
        "利息占比": f"{total_interest/principal*100:.1f}%",
        "前12个月明细": schedule
    }

def compare_methods(principal: float, annual_rate: float, years: int):
    """对比两种还款方式"""
    ep = calc_equal_payment(principal, annual_rate, years)
    dp = calc_decreasing_payment(principal, annual_rate, years)
    
    ep_interest = float(ep["支付利息"].replace("元", ""))
    dp_interest = float(dp["支付利息"].replace("元", ""))
    saving = ep_interest - dp_interest
    
    return {
        "等额本息": {
            "每月还款": ep["每月还款"],
            "总利息": ep["支付利息"],
            "特点": "每月固定，便于规划"
        },
        "等额本金": {
            "首月还款": dp["首月还款"],
            "末月还款": dp["末月还款"],
            "总利息": dp["支付利息"],
            "特点": "前期压力大，总利息少"
        },
        "对比结论": f"等额本金比等额本息少付利息 {saving:.2f}元",
        "建议": "收入稳定且前期资金充裕选等额本金；收入一般选等额本息"
    }

def calc_prepayment(principal: float, annual_rate: float, years: int,
                    prepay_amount: float, prepay_month: int = 12):
    """提前还款分析"""
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    
    # 原月供
    monthly_payment = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    
    # 提前还款时的剩余本金
    remaining = principal
    for i in range(prepay_month):
        interest = remaining * monthly_rate
        remaining -= (monthly_payment - interest)
    
    remaining_after_prepay = remaining - prepay_amount
    remaining_months = n - prepay_month
    
    # 提前还款后新月供（缩短年限方式）
    new_monthly = remaining_after_prepay * monthly_rate * (1 + monthly_rate)**remaining_months / ((1 + monthly_rate)**remaining_months - 1)
    
    # 原来剩余总利息
    orig_remaining_interest = monthly_payment * remaining_months - remaining
    
    # 新的剩余总利息
    new_remaining_interest = new_monthly * remaining_months - remaining_after_prepay
    
    saved_interest = orig_remaining_interest - new_remaining_interest
    
    return {
        "贷款信息": f"{principal/10000:.0f}万元，{years}年，{annual_rate}%",
        "提前还款": f"第{prepay_month}个月还入{prepay_amount/10000:.0f}万元",
        "原月供": f"{monthly_payment:.2f}元",
        "提前还款后月供": f"{new_monthly:.2f}元",
        "节省利息": f"{saved_interest:.2f}元",
        "建议": "提前还款节省利息显著，建议优先还款"
    }

def get_current_rates():
    """获取当前利率"""
    return {
        "更新时间": "2024年",
        "利率信息": RATES,
        "说明": "实际利率以银行审批为准，各地政策可能不同",
        "公积金贷款上限": {
            "个人": "一般50-80万元（各地不同）",
            "夫妻": "一般100-160万元"
        }
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python mortgage_calc.py <功能> [参数]")
        print("功能: equal(等额本息), decreasing(等额本金), compare(对比), prepay(提前还款), rates(利率)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "equal":
        principal = float(sys.argv[2]) * 10000 if len(sys.argv) > 2 else 1000000
        rate = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        result = calc_equal_payment(principal, rate, years)
    elif func == "decreasing":
        principal = float(sys.argv[2]) * 10000 if len(sys.argv) > 2 else 1000000
        rate = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        result = calc_decreasing_payment(principal, rate, years)
    elif func == "compare":
        principal = float(sys.argv[2]) * 10000 if len(sys.argv) > 2 else 1000000
        rate = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        result = compare_methods(principal, rate, years)
    elif func == "prepay":
        principal = float(sys.argv[2]) * 10000 if len(sys.argv) > 2 else 1000000
        rate = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        prepay = float(sys.argv[5]) * 10000 if len(sys.argv) > 5 else 100000
        result = calc_prepayment(principal, rate, years, prepay)
    elif func == "rates":
        result = get_current_rates()
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

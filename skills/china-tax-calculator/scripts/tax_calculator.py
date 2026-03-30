#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国个人所得税计算器
支持月度工资、年终奖、专项附加扣除
"""

import json
import sys

# 2024年个税税率表（综合所得）
TAX_BRACKETS = [
    (36000,    0.03, 0),
    (144000,   0.10, 2520),
    (300000,   0.20, 16920),
    (420000,   0.25, 31920),
    (660000,   0.30, 52920),
    (960000,   0.35, 85920),
    (float('inf'), 0.45, 181920),
]

# 专项附加扣除标准（月）
SPECIAL_DEDUCTIONS = {
    "子女教育":    {"金额": 2000, "说明": "每个子女每月2000元"},
    "继续教育":    {"金额": 400,  "说明": "学历教育每月400元，职业资格每年3600元"},
    "住房贷款利息": {"金额": 1000, "说明": "首套住房贷款利息每月1000元"},
    "住房租金":    {"金额": 1500, "说明": "直辖市/省会城市1500元，其他城市800-1100元"},
    "赡养老人":    {"金额": 3000, "说明": "独生子女3000元，非独生子女分摊不超2000元"},
    "婴幼儿照护":  {"金额": 2000, "说明": "3岁以下婴幼儿每月2000元"},
}

def calc_tax_from_annual(annual_taxable: float) -> float:
    """根据年度应纳税所得额计算税额"""
    for limit, rate, quick_deduction in TAX_BRACKETS:
        if annual_taxable <= limit:
            return annual_taxable * rate - quick_deduction
    return 0

def calc_monthly_tax(
    gross_salary: float,
    social_insurance: float = None,
    housing_fund: float = None,
    special_deductions_monthly: float = 0,
    month: int = 1
):
    """
    计算月度工资个税（累计预扣法）
    gross_salary: 税前工资
    social_insurance: 社保个人部分（默认工资的10.5%）
    housing_fund: 公积金个人部分（默认工资的12%）
    special_deductions_monthly: 专项附加扣除月合计
    month: 当前月份（用于累计预扣）
    """
    if social_insurance is None:
        social_insurance = gross_salary * 0.105  # 养老8% + 医疗2% + 失业0.5%
    if housing_fund is None:
        housing_fund = gross_salary * 0.12

    # 月度免征额
    monthly_exemption = 5000
    
    # 月度应纳税所得额
    monthly_taxable = gross_salary - social_insurance - housing_fund - monthly_exemption - special_deductions_monthly
    monthly_taxable = max(0, monthly_taxable)
    
    # 累计应纳税所得额（简化：按月份累计）
    cumulative_taxable = monthly_taxable * month
    
    # 累计应纳税额
    cumulative_tax = calc_tax_from_annual(cumulative_taxable)
    
    # 本月预扣税额（简化：平均分摊）
    monthly_tax = cumulative_tax / month
    
    # 税后工资
    net_salary = gross_salary - social_insurance - housing_fund - monthly_tax
    
    return {
        "税前工资": f"{gross_salary:.2f}元",
        "社保个人部分": f"{social_insurance:.2f}元",
        "公积金个人部分": f"{housing_fund:.2f}元",
        "专项附加扣除": f"{special_deductions_monthly:.2f}元",
        "应纳税所得额": f"{monthly_taxable:.2f}元",
        "本月个税": f"{monthly_tax:.2f}元",
        "税后工资": f"{net_salary:.2f}元",
        "实际税率": f"{(monthly_tax/gross_salary*100):.1f}%",
        "说明": "采用累计预扣法，实际以单位代扣为准"
    }

def calc_bonus_tax(bonus: float, monthly_salary: float = 10000):
    """
    年终奖个税计算（两种方式对比）
    方式一：单独计税
    方式二：并入当月综合所得
    """
    # 方式一：单独计税
    monthly_bonus = bonus / 12
    tax1 = 0
    for limit, rate, quick_deduction in TAX_BRACKETS:
        if monthly_bonus <= limit / 12:
            tax1 = bonus * rate - quick_deduction
            break
    tax1 = max(0, tax1)
    
    # 方式二：并入当月综合所得（简化计算）
    combined_income = monthly_salary + bonus
    # 假设当月已扣除5000免征额和社保公积金
    taxable_base = max(0, monthly_salary - 5000 - monthly_salary * 0.225)
    taxable_combined = max(0, combined_income - 5000 - monthly_salary * 0.225)
    
    tax_base = calc_tax_from_annual(taxable_base * 12) / 12
    tax_combined = calc_tax_from_annual(taxable_combined * 12) / 12
    tax2 = tax_combined - tax_base
    tax2 = max(0, tax2)
    
    recommendation = "单独计税" if tax1 <= tax2 else "并入综合所得"
    saving = abs(tax2 - tax1)
    
    return {
        "年终奖金额": f"{bonus:.0f}元",
        "方式一（单独计税）": {
            "应缴个税": f"{tax1:.2f}元",
            "税后到手": f"{bonus - tax1:.2f}元"
        },
        "方式二（并入综合所得）": {
            "应缴个税": f"{tax2:.2f}元",
            "税后到手": f"{bonus - tax2:.2f}元"
        },
        "建议": f"选择【{recommendation}】，可节税约{saving:.2f}元",
        "说明": "简化计算，实际以税务局核算为准"
    }

def get_special_deductions():
    """获取专项附加扣除说明"""
    return {
        "专项附加扣除项目": SPECIAL_DEDUCTIONS,
        "申报方式": "通过个人所得税APP申报",
        "提示": "每年1月需重新确认或修改扣除信息"
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python tax_calculator.py <功能> [参数]")
        print("功能: monthly(月薪), bonus(年终奖), deductions(专项扣除)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "monthly":
        salary = float(sys.argv[2]) if len(sys.argv) > 2 else 15000
        deductions = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        result = calc_monthly_tax(salary, special_deductions_monthly=deductions)
    elif func == "bonus":
        bonus = float(sys.argv[2]) if len(sys.argv) > 2 else 50000
        salary = float(sys.argv[3]) if len(sys.argv) > 3 else 15000
        result = calc_bonus_tax(bonus, salary)
    elif func == "deductions":
        result = get_special_deductions()
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

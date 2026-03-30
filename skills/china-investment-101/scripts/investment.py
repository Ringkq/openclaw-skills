#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国投资入门助手"""
import json, sys, math

ACCOUNT_GUIDE = {
    "A股开户": {
        "流程": ["选择券商（推荐华泰/东方财富/中信）", "下载APP，身份证实名认证", "视频核验", "绑定银行卡", "开通交易权限"],
        "费用": "佣金万分之2.5起，印花税0.1%（卖出）",
        "注意": "每人只能开一个A股账户"
    },
    "基金账户": {
        "平台": ["支付宝（基金超市）", "微信理财通", "天天基金", "各大银行APP"],
        "流程": "注册→实名认证→绑卡→购买",
        "起购金额": "一般10元起"
    }
}

POPULAR_ETF = [
    {"代码": "510300", "名称": "沪深300ETF", "特点": "跟踪沪深300指数，蓝筹股代表"},
    {"代码": "510500", "名称": "中证500ETF", "特点": "跟踪中证500，中小盘代表"},
    {"代码": "159915", "名称": "创业板ETF", "特点": "跟踪创业板指，成长股代表"},
    {"代码": "513100", "名称": "纳指ETF", "特点": "跟踪纳斯达克100，科技股"},
    {"代码": "518880", "名称": "黄金ETF", "特点": "跟踪黄金价格，避险资产"},
]

ASSET_ALLOCATION = {
    "保守型（风险低）": {"股票/基金": "20%", "债券/货币基金": "60%", "存款": "20%", "适合": "退休人员、风险厌恶者"},
    "稳健型（风险中）": {"股票/基金": "40%", "债券/货币基金": "40%", "存款": "20%", "适合": "大多数普通投资者"},
    "平衡型（风险中高）": {"股票/基金": "60%", "债券/货币基金": "30%", "存款": "10%", "适合": "有一定投资经验"},
    "进取型（风险高）": {"股票/基金": "80%", "债券/货币基金": "15%", "存款": "5%", "适合": "年轻人、高风险承受者"},
}

def calc_dca(monthly: float, years: int, annual_return: float = 8.0):
    """计算定投收益"""
    monthly_return = annual_return / 100 / 12
    n = years * 12
    # 等额定投终值公式
    fv = monthly * ((1 + monthly_return)**n - 1) / monthly_return * (1 + monthly_return)
    total_invested = monthly * n
    profit = fv - total_invested
    return {
        "每月定投": f"{monthly:.0f}元",
        "定投年限": f"{years}年",
        "预期年化收益": f"{annual_return}%",
        "总投入": f"{total_invested:.0f}元",
        "预期总资产": f"{fv:.0f}元",
        "预期收益": f"{profit:.0f}元",
        "收益率": f"{profit/total_invested*100:.1f}%",
        "说明": "实际收益受市场波动影响，历史不代表未来"
    }

def get_risk_profile(age: int, income: float, savings: float, risk_tolerance: str = "medium"):
    """获取资产配置建议"""
    # 股票比例 = 100 - 年龄（经典公式）
    stock_ratio = max(20, min(80, 100 - age))
    
    if risk_tolerance == "low":
        stock_ratio = max(10, stock_ratio - 20)
        profile = "保守型"
    elif risk_tolerance == "high":
        stock_ratio = min(90, stock_ratio + 20)
        profile = "进取型"
    else:
        profile = "稳健型"
    
    bond_ratio = max(10, 80 - stock_ratio)
    cash_ratio = 100 - stock_ratio - bond_ratio
    
    return {
        "年龄": age, "风险偏好": profile,
        "建议配置": {
            "股票/基金": f"{stock_ratio}%",
            "债券/货币基金": f"{bond_ratio}%",
            "现金/存款": f"{cash_ratio}%"
        },
        "紧急备用金": f"建议保留{income*6:.0f}元（6个月收入）",
        "投资建议": ["先建立紧急备用金再投资", "分散投资，不要把鸡蛋放一个篮子", "长期持有，避免频繁交易"]
    }

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "account":
        result = ACCOUNT_GUIDE
    elif func == "dca":
        monthly = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
        years = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        ret = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0
        result = calc_dca(monthly, years, ret)
    elif func == "etf":
        result = {"热门ETF": POPULAR_ETF, "购买方式": "证券账户直接买卖，像股票一样操作"}
    elif func == "allocation":
        result = ASSET_ALLOCATION
    elif func == "profile":
        age = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        income = float(sys.argv[3]) if len(sys.argv) > 3 else 10000
        savings = float(sys.argv[4]) if len(sys.argv) > 4 else 50000
        result = get_risk_profile(age, income, savings)
    else:
        result = {"功能": ["account(开户)", "dca(定投计算)", "etf(ETF入门)", "allocation(资产配置)", "profile(风险评估)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

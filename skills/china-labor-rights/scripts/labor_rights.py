#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国劳动权益助手"""
import json, sys

def calc_overtime(daily_wage: float, overtime_hours: float, day_type: str = "weekday"):
    """计算加班费"""
    rates = {"weekday": 1.5, "weekend": 2.0, "holiday": 3.0}
    rate = rates.get(day_type, 1.5)
    hourly = daily_wage / 8
    overtime_pay = hourly * overtime_hours * rate
    return {
        "日工资": f"{daily_wage:.2f}元",
        "加班类型": {"weekday": "工作日加班", "weekend": "周末加班", "holiday": "法定节假日加班"}[day_type],
        "加班倍率": f"{rate}倍",
        "加班小时数": overtime_hours,
        "应得加班费": f"{overtime_pay:.2f}元",
        "法律依据": "《劳动法》第44条"
    }

def calc_compensation(monthly_salary: float, years: float, reason: str = "illegal"):
    """计算离职赔偿"""
    n = years  # 工作年限
    if reason == "illegal":  # 违法解除
        comp = monthly_salary * n * 2
        comp_type = "2N赔偿金（违法解除）"
    elif reason == "legal_no_fault":  # 合法解除（非过失）
        comp = monthly_salary * (n + 1)
        comp_type = "N+1经济补偿金"
    else:  # 协商解除
        comp = monthly_salary * n
        comp_type = "N经济补偿金（协商解除）"

    return {
        "月工资": f"{monthly_salary:.0f}元",
        "工作年限": f"{years}年",
        "赔偿类型": comp_type,
        "应得赔偿": f"{comp:.0f}元",
        "注意": "月工资上限为当地社平工资3倍，工作年限上限12年（经济补偿金）",
        "法律依据": "《劳动合同法》第47、87条"
    }

ARBITRATION_STEPS = [
    {"步骤": "1. 收集证据", "内容": "劳动合同、工资条、考勤记录、微信聊天记录、录音"},
    {"步骤": "2. 申请仲裁", "内容": "向用人单位所在地劳动仲裁委提交申请书"},
    {"步骤": "3. 受理审查", "内容": "仲裁委5日内决定是否受理", "时限": "5天"},
    {"步骤": "4. 开庭审理", "内容": "双方陈述、举证、质证", "时限": "受理后45天内"},
    {"步骤": "5. 裁决", "内容": "仲裁委作出裁决书", "时限": "45天（可延长15天）"},
    {"步骤": "6. 不服可起诉", "内容": "对裁决不服可在15日内向法院起诉"},
]

RIGHTS_GUIDE = {
    "工资权益": ["工资不得低于当地最低工资标准", "工资必须按时足额发放", "拖欠工资可申请劳动仲裁"],
    "社保权益": ["用人单位必须为员工缴纳五险", "不缴社保可向社保局投诉", "离职后可转移社保关系"],
    "休假权益": ["年假：工作1年以上享有5-15天带薪年假", "产假：98天（难产增加15天）", "病假：按工龄享有带薪病假"],
    "维权渠道": ["劳动仲裁委（免费）", "劳动监察大队（投诉）", "法律援助中心（免费律师）", "12333热线"],
}

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "overtime":
        wage = float(sys.argv[2]) if len(sys.argv) > 2 else 300
        hours = float(sys.argv[3]) if len(sys.argv) > 3 else 2
        day_type = sys.argv[4] if len(sys.argv) > 4 else "weekday"
        result = calc_overtime(wage, hours, day_type)
    elif func == "compensation":
        salary = float(sys.argv[2]) if len(sys.argv) > 2 else 10000
        years = float(sys.argv[3]) if len(sys.argv) > 3 else 3
        reason = sys.argv[4] if len(sys.argv) > 4 else "illegal"
        result = calc_compensation(salary, years, reason)
    elif func == "arbitration":
        result = {"劳动仲裁流程": ARBITRATION_STEPS, "申请时效": "劳动争议发生之日起1年内"}
    elif func == "rights":
        result = RIGHTS_GUIDE
    else:
        result = {"功能": ["overtime(加班费)", "compensation(赔偿金)", "arbitration(仲裁流程)", "rights(权益指南)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

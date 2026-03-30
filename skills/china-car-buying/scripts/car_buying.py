#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国购车助手"""

import json, sys

BUDGET_GUIDE = {
    "5-8万": {"推荐": ["五菱宏光MINI EV", "比亚迪海鸥", "奇瑞QQ冰淇淋"], "类型": "微型车/代步车"},
    "8-12万": {"推荐": ["比亚迪海豚", "吉利帝豪", "大众朗逸", "日产轩逸"], "类型": "紧凑型轿车"},
    "12-18万": {"推荐": ["比亚迪秦Plus", "大众速腾", "丰田卡罗拉", "本田思域"], "类型": "主流家用车"},
    "18-25万": {"推荐": ["比亚迪汉", "特斯拉Model 3", "大众帕萨特", "丰田凯美瑞"], "类型": "中级车"},
    "25-40万": {"推荐": ["特斯拉Model Y", "宝马3系", "奔驰C级", "问界M7"], "类型": "豪华/高端车"},
    "40万以上": {"推荐": ["宝马5系", "奔驰E级", "理想L9", "问界M9"], "类型": "豪华车"},
}

NEV_VS_FUEL = {
    "新能源车优势": ["使用成本低（电费约燃油1/5）", "免购置税（部分车型）", "不限行（部分城市）",
                    "加速快、驾驶体验好", "维护成本低（无机油等）"],
    "新能源车劣势": ["续航焦虑（长途不便）", "充电时间长", "二手残值低", "冬季续航打折"],
    "燃油车优势": ["加油方便快捷", "长途无焦虑", "技术成熟稳定", "二手保值率高"],
    "燃油车劣势": ["使用成本高", "限行限购城市受限", "排放政策趋严"],
    "建议": {
        "选新能源": "有固定停车位可装充电桩、日常通勤为主、城市代步",
        "选燃油车": "经常长途出行、无固定充电条件、对续航要求高"
    }
}

REGISTRATION_PROCESS = [
    {"步骤": "1. 购车发票", "内容": "从4S店获取机动车销售统一发票"},
    {"步骤": "2. 交购置税", "内容": "新能源车免税，燃油车按车价10%缴纳"},
    {"步骤": "3. 购买保险", "内容": "交强险（必须）+ 商业险（建议）"},
    {"步骤": "4. 车辆检验", "内容": "新车免检，直接上牌"},
    {"步骤": "5. 办理上牌", "内容": "携带材料到车管所，摇号/竞拍（限牌城市）"},
    {"步骤": "6. 领取号牌", "内容": "审核通过后领取车牌"},
]

USED_CAR_GUIDE = {
    "查验要点": ["查车辆历史（事故/泡水/火烧）", "验车架号和发动机号", "检查里程表是否被调",
                "试驾检查异响和操控", "查年检和保险记录"],
    "查询平台": ["车质网", "天眼查（查车辆抵押）", "交管12123（查违章）"],
    "购买渠道": {
        "二手车平台": "瓜子、优信、懂车帝（价格透明，有保障）",
        "4S店置换": "价格稍高，但质量有保障",
        "个人转让": "价格最低，风险最高，需专业验车"
    },
    "防坑提示": ["不要轻信'一口价'，多平台比价", "必须做第三方检测（200-500元）",
                "过户前查清楚是否有抵押贷款", "签合同注明车况，保留证据"]
}

def get_budget_guide(budget_wan: float):
    for range_str, info in BUDGET_GUIDE.items():
        low, high = [float(x.replace("万以上", "999").replace("万", "")) for x in range_str.split("-")]
        if low <= budget_wan <= high:
            return {"预算": f"{budget_wan}万元", "推荐车型": info["推荐"],
                    "车型定位": info["类型"], "购车建议": "建议试驾对比，关注保值率和售后服务"}
    return {"提示": "请输入5-40万的预算范围"}

def calc_car_loan(car_price: float, down_payment_ratio: float = 0.3,
                  years: int = 3, annual_rate: float = 4.5):
    loan = car_price * (1 - down_payment_ratio)
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    monthly = loan * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    total_interest = monthly * n - loan
    return {
        "车价": f"{car_price:.0f}万元",
        "首付": f"{car_price * down_payment_ratio:.1f}万元（{down_payment_ratio*100:.0f}%）",
        "贷款金额": f"{loan:.1f}万元",
        "贷款年限": f"{years}年",
        "月供": f"{monthly*10000:.0f}元",
        "总利息": f"{total_interest*10000:.0f}元",
        "还款总额": f"{(loan + total_interest)*10000:.0f}元"
    }

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "budget":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 15
        result = get_budget_guide(budget)
    elif func == "nev":
        result = NEV_VS_FUEL
    elif func == "loan":
        price = float(sys.argv[2]) if len(sys.argv) > 2 else 15
        result = calc_car_loan(price)
    elif func == "used":
        result = USED_CAR_GUIDE
    elif func == "register":
        result = {"上牌流程": REGISTRATION_PROCESS}
    else:
        result = {"功能": ["budget(预算推荐)", "nev(新能源vs燃油)", "loan(贷款计算)", "used(二手车)", "register(上牌)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

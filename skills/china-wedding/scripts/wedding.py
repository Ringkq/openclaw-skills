#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国婚礼策划助手"""
import json, sys

BUDGET_GUIDE = {
    "简约型（5-15万）": {
        "婚宴": "农家乐/小型酒店，20-30桌",
        "婚纱照": "本地摄影，5000-15000元",
        "婚庆": "基础布置，5000-10000元",
        "蜜月": "国内短途，5000-10000元"
    },
    "标准型（15-30万）": {
        "婚宴": "三星酒店，30-40桌",
        "婚纱照": "品牌影楼，15000-30000元",
        "婚庆": "专业婚庆公司，15000-30000元",
        "蜜月": "东南亚/日本，15000-30000元"
    },
    "豪华型（30-100万）": {
        "婚宴": "五星酒店，40-60桌",
        "婚纱照": "旅拍+高端影楼，30000-80000元",
        "婚庆": "高端婚庆，50000-150000元",
        "蜜月": "欧洲/马尔代夫，30000-80000元"
    }
}

REGISTRATION_STEPS = [
    {"步骤": "1. 准备材料", "内容": "双方身份证、户口本、单身证明（部分地区需要）"},
    {"步骤": "2. 前往民政局", "内容": "双方本人必须到场，不可代办"},
    {"步骤": "3. 填写申请表", "内容": "填写《结婚登记申请书》"},
    {"步骤": "4. 拍照", "内容": "在民政局拍结婚照（免费）"},
    {"步骤": "5. 领取结婚证", "内容": "当场领取，费用9元"},
    {"注意": "需在双方户籍所在地或经常居住地民政局办理"}
]

TIMELINE = {
    "婚前12个月": ["确定婚期", "预订婚宴酒店", "选择婚庆公司"],
    "婚前9个月": ["拍婚纱照", "确定婚礼主题和风格", "发送邀请函"],
    "婚前6个月": ["购买婚戒", "预订蜜月酒店机票", "试婚纱"],
    "婚前3个月": ["确定婚礼流程", "安排伴郎伴娘", "准备婚礼用品"],
    "婚前1个月": ["彩排婚礼流程", "确认所有供应商", "领证"],
    "婚前1周": ["最终确认所有细节", "准备红包零钱", "休息好"],
}

HONEYMOON_DESTINATIONS = {
    "国内": [
        {"地点": "三亚", "特点": "海滩度假，适合冬季", "费用": "5000-15000元"},
        {"地点": "丽江/大理", "特点": "文艺小清新", "费用": "5000-10000元"},
        {"地点": "西藏", "特点": "壮观风景，需提前适应高原", "费用": "8000-15000元"},
    ],
    "东南亚": [
        {"地点": "巴厘岛", "特点": "浪漫海岛，性价比高", "费用": "15000-25000元"},
        {"地点": "马尔代夫", "特点": "顶级海岛，水上屋", "费用": "30000-80000元"},
        {"地点": "泰国", "特点": "文化+海滩，多样选择", "费用": "10000-20000元"},
    ],
    "欧洲": [
        {"地点": "法国+意大利", "特点": "浪漫之都，艺术文化", "费用": "40000-80000元"},
        {"地点": "希腊圣托里尼", "特点": "蓝白小镇，地中海风情", "费用": "30000-60000元"},
    ]
}

def get_budget(level: str = None):
    if level and level in BUDGET_GUIDE:
        return {level: BUDGET_GUIDE[level]}
    return BUDGET_GUIDE

def get_registration():
    return {"领证流程": REGISTRATION_STEPS}

def get_timeline():
    return {"婚礼准备时间线": TIMELINE}

def get_honeymoon(region: str = None):
    if region and region in HONEYMOON_DESTINATIONS:
        return {region: HONEYMOON_DESTINATIONS[region]}
    return HONEYMOON_DESTINATIONS

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "budget":
        level = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_budget(level)
    elif func == "register":
        result = get_registration()
    elif func == "timeline":
        result = get_timeline()
    elif func == "honeymoon":
        region = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_honeymoon(region)
    else:
        result = {"功能": ["budget(婚礼预算)", "register(领证流程)", "timeline(准备时间线)", "honeymoon(蜜月规划)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国副业/自由职业助手"""
import json, sys

SIDE_HUSTLES = {
    "程序员": {
        "推荐副业": ["接外包项目（猪八戒/程序员客栈）", "开发独立产品/SaaS", "技术博客/教程", "开源项目接赞助"],
        "月收入潜力": "5000-50000元",
        "平台": ["程序员客栈", "猪八戒", "码市", "Upwork（国际）"]
    },
    "设计师": {
        "推荐副业": ["接UI/平面设计单", "卖设计素材", "做品牌设计", "教设计课程"],
        "月收入潜力": "3000-30000元",
        "平台": ["猪八戒", "站酷", "花瓣", "摄图网（卖素材）"]
    },
    "写作/文案": {
        "推荐副业": ["自媒体写作", "企业文案外包", "出版/投稿", "知识付费课程"],
        "月收入潜力": "2000-20000元",
        "平台": ["今日头条", "微信公众号", "知乎", "简书", "猪八戒"]
    },
    "教育/培训": {
        "推荐副业": ["在线家教", "录制课程", "知识付费专栏", "企业培训"],
        "月收入潜力": "3000-30000元",
        "平台": ["猿辅导", "作业帮", "知乎盐选", "得到", "小鹅通"]
    },
    "摄影/视频": {
        "推荐副业": ["婚庆摄影", "商业摄影", "卖图库", "短视频创作"],
        "月收入潜力": "3000-50000元",
        "平台": ["图虫", "视觉中国", "抖音", "B站"]
    },
    "通用": {
        "推荐副业": ["电商/代购", "直播带货", "外卖骑手", "滴滴司机", "问卷调查"],
        "月收入潜力": "1000-10000元",
        "平台": ["淘宝", "拼多多", "抖音小店", "美团", "滴滴"]
    }
}

PLATFORMS = {
    "综合外包": ["猪八戒（最大）", "威客网", "一品威客"],
    "技术类": ["程序员客栈", "码市", "实现网"],
    "设计类": ["站酷", "猪八戒设计", "花瓣"],
    "写作类": ["猪八戒文案", "今日头条", "百家号"],
    "教育类": ["猿辅导", "作业帮", "小鹅通（自建课程）"],
    "知识付费": ["知乎盐选", "得到", "喜马拉雅", "荔枝微课"],
    "自媒体": ["微信公众号", "抖音", "B站", "小红书", "微博"],
}

TAX_GUIDE = {
    "月收入<800元": "免税",
    "月收入800-4000元": "劳务报酬所得，扣除20%费用后按20%税率",
    "月收入>4000元": "扣除20%费用后，超额累进税率20%-40%",
    "年收入>12万": "需要自行申报个税",
    "建议": ["注册个体工商户可享受更多税收优惠", "保留收入凭证和成本发票", "通过正规平台接单，平台会代扣代缴"],
    "合规方式": ["通过平台接单（平台代扣）", "注册个体工商户开发票", "使用灵活用工平台"]
}

def get_recommendations(skill: str = None):
    if skill:
        for key in SIDE_HUSTLES:
            if key in skill or skill in key:
                return {key: SIDE_HUSTLES[key]}
    return {"所有副业推荐": SIDE_HUSTLES}

def get_platforms(category: str = None):
    if category and category in PLATFORMS:
        return {category: PLATFORMS[category]}
    return PLATFORMS

def calc_income_goal(target_monthly: float, skill: str = "通用"):
    """计算达到收入目标需要的工作量"""
    hourly_rates = {"程序员": 200, "设计师": 150, "写作/文案": 80, "教育/培训": 200, "通用": 50}
    rate = hourly_rates.get(skill, 100)
    hours_needed = target_monthly / rate
    return {
        "目标月收入": f"{target_monthly:.0f}元",
        "技能类型": skill,
        "参考时薪": f"{rate}元/小时",
        "每月需工作": f"{hours_needed:.0f}小时",
        "每天需工作": f"{hours_needed/22:.1f}小时（按22个工作日）",
        "建议": "初期先积累口碑和案例，再逐步提高报价"
    }

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "recommend":
        skill = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_recommendations(skill)
    elif func == "platforms":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_platforms(cat)
    elif func == "tax":
        result = TAX_GUIDE
    elif func == "goal":
        target = float(sys.argv[2]) if len(sys.argv) > 2 else 5000
        skill = sys.argv[3] if len(sys.argv) > 3 else "通用"
        result = calc_income_goal(target, skill)
    else:
        result = {"功能": ["recommend(副业推荐)", "platforms(接单平台)", "tax(税务指南)", "goal(收入目标)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

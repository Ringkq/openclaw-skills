#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国健康生活助手 - BMI/减肥/睡眠/心理健康"""

import json, sys, math

def calc_bmi(height_cm: float, weight_kg: float, age: int = 30, gender: str = "male"):
    bmi = weight_kg / (height_cm / 100) ** 2
    if bmi < 18.5:
        status, advice = "偏瘦", "建议增加营养摄入，适当增重"
    elif bmi < 24:
        status, advice = "正常", "保持现有生活方式，继续保持"
    elif bmi < 28:
        status, advice = "超重", "建议控制饮食，增加运动"
    else:
        status, advice = "肥胖", "建议就医，制定专业减重方案"

    ideal_weight_min = 18.5 * (height_cm / 100) ** 2
    ideal_weight_max = 24.0 * (height_cm / 100) ** 2
    diff = weight_kg - ideal_weight_max

    # 基础代谢率 BMR (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    return {
        "身高": f"{height_cm}cm", "体重": f"{weight_kg}kg",
        "BMI": round(bmi, 1), "状态": status,
        "理想体重范围": f"{ideal_weight_min:.1f}-{ideal_weight_max:.1f}kg",
        "需减重": f"{max(0, diff):.1f}kg" if diff > 0 else "无需减重",
        "基础代谢率": f"{bmr:.0f}千卡/天",
        "建议": advice
    }

def calc_weight_loss(current_kg: float, target_kg: float, height_cm: float,
                     activity: str = "moderate", weeks: int = 12):
    diff = current_kg - target_kg
    if diff <= 0:
        return {"提示": "目标体重已达到或超过当前体重"}

    # 每周减重建议0.5-1kg（健康范围）
    weekly_loss = diff / weeks
    if weekly_loss > 1:
        weeks = math.ceil(diff / 1)
        weekly_loss = diff / weeks

    # 每日热量缺口（1kg脂肪≈7700千卡）
    daily_deficit = weekly_loss * 7700 / 7

    activity_factors = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    factor = activity_factors.get(activity, 1.55)
    bmr = 10 * current_kg + 6.25 * height_cm - 5 * 30 + 5
    tdee = bmr * factor
    target_calories = tdee - daily_deficit

    return {
        "当前体重": f"{current_kg}kg", "目标体重": f"{target_kg}kg",
        "需减重": f"{diff}kg", "建议周期": f"{weeks}周",
        "每周减重": f"{weekly_loss:.2f}kg",
        "每日摄入热量": f"{target_calories:.0f}千卡",
        "每日热量缺口": f"{daily_deficit:.0f}千卡",
        "饮食建议": ["减少精制碳水（白米饭、面包）", "增加蛋白质（鸡胸肉、鱼、豆腐）",
                    "多吃蔬菜（低热量高饱腹感）", "避免含糖饮料"],
        "运动建议": ["每周3-5次有氧运动（跑步/游泳/骑车）", "每次30-60分钟",
                    "配合力量训练保持肌肉量"]
    }

def get_sleep_guide(hours: float = None, quality: str = None):
    base = {
        "成年人推荐睡眠": "7-9小时",
        "改善睡眠方法": [
            "固定作息时间，即使周末也不超过1小时偏差",
            "睡前1小时避免手机/电脑蓝光",
            "保持卧室凉爽（18-22℃）、黑暗、安静",
            "睡前避免咖啡因（下午2点后）",
            "睡前可做冥想或深呼吸放松",
            "白天适量运动，但避免睡前3小时剧烈运动"
        ],
        "助眠食物": ["温牛奶", "香蕉", "燕麦", "杏仁", "甘菊茶"],
        "就医指征": ["长期失眠超过1个月", "白天严重嗜睡影响工作", "打鼾严重（可能是睡眠呼吸暂停）"]
    }
    if hours and hours < 6:
        base["评估"] = f"您每天睡{hours}小时，低于推荐值，长期不足会影响健康"
    return base

def get_mental_health_guide(symptom: str = None):
    guides = {
        "焦虑": {
            "自测": "GAD-7量表（可在网上搜索）",
            "缓解方法": ["4-7-8呼吸法（吸气4秒，屏息7秒，呼气8秒）",
                        "正念冥想（每天10分钟）", "规律运动", "减少咖啡因"],
            "就医建议": "症状持续2周以上或影响日常生活，建议就医"
        },
        "抑郁": {
            "自测": "PHQ-9量表（可在网上搜索）",
            "缓解方法": ["保持社交联系", "规律运动（每天30分钟）",
                        "保证睡眠", "设定小目标并完成"],
            "就医建议": "有自伤想法或症状持续2周以上，请立即就医",
            "热线": "北京心理危机研究与干预中心：010-82951332"
        },
        "压力": {
            "缓解方法": ["时间管理（番茄工作法）", "运动发泄", "倾诉和社交",
                        "培养爱好", "冥想放松"],
            "建议": "适度压力是动力，长期高压需要调整"
        }
    }
    if symptom and symptom in guides:
        return guides[symptom]
    return {"心理健康指南": guides, "提示": "心理问题不是软弱，及时寻求帮助很重要"}

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "bmi":
        h = float(sys.argv[2]) if len(sys.argv) > 2 else 170
        w = float(sys.argv[3]) if len(sys.argv) > 3 else 70
        result = calc_bmi(h, w)
    elif func == "weightloss":
        cur = float(sys.argv[2]) if len(sys.argv) > 2 else 75
        tgt = float(sys.argv[3]) if len(sys.argv) > 3 else 65
        h = float(sys.argv[4]) if len(sys.argv) > 4 else 170
        result = calc_weight_loss(cur, tgt, h)
    elif func == "sleep":
        hours = float(sys.argv[2]) if len(sys.argv) > 2 else None
        result = get_sleep_guide(hours)
    elif func == "mental":
        symptom = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_mental_health_guide(symptom)
    else:
        result = {"功能": ["bmi(体重评估)", "weightloss(减肥方案)", "sleep(睡眠改善)", "mental(心理健康)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

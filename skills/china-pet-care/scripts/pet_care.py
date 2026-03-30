#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国宠物护理助手"""
import json, sys

CAT_VACCINES = [
    {"时间": "8-9周龄", "疫苗": "猫三联第1针（猫瘟+猫鼻支+猫杯状）"},
    {"时间": "12周龄", "疫苗": "猫三联第2针"},
    {"时间": "16周龄", "疫苗": "猫三联第3针 + 狂犬疫苗"},
    {"时间": "每年", "疫苗": "猫三联加强针 + 狂犬疫苗（每3年）"},
]

DOG_VACCINES = [
    {"时间": "6-8周龄", "疫苗": "犬六联第1针"},
    {"时间": "10-12周龄", "疫苗": "犬六联第2针"},
    {"时间": "14-16周龄", "疫苗": "犬六联第3针 + 狂犬疫苗"},
    {"时间": "每年", "疫苗": "犬六联加强针 + 狂犬疫苗（每年）"},
]

FORBIDDEN_FOODS = {
    "猫": ["洋葱/大蒜（溶血）", "葡萄/葡萄干（肾衰）", "巧克力（中毒）", "牛奶（乳糖不耐）",
           "生鱼（硫胺素缺乏）", "咖啡因", "木糖醇"],
    "狗": ["巧克力（中毒）", "洋葱/大蒜（溶血）", "葡萄/葡萄干（肾衰）", "木糖醇（低血糖）",
           "夏威夷果（神经毒素）", "生面团", "酒精"],
}

COMMON_SYMPTOMS = {
    "不吃东西": {"可能原因": ["换粮期不适应", "应激反应", "消化问题", "疾病"],
                "处理": "观察24小时，若超过48小时不进食或伴随其他症状立即就医"},
    "呕吐": {"可能原因": ["吃太快", "毛球（猫）", "吃了异物", "胃肠炎"],
             "处理": "偶尔呕吐正常，频繁呕吐或呕吐物含血立即就医"},
    "腹泻": {"可能原因": ["换粮", "感染", "寄生虫", "食物不耐受"],
             "处理": "补充水分，观察2天，若有血便或精神差立即就医"},
    "精神萎靡": {"可能原因": ["疾病", "疼痛", "中毒", "应激"],
                "处理": "立即就医，这是严重症状的信号"},
}

CERTIFICATE_GUIDE = {
    "宠物证（犬证）": {
        "办理地点": "当地公安局或城管部门",
        "所需材料": ["狂犬疫苗接种证明", "宠物照片", "主人身份证", "缴纳费用"],
        "注意": "部分城市强制要求，未办证可能被没收"
    },
    "出行证明": {
        "国内出行": "需要狂犬疫苗证明和健康证（宠物医院开具）",
        "跨省": "部分省份需要检疫证明",
        "乘飞机": "需提前联系航空公司，一般需要健康证和疫苗证"
    }
}

def get_vaccine_schedule(pet_type: str = "cat"):
    if pet_type in ["cat", "猫"]:
        return {"宠物类型": "猫", "疫苗计划": CAT_VACCINES, "驱虫": "每月体内外驱虫一次"}
    elif pet_type in ["dog", "狗"]:
        return {"宠物类型": "狗", "疫苗计划": DOG_VACCINES, "驱虫": "每月体内外驱虫一次"}
    return {"提示": "请指定 cat(猫) 或 dog(狗)"}

def get_forbidden_foods(pet_type: str = "cat"):
    key = "猫" if pet_type in ["cat", "猫"] else "狗"
    return {"禁忌食物": FORBIDDEN_FOODS.get(key, []), "提示": "以上食物可能危及生命，请严格避免"}

def get_symptom_guide(symptom: str = None):
    if symptom:
        for key in COMMON_SYMPTOMS:
            if key in symptom:
                return {key: COMMON_SYMPTOMS[key]}
    return COMMON_SYMPTOMS

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "vaccine":
        pet = sys.argv[2] if len(sys.argv) > 2 else "cat"
        result = get_vaccine_schedule(pet)
    elif func == "food":
        pet = sys.argv[2] if len(sys.argv) > 2 else "cat"
        result = get_forbidden_foods(pet)
    elif func == "symptom":
        symptom = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_symptom_guide(symptom)
    elif func == "certificate":
        result = CERTIFICATE_GUIDE
    else:
        result = {"功能": ["vaccine(疫苗)", "food(饮食禁忌)", "symptom(症状处理)", "certificate(证件)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

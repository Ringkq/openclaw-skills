#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国育儿助手
发育里程碑、疫苗计划、辅食指南、常见疾病处理
"""

import json
import sys

# 发育里程碑
MILESTONES = {
    "1个月": {"运动": "俯卧时能短暂抬头", "社交": "对声音有反应", "认知": "能注视人脸"},
    "3个月": {"运动": "俯卧抬头45度，手能张开", "社交": "会微笑、咿呀发声", "认知": "追视移动物体"},
    "6个月": {"运动": "能独坐片刻，翻身", "社交": "认识父母，怕生", "认知": "伸手抓物"},
    "9个月": {"运动": "能爬行，扶站", "社交": "模仿动作，挥手再见", "认知": "理解简单指令"},
    "12个月": {"运动": "扶走或独走几步", "社交": "叫爸爸妈妈", "认知": "理解约10个词"},
    "18个月": {"运动": "独立行走稳", "社交": "词汇量约20个", "认知": "能指认图片"},
    "24个月": {"运动": "跑步、上下楼梯", "社交": "说2-3个词的句子", "认知": "能做简单游戏"},
    "36个月": {"运动": "单脚站立2秒", "社交": "说完整句子", "认知": "知道自己名字和性别"},
}

# 国家免疫规划疫苗（2024年）
VACCINES = [
    {"年龄": "出生24小时内", "疫苗": "乙肝疫苗第1针、卡介苗"},
    {"年龄": "1月龄", "疫苗": "乙肝疫苗第2针"},
    {"年龄": "2月龄", "疫苗": "脊灰灭活疫苗第1针"},
    {"年龄": "3月龄", "疫苗": "脊灰灭活疫苗第2针、百白破第1针"},
    {"年龄": "4月龄", "疫苗": "脊灰减毒活疫苗第1针、百白破第2针"},
    {"年龄": "5月龄", "疫苗": "百白破第3针"},
    {"年龄": "6月龄", "疫苗": "乙肝疫苗第3针、A群流脑多糖疫苗第1针"},
    {"年龄": "8月龄", "疫苗": "麻腮风疫苗第1针、乙脑减毒活疫苗第1针"},
    {"年龄": "9月龄", "疫苗": "A群流脑多糖疫苗第2针"},
    {"年龄": "18月龄", "疫苗": "百白破第4针、麻腮风疫苗第2针、甲肝减毒活疫苗"},
    {"年龄": "2岁", "疫苗": "乙脑减毒活疫苗第2针、A+C群流脑多糖疫苗第1针"},
    {"年龄": "3岁", "疫苗": "A+C群流脑多糖疫苗第2针"},
    {"年龄": "4岁", "疫苗": "脊灰减毒活疫苗第2针"},
    {"年龄": "6岁", "疫苗": "百白破（白破）疫苗、乙脑减毒活疫苗第3针"},
]

# 辅食添加指南
COMPLEMENTARY_FOOD = {
    "开始时间": "满6个月（180天）",
    "添加原则": ["由少到多", "由稀到稠", "由细到粗", "由一种到多种"],
    "6-7个月": {
        "食物": ["米粉（铁强化）", "南瓜泥", "红薯泥", "胡萝卜泥"],
        "质地": "泥状、糊状",
        "频次": "每天1-2次"
    },
    "7-9个月": {
        "食物": ["肉泥（猪/鸡/鱼）", "蛋黄", "豆腐", "各种蔬菜泥"],
        "质地": "末状、碎状",
        "频次": "每天2-3次"
    },
    "10-12个月": {
        "食物": ["软饭", "面条", "各种蔬菜", "水果", "全蛋"],
        "质地": "软烂块状",
        "频次": "每天3次"
    },
    "注意事项": [
        "1岁前不加盐、糖、蜂蜜",
        "花生、坚果等过敏食物谨慎添加",
        "每次新食物观察3天",
        "母乳/配方奶仍是主食"
    ]
}

# 常见疾病处理
COMMON_ILLNESS = {
    "发烧": {
        "处理原则": "38.5℃以下物理降温，38.5℃以上可用退烧药",
        "物理降温": ["温水擦浴", "退热贴", "多喝水", "减少衣物"],
        "退烧药": "对乙酰氨基酚（泰诺林）或布洛芬（美林），按体重用药",
        "就医指征": ["3个月以下婴儿发烧", "高烧超过39.5℃", "发烧超过3天", "伴有皮疹、抽搐、精神差"]
    },
    "腹泻": {
        "处理原则": "预防脱水，继续喂养",
        "处理方法": ["口服补液盐（ORS）", "继续母乳喂养", "避免高糖高脂食物"],
        "就医指征": ["腹泻超过3天", "有脱水症状（眼窝凹陷、尿少）", "血便", "高烧"]
    },
    "咳嗽": {
        "处理原则": "多喝水，保持室内湿度",
        "处理方法": ["蜂蜜水（1岁以上）", "雾化吸入", "拍背排痰"],
        "就医指征": ["咳嗽超过2周", "喘息、呼吸困难", "高烧", "咳出血"]
    }
}

def get_milestone(age_months: int):
    """获取发育里程碑"""
    milestones_list = list(MILESTONES.keys())
    # 找最近的里程碑
    age_map = {"1个月": 1, "3个月": 3, "6个月": 6, "9个月": 9,
               "12个月": 12, "18个月": 18, "24个月": 24, "36个月": 36}
    
    closest = min(age_map.keys(), key=lambda k: abs(age_map[k] - age_months))
    
    return {
        "宝宝月龄": f"{age_months}个月",
        "参考里程碑": f"{closest}",
        "发育标准": MILESTONES[closest],
        "提示": "每个孩子发育有个体差异，±2个月内均属正常"
    }

def get_vaccine_schedule(age_months: int = None):
    """获取疫苗接种计划"""
    if age_months is not None:
        # 返回该月龄应接种的疫苗
        age_map = {
            0: "出生24小时内", 1: "1月龄", 2: "2月龄", 3: "3月龄",
            4: "4月龄", 5: "5月龄", 6: "6月龄", 8: "8月龄",
            9: "9月龄", 18: "18月龄", 24: "2岁", 36: "3岁", 48: "4岁", 72: "6岁"
        }
        closest_age = min(age_map.keys(), key=lambda k: abs(k - age_months))
        age_label = age_map[closest_age]
        vaccines = [v for v in VACCINES if v["年龄"] == age_label]
        return {
            "月龄": f"{age_months}个月",
            "本阶段疫苗": vaccines if vaccines else [{"提示": "该月龄无固定接种计划"}],
            "完整计划": VACCINES
        }
    return {"完整疫苗计划": VACCINES}

def get_food_guide(age_months: int = 6):
    """获取辅食指南"""
    if age_months < 6:
        return {"提示": "6个月前不建议添加辅食，纯母乳或配方奶喂养"}
    elif age_months <= 7:
        stage = "6-7个月"
    elif age_months <= 9:
        stage = "7-9个月"
    else:
        stage = "10-12个月"
    
    return {
        "月龄": f"{age_months}个月",
        "辅食阶段": stage,
        "本阶段指南": COMPLEMENTARY_FOOD.get(stage, {}),
        "添加原则": COMPLEMENTARY_FOOD["添加原则"],
        "注意事项": COMPLEMENTARY_FOOD["注意事项"]
    }

def get_illness_guide(illness: str):
    """获取疾病处理指南"""
    illness_map = {"发烧": "发烧", "fever": "发烧", "腹泻": "腹泻", "diarrhea": "腹泻",
                   "咳嗽": "咳嗽", "cough": "咳嗽"}
    key = illness_map.get(illness, illness)
    if key in COMMON_ILLNESS:
        return COMMON_ILLNESS[key]
    return {"提示": f"暂无{illness}的处理指南，请咨询医生"}

def main():
    if len(sys.argv) < 2:
        print("用法: python parenting.py <功能> [参数]")
        print("功能: milestone(发育), vaccine(疫苗), food(辅食), illness(疾病)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "milestone":
        age = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        result = get_milestone(age)
    elif func == "vaccine":
        age = int(sys.argv[2]) if len(sys.argv) > 2 else None
        result = get_vaccine_schedule(age)
    elif func == "food":
        age = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        result = get_food_guide(age)
    elif func == "illness":
        illness = sys.argv[2] if len(sys.argv) > 2 else "发烧"
        result = get_illness_guide(illness)
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

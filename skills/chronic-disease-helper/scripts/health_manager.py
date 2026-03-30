#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
慢性病管理脚本
提供血糖、血压等指标记录和分析
"""

import json
import sys
from datetime import datetime

# 正常值参考范围
NORMAL_RANGES = {
    "血糖": {
        "空腹血糖": {"正常": "3.9-6.1", "偏高": "6.1-7.0", "糖尿病": ">7.0"},
        "餐后2小时血糖": {"正常": "<7.8", "偏高": "7.8-11.1", "糖尿病": ">11.1"},
        "糖化血红蛋白": {"正常": "<6.0%", "偏高": "6.0-6.5%", "糖尿病": ">6.5%"}
    },
    "血压": {
        "收缩压": {"正常": "90-120", "正常高值": "120-139", "高血压": ">=140"},
        "舒张压": {"正常": "60-80", "正常高值": "80-89", "高血压": ">=90"}
    },
    "心率": {
        "静息心率": {"正常": "60-100", "偏低": "<60", "偏高": ">100"}
    }
}

# 糖尿病饮食建议
DIABETES_DIET = {
    "推荐食物": [
        "绿叶蔬菜（菠菜、芹菜、西兰花）",
        "粗粮（燕麦、糙米、全麦面包）",
        "优质蛋白（鱼肉、鸡胸肉、豆腐）",
        "低糖水果（柚子、草莓、樱桃）"
    ],
    "限制食物": [
        "精制糖（糖果、蛋糕、含糖饮料）",
        "高淀粉（白米饭、白面条、土豆）",
        "高脂肪（肥肉、油炸食品）",
        "高糖水果（葡萄、香蕉、荔枝）"
    ],
    "饮食原则": [
        "少食多餐，每日3主餐+2加餐",
        "每餐主食不超过1两（生重）",
        "先吃蔬菜，再吃蛋白，最后吃主食",
        "细嚼慢咽，控制进食速度"
    ]
}

# 高血压生活方式建议
HYPERTENSION_LIFESTYLE = {
    "饮食": [
        "低盐饮食（每日盐摄入<5克）",
        "增加钾摄入（香蕉、橙子、土豆）",
        "多吃蔬菜水果",
        "限制饮酒"
    ],
    "运动": [
        "每周至少150分钟中等强度有氧运动",
        "推荐快走、游泳、骑自行车",
        "避免剧烈运动和憋气动作",
        "运动前后监测血压"
    ],
    "生活习惯": [
        "戒烟限酒",
        "保持理想体重",
        "减少精神压力",
        "保证充足睡眠"
    ]
}

def analyze_blood_sugar(fasting: float = None, post_meal: float = None):
    """分析血糖水平"""
    result = {
        "记录时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "血糖数值": {},
        "评估结果": {},
        "建议": []
    }
    
    if fasting is not None:
        result["血糖数值"]["空腹血糖"] = f"{fasting} mmol/L"
        if fasting <= 6.1:
            result["评估结果"]["空腹血糖"] = "正常"
        elif fasting <= 7.0:
            result["评估结果"]["空腹血糖"] = "偏高（空腹血糖受损）"
            result["建议"].append("建议控制饮食，增加运动")
        else:
            result["评估结果"]["空腹血糖"] = "糖尿病水平，请及时就医"
            result["建议"].append("请尽快就医，遵医嘱用药")
    
    if post_meal is not None:
        result["血糖数值"]["餐后2小时血糖"] = f"{post_meal} mmol/L"
        if post_meal < 7.8:
            result["评估结果"]["餐后血糖"] = "正常"
        elif post_meal <= 11.1:
            result["评估结果"]["餐后血糖"] = "偏高（糖耐量受损）"
            result["建议"].append("餐后适当运动，控制碳水摄入")
        else:
            result["评估结果"]["餐后血糖"] = "糖尿病水平，请及时就医"
    
    return result

def analyze_blood_pressure(systolic: int, diastolic: int):
    """分析血压水平"""
    result = {
        "记录时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "血压数值": f"{systolic}/{diastolic} mmHg",
        "评估结果": {},
        "建议": []
    }
    
    # 收缩压评估
    if systolic < 90:
        result["评估结果"]["收缩压"] = "偏低"
        result["建议"].append("血压偏低，注意补充水分和营养")
    elif systolic <= 120:
        result["评估结果"]["收缩压"] = "正常"
    elif systolic <= 139:
        result["评估结果"]["收缩压"] = "正常高值"
        result["建议"].append("建议改善生活方式，定期监测")
    else:
        result["评估结果"]["收缩压"] = "高血压"
        result["建议"].append("请就医，遵医嘱用药")
    
    # 舒张压评估
    if diastolic < 60:
        result["评估结果"]["舒张压"] = "偏低"
    elif diastolic <= 80:
        result["评估结果"]["舒张压"] = "正常"
    elif diastolic <= 89:
        result["评估结果"]["舒张压"] = "正常高值"
    else:
        result["评估结果"]["舒张压"] = "高血压"
    
    # 综合建议
    if systolic >= 140 or diastolic >= 90:
        result["建议"].extend(HYPERTENSION_LIFESTYLE["饮食"][:3])
    
    return result

def get_diet_advice(disease_type: str = "diabetes"):
    """获取饮食建议"""
    if disease_type == "diabetes":
        return DIABETES_DIET
    elif disease_type == "hypertension":
        return {"饮食建议": HYPERTENSION_LIFESTYLE["饮食"]}
    return {"提示": "暂无该疾病的饮食建议"}

def main():
    if len(sys.argv) < 2:
        print("用法: python chronic_disease.py <功能> [参数]")
        print("功能: blood_sugar(血糖), blood_pressure(血压), diet(饮食)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "blood_sugar":
        fasting = float(sys.argv[2]) if len(sys.argv) > 2 else None
        post_meal = float(sys.argv[3]) if len(sys.argv) > 3 else None
        result = analyze_blood_sugar(fasting, post_meal)
    elif func == "blood_pressure":
        systolic = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        diastolic = int(sys.argv[3]) if len(sys.argv) > 3 else 80
        result = analyze_blood_pressure(systolic, diastolic)
    elif func == "diet":
        disease = sys.argv[2] if len(sys.argv) > 2 else "diabetes"
        result = get_diet_advice(disease)
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

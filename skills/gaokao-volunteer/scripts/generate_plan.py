#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
志愿方案生成脚本
根据考生信息生成完整的冲稳保志愿方案
"""

import json
import sys

def generate_volunteer_plan(score: int, province: str, subject_type: str,
                             preferred_cities: list = None, 
                             preferred_majors: list = None,
                             avoid_majors: list = None):
    """
    生成完整志愿填报方案
    
    Args:
        score: 高考分数
        province: 省份
        subject_type: 科目类型
        preferred_cities: 意向城市列表
        preferred_majors: 意向专业列表
        avoid_majors: 不想报的专业
    
    Returns:
        dict: 完整志愿方案
    """
    
    plan = {
        "考生信息": {
            "分数": score,
            "省份": province,
            "科目": subject_type,
            "意向城市": preferred_cities or ["不限"],
            "意向专业": preferred_majors or ["不限"],
            "排除专业": avoid_majors or []
        },
        "志愿方案": {
            "冲（2-3个）": {
                "策略": "选择录取分数线比您高10-20分的院校，有一定风险",
                "建议数量": "2-3个",
                "院校示例": []
            },
            "稳（3-4个）": {
                "策略": "选择录取分数线与您相近（±10分）的院校，录取概率较高",
                "建议数量": "3-4个",
                "院校示例": []
            },
            "保（2-3个）": {
                "策略": "选择录取分数线比您低20-30分的院校，确保有学可上",
                "建议数量": "2-3个",
                "院校示例": []
            }
        },
        "填报注意事项": [],
        "时间节点": {}
    }
    
    # 根据分数段填充院校建议
    if score >= 680:
        plan["志愿方案"]["冲（2-3个）"]["院校示例"] = ["清华大学", "北京大学"]
        plan["志愿方案"]["稳（3-4个）"]["院校示例"] = ["复旦大学", "上海交通大学", "浙江大学", "中国科学技术大学"]
        plan["志愿方案"]["保（2-3个）"]["院校示例"] = ["南京大学", "武汉大学", "中山大学"]
    elif score >= 640:
        plan["志愿方案"]["冲（2-3个）"]["院校示例"] = ["复旦大学", "上海交通大学"]
        plan["志愿方案"]["稳（3-4个）"]["院校示例"] = ["浙江大学", "南京大学", "武汉大学", "中山大学"]
        plan["志愿方案"]["保（2-3个）"]["院校示例"] = ["华中科技大学", "四川大学", "西安交通大学"]
    elif score >= 600:
        plan["志愿方案"]["冲（2-3个）"]["院校示例"] = ["华中科技大学", "四川大学"]
        plan["志愿方案"]["稳（3-4个）"]["院校示例"] = ["北京航空航天大学", "北京理工大学", "东南大学"]
        plan["志愿方案"]["保（2-3个）"]["院校示例"] = ["省内重点211院校"]
    elif score >= 550:
        plan["志愿方案"]["冲（2-3个）"]["院校示例"] = ["省内重点211院校"]
        plan["志愿方案"]["稳（3-4个）"]["院校示例"] = ["省内一本重点院校"]
        plan["志愿方案"]["保（2-3个）"]["院校示例"] = ["省内一本普通院校"]
    else:
        plan["志愿方案"]["冲（2-3个）"]["院校示例"] = ["省内一本院校（部分专业）"]
        plan["志愿方案"]["稳（3-4个）"]["院校示例"] = ["省内二本重点院校"]
        plan["志愿方案"]["保（2-3个）"]["院校示例"] = ["省内二本普通院校"]
    
    # 填报注意事项
    plan["填报注意事项"] = [
        "1. 参考近3年录取数据，不要只看最低分，要看平均分和位次",
        "2. 关注专业录取分数，热门专业可能比院校平均分高很多",
        "3. 了解各省平行志愿规则，合理排序（分数高的院校排前面）",
        "4. 提前了解目标院校的招生计划数量，计划少的专业风险更高",
        "5. 注意院校的专业调剂政策，是否服从调剂",
        "6. 关注院校所在城市，城市发展影响就业机会",
        "7. 了解院校的转专业政策，给自己留退路",
        "8. 查看院校官网最新招生简章，以官方信息为准"
    ]
    
    # 时间节点（以2025年为例）
    plan["时间节点"] = {
        "高考": "6月7-8日",
        "成绩公布": "6月下旬",
        "本科志愿填报": "6月下旬至7月初",
        "本科录取结果": "7月中下旬",
        "专科志愿填报": "8月上旬",
        "提示": "具体时间以各省招生办公室公告为准"
    }
    
    return plan


def main():
    if len(sys.argv) < 3:
        print("用法: python generate_plan.py <分数> <省份> [科目] [意向城市1,城市2] [意向专业1,专业2]")
        print("示例: python generate_plan.py 580 湖南 理科 北京,上海 计算机,金融")
        sys.exit(1)
    
    score = int(sys.argv[1])
    province = sys.argv[2]
    subject_type = sys.argv[3] if len(sys.argv) > 3 else "理科"
    preferred_cities = sys.argv[4].split(',') if len(sys.argv) > 4 else None
    preferred_majors = sys.argv[5].split(',') if len(sys.argv) > 5 else None
    
    result = generate_volunteer_plan(score, province, subject_type, preferred_cities, preferred_majors)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

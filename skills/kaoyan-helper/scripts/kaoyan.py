#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""考研备考助手"""

import json, sys

SCHEDULE = {
    "3月-6月": {"任务": "打基础", "英语": "单词+长难句", "数学": "高数基础", "政治": "暂不开始", "专业课": "教材精读"},
    "7月-8月": {"任务": "强化提升", "英语": "阅读理解专项", "数学": "强化班+刷题", "政治": "马原+史纲", "专业课": "笔记整理"},
    "9月-10月": {"任务": "全面冲刺", "英语": "真题精练", "数学": "真题+模拟", "政治": "全科+时政", "专业课": "真题+背诵"},
    "11月-12月": {"任务": "查漏补缺", "英语": "作文模板+押题", "数学": "错题回顾", "政治": "肖四肖八", "专业课": "重点背诵"},
}

SUBJECT_TIPS = {
    "英语": {
        "核心": "阅读理解是关键（占60分）",
        "单词": "每天100个，坚持到考前",
        "阅读": "真题精读，分析出题逻辑",
        "作文": "10月开始，背模板+仿写",
        "推荐资料": "朱伟恋词、唐迟阅读、王江涛作文"
    },
    "数学": {
        "核心": "基础题必须全对，难题争取",
        "高数": "张宇/汤家凤基础班",
        "线代": "李永乐线代",
        "概率": "余炳森概率",
        "推荐资料": "660题、880题、历年真题"
    },
    "政治": {
        "核心": "9月后开始，效率高",
        "方法": "肖秀荣1000题刷3遍",
        "重点": "马原理解+史纲记忆",
        "冲刺": "肖四肖八必背",
        "推荐资料": "肖秀荣精讲精练、腿姐技巧班"
    },
}

REGISTRATION_PROCESS = [
    {"步骤": "1. 网上报名", "时间": "10月上旬", "内容": "中国研究生招生信息网填报志愿"},
    {"步骤": "2. 网上确认", "时间": "11月上旬", "内容": "上传照片、确认信息、缴费"},
    {"步骤": "3. 打印准考证", "时间": "12月中旬", "内容": "研招网下载打印"},
    {"步骤": "4. 初试", "时间": "12月下旬", "内容": "笔试，一般持续2天"},
    {"步骤": "5. 查成绩", "时间": "次年2月", "内容": "研招网查询"},
    {"步骤": "6. 复试/调剂", "时间": "次年3-4月", "内容": "过线参加复试，未过线申请调剂"},
]

def get_schedule(month: int = None):
    if month:
        for period, info in SCHEDULE.items():
            start, end = [int(x.replace("月", "")) for x in period.split("-")]
            if start <= month <= end:
                return {"当前阶段": period, "备考建议": info}
    return {"全年规划": SCHEDULE}

def get_subject_tips(subject: str = None):
    if subject and subject in SUBJECT_TIPS:
        return SUBJECT_TIPS[subject]
    return SUBJECT_TIPS

def get_registration():
    return {"报名流程": REGISTRATION_PROCESS, "官网": "https://yz.chsi.com.cn/"}

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "schedule":
        month = int(sys.argv[2]) if len(sys.argv) > 2 else None
        result = get_schedule(month)
    elif func == "subject":
        subject = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_subject_tips(subject)
    elif func == "register":
        result = get_registration()
    else:
        result = {"功能": ["schedule(备考规划)", "subject(科目策略)", "register(报名流程)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

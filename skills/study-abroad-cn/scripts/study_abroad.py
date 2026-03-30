#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国留学申请助手"""
import json, sys

DESTINATIONS = {
    "美国": {"优势": "顶尖大学多，科研强，就业机会好", "劣势": "签证难，费用高，政治风险",
             "费用": "本科$30-60k/年，研究生$25-55k/年", "语言": "托福100+/雅思7.0+",
             "热门专业": ["CS", "金融", "MBA", "工程"], "申请季": "9月-次年1月"},
    "英国": {"优势": "学制短（1年硕士），名校多，欧洲中心", "劣势": "费用高，天气差",
             "费用": "£15-35k/年", "语言": "雅思6.5-7.5",
             "热门专业": ["金融", "法律", "传媒", "管理"], "申请季": "10月-次年3月"},
    "澳大利亚": {"优势": "移民友好，环境好，华人多", "劣势": "就业机会相对少",
                "费用": "AUD$25-45k/年", "语言": "雅思6.5+",
                "热门专业": ["会计", "IT", "工程", "教育"], "申请季": "全年滚动"},
    "加拿大": {"优势": "移民政策好，双语环境，安全", "劣势": "冬天冷，部分城市就业有限",
              "费用": "CAD$20-40k/年", "语言": "雅思6.5+/托福88+",
              "热门专业": ["CS", "商科", "工程", "医疗"], "申请季": "9月-次年2月"},
    "新加坡": {"优势": "亚洲金融中心，华语环境，费用相对低", "劣势": "竞争激烈，名额少",
              "费用": "SGD$20-35k/年", "语言": "托福90+/雅思6.5+",
              "热门专业": ["金融", "CS", "工程"], "申请季": "10月-次年3月"},
}

EXAM_GUIDE = {
    "雅思": {"满分": 9.0, "一般要求": "6.5-7.5", "备考时间": "3-6个月",
             "策略": ["听力：精听BBC/CNN", "阅读：限时练习", "写作：背模板+练习", "口语：找外教练习"]},
    "托福": {"满分": 120, "一般要求": "90-110", "备考时间": "3-6个月",
             "策略": ["刷TPO真题", "口语用模板", "写作练独立+综合", "听力多听学术材料"]},
    "GRE": {"满分": "340+3.5", "一般要求": "320+4.0", "备考时间": "3-6个月",
            "策略": ["单词是核心（红宝书/再要你命3000）", "数学相对简单", "写作练模板"]},
    "GMAT": {"满分": 800, "一般要求": "680-720+", "备考时间": "3-6个月",
             "策略": ["逻辑推理是重点", "数学需要练习", "语文靠语感积累"]},
}

TIMELINE = {
    "大三上（9-12月）": ["确定留学意向和目标国家", "开始语言考试备考", "了解目标学校要求"],
    "大三下（1-6月）": ["参加语言考试", "准备实习/科研经历", "联系推荐人"],
    "大四上（7-12月）": ["完成语言考试", "撰写文书（PS/SOP）", "提交申请（美国12月前）"],
    "大四下（1-6月）": ["等待录取通知", "申请签证", "办理入学手续"],
}

def get_destination(country: str = None):
    if country and country in DESTINATIONS:
        return DESTINATIONS[country]
    return {"热门留学目的地": DESTINATIONS}

def get_exam_guide(exam: str = None):
    if exam and exam in EXAM_GUIDE:
        return EXAM_GUIDE[exam]
    return EXAM_GUIDE

def get_timeline():
    return {"申请时间线（本科生）": TIMELINE, "提示": "研究生申请时间线类似，提前1-1.5年开始准备"}

def main():
    func = sys.argv[1] if len(sys.argv) > 1 else "help"
    if func == "destination":
        country = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_destination(country)
    elif func == "exam":
        exam = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_exam_guide(exam)
    elif func == "timeline":
        result = get_timeline()
    else:
        result = {"功能": ["destination(目的地)", "exam(语言考试)", "timeline(申请时间线)"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

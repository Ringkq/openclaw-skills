#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驾考题库练习脚本
提供科目一/科目四题目练习
"""

import json
import random
import sys

# 科目一题库（精选高频题）
SUBJECT_1_QUESTIONS = [
    {
        "id": 1,
        "question": "驾驶机动车在道路上行驶时，下列哪种行为是正确的？",
        "options": {
            "A": "超车时可以不开转向灯",
            "B": "行驶中可以拨打手持电话",
            "C": "通过路口时减速慢行",
            "D": "在高速公路上可以倒车"
        },
        "answer": "C",
        "explanation": "通过路口时应减速慢行，注意观察左右来车。超车必须开转向灯，行驶中不得拨打手持电话，高速公路严禁倒车。"
    },
    {
        "id": 2,
        "question": "这个标志是什么意思？（圆形，红色边框，中间有向左的箭头）",
        "options": {
            "A": "禁止向左转弯",
            "B": "允许向左转弯",
            "C": "向左单行道",
            "D": "前方向左弯道"
        },
        "answer": "A",
        "explanation": "圆形红色边框的标志是禁令标志，中间向左箭头表示禁止向左转弯。"
    },
    {
        "id": 3,
        "question": "在没有中心线的道路上，夜间会车时，距对方来车多少米以外改用近光灯？",
        "options": {
            "A": "50米",
            "B": "100米",
            "C": "150米",
            "D": "200米"
        },
        "answer": "C",
        "explanation": "在没有中心线的道路上，夜间会车时，应在距对方来车150米以外改用近光灯。"
    },
    {
        "id": 4,
        "question": "饮酒后驾车，血液中酒精含量的标准是多少？",
        "options": {
            "A": "20mg/100ml以上，不足80mg/100ml",
            "B": "30mg/100ml以上，不足80mg/100ml",
            "C": "50mg/100ml以上，不足80mg/100ml",
            "D": "60mg/100ml以上，不足80mg/100ml"
        },
        "answer": "A",
        "explanation": "饮酒驾车：血液中酒精含量≥20mg/100ml且<80mg/100ml。醉酒驾车：血液中酒精含量≥80mg/100ml。"
    },
    {
        "id": 5,
        "question": "机动车在高速公路上行驶，车速超过100km/h时，应与同车道前车保持多少米以上的距离？",
        "options": {
            "A": "50米",
            "B": "80米",
            "C": "100米",
            "D": "120米"
        },
        "answer": "C",
        "explanation": "在高速公路上，车速超过100km/h时，应与同车道前车保持100米以上的行车间距。"
    },
    {
        "id": 6,
        "question": "驾驶机动车遇到前方路口交通阻塞时，应怎样做？",
        "options": {
            "A": "跟随前车进入路口",
            "B": "依次停在路口外等候",
            "C": "借对向车道通过路口",
            "D": "从路口右侧绕行"
        },
        "answer": "B",
        "explanation": "遇前方路口交通阻塞时，应依次停在路口外等候，不得进入路口，以免造成更严重的堵塞。"
    },
    {
        "id": 7,
        "question": "这个标志是什么意思？（蓝色矩形，白色P字）",
        "options": {
            "A": "禁止停车",
            "B": "允许临时停车",
            "C": "停车场",
            "D": "收费停车场"
        },
        "answer": "C",
        "explanation": "蓝色矩形白色P字是指示标志，表示停车场，指示驾驶人可以在此停车。"
    },
    {
        "id": 8,
        "question": "驾驶机动车在雨天行车时，下列做法正确的是？",
        "options": {
            "A": "适当提高车速，尽快通过",
            "B": "减速慢行，保持安全距离",
            "C": "紧跟前车，防止走错路",
            "D": "开启危险报警闪光灯行驶"
        },
        "answer": "B",
        "explanation": "雨天路面湿滑，制动距离增大，应减速慢行，保持比晴天更大的安全距离。"
    },
    {
        "id": 9,
        "question": "机动车驾驶人在实习期内驾车上高速公路，应当怎样做？",
        "options": {
            "A": "不得驾车上高速公路",
            "B": "由持相应或更高驾照3年以上的驾驶人陪同",
            "C": "由持相应或更高驾照1年以上的驾驶人陪同",
            "D": "可以独自驾车上高速公路"
        },
        "answer": "B",
        "explanation": "实习期内驾驶人不得独自驾车上高速公路，须由持相应或更高驾照3年以上的驾驶人陪同。"
    },
    {
        "id": 10,
        "question": "行车中发现前方道路塌陷，应怎样做？",
        "options": {
            "A": "加速通过",
            "B": "减速通过",
            "C": "立即停车，查明情况",
            "D": "鸣喇叭通过"
        },
        "answer": "C",
        "explanation": "发现前方道路塌陷，应立即停车，查明情况，不得冒险通过，必要时设置警示标志并报警。"
    }
]

# 科目四题库（精选）
SUBJECT_4_QUESTIONS = [
    {
        "id": 101,
        "question": "驾驶机动车遇到老年人过马路时，应怎样做？",
        "options": {
            "A": "鸣喇叭催促",
            "B": "减速慢行，必要时停车让行",
            "C": "绕行通过",
            "D": "加速通过"
        },
        "answer": "B",
        "explanation": "文明驾驶要求礼让行人，遇老年人、儿童、残疾人等过马路时，应减速慢行，必要时停车让行。"
    },
    {
        "id": 102,
        "question": "驾驶机动车发生交通事故后，当事人应怎样做？",
        "options": {
            "A": "立即离开现场",
            "B": "立即停车，保护现场，报警",
            "C": "先离开，事后再报警",
            "D": "与对方私下协商解决"
        },
        "answer": "B",
        "explanation": "发生交通事故后，当事人应立即停车，保护现场，抢救伤员，并立即报警。逃逸将承担更重的法律责任。"
    }
]

def get_quiz(subject: int = 1, count: int = 5):
    """获取练习题目"""
    if subject == 1:
        questions = SUBJECT_1_QUESTIONS
    elif subject == 4:
        questions = SUBJECT_4_QUESTIONS
    else:
        questions = SUBJECT_1_QUESTIONS + SUBJECT_4_QUESTIONS
    
    selected = random.sample(questions, min(count, len(questions)))
    
    result = {
        "科目": f"科目{'一' if subject == 1 else '四' if subject == 4 else '一+四'}",
        "题目数量": len(selected),
        "题目": []
    }
    
    for q in selected:
        result["题目"].append({
            "题号": q["id"],
            "题目": q["question"],
            "选项": q["options"],
            "答案": q["answer"],
            "解析": q["explanation"]
        })
    
    return result

def main():
    subject = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    result = get_quiz(subject, count)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

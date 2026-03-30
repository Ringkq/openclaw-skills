#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国家装助手
装修预算、施工流程、材料选购、防坑指南
"""

import json
import sys

# 装修档次费用参考（元/平米）
DECORATION_COST = {
    "经济型": {"范围": "600-1000", "特点": "基础装修，实用为主，主材自购"},
    "中档": {"范围": "1000-2000", "特点": "品质装修，部分品牌主材，半包或全包"},
    "高档": {"范围": "2000-4000", "特点": "精装修，知名品牌主材，全包"},
    "豪华": {"范围": "4000以上", "特点": "定制装修，顶级品牌，设计师全程跟进"},
}

# 装修风格
STYLES = {
    "现代简约": {
        "特点": "线条简洁，色彩素雅，功能实用",
        "主色调": "白色、灰色、米色",
        "适合人群": "年轻人、追求简洁生活",
        "预算系数": 1.0
    },
    "北欧风": {
        "特点": "自然材质，原木色，清新明亮",
        "主色调": "白色、原木色、浅灰",
        "适合人群": "文艺青年、喜欢自然风",
        "预算系数": 1.1
    },
    "新中式": {
        "特点": "传统元素现代化，典雅大气",
        "主色调": "深木色、米白、墨绿",
        "适合人群": "中年人、喜欢传统文化",
        "预算系数": 1.3
    },
    "轻奢风": {
        "特点": "金属元素，大理石纹，精致优雅",
        "主色调": "金色、黑白、大理石纹",
        "适合人群": "追求品质生活",
        "预算系数": 1.5
    },
    "工业风": {
        "特点": "裸露管道，金属质感，粗犷个性",
        "主色调": "灰色、黑色、铁锈红",
        "适合人群": "个性男性、loft户型",
        "预算系数": 1.0
    },
}

# 施工流程
CONSTRUCTION_PROCESS = [
    {"阶段": "1. 拆改阶段", "内容": "拆除旧墙、门窗，改水电管线", "周期": "3-7天"},
    {"阶段": "2. 水电阶段", "内容": "水管铺设、电线布线、开关插座定位", "周期": "5-10天"},
    {"阶段": "3. 泥瓦阶段", "内容": "墙面防水、贴瓷砖、地面找平", "周期": "10-20天"},
    {"阶段": "4. 木工阶段", "内容": "吊顶、门套、柜体制作", "周期": "10-15天"},
    {"阶段": "5. 油漆阶段", "内容": "墙面刮腻子、刷乳胶漆", "周期": "7-10天"},
    {"阶段": "6. 安装阶段", "内容": "安装门窗、橱柜、洁具、灯具", "周期": "3-5天"},
    {"阶段": "7. 软装阶段", "内容": "家具、窗帘、装饰品布置", "周期": "1-3天"},
    {"阶段": "8. 保洁验收", "内容": "开荒保洁、竣工验收", "周期": "1-2天"},
]

# 防坑指南
PITFALL_GUIDE = {
    "合同陷阱": [
        "签合同前仔细核对材料品牌型号",
        "注意增项条款，避免无限增项",
        "明确付款节点，不要一次性付清",
        "保留10%质保金"
    ],
    "施工陷阱": [
        "水电改造按实际用量计费，提前确认单价",
        "防水工程不能省，卫生间做闭水试验",
        "瓷砖铺贴前确认损耗率（一般5-10%）",
        "木工板材要查看环保等级"
    ],
    "材料陷阱": [
        "主材自购要核对型号，防止以次充好",
        "进口材料要查验原产地证明",
        "橱柜要确认板材品牌和五金品牌",
        "地板要确认是否含安装费"
    ],
    "验收要点": [
        "水电验收：通水通电，无漏水漏电",
        "瓷砖验收：空鼓率<5%，缝隙均匀",
        "墙面验收：无裂缝，平整度<3mm",
        "门窗验收：开关顺畅，密封良好"
    ]
}

def estimate_budget(area: float, level: str = "中档", style: str = "现代简约"):
    """估算装修预算"""
    if level not in DECORATION_COST:
        level = "中档"
    if style not in STYLES:
        style = "现代简约"
    
    cost_range = DECORATION_COST[level]["范围"].split("-")
    style_factor = STYLES[style]["预算系数"]
    
    min_cost = float(cost_range[0]) * area * style_factor
    max_cost = float(cost_range[-1]) * area * style_factor
    
    # 各项费用分配
    total_mid = (min_cost + max_cost) / 2
    
    return {
        "房屋面积": f"{area}平米",
        "装修档次": level,
        "装修风格": style,
        "预算范围": f"{min_cost:.0f} - {max_cost:.0f}元",
        "费用分配参考": {
            "硬装人工费": f"{total_mid * 0.3:.0f}元（约30%）",
            "主材费": f"{total_mid * 0.4:.0f}元（约40%）",
            "辅材费": f"{total_mid * 0.15:.0f}元（约15%）",
            "设计费": f"{total_mid * 0.05:.0f}元（约5%）",
            "软装预留": f"{total_mid * 0.1:.0f}元（约10%）"
        },
        "风格特点": STYLES[style]["特点"],
        "建议": "实际费用以装修公司报价为准，建议多家对比"
    }

def get_process_guide():
    """获取施工流程"""
    total_days = sum([int(p["周期"].split("-")[1].replace("天", "")) for p in CONSTRUCTION_PROCESS])
    return {
        "施工流程": CONSTRUCTION_PROCESS,
        "总工期参考": f"约{total_days}天（2-3个月）",
        "注意事项": ["各阶段需验收合格后再进行下一阶段", "雨季施工注意防潮", "保留每阶段施工照片"]
    }

def get_pitfall_guide():
    """获取防坑指南"""
    return PITFALL_GUIDE

def main():
    if len(sys.argv) < 2:
        print("用法: python decoration.py <功能> [参数]")
        print("功能: budget(预算), process(流程), pitfall(防坑), styles(风格)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "budget":
        area = float(sys.argv[2]) if len(sys.argv) > 2 else 100
        level = sys.argv[3] if len(sys.argv) > 3 else "中档"
        style = sys.argv[4] if len(sys.argv) > 4 else "现代简约"
        result = estimate_budget(area, level, style)
    elif func == "process":
        result = get_process_guide()
    elif func == "pitfall":
        result = get_pitfall_guide()
    elif func == "styles":
        result = STYLES
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

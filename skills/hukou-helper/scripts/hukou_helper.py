#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
户口/落户助手
提供各城市落户条件查询和积分计算
"""

import json
import sys

# 主要城市落户政策
HUKOU_POLICIES = {
    "北京": {
        "方式": ["积分落户", "人才引进", "投靠落户", "应届毕业生"],
        "积分落户": {
            "基本条件": ["持北京居住证", "不超过法定退休年龄", "在京缴纳社保7年以上", "无刑事犯罪记录"],
            "积分指标": {
                "合法稳定就业": "最高60分",
                "合法稳定住所": "最高30分",
                "教育背景": "最高100分（博士100/硕士90/本科75/大专60）",
                "职住区域": "最高30分",
                "创新创业": "最高100分",
                "纳税": "最高30分",
                "年龄": "最高20分",
                "荣誉表彰": "最高20分"
            },
            "申请时间": "每年4-5月",
            "官网": "http://jzzd.yjj.beijing.gov.cn/"
        },
        "人才引进": {
            "条件": ["国家级人才计划入选者", "博士学位+副高职称", "世界500强企业高管"],
            "特点": "无需积分，直接落户"
        }
    },
    "上海": {
        "方式": ["居转户", "人才引进", "留学生落户", "应届生落户"],
        "居转户": {
            "基本条件": [
                "持上海居住证满7年",
                "持证期间缴纳社保满7年",
                "依法缴纳个人所得税",
                "被聘任为中级及以上专业技术职务"
            ],
            "特殊通道": "重点机构、特殊人才可缩短至3-5年",
            "官网": "http://rsj.sh.gov.cn/"
        },
        "应届生落户": {
            "条件": ["985/211高校本科及以上", "上海高校硕士及以上", "特定紧缺专业"],
            "年龄限制": "本科≤22岁，硕士≤27岁，博士≤35岁"
        }
    },
    "深圳": {
        "方式": ["人才引进", "积分入户", "随迁入户"],
        "人才引进": {
            "学历要求": {
                "大专": "35周岁以下",
                "本科": "45周岁以下",
                "硕士": "50周岁以下",
                "博士": "55周岁以下"
            },
            "其他条件": ["在深圳合法就业", "缴纳社保"],
            "官网": "http://hrss.sz.gov.cn/"
        },
        "积分入户": {
            "基本条件": ["持深圳居住证", "在深圳合法就业", "缴纳社保"],
            "积分指标": "年龄、学历、技能、居住年限、纳税等"
        }
    },
    "广州": {
        "方式": ["积分入户", "人才入户", "投靠入户"],
        "积分入户": {
            "基本条件": [
                "年龄45周岁以下",
                "持广东省居住证",
                "在广州合法稳定就业或创业并缴纳社保满4年",
                "积分总分值满85分"
            ],
            "官网": "http://rsj.gz.gov.cn/"
        }
    },
    "杭州": {
        "方式": ["学历落户", "技能落户", "积分落户", "投靠落户"],
        "学历落户": {
            "条件": {
                "大专": "35周岁以下，在杭就业",
                "本科": "45周岁以下，在杭就业",
                "硕士": "50周岁以下",
                "博士": "无年龄限制"
            },
            "官网": "http://www.hangzhou.gov.cn/"
        }
    },
    "成都": {
        "方式": ["人才落户", "投靠落户", "积分落户"],
        "人才落户": {
            "条件": ["大专及以上学历", "在成都就业或创业", "缴纳社保"],
            "特点": "政策宽松，大专即可落户",
            "官网": "http://cdhrss.chengdu.gov.cn/"
        }
    },
    "西安": {
        "方式": ["学历落户", "人才落户", "投靠落户"],
        "学历落户": {
            "条件": "大专及以上学历，无年龄限制",
            "特点": "全国最宽松之一，大专即可，无需就业证明",
            "官网": "http://rsj.xa.gov.cn/"
        }
    }
}

# 迁移所需材料
MIGRATION_MATERIALS = {
    "基本材料": [
        "居民身份证（原件+复印件）",
        "户口本（原件+复印件）",
        "迁移证明（原户籍地开具）",
        "近期免冠照片2张"
    ],
    "就业迁移": [
        "劳动合同或就业证明",
        "社保缴纳证明",
        "居住证"
    ],
    "投靠迁移": [
        "结婚证/出生证明（证明亲属关系）",
        "被投靠人户口本",
        "房产证或租房合同"
    ],
    "学历迁移": [
        "毕业证书",
        "学位证书",
        "报到证（应届生）"
    ]
}

def query_policy(city: str):
    """查询城市落户政策"""
    city = city.replace("市", "")
    if city in HUKOU_POLICIES:
        return HUKOU_POLICIES[city]
    return {
        "提示": f"暂无{city}详细政策",
        "建议": "请访问当地人社局官网或拨打12333热线",
        "已收录城市": list(HUKOU_POLICIES.keys())
    }

def estimate_score(education: str, age: int, social_insurance_years: int, city: str = "北京"):
    """估算积分落户分数（以北京为例）"""
    score = 0
    details = {}
    
    # 教育背景
    edu_scores = {"博士": 100, "硕士": 90, "本科": 75, "大专": 60, "高中": 30}
    edu_score = edu_scores.get(education, 0)
    score += edu_score
    details["教育背景"] = f"{edu_score}分（{education}）"
    
    # 年龄（越年轻分越高）
    if age <= 30:
        age_score = 20
    elif age <= 35:
        age_score = 15
    elif age <= 40:
        age_score = 10
    elif age <= 45:
        age_score = 5
    else:
        age_score = 0
    score += age_score
    details["年龄"] = f"{age_score}分（{age}岁）"
    
    # 社保年限
    insurance_score = min(social_insurance_years * 5, 60)
    score += insurance_score
    details["社保年限"] = f"{insurance_score}分（{social_insurance_years}年）"
    
    return {
        "城市": city,
        "估算总分": score,
        "分项明细": details,
        "说明": "此为简化估算，实际积分以官方计算为准",
        "参考": f"北京2023年落户分数线约为100分"
    }

def get_migration_guide():
    """获取迁移材料清单"""
    return MIGRATION_MATERIALS

def main():
    if len(sys.argv) < 2:
        print("用法: python hukou_helper.py <功能> [参数]")
        print("功能: policy(政策查询), score(积分估算), materials(材料清单)")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "policy":
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
        result = query_policy(city)
    elif func == "score":
        education = sys.argv[2] if len(sys.argv) > 2 else "本科"
        age = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        result = estimate_score(education, age, years)
    elif func == "materials":
        result = get_migration_guide()
    else:
        result = {"提示": f"不支持的功能: {func}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

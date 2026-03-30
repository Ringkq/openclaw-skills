#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国政务服务指南
提供户口、公积金、社保、养老等政务办理指南
"""

import json
import sys

# 落户条件数据库
HUKOU_REQUIREMENTS = {
    "北京": {
        "落户方式": ["积分落户", "人才引进", "投靠落户", "应届毕业生落户"],
        "积分落户条件": [
            "持有北京市居住证",
            "不超过法定退休年龄",
            "在京连续缴纳社会保险7年及以上",
            "无刑事犯罪记录"
        ],
        "积分指标": "合法稳定就业、合法稳定住所、教育背景、职住区域、创新创业、纳税、年龄、荣誉表彰、守法记录",
        "官网": "http://www.beijing.gov.cn/"
    },
    "上海": {
        "落户方式": ["居转户", "人才引进", "留学生落户", "应届生落户"],
        "居转户条件": [
            "持有《上海市居住证》满7年",
            "持证期间按规定参加本市城镇社会保险满7年",
            "持证期间依法在本市缴纳所得税",
            "在本市被聘任为中级及以上专业技术职务"
        ],
        "官网": "http://www.shanghai.gov.cn/"
    },
    "深圳": {
        "落户方式": ["人才引进", "积分入户", "随迁入户"],
        "人才引进条件": [
            "全日制大专学历，35周岁以下",
            "全日制本科及以上学历，45周岁以下",
            "中级专业技术资格，45周岁以下",
            "高级专业技术资格，50周岁以下"
        ],
        "官网": "http://www.sz.gov.cn/"
    },
    "广州": {
        "落户方式": ["积分入户", "人才入户", "投靠入户"],
        "积分入户条件": [
            "年龄45周岁以下",
            "持本市办理有效《广东省居住证》",
            "在本市合法稳定就业或创业并缴纳社会保险满4年",
            "积分总分值满85分"
        ],
        "官网": "http://www.gz.gov.cn/"
    },
    "杭州": {
        "落户方式": ["学历落户", "技能落户", "积分落户", "投靠落户"],
        "学历落户条件": [
            "全日制大专学历，35周岁以下",
            "全日制本科及以上学历，45周岁以下",
            "硕士及以上学历，50周岁以下"
        ],
        "官网": "http://www.hangzhou.gov.cn/"
    }
}

# 公积金提取类型
GONGJIJIN_EXTRACTION = {
    "购房提取": {
        "条件": "购买自住住房",
        "材料": ["身份证", "购房合同/房产证", "发票", "银行卡"],
        "额度": "不超过购房总价"
    },
    "租房提取": {
        "条件": "在本市无自有住房且租赁住房",
        "材料": ["身份证", "无房证明", "租房合同", "银行卡"],
        "额度": "各地政策不同，一般每月最高1500-3000元"
    },
    "还贷提取": {
        "条件": "偿还住房贷款本息",
        "材料": ["身份证", "借款合同", "还款明细", "银行卡"],
        "额度": "不超过实际还款额"
    },
    "离职提取": {
        "条件": "与单位解除劳动关系，未重新就业满一定期限",
        "材料": ["身份证", "离职证明", "银行卡"],
        "额度": "账户全部余额"
    },
    "退休提取": {
        "条件": "达到法定退休年龄",
        "材料": ["身份证", "退休证明", "银行卡"],
        "额度": "账户全部余额"
    }
}

# 社保服务
SHEBAO_SERVICES = {
    "查询缴纳记录": {
        "方式": ["社保局官网", "社保APP", "支付宝/微信城市服务", "12333热线"],
        "需要材料": "身份证号"
    },
    "社保转移": {
        "条件": "跨省就业变动",
        "材料": ["身份证", "社保卡", "转入地社保机构名称"],
        "流程": "原参保地办理转出 → 新参保地办理转入"
    },
    "退休计算": {
        "养老金公式": "基础养老金 + 个人账户养老金",
        "基础养老金": "（退休时上年度社平工资 + 本人指数化月平均工资）÷ 2 × 缴费年限 × 1%",
        "个人账户养老金": "个人账户储存额 ÷ 计发月数"
    }
}

def get_hukou_guide(city: str):
    """获取落户指南"""
    city = city.replace("市", "")
    if city in HUKOU_REQUIREMENTS:
        return {
            "城市": city,
            **HUKOU_REQUIREMENTS[city]
        }
    return {
        "提示": f"暂无{city}的详细落户信息",
        "建议": "请访问当地政务网站查询，或拨打12345热线咨询"
    }

def get_gongjijin_guide(extraction_type: str = None):
    """获取公积金提取指南"""
    if extraction_type and extraction_type in GONGJIJIN_EXTRACTION:
        return {
            "提取类型": extraction_type,
            **GONGJIJIN_EXTRACTION[extraction_type]
        }
    return {
        "公积金提取类型": list(GONGJIJIN_EXTRACTION.keys()),
        "说明": "请指定具体提取类型获取详细指南"
    }

def calculate_pension(salary: float, years: int, city: str = "北京"):
    """估算养老金"""
    # 简化计算，仅供参考
    social_avg_salary = 10000  # 假设社平工资
    
    # 基础养老金（假设缴费指数为1）
    base_pension = (social_avg_salary + salary) / 2 * years * 0.01
    
    # 个人账户养老金（假设个人账户累计为工资的8% * 年限）
    personal_account = salary * 0.08 * 12 * years
    personal_pension = personal_account / 139  # 60岁退休计发月数
    
    total = base_pension + personal_pension
    
    return {
        "预估月养老金": f"{total:.0f}元",
        "基础养老金": f"{base_pension:.0f}元",
        "个人账户养老金": f"{personal_pension:.0f}元",
        "个人账户累计": f"{personal_account:.0f}元",
        "缴费年限": f"{years}年",
        "说明": "此为简化估算，实际金额以社保局核算为准"
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python gov_service.py <服务类型> [参数]")
        print("服务类型: hukou(户口), gongjijin(公积金), shebao(社保), pension(养老金)")
        sys.exit(1)
    
    service = sys.argv[1]
    
    if service == "hukou":
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
        result = get_hukou_guide(city)
    elif service == "gongjijin":
        ext_type = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_gongjijin_guide(ext_type)
    elif service == "pension":
        salary = float(sys.argv[2]) if len(sys.argv) > 2 else 10000
        years = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        result = calculate_pension(salary, years)
    else:
        result = {"提示": f"暂不支持{service}服务"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

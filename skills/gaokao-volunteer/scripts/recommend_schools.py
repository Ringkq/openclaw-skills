#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高考院校推荐脚本
根据考生分数、省份、科目类型推荐适合的院校
"""

import json
import sys
import urllib.request
import urllib.parse

def get_school_recommendations(score: int, province: str, subject_type: str = "理科"):
    """
    根据分数推荐院校
    
    Args:
        score: 高考分数
        province: 省份名称
        subject_type: 科目类型 (理科/文科/综合)
    
    Returns:
        dict: 包含冲/稳/保三档院校推荐
    """
    
    # 分数段定义（示例数据，实际应从API获取）
    # 冲：分数线比考生分数高10-20分的院校
    # 稳：分数线与考生分数相近（±10分）的院校  
    # 保：分数线比考生分数低20-30分的院校
    
    result = {
        "考生信息": {
            "分数": score,
            "省份": province,
            "科目": subject_type
        },
        "志愿建议": {
            "冲": [],
            "稳": [],
            "保": []
        },
        "填报建议": ""
    }
    
    # 尝试从掌上高考API获取数据
    try:
        # 掌上高考公开API
        api_url = f"https://api.zjzw.cn/web/interface/?e_code=0&page=1&page_size=10&score={score}&province_name={urllib.parse.quote(province)}&type={urllib.parse.quote(subject_type)}&request_type=1&uri=apidata/api/gk/school/lists"
        
        req = urllib.request.Request(api_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('code') == '0000' and data.get('data'):
                schools = data['data'].get('item', [])
                
                for school in schools[:15]:
                    school_info = {
                        "院校名称": school.get('name', ''),
                        "院校类型": school.get('type_name', ''),
                        "所在城市": school.get('city_name', ''),
                        "近年最低分": school.get('min_score', ''),
                        "院校层次": school.get('level_name', '')
                    }
                    
                    min_score = int(school.get('min_score', 0) or 0)
                    
                    if min_score > score + 10:
                        result["志愿建议"]["冲"].append(school_info)
                    elif abs(min_score - score) <= 10:
                        result["志愿建议"]["稳"].append(school_info)
                    elif min_score < score - 10:
                        result["志愿建议"]["保"].append(school_info)
    
    except Exception as e:
        # API失败时使用本地知识库
        result["数据来源"] = "本地知识库（API暂不可用）"
        result["提示"] = f"建议访问 https://gaokao.chsi.com.cn/ 获取最新数据"
        
        # 基于分数段给出通用建议
        if score >= 680:
            result["志愿建议"]["冲"] = [{"建议": "清华大学、北京大学等顶尖985院校"}]
            result["志愿建议"]["稳"] = [{"建议": "复旦大学、上海交通大学、浙江大学等"}]
            result["志愿建议"]["保"] = [{"建议": "南京大学、武汉大学、中山大学等"}]
        elif score >= 620:
            result["志愿建议"]["冲"] = [{"建议": "复旦大学、上海交通大学等顶尖985"}]
            result["志愿建议"]["稳"] = [{"建议": "南京大学、武汉大学、中山大学等985"}]
            result["志愿建议"]["保"] = [{"建议": "华中科技大学、四川大学等985/211"}]
        elif score >= 580:
            result["志愿建议"]["冲"] = [{"建议": "华中科技大学、四川大学等985"}]
            result["志愿建议"]["稳"] = [{"建议": "北京航空航天大学、北京理工大学等211"}]
            result["志愿建议"]["保"] = [{"建议": "各省重点211院校"}]
        elif score >= 500:
            result["志愿建议"]["冲"] = [{"建议": "省内重点211院校"}]
            result["志愿建议"]["稳"] = [{"建议": "省内一本院校"}]
            result["志愿建议"]["保"] = [{"建议": "省内二本重点院校"}]
        else:
            result["志愿建议"]["冲"] = [{"建议": "省内一本院校（部分专业）"}]
            result["志愿建议"]["稳"] = [{"建议": "省内二本院校"}]
            result["志愿建议"]["保"] = [{"建议": "省内三本/专科院校"}]
    
    result["填报建议"] = f"""
冲稳保策略建议：
- 冲：选2-3所，分数线略高于您的分数，有一定风险但值得尝试
- 稳：选3-4所，分数线与您相近，录取概率较高
- 保：选2-3所，分数线明显低于您，确保有学可上

注意事项：
1. 参考近3年录取数据，不要只看最低分
2. 关注专业录取分数，热门专业可能比院校平均分高很多
3. 了解各省平行志愿规则，合理排序
4. 提前了解目标院校的招生计划数量
"""
    
    return result


def main():
    if len(sys.argv) < 3:
        print("用法: python recommend_schools.py <分数> <省份> [科目类型]")
        print("示例: python recommend_schools.py 580 湖南 理科")
        sys.exit(1)
    
    score = int(sys.argv[1])
    province = sys.argv[2]
    subject_type = sys.argv[3] if len(sys.argv) > 3 else "理科"
    
    result = get_school_recommendations(score, province, subject_type)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

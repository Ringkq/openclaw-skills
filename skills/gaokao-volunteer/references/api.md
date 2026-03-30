# 高考志愿填报 API 参考

## 数据来源

### 1. 掌上高考 API（公开）
- 院校列表：`https://api.zjzw.cn/web/interface/?uri=apidata/api/gk/school/lists`
- 院校详情：`https://api.zjzw.cn/web/interface/?uri=apidata/api/gk/school/detail`
- 专业列表：`https://api.zjzw.cn/web/interface/?uri=apidata/api/gk/major/lists`

### 2. 教育部阳光高考平台
- 官网：https://gaokao.chsi.com.cn/
- 院校查询：https://gaokao.chsi.com.cn/sch/search.do

### 3. 各省招生考试院
- 北京：https://www.bjeea.cn/
- 上海：https://www.shmeea.edu.cn/
- 广东：https://eea.gd.gov.cn/
- 湖南：https://www.hneeb.cn/

## 关键参数说明

### 科目类型
- `理科` / `文科` - 传统高考省份
- `综合` - 新高考省份（浙江、上海等）

### 录取批次
- `本科提前批` - 军校、警校、艺术类等
- `本科一批（A批）` - 重点本科
- `本科二批（B批）` - 普通本科
- `专科批` - 高职专科

### 志愿类型
- `平行志愿` - 大多数省份采用，同批次多个志愿平行投档
- `顺序志愿` - 少数省份，按志愿顺序投档

## 数据字段说明

```json
{
  "school_id": "院校代码",
  "name": "院校名称",
  "province_name": "所在省份",
  "city_name": "所在城市",
  "type_name": "院校类型（综合/理工/师范等）",
  "level_name": "院校层次（985/211/双一流等）",
  "min_score": "最低录取分数",
  "min_rank": "最低录取位次",
  "year": "年份"
}
```

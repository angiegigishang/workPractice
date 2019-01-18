# 工资结算app对外提供接口说明
## 获取工序-物料分组单价接口
- url: `/api/wage_settlement/process_materiel_price_mapper?person_code=xxxx`
- method: `get`
- desc: 获取当前工资-物料分组单价映射关系,如果请求中包含person_code,则返回该员工对应工序的物料单价映射
- response_body:
```json
{
  "app_group": "乐清工业云",
  "app_name": "工资管理",
  "code": "success",
  "data": {
    "columns": [
      {
        "field": "process",
        "label": "工序",
        "name": "process"
      },
      {
        "field": "materiel_group_instance_g1",
        "label": "物料分组1",
        "name": "materiel_group_instance_g1"
      },
      {
        "field": "materiel_group_instance_g2",
        "label": "物料分组2",
        "name": "materiel_group_instance_g2"
      },
      {
        "field": "materiel_group_instance_g3",
        "label": "物料分组3",
        "name": "materiel_group_instance_g3"
      }
    ],
    "mapper": [
      {
        "code": "materiel_group_instance_g1",
        "materiel_names": [
          "T901H30ADC24V 4脚 47规格",
          "T901H40ADC24V 4脚 客户标",
          "T901Z30ADC12V 6脚",
          "T901D40ADC12V 4脚 24规格",
          "T901H40ADC24V 4脚",
          "NNC67E-1Z30ADC110V",
          "T901H40ADC12V 4脚 23规格",
          "T901D40ADC12V 4脚",
          "YONGNENG YX209E-S-124DM",
          "T901H40ADC12V 5脚"
        ],
        "name": "物料分组1"
      },
      {
        "code": "materiel_group_instance_g2",
        "materiel_names": [
          "T901H30ADC5V 4脚 永能标",
          "HHC67E(T90)1H40ADC12V4脚",
          "T901D40ADC24V 4脚",
          "T901Z40ADC12V 6脚",
          "YONGNENG YX209E-S-112D",
          "T901H30ADC48V 4脚 20S",
          "T901Z30ADC24V 5脚",
          "T901D40ADC12V 5脚 24规格",
          "T901Z30ADC12V 6脚",
          "T901Z30ADC12V 5脚 永能标"
        ],
        "name": "物料分组2"
      },
      {
        "code": "materiel_group_instance_g3",
        "materiel_names": [
          "T901D40ADC12V 5脚 24规格",
          "HHC67E(T90)1H30ADC24V4脚S",
          "T901H30ADC110V 5脚",
          "T901D30ADC12V 5脚 17规格",
          "T901Z30ADC12V 5脚",
          "T901Z40ADC12V 6脚",
          "T901H30ADC12V 4脚 永能标",
          "T901H30ADC48V 4脚 20S",
          "T901Z40ADC6V 5脚 NNC标"
        ],
        "name": "物料分组3"
      }
    ],
    "rows": [
      {
        "materiel_group_instance_g1": "0.008",
        "materiel_group_instance_g2": "0.001",
        "materiel_group_instance_g3": "0.008",
        "process": "铆芯",
        "process_code": "process_0001"
      }
    ]
  },
  "info": "get process/materiel_group price mapper succefully"
}
```
## 调整工序-物料分组单价接口
- url: `/api/wage_settlement/process_materiel_price_mapper`
- method: 'post'
- desc: 前端通过页面调整工序-物料对应单价
- request_body:
```json
{
    "materiel_group_instance_g1": "1",
    "materiel_group_instance_g2": "210",
    "materiel_group_instance_g3": "3",
    "process": "铆芯",
    "process_code": "process_0001"
}
```
## 获取计时工资信息
- url: `/api/wage_settlement/timely_wage_mapper?person_code=xxx`
- method: `get`
- desc: 获取计时工资员工列表,如果提供person_code则只返回该员工的计时工资单价
- response_body:
```json
{
    "app_group": "",
    "app_name": "",
    "code": "success",
    "data": [
        {
            "person_code": "person_wuzhilan",
            "person_name": "吴志兰",
            "price": "",
            "wage_code": "dayly_wage",
            "wage_name": "日薪"
        }
    ],
    "info": "get timely_wage_info successfully"
}
```
## 更新计时工资信息
- url: `/api/wage_settlement/timely_wage_mapper`
- method: `post`
- desc: 更新计时工资员工列表
- request_body:
```json
{
  "person_code": "person_wuzhilan",
  "price": "",
  "wage_code": "dayly_wage"
}
```
## 获取员工工资信息
- url: `/api/wage_settlement/wage_detail`
- method: `get`
- desc: 获取员工当前工资信息
- response_body:
```json
{
  "app_group": "",
  "app_name": "",
  "code": "success",
  "data": [
    {
      "person_code": "person_fuxunmin",
      "person_name": "付训民",
      "piece_amount": 50.0,
      "total_time": null,
      "wage": 900.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_liujiangzhong",
      "person_name": "刘江中",
      "piece_amount": 50.0,
      "total_time": null,
      "wage": 900.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_linfeng",
      "person_name": "林峰",
      "piece_amount": 28.0,
      "total_time": null,
      "wage": 140.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_raoguihe",
      "person_name": "绕桂和",
      "piece_amount": 0.0,
      "total_time": null,
      "wage": 0.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_yinxuejie",
      "person_name": "殷学杰",
      "piece_amount": 0.0,
      "total_time": null,
      "wage": 0.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_wangtao",
      "person_name": "王涛",
      "piece_amount": 0.0,
      "total_time": null,
      "wage": 0.0,
      "wage_type": "计件工资"
    },
    {
      "person_code": "person_wuzhilan",
      "person_name": "吴志兰",
      "piece_amount": null,
      "total_time": 4,
      "wage": 492.0,
      "wage_type": "日薪"
    }
  ],
  "info": "get wage detail successfully"
}
```

### 1.获取所有未下发和已下发的计划
```
url: GET /api/plan_management/manage/plan/list
```
前端请求后端的数据结构： 无
后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data":
     [
        {
          "task_no": "11111",  //任务单号
          "material_code": "557",  //物料编码
          "material_name": "物料A", //物料名
          "material_unit": "个", //物料单位
          "plan_count": 100,  //计划数量
          "plan_start_date": "2018-12-12",  //计划开工日期
          "comment": "",  //备注信息
          "workshop_name": "车间1",  //车间名
          "workshop_code": "workshop_6", //车间编码
          "product_line_code": "6t90",  //产线编码
          "operator": "admin",   //录入人员
          "create_time": "2018-12-10: 10:00:00",  //录入时间
          "modify_time": "2018-12-20: 13:10:20",  //修改时间
          "plan_status": 0,  //计划状态, 0表示未下发，1表示已下发, 3表示暂停
          "erp_plan_status": "下达", //ERP导入计划原状态文字说明
          "plan_type": 0, //计划类型，0表示ERP导入，1表示自定义添加
          "dzzd_task_type": "常规产品", //任务类型，定制字段
          "dzzd_task_date": "2019-01-10", //开单日期
          "dzzd_plan_no": "11111", //计划单号, 定制字段
          "dzzd_main_plan_no": "4545545",  //主计划号，定制字段
          "dzzd_material_spec": "NNC",     //规格，定制字段
          "dzzd_special_requirements": "" //特殊要求，定制字段
        }
     ]
}
```


### 2. 添加自定义计划
```
url: POST /api/plan_management/manage/plan/add
```
前端请求后端的数据结构：
```
{
  "task_no": "11111",   //必填
  "material_code": "557", //必填，选择
  "material_name": "物料A",  //必填，选择
  "material_unit": "个",  //必填，选择
  "plan_count": 100,  //必填
  "plan_start_date": "2018-12-12",
  "comment": "",
  "workshop_name": "车间1",  //必填，选择
  "workshop_code": "workshop_6",
  "dzzd_task_type": "常规产品",
  "dzzd_task_date": "2019-01-10",
  "dzzd_plan_no": "11111",
  "dzzd_main_plan_no": "4545545",
  "dzzd_material_spec": "NNC",
  "dzzd_special_requirements": ""
}
```
后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data":
    {
      "task_no": "11111",
      "material_code": "557",
      "material_name": "物料A",
      "material_unit": "个",
      "plan_count": 100,
      "plan_start_date": "2018-12-12",
      "comment": "",
      "workshop_name": "车间1",
      "workshop_code": "workshop_6",
      "product_line_code": "6t90",
      "operator": "admin",
      "create_time": "2018-12-10: 10:00:00",
      "modify_time": "2018-12-20: 13:10:20",
      "plan_status": "0",
      "plan_type": 0,
      "dzzd_task_type": "常规产品",
      "dzzd_task_date": "2019-01-10",
      "dzzd_plan_no": "11111",
      "dzzd_main_plan_no": "4545545",
      "dzzd_material_spec": "NNC",
      "dzzd_special_requirements": ""
    }
}
```


### 3. 下发计划（包含批量下发）
```
url: POST /api/plan_management/manage/plan/dispatch
```
前端请求后端的数据结构：
```
{
    "task_no_list": ["task_no1", "task_no2"],   //需要下发的任务单号列表
    "task_seq_list": ["task_no3", "task_no2","task_no1", "task_no4"],  //所有当天该产线所有任务的生产顺序任务单号列表
    "product_line_code": "product_line_6t90",
    "plan_start_date": "2019-01-10"
}
```

后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data":
    [
        {
            "task_no": "A181120203-00",
            "task_type": "常规产品",
            "task_date": "2019-01-10",
            "material_code": "material_t901d40adc24v4",
            "material_name": "T901D40ADC24V 4脚",
            "material_spec": "NNC",
            "material_unit": "个",
            "plan_count": 4000,
            "plan_no": "A181120203-00",
            "plan_start_date": "2019-01-15",
            "plan_end_date": "2019-01-16",
            "real_start_date": "",
            "real_end_date": "",
            "workshop_name": "六车间",
            "create_time": "2019-01-14 10:13:38.348108",
            "erp_plan_status": "",
            "plan_status": 1,
            "main_plan_no": "",
            "special_requirements": "",
            "workshop_code": "workshop_6",
            "comment": "",
            "product_line_code": "product_line_6t90",
            "operator": "admin",
            "modified_time": "",
            "dispatch_time": "2019-01-14 10:42:39.986123",
            "qualified_count": 0,
            "unqualified_count": 0,
            "plan_type": 1
        }
    ]
}
```


### 4. 删除未下发的计划
```
url: POST /api/plan_management/manage/plan/delete
```
前端请求后端的数据结构：
```
{
    "task_no": "11111"  //需要删除的计划任务单号
}
```

后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data": null
}
```

### 5. 回退已下发的计划
```
url: POST /api/plan_management/manage/plan/rollback
```
前端请求后端的数据结构：
```
{
    "task_no": "11111"  //需要回退的计划任务单号
}
```
后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data": null
}
```

### 6. 获取计划相关的配置数据，包括物料名称和编码，车间名称和编码，产线名称和编码以及所有的计划定制字段
```
url: GET /api/plan_management/manage/plan/config
```
前端请求后端的数据结构：无

后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data":
    {
        "material_config":
        [
            {
              "material_code": "557",
              "material_name": "物料A",
              "material_unit": "个",
            }
        ],
        "workshop_config":
        [
            {
               "workshop_name": "六车间",
               "workshop_code": "workshop_6",
               "pl_list":
               [
                  {
                    "product_line_code": "product_line_6t90",
                    "product_line_name": "T90继电器生产线"
                  }
               ]
            }
        ],
        "custom_fields":
        [
            {
                "field_code": "custom_field_main_plan_no",
                "field_name": "主计划号"
            },
            {
                "field_code": "custom_field_material_spec",
                "field_name": "规格型号"
            },
            {
                "field_code": "custom_field_special_requirements",
                "field_name": "特殊要求"
            },
            {
                "field_code": "custom_field_plan_no",
                "field_name": "计划单号"
            },
            {
                "field_code": "custom_field_task_type",
                "field_name": "任务类型"
            }
        ]
    }
}
```


### 7. 获取下发计划时某个产线某一个开工日期的相关其他计划

```
url: GET /api/plan_management/manage/(?P<product_line>.*)/(?P<plan_start_date>.*)/dispatched_plan/list
```

前端请求后端的数据结构：无


后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",
    "data":
    [
        {
            "task_no": "11111",
            "material_name": "物料A",
            "plan_status": 2, //已下发/1, 进行中/2, 已完工/4
        }
    ]
}
```
`注`: 返回给前端的计划数据列表中计划是按照序号顺序排列的。


### 8. 检查准备下发的计划是否都是还没下发的状态
```
url: POST /api/plan_management/manage/plan/dispatch_check
```
前端请求后端的数据结构：
```
["task_no1", "task_no2"]
```
后端返回前端的数据结构：
```
{
    "code":"success",
    "info": "",  //失败会给出具体失败原因
    "data": null
}
```



1、获取某产线所有人员信息
```
url: GET /api/progress_report/(?P<product_line_code>.*)/employee/list
```
前端发送到后端的请求数据结构: 无

后端返回的数据结构:
```
[
  {
    "group_code": "",
    "member_list":
    [
        {
          "name": "",
          "code": ""
        }
    ]
  }
]
```
`注`: 返回的分组是以报工点为区分的逻辑组, 组内所有员工仅包括该组内当前上班的员工信息.

2、获取某产线包含的所有工序信息
```
url: GET /api/progress_report/(?P<product_line_code>.*)/process/list
```
前端发送到后端的请求数据结构: 无

后端返回的数据结构:
```
[
  {
     "group_code": "",
     "process_list":
     [
        {
            "name": "",  //工序名
            "code": "",  //工序编码
            "type": 0,   //0: 自动工序 1：人工工序
            "is_report_point": 1 //0: 不是报工点 1：是报工点
        }
     ]
  }
]
```

`注`: 获取的工序信息列表的顺序是按照主数据上的sequence字段排序的。

3、获取某个报工点工序的相关计划列表和计划的相关监控报工数据
```
url: GET /api/progress_report/(?P<product_line_code>.*)/(?P<group_code>.*)/(?P<process_code>.*)/production_plan/list
```
前端发送到后端的请求数据结构: 无

后端返回的数据结构:
```
[
  {
    "plan_number": "",  //计划号
    "material_name": "",   //物料名称
    "material_code": "",   //物料编码
    "plan_count": 10,   //计划生产数量
    "qualified_count": 10,  //总监控合格数
    "unqualified_count": 5,    //总监控不合格数
    "plan_progress": "",    //计划完成进度百分比
    "report_data":
    {
        "current_detected_count": { //当天监测的合格数和不合格数
          "qualified_count": 60,
          "unqualified_count": 2
        }
        "remain_submit_count": {  //剩余可报工数
          "qualified_count": 40,
          "unqualified_count": 2
        },
        "current_submitted_count": {   //当前组已提交的报工数, 如果没有报过则都为0
          "qualified_count": 0,
          "unqualified_count": 0
        }
    }
  }
]
```

4、保存某一个计划下的报工数据
```
url: POST /api/progress_report/report/save
```
前端发送到后端的请求数据结构:
```
{
  "group_code": "group_code1", // 当前报工组编码
  "plan_number": "", //计划号
  "process_code": "", // 工序编码
  "material_name": "", //物料名
  "material_code": "", //物料编码
  "qualified_count": 50, //合格数
  "unqualified_count": 20 //不合格数
}
```

后端返回的数据结构:
```
{
    "code":"success",
    "info": "",
    "data": null
}
```




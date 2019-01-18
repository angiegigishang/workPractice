1. 获取某个报工点工序当天相关的所有计划数据和监控数

```
url: GET /api/monitor/production_plan_data/(?P<product_line_code>.*)/(?P<process_code>.*)
```

报工app发往生产监控app的数据结构: 无

生产监控app返回的数据结构:
```
[
    {
        "plan_number": "",  //计划号
        "material_name": "",  //物料名称
        "material_code": "",  //物料编码
        "plan_count": "",   //计划生产数量
        "total_plan_qualified_count": 100,  //计划总的监控合格数
        "total_plan_unqualified_count": 5,  //计划总的监控不合格数
        "current_qualified_count": 20,  //当前报工工序监测的监控合格数
        "current_unqualified_count": 3,  //当前报工工序监测的的监控不合格数
        "plan_progress": "",     //计划完成进度百分比
    }
]
```

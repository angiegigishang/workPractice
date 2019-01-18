1) 计划状态变更
```
url: POST /api/plan_management/plan/status_update
```
计划
监控app发往计划管理app的数据结构:
```
[
    {
        "plan_no": "A181120203-00",
        "status": 2, //2表示进行中，3表示暂停，4表示已完工
        "progress_detail":  //仅更新状态为暂停和已完工时传合格数和不合格数，对于进行中没有这个字段
        {
            "qualified_count": 1000,
            "unqualified_count": 2
        }
    }
]
```

计划管理app返回的数据结构:
```
{
    "code":"success",
    "info": "",
    "data": null
}
```

2) 获取当天某个产线已下发的所有计划
```
url: GET /api/plan_management/manage/(?P<product_line>.*)/dispatched_plan/list
```
计划管理app返回给监控app的数据结构:
```
[
	{
		"plan_no": "A181120203-00",
		"sequence": 1,  //计划之间的顺序
		"material_name": "T901H40ADC12V 4脚 23规格",
		"material_code": "materiel_t901h40adc12v4_23",
		"plan_count": 10000,
		"qualified_count": 1000,
		"unqualified_count": 2
	}
]
```

3) 推送当天已下发的所有计划到监控app
```
url: POST /api/monitor/recevie_plan/(?P<product_line>.*)
```
计划管理app返回给监控app的数据结构:
```
[
	{
		"plan_no": "A181120203-00",
		"sequence": 1,  //计划之间的顺序
		"material_name": "T901H40ADC12V 4脚 23规格",
		"material_code": "materiel_t901h40adc12v4_23",
		"plan_count": 10000,
		"qualified_count": 1000,
		"unqualified_count": 2
	}
]
```
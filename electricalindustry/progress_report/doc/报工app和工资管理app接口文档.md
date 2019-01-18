1) 获取本月的所有报工组的报工数据
```
url: /api/progress_report/report/current_month
```
工资管理app发给报工app数据结构: 无

返回给报工app的数据结构:
```
{
    "code":"success",
    "info": "",
    "data":
	[
		{
			"groupCode": "bg_ryfz_6t90_z3",
			"report":
			[
				{
					"materielCode": "materiel_t901z30adc12v5_ynb",
					"qualified_count": 30,
					"unqualified_count": 0,
					"date": "2019-01-11"
				}
			]
		}
	]
}
```

`注`: 上面数组中每一项为某一天的数据，之前某个报工组按月统计总数改为按天统计。
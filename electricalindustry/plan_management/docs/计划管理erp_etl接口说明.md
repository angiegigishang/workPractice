1) 接收ERP计划数据
```
url: POST /api/plan_management/erp_plan/transfer
```

发送数据app发往计划管理app数据结构:
```
{
	"plan_list":
	[
		{
			"task_no": "A181120203-00", //字段task_serial, 必要字段
			"task_type": "常规产品",  //字段task_type, 可选字段
			"task_date": "2019-01-09", //字段task_date， 可选字段
			"material_code": "materiel_t901h40adc12v4_23", //字段product_code， 必要字段
			"material_name": "T901H40ADC12V 4脚 23规格",  //字段product_name， 必要字段
			"material_spec": "NNC", //字段product_spec, 可选字段
			"material_unit": "个", //字段product_unit， 必要字段
			"plan_count": 1000,  //字段plan_num， 必要字段
			"plan_no": "A181120203-00",  //字段plan_serial, 可选字段
			"plan_start_date": "2019-01-10", //字段plan_start， 必要字段
			"plan_end_date": "2019-01-12",  //字段plan_end， 必要字段
			"real_start_date": "2019-01-10", //字段real_start, 可选字段
			"real_end_date": "2019-01-12", //字段real_end, 可选字段
			"workshop_name": "六车间",  //字段work_center， 必要字段
			"create_time": "2019-01-10", //字段chage_time， 必要字段
			"erp_plan_status": "投放",  //字段plan_status对应状态文字(1.锁定，2.确认，3.下达，4.投放，5.流转，6.暂停, 7.完工), 可选字段
			"plan_status": "可下发"  //3种状态，可下发，已完成和不可下发, 这个字段值由上一个字段erp_plan_status决定
		}
	]
}
```

返回给发送数据app的数据结构:
```
{
    "code":"success",   //成功时为success, 失败为fail
    "info": "",
    "data": null
}
```

`注`: etl app发送过来的material_code在主数据中对应物料编号，在存入数据库时需要对应转换成主数据中的物料编码。
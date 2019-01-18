1) 获取某一个月所有的报工统计记录.
```
url: /api/progress_report/statistics/(?P<month>.*)
```
前端发往后端的数据结构: 无

后端返回给前端的数据结构:
```
{
  "header_list":
  [
    {
      "code": "m1",   //物料编码
      "name": "物料1"  //物料名称
    }
  ],
  "data_list":
  [
    {
      "name": "组1",  //组名
      "data":
      {
        "code1": "1000/2",  //物料编码和对应的报工数, 报工数格式为 合格数/不合格数
        "code2": "200/1"
      }
    }
  ]
}
```
`注`: url参数中month参数格式为yyyyMM, 例如201901.

2) 获取某一个月所有的考勤统计记录.
```
url: /api/attendance_manage/statistics/(?P<month>.*)
```
前端发往后端的数据结构: 无

后端返回给前端的数据结构:
```
{
  "header_list":
  [
    {
      "code": "normal",   //考勤类型编码
      "name": "正常上班"  //考勤类型名称
    }
  ],
  "data_list":
  [
    {
      "name": "名字1",  //人名
      "data":
      {
        "normal": 20,  //考勤类型编码和对应类型的数目
        "abnormal": 2
      }
    }
  ]
}
```


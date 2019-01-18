1. 获取当前时间在岗的所有员工信息
```
url: GET /api/attendance_manage/pipeline/(?P<pipeline_code>.*)/on_work_info
```

报工app发往考勤app数据结构: 无

考勤app返回的数据结构:
```
["person_code1", "person_code2"]
```

`注`: 当前接口返回所有某一条产线的在岗员工编码列表
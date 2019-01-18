from attendance_manage.handlers.http_handler.handler import (
    WebHandler, AllCheckinInfo, OnWorkInfo,
    CheckinInfo, OnworkCheckinInfo, WorkStatInfo,
    WorkingHoursHandler
)

url = [
    (r'/http_url', WebHandler),
    (r'/api/attendance_manage/pipeline/(?P<pipeline_code>.*)/attendance_info', AllCheckinInfo),
    (r'/api/attendance_manage/pipeline/(?P<pipeline_code>.*)/onwork_attendance', OnworkCheckinInfo),
    (r'/api/attendance_manage/pipeline/(?P<pipeline_code>.*)/on_work_info', OnWorkInfo),
    (r'/api/attendance_manage/checkin_info', CheckinInfo),
    (r'/api/attendance_manage/statistics/(?P<month>.*)', WorkStatInfo),
    (r'/api/attendance_manage/working_hours', WorkingHoursHandler)
]

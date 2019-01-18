from progress_report.handlers.http_handler.web_handler import *

url = [
    (r'/api/progress_report/(?P<product_line_code>.*)/employee/list', EmployeeFetchHandler),
    (r'/api/progress_report/(?P<product_line_code>.*)/process/list', ProcessFetchHandler),
    (r'/api/progress_report/(?P<product_line_code>.*)/(?P<group_code>.*)/(?P<process_code>.*)/production_plan/list', PlanFetchHandler),
    (r'/api/progress_report/report/save', ReportSaveHandler),
    (r'/api/progress_report/statistics/(?P<month>.*)', ReportStatFetchHandler),
    (r'/api/progress_report/report/current_month', CurrentMonthReportFetchHandler),
    (r'/api/progress_report/report/data_per_month', ReportDataPerMonthHandler)
]

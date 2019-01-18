from plan_management.handlers.http_handler.history_web_handler import *
from plan_management.handlers.http_handler.manage_web_handler import *
from plan_management.handlers.http_handler.manage_app_handler import *
from plan_management.handlers.http_handler.etl_process_handler import *

url = [
    (r'/api/plan_management/manage/plan/list', PlanFetchHandler),
    (r'/api/plan_management/manage/plan/add', PlanAddHandler),
    (r'/api/plan_management/manage/plan/dispatch', PlanDispatchHandler),
    (r'/api/plan_management/manage/plan/delete', PlanDeleteHandler),
    (r'/api/plan_management/manage/plan/rollback', PlanRollbackHandler),
    (r'/api/plan_management/manage/plan/config', PlanConfigFetchHandler),
    (r'/api/plan_management/manage/(?P<product_line>.*)/(?P<plan_start_date>.*)/dispatched_plan/list', RemainingDispatchedPlanFetchHandler),
    (r'/api/plan_management/manage/plan/dispatch_check', PlanDispatchCheckHandler),
    (r'/api/plan_management/manage/plan/history/(?P<start_date>.*)/(?P<end_date>.*)', PlanHistoryHandler),

    (r'/api/plan_management/plan/status_update', PlanStatusUpdateHandler),
    (r'/api/plan_management/manage/(?P<product_line>.*)/dispatched_plan/list', DispatchedPlanFetchHandler),

    (r'/api/plan_management/erp_plan/transfer', ErpPlanTransferHandler)
]

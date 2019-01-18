from production_line_monitor.handlers.http_handler.handler import (
    ChangePlanHandler,
    ProductLineHandler,
    SectionsHandler,
    ReceiveHandler,
    AllDataHandler,
    ReceivePlanHandler,
    ReceiveCheckInHandler,
)

url = [
    (r'/api/monitor/change_plan/(?P<product_line>.*)/(?P<process_code>.*)',
     ChangePlanHandler),
    (r'/api/monitor/production_plan_data/(?P<product_line>.*)/(?P<process_code>.*)', ProductLineHandler),
    (r'/api/monitor/sections/(?P<product_line>.*)', SectionsHandler),
    (r'/api/monitor/recevie/(?P<product_line>.*)', ReceiveHandler),  # useless
    (r'/api/monitor/recevie_plan/(?P<product_line>.*)', ReceivePlanHandler),  # useless
    (r'/api/monitor/recevie_checkin/(?P<product_line>.*)', ReceiveCheckInHandler),  # useless
    (r'/api/monitor/all/(?P<product_line>.*)', AllDataHandler),
]

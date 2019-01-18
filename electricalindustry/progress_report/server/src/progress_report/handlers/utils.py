from mg_app_framework import get_logger, get_handler, TaskKey
import traceback
import tornado.httpclient as http_lib
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


def log_exception(e, err_info):
    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    err_msg = '程序错误信息: {0}, 异常信息: {1}\n'.format(err_info, str(e))
    get_logger().error(err_msg)
    get_logger().error('\n')
    get_logger().error('traceback信息: {0}'.format(traceback_str))


# 获取报工的mongodb collection
def get_report_db_collection():
    handler = get_handler(TaskKey.mongodb_async)
    return handler.progress_report.report


async def send_request(url, request_data, request_type):
    response = None
    try:
        http_request = http_lib.HTTPRequest(url)
        http_request.method = request_type
        http_request.allow_nonstandard_methods = True
        if request_data:
            http_request.body = json.dumps(request_data, ensure_ascii=False)
        http_client = http_lib.AsyncHTTPClient()
        response = await http_client.fetch(http_request)
    except Exception as e:
        log_exception(e, '发送rest请求失败, url:{0}'.format(url))
    return response


def get_current_month_date_range():
    current_time = datetime.today().date()
    first_day = current_time + relativedelta(day=1)
    last_day = current_time + relativedelta(months=+1, days=-1, day=1)
    return str(first_day), str(last_day)

from tornado.httpclient import AsyncHTTPClient

from mg_app_framework import get_store, HttpClient, get_logger

async def push_attendance_info(pipeline_code, attendance_info=None):
    # 从考勤模块获取工时
    try:
        store = get_store()
        report_module_url = store.data['data']['api']['monitor_push'].format(pipeline_code)
        get_logger().info(report_module_url)
        client = HttpClient(AsyncHTTPClient(max_clients=1000))
        report_data = await client.post(report_module_url, data=attendance_info)
        client.close()
        return report_data.data
    except Exception as e:
        get_logger().exception(e)
        raise Exception('推送考勤信息失败')
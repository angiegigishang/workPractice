from tornado.httpclient import AsyncHTTPClient

from mg_app_framework import get_store, HttpClient, get_logger

async def get_report_info():
    # 从报工模块获取当月信息
    # TODO:报工模块将会返回具体到天的报工量，对应的计算接口需要调整
    try:
        store = get_store()
        report_module_url = store.data['data']['api']['report']
        client = HttpClient(AsyncHTTPClient(max_clients=1000))
        report_data = await client.get(report_module_url, data={})
        client.close()
        return report_data.data
    except Exception as e:
        get_logger().exception(e)
        raise Exception('报工信息获取失败')


async def get_working_hour_info(person_info=None):
    # 从考勤模块获取工时
    try:
        store = get_store()
        report_module_url = store.data['data']['api']['working_hour']
        client = HttpClient(AsyncHTTPClient(max_clients=1000))
        report_data = await client.post(report_module_url, data=person_info)
        client.close()
        return report_data.data
    except Exception as e:
        get_logger().exception(e)
        raise Exception('考勤信息获取失败')

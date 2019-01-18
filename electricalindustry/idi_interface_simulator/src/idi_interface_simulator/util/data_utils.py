from mg_app_framework import get_handler,get_logger,TaskKey,get_context,HttpClient,get_store
from datetime import datetime,timedelta
import urllib
import string
import traceback

date_format = "%Y-%m-%d %H:%M:%S"


def get_now_timestamp():
    return datetime.now().strftime(date_format)

async def clear_plan_range(product_line):
    try:
        mongo_handler = get_handler(TaskKey.mongodb)
        plan_collection = mongo_handler.xldq.plan_range
        plan_collection.delete_many({"product_line":product_line})
    except Exception as e:
        get_logger().error("get_plan_code_list error:%s", e)
        raise e


def get_process_code_list(product_line):
    # 从内存中获取信息
    pipeline_device_in_memory = get_context('pipeline_device')
    target_pipeline_info = pipeline_device_in_memory.get(product_line, {})
    process_seq = []
    for value in target_pipeline_info.values():
        process_info = value.setdefault('process', [])
        for p in process_info:
            process_seq.append(p['code'])
    return process_seq

def get_code_map_dict(product_line):
    # 从内存中获取信息
    response = {}
    pipeline_device_in_memory = get_context('pipeline_device')
    target_pipeline_info = pipeline_device_in_memory.get(product_line, {})
    pipeline_response = response.setdefault(product_line, {})
    for value in target_pipeline_info.values():
        process_list = value.setdefault('process', [])
        if process_list:
            process_code = process_list[0]['code']
        if process_code:
            point_response = {}
            point_list = value.setdefault('point', [])
            for p in point_list:
                if p['classify'] == '状态':
                    point_response.update({
                        'status': p['code']
                    })
                elif p['classify'] == '数量':
                    point_response.update({
                        'positive': p['code']
                    })
                elif p['classify'] == '不合格数':
                    point_response.update({
                        'negative': p['code']
                    })
            pipeline_response.update(
                {
                    process_code: point_response
                }
            )
    return response


async def get_data(url, data):
    client = HttpClient()
    url = urllib.parse.quote(url, safe=string.printable)
    res = await client.get(url, data=data)
    return res.data


async def get_idi_data(tag_code_list, start_time, end_time, org="organization_xldq"):
    logger = get_logger()
    logger.debug("get_idi_data start,tag_code_list info:%s,start_time:%s,end_time:%s", tag_code_list, start_time,
                end_time)
    try:
        if isinstance(start_time, datetime):
            start_time = start_time.strftime(date_format)
            end_time = end_time.strftime(date_format)
        url = get_store().get_idi_url()
        data = [
            {"code": tag_code,
             "start_time": start_time,
             "end_time": end_time,
             } for tag_code in tag_code_list]
        logger.debug("idi request url:%s", url)
        logger.debug("idi request data:%s", data)
        res = await get_data(url, {org: data})
        logger.debug("idi res data:%s", res)
        return res[org] if res else {}
    except Exception as e:
        traceback.print_exc()
        logger.error("get_idi_data error:%s", e)
        return {}

async def get_idi_lastest_value(code_list,timestamp,org="organization_xldq"):
    logger = get_logger()
    try:
        if isinstance(timestamp,str):
            timestamp = datetime.strptime(timestamp,date_format)
        start_timestamp = timestamp - timedelta(days=30)
        start_timestamp_str = start_timestamp.strftime(date_format)
        end_timestamp_str = timestamp.strftime(date_format)
        idi_data_dict = await get_idi_data(code_list,start_timestamp_str,end_timestamp_str)
        res = {}
        for code,value_dict in idi_data_dict.items():
            try:
                value = value_dict[max(value_dict)]
            except:
                value = 0
            res[code] = value
        return res
    except Exception as e:
        logger.error("get_idi_lastest_value error:%s",e)
        return {}

async def send_change_flag(product_line,process_code_list,status):
    client = HttpClient()
    url = "http://127.0.0.1:8989/api/monitor/recevie/%s" %product_line
    url = urllib.parse.quote(url, safe=string.printable)
    data = {
        "msg_type":"status",
        "status":status,
        "process_code_list":process_code_list
    }
    res = await client.post(url,data)
    get_logger().info("send_change_flag res~~~~~~~~~~~~~~~~~~~~~~~~~~:%s",res)
    return True

async def send_reset_flag(product_line):
    client = HttpClient()
    url = "http://127.0.0.1:8989/api/monitor/recevie/%s" %product_line
    url = urllib.parse.quote(url, safe=string.printable)
    data = {
        "msg_type":"reset",
    }
    res = await client.post(url,data)
    get_logger().info("send_reset_flag res~~~~~~~~~~~~~~~~~~~~~~~~~~:%s",res)
    return True







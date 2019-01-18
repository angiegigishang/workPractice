from mg_app_framework import HttpClient, get_logger, get_store, get_handler, TaskKey, get_context,update_context
import urllib
import string
from datetime import datetime, timedelta
import traceback
from production_line_monitor.util.query_utils import (
    get_plan_time_range,
    get_plan_code_list,
    # get_plan_info,
    get_now_timestamp)
from production_line_monitor.handlers.sds import (get_process_msg)
from production_line_monitor.core.all_data import (all_data)

date_format = "%Y-%m-%d %H:%M:%S"

'''
 "planId": i["code"],
        "planProduct": i["product"],
        "productCode": i["product_code"],
        "planNum": i["num"],
'''

async def get_plan_info(product_line="product_line_6t90"):
    try:
        logger = get_logger()
        url = get_store().get_dispatched_plan_url() % product_line
        logger.info("get_plan_info url:%s", url)
        res = await get_data(url)
        """
        :[{'plan_no': '11111', 'sequence': 1, 'material_name': 'T901H40ADC12V 4脚 永能标', 'material_code': 'materiel_t901h40adc12v4_ynb', 
        'plan_count': 1000, 'qualified_count': 0, 'unqualified_count': 0}]
        """
        logger.info("get_plan_info data:%s,url:%s",res,url)
        return [{
            "planId":i["plan_no"],
            "sequence":i["sequence"],
            "planProduct":i["material_name"],
            "productCode":i["material_code"],
            "planNum":i["plan_count"]
        } for i in res]
    except Exception as e:
        logger.error("get_plan_info error:%s",e)
        return []

async def get_data(url, data={}):
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


async def get_lastest_data(codelist, timestamp):
    if isinstance(timestamp, str):
        timestamp = datetime.strptime(timestamp, date_format)
    last_timestamp_str = (timestamp - timedelta(days=1)).strftime(date_format)
    end_timestamp_str = timestamp.strftime(date_format)
    get_logger().info("get_lastest_data ~~~~~~~~~~~ end_timestamp_str:%s",end_timestamp_str)
    idi_data_dict = await get_idi_data(codelist, last_timestamp_str, end_timestamp_str)
    value_data_dict = {}
    for code in codelist:
        try:
            if idi_data_dict[code]:
                last_timestamp = max(idi_data_dict[code])
                value_data_dict[code] = idi_data_dict[code].get(last_timestamp, 0)
                get_logger().info("last_timestamp:%s,code:%s,value:%s",last_timestamp,code, idi_data_dict[code])
            else:
                value_data_dict[code] = 0
        except Exception as e:
            value_data_dict[code] = 0
    return value_data_dict


async def get_idi_diff(code, start_time, end_time, idi_data_dict):
    def query_tag_diff(data, code):
        try:
            if data:
                data = {k: v for k, v in data.items() if v is not None}
                return data[max(data)] - data[min(data)]
            else:
                # raise Exception("%s no data" % code)
                return 0
        except Exception as e:
            # raise Exception("%s:%s" % (code, str(e)))
            return 0

    data = idi_data_dict.get(code, {})
    data = {t: v for t, v in data.items() if t >= start_time and t <= end_time}
    return query_tag_diff(data, code)


async def get_process_count_by_plan(process_code, num_code, plan_code, plan_time_range_list, idi_data_dict):
    try:
        logger = get_logger()
        logger.debug("plan_time_range_list~~~~~~~~~~~`:%s", plan_time_range_list)
        total = 0
        for [start_time, end_time] in plan_time_range_list:
            total += await get_idi_diff(num_code, start_time, end_time, idi_data_dict)
            logger.debug("total:%s,start_time:%s,end_time:%s", total, start_time, end_time)
        return total
    except Exception as e:
        get_logger().error("get_process_count_by_plan error:%s", e)
        traceback.print_exc()
        return 0


async def get_process_count_current_day(num_code, timestamp,idi_data_dict):
    if isinstance(timestamp, str):
        timestamp = datetime.strptime(timestamp, date_format)
    today_start_timestamp = datetime(timestamp.year, timestamp.month, timestamp.day)
    start_timestamp_str = today_start_timestamp.strftime(date_format)
    end_timestamp_str = timestamp.strftime(date_format)
    return await get_idi_diff(num_code, start_timestamp_str, end_timestamp_str,idi_data_dict)


def get_finally_process(product_line):
    # 从内存中获取信息
    pipeline_device_in_memory = get_context('pipeline_device')
    target_pipeline_info = pipeline_device_in_memory.get(product_line, {})
    process_seq = []
    for value in target_pipeline_info.values():
        process_info = value.setdefault('process', [])
        for p in process_info:
            process_seq.append({'code': p['code'], 'seq': int(p['sequence'])})
    if process_seq:
        process_seq = sorted(process_seq, key=lambda x: x['seq'])
        return process_seq[-1]['code']
    else:
        return None


def get_percent(v1, v2):
    try:
        rate = float(v1) / float(v2)
        return '%.1f%%' % (rate * 100)
    except Exception as e:
        return "0%"


def get_process_sequence_dict(product_line):
    # 从内存中获取信息
    pipeline_process_in_memory = get_context('pipeline_process')
    return pipeline_process_in_memory.get(product_line, None)


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



# async def get_plan_list_by_process_code(product_line, process_code):
#     logger = get_logger()
#     # plan_code_list = await get_plan_code_list(process_code)
#     plan_info_list = await get_plan_info(product_line)
#     logger.debug("plan_code_list~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", plan_info_list)
#     plan_list =  [{
#         "plan_number": i["planId"],
#         "material_name": i["planProduct"],
#         "material_code": i["productCode"],
#         "plan_count": i["planNum"]
#     } for i in plan_info_list]
#     update_context("plan_list", plan_list)



def get_next_plan(current_plan):
    plan_list = get_context("plan_list")
    plan_code_list = [i["planId"] for i in sorted(plan_list,key=lambda x:x["sequence"])]
    get_logger().debug("get_next_plan ~~~~~~~~~~~~~~~~~~ plan_list:%s",plan_code_list)
    length = len(plan_code_list)
    if not current_plan:
        return plan_code_list[0]
    elif current_plan in plan_code_list:
        index = plan_code_list.index(current_plan)
        if index < length - 1:
            return plan_code_list[index + 1]
    else:
        raise Exception("no next plan")


async def get_positive_and_nagetive_count(product_line, timestamp):
    try:
        logger = get_logger()
        data_collection = {
            "process_quality":{},
            "plan_quality":{},
            "total":{}
        }
        code_map_dict = get_code_map_dict(product_line)[product_line]
        logger.debug("code_map_dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%s", code_map_dict)
        process_msg = get_process_msg()
        positive_code_list = [code_map_dict.get(i["code"], {}).get("positive", None) for i in process_msg if
                              i["code"] in code_map_dict]
        nagetive_code_list = [code_map_dict.get(i["code"], {}).get("nagetive", None) for i in process_msg if
                              i["code"] in code_map_dict]
        num_code_list = []
        num_code_list.extend(positive_code_list)
        num_code_list.extend(nagetive_code_list)
        num_code_list = [i for i in num_code_list if i]
        plan_time_range_dict, first_start_time = await get_plan_time_range(timestamp)
        logger.debug("plan_time_range_dict~~~~~~~~~~~~~~~~~~~~~~~:%s",plan_time_range_dict)
        now = datetime.now().strftime(date_format)
        idi_data_dict = await get_idi_data(num_code_list, first_start_time, now)
        update_context("idi_data_dict", idi_data_dict)
        current_plan_list = all_data["current_plan"]
        process_quality = data_collection["process_quality"]
        plan_quality = data_collection["plan_quality"]
        process_plan_map_dict = {}
        for i in current_plan_list:
            process_plan_map_dict.update({code: i["plan_id"] for code in i["group"]})
        for i in process_msg:
            process_code = i["code"]
            current_plan_code = process_plan_map_dict.get(process_code, None)
            positive_code = code_map_dict.get(process_code, {}).get("positive", None)
            negative_code = code_map_dict.get(process_code, {}).get("negative", None)
            if current_plan_code:
                plan_time_range_list = plan_time_range_dict.get(process_code, {}).get(current_plan_code,[])
                if positive_code:
                    positive_num = await get_process_count_by_plan(process_code, positive_code, current_plan_code,
                                                         plan_time_range_list, idi_data_dict)
                else:
                    positive_num = None
                if negative_code:
                    negative_num = await get_process_count_by_plan(process_code, negative_code, current_plan_code,
                                                         plan_time_range_list, idi_data_dict)
                else:
                    negative_num = None
            else:
                positive_num = 0 if positive_code else None
                negative_num = 0 if negative_code else None
            process_quality[process_code] = {
                "positive_num": positive_num,
                "negative_num": negative_num,
            }
        logger.debug("process_quality~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s",process_quality)
        plan_code_list = [i["planId"] for i in all_data["plan"]]
        finally_process_code = get_finally_process(product_line)
        finally_positive_code = code_map_dict.get(finally_process_code, {}).get("positive", None)
        finally_negative_code = code_map_dict.get(finally_process_code, {}).get("negative", None)
        logger.debug("finally_process_code:%s,finally_positive_code:%s,finally_nagetive_code:%s",finally_process_code,
                    finally_positive_code,finally_negative_code)
        for plan_code in plan_code_list:
            plan_time_range_list = plan_time_range_dict.get(process_code, {}).get(plan_code,[])

            positive_num = await get_process_count_by_plan(finally_process_code, finally_positive_code, plan_code,
                                                 plan_time_range_list, idi_data_dict)

            negative_num = await get_process_count_by_plan(finally_process_code, finally_negative_code, plan_code,
                                                 plan_time_range_list, idi_data_dict)

            plan_quality[plan_code] = {
                "positive_num": positive_num,
                "negative_num": negative_num,
            }
        logger.debug("plan_quality~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", plan_quality)
        total_positive_num = await get_process_count_current_day(finally_positive_code, timestamp,idi_data_dict)
        total_negative_num = await get_process_count_current_day(finally_negative_code, timestamp, idi_data_dict)
        data_collection["total"] = {
            "positive":total_positive_num,
            "negative":total_negative_num
        }
        return data_collection

    except Exception as e:
        traceback.print_exc()
        get_logger().error("get_positive_and_nagetive_count error:%s", e)

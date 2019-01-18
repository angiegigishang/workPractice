from mg_app_framework import HttpClient, get_logger, get_store, get_handler, TaskKey
import urllib
import string
from datetime import datetime, timedelta
import traceback

date_format = "%Y-%m-%d %H:%M:%S"


def get_now_timestamp():
    return datetime.now().strftime(date_format)

def get_day_start_time(timestamp):
    if isinstance(timestamp,str):
        timestamp = datetime.strptime(timestamp,date_format)
    return timestamp.strftime("%Y-%m-%d 00:00:00")

async def get_plan_time_range(timestamp):
    logger = get_logger()
    mongo_handler = get_handler(TaskKey.mongodb)
    plan_collection = mongo_handler.xldq.plan_range
    find_res = plan_collection.find({}).sort("timestamp", 1)
    find_res = [{"plan_code":i["plan_code"],"timestamp":i["timestamp"],"process_code":i["process_code"]} for i in find_res]
    find_res = sorted(find_res,key=lambda x:x["process_code"])
    logger.debug("plan_list~~~~~~~~~~~~~~~~~~~~~~~~~:%s",find_res)
    from itertools import groupby
    res = {}
    first_start_time = get_day_start_time(timestamp)
    for process_code, group in groupby(find_res, lambda p: p['process_code']):
        res.setdefault(process_code,{})
        plan_list = list(group)
        for n, item in enumerate(plan_list):
            plan_code = item["plan_code"]
            process_code = item["process_code"]
            res[process_code].setdefault(plan_code, [])
            start_time = item["timestamp"]
            if start_time < first_start_time:
                first_start_time = start_time
            if n < len(plan_list) - 1:
                end_time = plan_list[n + 1]["timestamp"]
            else:
                end_time = get_now_timestamp()
            res[process_code][plan_code].append([start_time, end_time])
    return res,first_start_time



async def get_current_plan():
    mongo_handler = get_handler(TaskKey.mongodb)
    plan_collection = mongo_handler.xldq.plan_range
    res = plan_collection.find({})
    process_plan_dict = {}
    for i in res:
        process_code = i["process_code"]
        process_plan_dict.setdefault(process_code,[])
        process_plan_dict[process_code].append({"timestamp":i["timestamp"],"plan_code":i["plan_code"]})
    for process_code,plan_list in process_plan_dict.items():
        plan_list = sorted(plan_list,key=lambda x:x["timestamp"],reverse=True)
        process_plan_dict[process_code] = plan_list[0]["plan_code"]
    get_logger().info("get_current_plan process_plan_dict~~~~~~~~~~~~~~~~~~~~~~~~~:%s", process_plan_dict)
    return process_plan_dict


# async def get_plan_info(product_line, plan_code_list=[]):
#     mongo_handler = get_handler(TaskKey.mongodb)
#     plan_info_collection = mongo_handler.xldq.plan_info
#     if plan_code_list:
#         plan_info_list = plan_info_collection.find({
#             "product_line": product_line,
#             "code": {"$in": plan_code_list}
#         })
#     else:
#         plan_info_list = plan_info_collection.find({
#             "product_line": product_line,
#         })
#     return [{
#         "planId": i["code"],
#         "planProduct": i["product"],
#         "productCode": i["product_code"],
#         "planNum": i["num"],
#     } for i in plan_info_list]


async def insert_plan(process_code_list, product_line, plan_code, timestamp):
    try:
        mongo_handler = get_handler(TaskKey.mongodb)
        plan_collection = mongo_handler.xldq.plan_range
        plan_collection.insert_many([{
            "product_line": product_line,
            "plan_code": plan_code,
            "process_code": process_code,
            "timestamp": timestamp} for process_code in process_code_list])
    except Exception as e:
        get_logger().error("insert_plan error:%s", e)
        raise e


async def get_plan_code_list(process_code):
    try:
        mongo_handler = get_handler(TaskKey.mongodb)
        plan_collection = mongo_handler.xldq.plan_range
        plan_list = plan_collection.find({"process_code": process_code}, {'plan_code': True}).distinct("plan_code")
        return plan_list
    except Exception as e:
        get_logger().error("get_plan_code_list error:%s", e)
        raise e

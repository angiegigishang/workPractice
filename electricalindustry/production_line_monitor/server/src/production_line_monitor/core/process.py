from tornado.httpclient import AsyncHTTPClient
import traceback
from tornado.gen import multi
from datetime import datetime

from mg_app_framework import HttpBasicHandler, MesCode, get_handler, TaskKey, get_logger, HttpClient, get_store, \
    update_context, get_context, send_mes

from production_line_monitor.handlers.sds import (
    get_process_msg,
    get_change_process_list,
    get_change_sequence_list,
    get_change_process_dict_list)
from production_line_monitor.util.data_utils import (
    get_lastest_data,
    get_finally_process,
    get_percent,
    get_process_sequence_dict,
    get_process_count_by_plan,
    get_code_map_dict,
    get_process_count_current_day,
    get_next_plan,
    get_positive_and_nagetive_count,
    get_plan_info)

from production_line_monitor.util.query_utils import (
    get_current_plan,
    insert_plan,
    get_now_timestamp,
    get_plan_time_range)
import traceback

date_format = "%Y-%m-%d %H:%M:%S"


async def cron_main():
    try:
        timestamp = get_now_timestamp()
        product_line = get_context("product_line")
        websocket_list = get_context("websocket_list")
        if not product_line:
            product_line = "product_line_6t90"
        all_data = get_context("all_data")
        if not all_data["is_computed"]:
            await get_init_all_data(product_line)
        else:
            all_data["data_collection"] = await get_positive_and_nagetive_count(product_line, timestamp)
        for handler in websocket_list:
            try:
                await send_mes(handler, mes_type="data_collection",
                               data={"data_collection": all_data["data_collection"],
                                     "current_plan": all_data["current_plan"]})
            except Exception as e:
                get_logger().error("send_mes error:%s", e)
    except Exception as e:
        get_logger().error("cron_main error:%s", e)


async def get_init_all_data(product_line):
    try:
        logger = get_logger()
        all_data = get_context("all_data")
        update_context("product_line", product_line)
        timestamp = get_now_timestamp()
        all_data["process_list"] = await get_process_list(product_line, timestamp)
        logger.debug("process_list~~~~~~~~~~~~~~~~~~~~:%s", all_data["process_list"])
        all_data["check_in"] = await get_attendance_data(product_line)
        logger.debug("check_in~~~~~~~~~~~~~~~~~~~~~~~~:%s", all_data["check_in"])
        all_data["plan"] = await get_plan_data(product_line)
        logger.debug("plan~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", all_data["plan"])
        all_data["equipment_status"] = await get_status(product_line, timestamp)
        logger.debug("equipment_status~~~~~~~~~~~~~~~~~~~~~~~~:%s", all_data["equipment_status"])
        all_data["current_plan"] = await get_current_plan_by_group(product_line)
        logger.debug("current_plan~~~~~~~~~~~~~~~~~~~~~~~~:%s", all_data["current_plan"])
        all_data["data_collection"] = await get_positive_and_nagetive_count(product_line, timestamp)
        logger.debug("data_collection~~~~~~~~~~~~~~~~~~~~~~~~:%s", all_data["data_collection"])
        all_data["is_computed"] = True
        return all_data
    except Exception as e:
        traceback.print_exc()
        get_logger().error("get_all_data error:%s", e)


async def get_group_process(product_line):
    logger = get_logger()
    change_process_list = get_change_process_dict_list(product_line)
    change_process_list = sorted(change_process_list, key=lambda x: float(x["sequence"]), reverse=False)
    process_sequence_dict = get_process_sequence_dict(product_line)
    group_dict_list = []
    for item in change_process_list:
        process_code = item["code"]
        process_sequence = item["sequence"]
        process_change_list = get_process_code_list_by_change(product_line, process_sequence, process_sequence_dict)
        group_dict_list.append({"process_code": process_code, "group": process_change_list})
    return group_dict_list


async def get_current_plan_by_group(product_line):
    logger = get_logger()
    process_plan_dict = await get_current_plan()
    group_dict_list = await get_group_process(product_line)
    res_list = []
    id = 1
    for item in group_dict_list:
        change_process_code = item["process_code"]
        group = item["group"]
        plan_code = process_plan_dict.get(change_process_code, "")
        res_list.append({
            "id": id,
            "plan_id": plan_code,
            "group": group,
        })
        id += 1
    return res_list


async def get_attendance_data(product_line):
    try:
        global all_data
        target_url = get_store().get_onwork_attendance_url()
        client = HttpClient(AsyncHTTPClient(max_clients=1000))
        attendance_data = await client.get(target_url.format(product_line), data={})
        get_logger().debug("get_attendance_data~~~~~~~~~~~~~~~~~~~~:%s", attendance_data.data)
        client.close()
        return attendance_data.data
    except Exception as e:
        get_logger().error("get_attendance_data error:%s",e)
        return {}


async def get_process_list(product_line, timestamp):
    try:
        logger = get_logger()
        change_code_list = get_change_process_list(product_line)
        logger.debug("change_code_list~~~~~~~~~~~:%s", change_code_list)
        process_msg = get_process_msg()
        logger.debug("process_msg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%s", process_msg)
        res = []
        for i in process_msg:
            process_code = i["code"]
            res.append({
                "name": i["name"],
                "code": process_code,
                "if_change": True if i["code"] in change_code_list else False,
                "is_manul": True if i["classify"] == "人工" else False,
            })
        return res
    except Exception as e:
        traceback.print_exc()
        get_logger().error("get_process_info error :%s", e)
        raise e


#     "planId": "1811019380",
#     "planProduct": "T901H40ADC12V 4脚 23规格",
#     "productCode": "materiel_t901h40adc12v4_23",
#     "planNum": 4000,

async def get_plan_data(product_line, timestamp=None):
    logger = get_logger()
    plan_list = await get_plan_info(product_line)
    update_context("plan_list", plan_list)
    logger.debug("plan_list~~~~~~~~~~~~~~~~~~~`:%s", plan_list)
    return plan_list


async def get_status(product_line, timestamp):
    logger = get_logger()
    code_map_dict = get_code_map_dict(product_line)[product_line]
    logger.info("code_map_dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%s", code_map_dict)
    process_msg = get_process_msg()
    status_code_list = [code_map_dict.get(i["code"], {}).get("status", None) for i in process_msg if
                        i["code"] in code_map_dict]
    logger.info("status_code_list~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%s", status_code_list)
    status_dict = await get_lastest_data(status_code_list, timestamp)
    return {
        i["code"]: str(status_dict.get(code_map_dict.get(i["code"], {}).get("status", None), '3')) for i in process_msg
    }


def get_process_code_list_by_change(product_line, process_sequence, process_sequence_dict):
    try:
        logger = get_logger()
        change_sequence_list = get_change_sequence_list(product_line)
        change_sequence_list = sorted([i for i in change_sequence_list], key=lambda x: float(x))
        length = len(change_sequence_list)
        index = change_sequence_list.index(process_sequence)
        if index < length - 1:
            process_change_list = [code for code, sequence in
                                   sorted(process_sequence_dict.items(), key=lambda x: float(x[1]))
                                   if float(sequence) >= float(process_sequence) and float(sequence) < float(
                    change_sequence_list[index + 1])]
        else:
            process_change_list = [code for code, sequence in
                                   sorted(process_sequence_dict.items(), key=lambda x: float(x[1]))
                                   if float(sequence) >= float(process_sequence)]
        logger.debug("process_change_list:%s", process_change_list)
        return process_change_list
    except Exception as e:
        get_logger().error("get_process_code_list_by_change error:%s", e)
        return []


async def post_update_plan(next_plan, current_plan):
    try:
        url = get_store().get_update_plan_url()
        all_data = get_context("all_data")
        plan_quality = all_data["data_collection"]["plan_quality"]
        client = HttpClient(AsyncHTTPClient(max_clients=1000))
        data = []
        # if current_plan:
        #     data.append({
        #         "plan_no": current_plan,
        #         "status": 3,  # 2表示进行中，3表示暂停，4表示已完工
        #         "progress_detail":  # 仅更新状态为暂停和已完工时传合格数和不合格数，对于进行中没有这个字段
        #             {
        #                 "qualified_count": plan_quality.get(next_plan,{}).get("positive_num",0),
        #                 "unqualified_count": plan_quality.get(next_plan,{}).get("negative_num",0)
        #             }
        #     }
        #     )
        data.append({
                "plan_no": next_plan,
                "status": 2,  # 2表示进行中，3表示暂停，4表示已完工
                "progress_detail":  # 仅更新状态为暂停和已完工时传合格数和不合格数，对于进行中没有这个字段
                    {
                        "qualified_count": plan_quality.get(next_plan,{}).get("positive_num",0),
                        "unqualified_count": plan_quality.get(next_plan,{}).get("negative_num",0)
                    }
            })
        res = await client.post(url, data=data)
        get_logger().info("post_update_plan data~~~~~~~~~~~~~~~~~~~~:%s", data)
        get_logger().debug("post_update_plan res~~~~~~~~~~~~~~~~~~~~:%s", res)
        client.close()
    except Exception as e:
        get_logger().error("post_update_plan error :%s", e)


async def change_plan(product_line, process_code, timestamp):
    try:
        logger = get_logger()
        process_sequence_dict = get_process_sequence_dict(product_line)
        logger.debug("process_sequence_dict~~~~~~~~~~~~~~~~~~~~~:%s", process_sequence_dict)
        current_plan_dict = await get_current_plan()
        current_plan = current_plan_dict.get(process_code, None)
        logger.info("current_plan~~~~~~~~~~~~~~~~~~~~~:%s", current_plan)
        plan_code = get_next_plan(current_plan)
        try:
            change_sequence_list = get_change_sequence_list(product_line)
            change_sequence_list = sorted([i for i in change_sequence_list], key=lambda x: float(x))
            first_process_code = change_sequence_list[0]["process_code"]
            if first_process_code:
                await post_update_plan(plan_code, current_plan)
        except Exception as e:
            logger.error("change_sequence_list error:%s",e)
        logger.debug("plan_code~~~~~~~~~~~~~~~~~~~~~:%s", plan_code)
        process_sequence = process_sequence_dict[process_code]
        logger.debug("process_sequence~~~~~~~~~~~~~~~~~~~~~:%s", process_sequence)
        process_change_list = get_process_code_list_by_change(product_line, process_sequence, process_sequence_dict)
        logger.debug("process_change_list~~~~~~~~~~~~~~~~~~~~~:%s", process_change_list)
        await insert_plan(process_change_list, product_line, plan_code, timestamp)
        return {process_code: plan_code for process_code in process_change_list}
    except Exception as e:
        traceback.print_exc()
        get_logger().error("change_plan error :%s", e)
        raise e


'''
[
    {
        "plan_number": "",  //计划号
        "material_name": "",  //物料名称
        "material_code": "",  //物料编码
        "plan_count": "",   //计划生产数量
        "total_plan_qualified_count": 100,  //计划总的监控合格数
        "total_plan_unqualified_count": 5,  //计划总的监控不合格数
        "current_qualified_count": 20,  //当前报工工序监测的监控合格数
        "current_unqualified_count": 3,  //当前报工工序监测的的监控不合格数
        "plan_progress": "",     //计划完成进 度百分比
    }
]
"planId":i["plan_no"],
            "sequence":i["sequence"],
            "planProduct":i["material_name"],
            "productCode":i["material_code"],
            "planNum":i["plan_count"]

'''


async def get_product_line_data(product_line, process_code):
    try:
        logger = get_logger()
        timestamp = get_now_timestamp()
        last_process_code = get_finally_process(product_line)
        logger.debug("last_process_code~~~~~~~~~~~~~~~~~~~~~~:%s", last_process_code)
        plan_list = get_context("plan_list")
        logger.info("plan_list~~~~~~~~~~~~~~~~~~~~~~:%s", plan_list)
        code_map_dict = get_code_map_dict(product_line)[product_line]
        all_data = get_context("all_data")
        idi_data_dict = get_context("idi_data_dict")
        plan_quality = all_data["data_collection"]["plan_quality"]
        plan_time_range_dict, first_start_time = await get_plan_time_range(timestamp)
        for item in plan_list:
            plan_code = item["planId"]
            item["plan_number"] = plan_code
            item["material_name"] = item["planProduct"]
            item["material_code"] = item["productCode"]
            item["plan_count"] = item["planNum"]
            positive = plan_quality.get(plan_code,{}).get("positive_num",0)
            negative = plan_quality.get(plan_code,{}).get("negative_num",0)
            progress = get_percent(positive, item["plan_count"])
            item["total_plan_qualified_count"] = positive
            item["total_plan_unqualified_count"] = negative
            item["plan_progress"] = progress
            if process_code in code_map_dict:
                current_positive_code = code_map_dict[process_code].get("positive", None)
                current_negative_code = code_map_dict[process_code].get("negative", None)
                plan_time_range_list = plan_time_range_dict.get(process_code, {}).get(plan_code, [])
                logger.debug("current_positive_code:%s,current_negative_code:%s~~~~~~~~~~~~~~~~~~~~~~",
                             current_positive_code, current_negative_code)
                if current_positive_code:
                    current_positive = await get_process_count_by_plan(process_code, current_positive_code, plan_code, plan_time_range_list, idi_data_dict)
                else:
                    current_positive = None
                if current_negative_code:
                    current_negative = await get_process_count_by_plan(process_code, current_negative_code, plan_code,
                                                                 plan_time_range_list, idi_data_dict)
                else:
                    current_negative = None
                item["current_qualified_count"] = current_positive
                item["current_unqualified_count"] = current_negative
            else:
                item["current_qualified_count"] = None
                item["current_unqualified_count"] = None
        return plan_list
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


async def get_current_day_count(product_line, timestamp):
    logger = get_logger()
    last_process_code = get_finally_process(product_line)
    logger.debug("last_process_code~~~~~~~~~~~~~~~~~~~~~~`:%s", last_process_code)
    code_map_dict = get_code_map_dict(product_line)[product_line]
    positive_code = code_map_dict[last_process_code].get("positive", None)
    if positive_code:
        positive = await get_process_count_current_day(positive_code, timestamp)
    else:
        positive = 0
    negative_code = code_map_dict[last_process_code].get("negative", None)
    if negative_code:
        negative = await get_process_count_current_day(negative_code, timestamp)
    else:
        negative = 0
    return {"total": {
        "positive": positive,
        "negative": negative
    }}

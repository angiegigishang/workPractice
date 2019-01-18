from mg_app_framework import get_logger, idi_send_data, IdiMesType
import traceback

from idi_interface_simulator.util.data_utils import (
    clear_plan_range,
    get_process_code_list,
    get_now_timestamp,
    get_code_map_dict,
    get_idi_lastest_value)

working_code_set = set()


async def cron_main(product_line="product_line_6t90", org="organization_xldq"):
    try:
        logger = get_logger()
        timestamp = get_now_timestamp()
        process_code_list = [code for code in working_code_set]
        logger.info("process_code_list:%s", process_code_list)
        code_map_dict = get_code_map_dict(product_line)[product_line]
        positive_code_list = [code_map_dict.get(code, {}).get("positive", None) for code in process_code_list if
                              code_map_dict.get(code, {}).get("positive", None)]
        status_code_list = [code_map_dict.get(code, {}).get("status", None) for code in process_code_list if
                              code_map_dict.get(code, {}).get("status", None)]
        lastest_value_dict = await get_idi_lastest_value(positive_code_list, timestamp)
        lastest_status_dict = await get_idi_lastest_value(status_code_list, timestamp)
        data = []
        for process_code in process_code_list:
            status_code = code_map_dict.get(process_code, {}).get("status", None)
            logger.info("status_code:%s",status_code)
            logger.info("lastest_status_dict:%s", lastest_status_dict)
            if str(lastest_status_dict.get(status_code,0)) == '3':
                code = code_map_dict.get(process_code, {}).get("positive", None)
                data.append({
                    "code": code,
                    "timestamp": timestamp,
                    "value": int(lastest_value_dict.get(code, 0)) + 1
                })
        logger.info("idi send data:%s,length:%s", {org: data}, len(data))
        await idi_send_data(IdiMesType.idi_tag_data, {org: data})
    except Exception as e:
        traceback.print_exc()
        logger.error("cron_main error:%s", e)


async def set_init(product_line):
    try:
        #
        global working_code_set
        logger = get_logger()
        working_code_set.clear()
        logger.info("set_init working_code_set:%s", working_code_set)
        #
        process_code_list = get_process_code_list(product_line)
        logger.info("process_code_list:%s", process_code_list)
        await change_status(product_line, process_code_list, '0')
        #
        await clear_plan_range(product_line)
    except Exception as e:
        get_logger().error("set_init error:%s", e)
        traceback.print_exc()
        raise e


async def change_status(product_line, process_code_list, status, org="organization_xldq"):
    try:
        logger = get_logger()
        timestamp = get_now_timestamp()
        code_map_dict = get_code_map_dict(product_line)[product_line]
        data = []
        for process_code in process_code_list:
            status_code = code_map_dict.get(process_code, {}).get("status", None)
            if status_code:
                data.append({
                    "code": status_code,
                    "timestamp": timestamp,
                    "value": status
                })
        logger.info("idi send data:%s,length:%s", {org: data}, len(data))
        await idi_send_data(IdiMesType.idi_tag_data, {org: data})
    except Exception as e:
        get_logger().error("change_status error:%s", e)
        traceback.print_exc()
        raise e


async def count_start(process_code_list):
    try:
        global working_code_set
        for code in process_code_list:
            working_code_set.add(code)
        get_logger().info("count_start working_code_set:%s", working_code_set)
    except Exception as e:
        get_logger().error("count error:%s", e)
        traceback.print_exc()
        raise e

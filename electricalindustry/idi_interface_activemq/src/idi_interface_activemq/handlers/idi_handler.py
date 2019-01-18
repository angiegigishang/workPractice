from mg_app_framework import (
    TaskKey, get_logger, get_store, get_handler,
    IdiConfigBasic, IdiAppType, IdiMesType)
import json


class IdiConfig(IdiConfigBasic):
    def get_idi_history_connect_dict(self):
        return {get_store().get_idi_server_wskey(): get_store().get_idi_server_wsurl()}

    def get_idi_realtime_connect_dict(self):
        return {
            get_store().get_kpi_monitor_msg_post_key(): get_store().get_kpi_monitor_msg_post_url(),
            get_store().get_scheduling_instruction_key(): get_store().get_scheduling_instruction_url(),
        }

    def get_idi_app_type(self):
        return IdiAppType.idi_calculation

    def get_mongodb_db_handle(self):
        handle = get_handler(TaskKey.mongodb)
        return handle.idi

    async def idi_msg_process(self, msg):
        logger = get_logger()
        try:
            msg = json.loads(msg)
            logger.info("msg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s",msg)
            if msg['type'] == IdiMesType.idi_init:
                # await  idi_init_msg_process(msg)
                pass
            elif msg['type'] == IdiMesType.idi_mdm_tag_info:
                await  idi_init_msg_process(msg)
            else:
                logger.warning('Invalid message type')
        except Exception as e:
            get_logger().exception(e)


compute_msg = []
device_run_status = []
device_run_time = []
kpi_collection_instruct_status = []
internal_kpi_msg = []
production_report_kpi_msg = []

compute_msg_dict = {}
device_run_status_dict = {}
device_run_time_dict = {}
production_report_kpi_msg_dict = {}


async def idi_init_msg_process(msg):
    global compute_msg
    global compute_msg_dict
    global device_run_status
    global device_run_status_dict
    global device_run_time
    global device_run_time_dict
    global internal_kpi_msg
    global kpi_collection_instruct_status
    global production_report_kpi_msg
    global production_report_kpi_msg_dict
    logger = get_logger()
    logger.info("idi_init_msg_process********************************:%s", msg)
    data = msg["data"]
    logger.info("idi data***************************:%s", data)



    for i in data:
        i_list = i["instance_list"]
        for ii in i_list:
            if ii["code"] == "multi_kpi_production_kpi_cal":
                compute_msg = []
                for iii in ii["children"]:
                    iii_list = iii["instance_list"]
                    for iiii in iii_list:
                        compute_msg.append(iiii)
                compute_msg_dict = {i["code"]: i for i in compute_msg}
                logger.info("compute_msg~~~~~~~~~~~~~~~:%s", compute_msg)
            elif ii["code"] == "multi_kpi_device_running_status_cal":
                device_run_status = []
                for iii in ii["children"]:
                    iii_list = iii["instance_list"]
                    for iiii in iii_list:
                        device_run_status.append(iiii)
                        device_run_status_dict = {i["code"]: i for i in device_run_status}
                logger.info("device_run_status~~~~~~~~~~~~~~~:%s", device_run_status)
            elif ii["code"] == "multi_kpi_device_running_time_cal":
                device_run_time = []
                for iii in ii["children"]:
                    iii_list = iii["instance_list"]
                    for iiii in iii_list:
                        device_run_time.append(iiii)
                        device_run_time_dict = {i["code"]: i for i in device_run_time}
                logger.info("device_run_time~~~~~~~~~~~~~~~:%s", device_run_time)


    # for item in data:
    #     if item["code"] == "multi_kpi_production_kpi_cal":
    #         compute_msg = item["instance_list"]
    #         compute_msg_dict = {i["code"]: i for i in compute_msg}
    #         logger.info("compute_msg~~~~~~~~~~~~~~~:%s", compute_msg)
    #     elif item["code"] == "multi_kpi_production_report_kpi_cal":
    #         production_report_kpi_msg = item["instance_list"]
    #         production_report_kpi_msg_dict = {i["code"]: i for i in production_report_kpi_msg}
    #         logger.info("production_report_kpi_msg:%s", production_report_kpi_msg)
    #     elif item["code"] == "multi_kpi_system_kpi_cal":
    #         internal_kpi_msg = item["instance_list"]
    #         logger.info("internal_kpi_msg:%s", internal_kpi_msg)
    #
    #     elif item["code"] == "multi_kpi_device_running_status":
    #         device_run_status = item["instance_list"]
    #         device_run_status_dict = {i["code"]: i for i in device_run_status}
    #         logger.info("device_run_status:%s", device_run_status)
    #     elif item["code"] == "multi_kpi_operation_instruction_cal":
    #         kpi_collection_instruct_status = item["instance_list"]
    #         logger.info("kpi_collection_instruct_status:%s", kpi_collection_instruct_status)
    #     elif item["code"] == "multi_kpi_device_running_time_cal":
    #         device_run_time = item["instance_list"]
    #         device_run_time_dict = {i["code"]: i for i in device_run_time}


def get_compute_single_msg():
    return compute_msg


def get_production_report_kpi_msg():
    return production_report_kpi_msg


def get_compute_msg():
    res = []
    res.extend(compute_msg)
    res.extend(production_report_kpi_msg)
    return res


def get_compute_msg_dict():
    res = {}
    res.update(compute_msg_dict)
    res.update(production_report_kpi_msg_dict)
    return res


def get_compute_kpi_list():
    _compute_msg = get_compute_msg()
    return [i["code"] for i in _compute_msg]


def get_device_run_status():
    return device_run_status


def get_device_run_status_dict():
    return device_run_status_dict


def get_device_run_status_code_list():
    return [i["code"] for i in device_run_status]


def get_device_run_time():
    return device_run_time


def get_device_run_time_dict():
    return device_run_time_dict


def get_internal_kpi_msg():
    return internal_kpi_msg


def get_internal_kpi_list():
    return [i["code"] for i in internal_kpi_msg]


def get_kpi_collection_instruct_status():
    return kpi_collection_instruct_status

from mg_app_framework import app_start, set_store, set_config_func, set_data_func, set_init_task, TaskKey, set_context,get_logger
from production_line_monitor.config import ConfigStore, MongodbConfig
from production_line_monitor.handlers.sds import SdsConfig
from production_line_monitor.core.all_data import all_data
from production_line_monitor.core.process import (get_init_all_data,cron_main)


async def config_process():
    pass

async def data_process():
    logger = get_logger()
    logger.info("data_process start ~~~~~~~~~~~~")
    await cron_main()

def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    set_data_func(data_process)
    set_context('pipeline_process', {})
    set_context('pipeline_device', {})
    set_context('all_data', all_data)
    set_context("websocket_list",[])
    set_context("idi_data_dict",{})
    set_context("plan_list",[])
    set_init_task([{TaskKey.mongodb: MongodbConfig()}, {TaskKey.sds: SdsConfig()}])
    app_start(debug_flag)

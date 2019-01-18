from mg_app_framework import app_start, set_store, set_config_func, set_data_func, set_init_task,TaskKey,set_context
from idi_interface_simulator.config import ConfigStore

from idi_interface_simulator.config import ConfigStore, MongodbConfig
from idi_interface_simulator.handlers.sds import SdsConfig
from idi_interface_simulator.handlers.idi_handler import (IdiConfig)
from idi_interface_simulator.core.process import cron_main

async def config_process():
    pass

async def data_process():
    await cron_main()


def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    set_context('pipeline_process', {})
    set_context('pipeline_device', {})
    set_data_func(data_process)
    set_init_task([{TaskKey.mongodb: MongodbConfig()}, {TaskKey.sds: SdsConfig()},{TaskKey.idi:IdiConfig()}])

    app_start(debug_flag)

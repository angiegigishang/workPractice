from mg_app_framework import app_start, set_store, set_config_func, set_data_func, set_init_task, TaskKey
from progress_report.config import ConfigStore, MongodbConfig, SdsConfig


async def config_process():
    pass


def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    set_init_task([{TaskKey.mongodb_async:MongodbConfig()}, {TaskKey.sds:SdsConfig()}])
    app_start(debug_flag)

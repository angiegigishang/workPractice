from mg_app_framework import app_start, set_store, set_config_func, set_init_task, TaskKey, set_context, get_logger
from wage_settlement.config import ConfigStore, MongoConfigStore
from wage_settlement.sds_config import SdsConfig


async def config_process():
    # get_logger().info("*" * 20)
    pass

def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    set_context('person_code_name_mapper', {})
    set_context('materiel_group_info', [])
    set_context('process_info', [])
    set_context('group_info', [])
    set_context('timely_wage_info', {})
    set_init_task([{TaskKey.mongodb: MongoConfigStore()}, {TaskKey.sds: SdsConfig()}])

    app_start(debug_flag)

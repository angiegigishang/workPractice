from mg_app_framework import app_start, set_store, set_config_func, set_data_func, set_init_task, TaskKey, set_context
from attendance_manage.config import ConfigStore

from attendance_manage.config import MongoConfigStore
from attendance_manage.sds_config import SdsConfig


async def config_process():
    pass


def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    # attendance_info用于在内存中保存产线出勤信息
    set_context('attendance_info', {})
    set_context('mdm_group_info',{})
    set_context('process_threshold', {})
    set_context('person_info', [])
    set_init_task([{TaskKey.mongodb: MongoConfigStore()}, {TaskKey.sds: SdsConfig()}])

    app_start(debug_flag)

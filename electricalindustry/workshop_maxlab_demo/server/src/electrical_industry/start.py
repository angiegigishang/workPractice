from mg_app_framework import app_start, set_store, set_config_func, set_init_task
from electrical_industry.config import ConfigStore


async def config_process():
    pass


def main(debug_flag=True):
    set_store(ConfigStore())
    set_config_func(config_process)
    set_init_task([])

    app_start(debug_flag)

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





async def idi_init_msg_process(msg):
    pass



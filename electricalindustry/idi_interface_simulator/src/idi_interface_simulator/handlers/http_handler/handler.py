from mg_app_framework import HttpBasicHandler, MesCode,get_logger
from idi_interface_simulator.core.process import (
    set_init,
    change_status,
    count_start)
from idi_interface_simulator.util.data_utils import (send_change_flag,send_reset_flag)



class SetHandler(HttpBasicHandler):
    async def get_process(self,product_line):
        try:
            num_data = {}
            await set_init(product_line)
            await send_reset_flag(product_line)
            self.send_response_data(MesCode.success, num_data, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


class ChangeStatusHandler(HttpBasicHandler):
    async def post_process(self):
        try:
            num_data = {}
            product_line = self.data["product_line"]
            process_code_list = self.data["process_code_list"]
            status = self.data["status"]
            get_logger().info("product_line:%s,process_code_list:%s,status:%s",product_line,process_code_list,status)
            await change_status(product_line,process_code_list,status)
            await send_change_flag(product_line,process_code_list,status)
            self.send_response_data(MesCode.success, num_data, 'success get data')
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_response_data(MesCode.fail, {}, str(e))


class CountHandler(HttpBasicHandler):
    async def post_process(self):
        try:
            num_data = {}
            product_line = self.data["product_line"]
            process_code_list = self.data["process_code_list"]
            await count_start(process_code_list)
            #await send_change_flag(product_line)
            self.send_response_data(MesCode.success, num_data, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


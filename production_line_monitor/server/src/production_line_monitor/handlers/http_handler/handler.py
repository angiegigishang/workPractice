from tornado.httpclient import AsyncHTTPClient

from mg_app_framework import HttpBasicHandler, MesCode, get_logger, HttpClient, get_store, send_mes, get_context

from datetime import datetime
from production_line_monitor.core.process import (
    get_product_line_data,
    get_plan_data,
    change_plan,
    get_current_day_count,
    get_init_all_data,
    get_current_plan_by_group,
    get_status)
from production_line_monitor.util.data_utils import (get_positive_and_nagetive_count)
import time
import json
# from production_line_monitor.handlers.websocket_handler.handler import (get_websocket_list)

from production_line_monitor.util.query_utils import (get_now_timestamp)


class AllDataHandler(HttpBasicHandler):
    async def get_process(self, product_line):
        try:
            t1 = time.time()
            all_data = get_context("all_data")
            # if all_data.get("is_computed"):
            #     num_data = all_data
            # else:
            num_data = await get_init_all_data(product_line)
            get_logger().info("all data time:%s", time.time() - t1)
            self.send_response_data(MesCode.success, num_data, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


class ChangePlanHandler(HttpBasicHandler):
    async def get_process(self, product_line, process_code):
        try:
            timestamp = get_now_timestamp()
            await change_plan(product_line, process_code, timestamp)
            all_data = get_context("all_data")
            all_data["current_plan"] = await get_current_plan_by_group(product_line)
            all_data["data_collection"] = await get_positive_and_nagetive_count(product_line, timestamp)
            websocket_list = get_context("websocket_list")
            for handler in websocket_list:
                try:
                    await send_mes(handler, mes_type="data_collection",
                                   data={"data_collection": all_data["data_collection"],
                                         "current_plan": all_data["current_plan"]})
                except Exception as e:
                    get_logger().error("send_mes error:%s", e)
            self.send_response_data(MesCode.success, {}, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


class ProductLineHandler(HttpBasicHandler):
    async def get_process(self, product_line, process_code):
        try:
            num_data = await get_product_line_data(product_line, process_code)
            self.send_response_data(MesCode.success, num_data, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))

    async def post_process(self, product_line, process_code):
        await self.get_process(product_line, process_code)


class ReceiveHandler(HttpBasicHandler):
    async def post_process(self, product_line):
        try:
            timestamp = get_now_timestamp()
            msg_type = self.data.get("msg_type", None)

            all_data = get_context("all_data")
            websocket_list = get_context("websocket_list")
            if msg_type == "status":
                process_code_list = self.data["process_code_list"]
                status = self.data["status"]
                get_logger().info("receive~~~~~~~~~~~~~~~~~~~~~~~~~~~~~msg_type:%s,process_code_list:%s,status:%s", msg_type,process_code_list,status)
                get_logger().debug("equipment_status~~~~~~~~~~~~~~~~~~~~~~~```%s", all_data["equipment_status"])
                all_data["equipment_status"].update({code: str(status) for code in process_code_list})
                get_logger().debug("equipment_status~~~~~~~~~~~~~~~~~~~~~~~```%s", all_data["equipment_status"])
                get_logger().debug("websocket_handlers:%s", websocket_list)
                for handler in websocket_list:
                    try:
                        await send_mes(handler, mes_type="equipment_status", data=all_data["equipment_status"])
                    except Exception as e:
                        get_logger().error("send_mes error:%s", e)
            elif msg_type == "reset":
                all_data["equipment_status"] = await get_status(product_line, timestamp)
                all_data["current_plan"] = await get_current_plan_by_group(product_line)
                all_data["data_collection"] = await get_positive_and_nagetive_count(product_line, timestamp)
                for handler in websocket_list:
                    try:
                        await send_mes(handler, mes_type="all", data=all_data)
                    except Exception as e:
                        get_logger().error("send_mes error:%s", e)
            self.send_response_data(MesCode.success, {}, 'success get data')
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_response_data(MesCode.fail, {}, str(e))


class ReceiveCheckInHandler(HttpBasicHandler):
    async def post_process(self, product_line):
        try:
            get_logger().info("receive checkin data:%s", self.data)
            all_data = get_context("all_data")
            all_data["check_in"] = {"checkinInfo": self.data["checkinInfo"]}
            websocket_list = get_context("websocket_list")
            get_logger().debug("websocket_handlers:%s", websocket_list)
            for handler in websocket_list:
                try:
                    await send_mes(handler, mes_type="check_in", data=all_data["check_in"])
                except Exception as e:
                    get_logger().error("send_mes error:%s", e)
            self.send_response_data(MesCode.success, {}, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


class ReceivePlanHandler(HttpBasicHandler):
    async def post_process(self, product_line):
        try:
            plan_list = json.loads(self.request.body)
            get_logger().info("receive plan data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", plan_list)
            self.send_response_data(MesCode.success, {}, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, {}, str(e))


class SectionsHandler(HttpBasicHandler):
    async def get_process(self, product_line):
        try:
            target_url = get_store().get_onwork_attendance_url()
            client = HttpClient(AsyncHTTPClient(max_clients=1000))
            attendance_data = await client.get(target_url.format(product_line), data={})
            client.close()
            attendance_response = attendance_data.data
            self.send_response_data(MesCode.success, attendance_response, 'success get data')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))

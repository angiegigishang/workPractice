from mg_app_framework import WebsocketBasicHandler, send_mes, get_logger,get_context
from tornado.gen import multi

from production_line_monitor.util.query_utils import (get_now_timestamp)
from tornado.gen import sleep
import json


class WebHandler(WebsocketBasicHandler):
    async def open(self):
        websocket_list = get_context("websocket_list")
        websocket_list.append(self)

    async def on_message(self, message):
        # all_data = get_context("all_data")
        # await send_mes(self, mes_type="all", data=all_data)
        pass

    def on_close(self):
        websocket_list = get_context("websocket_list")
        websocket_list.remove(self)

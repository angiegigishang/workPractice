import paho.mqtt.client as paho
import json
from mg_app_framework import HttpClient, get_store, get_logger,idi_send_data,IdiMesType
from idi_interface_activemq.handlers.sds import get_tag_map_dict
from datetime import datetime
from tornado.ioloop import IOLoop
import asyncio
import traceback
from tornado.gen import sleep
import urllib
import string
from idi_interface_activemq.util.data_util import (get_status_code_map)
# import requests
date_format = "%Y-%m-%d %H:%M:%S"

'''
{'test_factory1': [{'timestamp': '2018-11-28 11:41:22', 'code': 'opc_test0', 'value': 1}], 
'''

def timstamp_to_str(timstamp):
    return datetime.fromtimestamp(timstamp).strftime(date_format)

async def send_data():
    # global q
    # message = q.get()
    await sleep(2)
    print("send ~~~~~~~~~~~~~~~~~~~~`")
    data = {'organization_xldq': [{'code': 'test', 'value': 0, 'timestamp': '2018-12-27 17:38:56'}]}
    await idi_send_data(IdiMesType.idi_tag_data, data)
    print("end~~~~~~~~~~~~~~~~~~~~~~~~~~~`")

async def send_change_flag(product_line,process_code_list,status):
    try:
        client = HttpClient()
        url = "http://127.0.0.1:8989/api/monitor/recevie/%s" %product_line
        url = urllib.parse.quote(url, safe=string.printable)
        data = {
            "msg_type":"status",
            "status":status,
            "process_code_list":process_code_list
        }
        res = await client.post(url,data)
        get_logger().info("send_change_flag,data:%s,res~~~~~~~~~~~~~~~~~~~~~~~~~~:%s",data,res)
        return True
    except Exception as e:
        get_logger().info("send_change_flag error~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", e)

async def post_data(message):
    logger = get_logger()
    # logger.info("start post_data~~~~~~~~~~~~~~~~~~~~~~")
    product_line = "product_line_6t90"
    try:
        url = get_store().get_idi_server_wsurl()
        tag_map_dict = get_tag_map_dict()
        value = message["value"]
        timestamp = timstamp_to_str(message["ts"])
        code = tag_map_dict[message["tag"]]
        status_map_dict = get_status_code_map(product_line)
        logger.info("status_map_dict~~~~~~~~~~~~~~~~~~~~~~~:%s",status_map_dict)
        if code in status_map_dict:
            process_code = status_map_dict[code]
            await send_change_flag(product_line, [process_code], value)
        logger.debug("tag_map_dict:%s",tag_map_dict)
        data_dict = {
            "code": code ,
            "value": value,
            "timestamp": timestamp ,
        }
        try:
            data = {
                "organization_xldq": [data_dict]
            }
            logger.info("post data~~~~~~~~:%s,url:%s",data,url)
            await idi_send_data(IdiMesType.idi_tag_data,data)
        except Exception as e:
            traceback.print_exc()
            logger.error("post data error,message:%s,error:%s", message, e)
        # try:
        #     await send_real_data(data_dict)
        #     pass
        # except Exception as e:
        #     logger.error("send real data error,message:%s,error:%s", data_dict, e)
    except Exception as e:
        logger.error("post data error,message:%s,error:%s",message,e)

async def send_real_data(data_dict,org="organization_xldq"):
    logger = get_logger()

    try:
        url = get_store().get_kpi_monitor_msg_post_url()
        client = HttpClient()
        data = {
            "kpi_realtime":{"data":[data_dict],"org":org},
        }
        # logger.info("send real_data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:%s", data)
        res = await client.post(url,data=data)
        # logger.info("send_real_data res:%s",res)
    except Exception as e:
        logger.error("send real data error,message:%s,error:%s", data_dict, e)


def on_message(conn, userdata, message):
    try:
        message = json.loads(message.payload, encoding="utf-8")
        get_logger().info("received message~~~~~~:%s", message)
        loop = asyncio.new_event_loop()
        # 执行coroutine
        loop.run_until_complete(post_data(message))
        loop.close()
        # IOLoop.current().spawn_callback(post_data,message)
    except Exception as e:
        get_logger().error("received message error:%s",e)


class SubMqtt:
    def __init__(self, broker, topic, client):
        self.broker = broker
        self.topic = topic
        self.client = client
        self.conn = paho.Client(client)

    def __del__(self):
        self.disconnect()

    def connect(self):
        # Bind function to callback
        self.conn.on_message = on_message
        self.conn.connect(self.broker)  # connect default 1883
        self.conn.subscribe(self.topic)  # subscribe
        # self.conn.loop_forever()
        self.conn.loop_start()

    def disconnect(self):
        self.conn.disconnect()  # disconnect
        self.conn.loop_stop()  # stop loop

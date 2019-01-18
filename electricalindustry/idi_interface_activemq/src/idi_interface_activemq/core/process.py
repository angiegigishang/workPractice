import sys
import time
from idi_interface_activemq.util.submqtt import SubMqtt,send_data
from tornado.gen import sleep


async def process_main():
    submqtt = SubMqtt('125.124.23.181', 'xlgf','client1')
    submqtt.connect()
    # await send_data()
    while True:
        await sleep(0.1)


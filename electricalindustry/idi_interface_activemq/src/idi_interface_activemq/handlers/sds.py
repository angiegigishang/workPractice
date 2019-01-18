from mg_app_framework import get_logger, SdsConfigBasic, TaskKey, get_handler,unpack_consume_key,get_context


'''
sds_info:{"key":"","info":[]}
'''

point_msg = []
tag_map_dict = {}



def my_msg_process(data):
    for msg in data:
        _,ori_key = unpack_consume_key(msg["key"])
        msg_handler[ori_key](msg['data'])



def point_handler(msg):
    global point_msg
    global tag_map_dict
    point_msg = msg["instance_list"]
    tag_map_dict = {i["identifier"]:i["code"] for i in point_msg}
    get_logger().info("tag_map_dict : %s" % msg)


def device_handler(msg):
    get_logger().info('init pipeline device info')
    get_logger().info(msg)
    if msg:
        msg = msg[0]['children'][0]
        pipeline_device_in_memory = get_context('pipeline_device')
        for pipeline_info in msg.setdefault('instance_list', []):
            get_logger().debug(pipeline_info)
            pipeline_code = pipeline_info['code']
            device_info = pipeline_info['children'][0].setdefault('instance_list', [])
            get_logger().debug(device_info)
            pipeline_device = {}
            for d in device_info:
                device_code = d['code']
                deivce_data_mapper = {}
                for i in d.setdefault('children', []):
                    # 此处将设备下面挂载的所有类型数据放入内存，后边可能会用到
                    i_type = i['class_code']
                    i_data = i.setdefault('instance_list', [])
                    deivce_data_mapper.update({
                        i_type: i_data
                    })
                pipeline_device.update({device_code: deivce_data_mapper})
            pipeline_device_in_memory.update({
                pipeline_code: pipeline_device
            })
            get_logger().info(pipeline_device_in_memory)
            get_logger().info('pipeline:{} device info inited'.format(pipeline_code))


msg_handler = {
    "point":point_handler,
    "cxjk_cxsb": device_handler,
}
my_consume_list = list(msg_handler.keys())


# my_produce_list = [{'key': 'kpi_realtime', 'data': kpi_realtime_handler()}]


class SdsConfig(SdsConfigBasic):
    def get_consume_list(self):
        return my_consume_list

    def get_produce_list(self):
        return []

    async def msg_process(self, data):
        my_msg_process(data)

    def get_organization_code(self):
        return "organization_xldq"


def get_point_msg():
    return point_msg

def get_tag_map_dict():
    return tag_map_dict





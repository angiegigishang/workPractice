from mg_app_framework import get_logger, SdsConfigBasic, TaskKey, get_handler, unpack_consume_key, get_context

'''
sds_info:{"key":"","info":[]}
'''

process_msg = []
change_process_dict = {}


def my_msg_process(data):
    for msg in data:
        _, ori_key = unpack_consume_key(msg["key"])
        msg_handler[ori_key](msg['data'])


def process_handler(msg):
    global process_msg
    # global tag_map_dict
    process_msg = msg["instance_list"]
    get_logger().info("process_msg : %s" % process_msg)


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


def pipeline_process_handler(msg):
    get_logger().info('init pipeline process info')
    get_logger().debug(msg)
    if msg:
        msg = msg[0]['children'][0]
        pipeline_process_in_memory = get_context('pipeline_process')
        for pipeline_info in msg.setdefault('instance_list', []):
            get_logger().debug(pipeline_info)
            pipeline_code = pipeline_info['code']
            process_info = pipeline_info['children'][0].setdefault('instance_list', [])
            get_logger().debug(process_info)
            pipeline_process = {}
            for x in process_info:
                pipeline_process.update({
                    x['code']: x['sequence']
                })
            pipeline_process_in_memory.update({
                pipeline_code: pipeline_process
            })
            get_logger().info('pipeline:{} process info inited'.format(pipeline_code))


def hxd_handler(msg):
    get_logger().debug('hxd_handler msg~~~~~~~~~~~~~~~~~~~:%s ',msg)
    global change_process_dict
    line_list = msg[0]["children"][0]["instance_list"]
    for line in line_list:
        product_line = line["code"]
        change_process_dict.setdefault(product_line,[])
        process_list = line["children"][0]["instance_list"]
        for process in process_list:
            change_process_dict[product_line].append(process["code"])
    get_logger().info('change_process_dict ~~~~~~~~~~~~~~~~~~~:%s ', change_process_dict)


msg_handler = {
    "process": process_handler,
    "cxjk_cxsb": device_handler,
    'cxjk_cxgx': pipeline_process_handler,
    "cxjk_hxd":hxd_handler,
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


def get_process_msg():
    return process_msg

def get_change_process_list(product_line):
    return change_process_dict[product_line]

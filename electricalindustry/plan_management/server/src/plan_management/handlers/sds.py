from mg_app_framework import get_logger, unpack_consume_key
from plan_management.handlers.utils import log_exception

# 所有从主数据sds获取到的计划管理相关配置
__workshop_pl_config = None
__material_config = None
__custom_field_config = None


async def plan_sds_msg_processor(data):
    try:
        for msg in data:
            organization_code, original_key = unpack_consume_key(msg['key'])
            # get_logger().info('current key is: {}'.format(msg['key']))
            # get_logger().info('current organization code is: {}'.format(organization_code))
            if original_key in plan_msg_handler:
                await plan_msg_handler[original_key](msg['data'])
    except Exception as e:
        log_exception(e, '处理sds消息异常')


async def plan_pl_msg_handler(msg_data):
    global __workshop_pl_config
    # get_logger().info("plan productline msg : {}".format(msg_data))
    __workshop_pl_config = set_plan_pl_config(msg_data)
    get_logger().info('plan productline config: {}'.format(__workshop_pl_config))


def set_plan_pl_config(msg_data):
    pl_config = dict()
    root_dir_children = msg_data[0]['children']
    if root_dir_children:
        # 获取车间节点
        workshop_node = root_dir_children[0]
        for workshop_instance in workshop_node['instance_list']:
            workshop_code = workshop_instance['code']
            workshop_name, workshop_description = workshop_instance['name'], workshop_instance['description']
            pl_config[workshop_code] = {'workshop_name': workshop_name, 'workshop_description': workshop_description, 'pl_data': {}}
            # 获取产线节点
            if workshop_instance['children']:
                pl_node = workshop_instance['children'][0]
                if pl_node:
                    pl_instance_list = pl_node['instance_list']
                    if pl_instance_list:
                        for pl_instance in pl_instance_list:
                            pl_code = pl_instance['code']
                            del pl_instance['children']
                            pl_config[workshop_code]['pl_data'][pl_code] = pl_instance
    return pl_config


def get_plan_pl_config():
    return __workshop_pl_config


def get_workshop_name_code_dict():
    global __workshop_pl_config
    workshop_name_code_dict = dict()
    if __workshop_pl_config:
        for workshop_code, workshop_data_dict in __workshop_pl_config.items():
            workshop_name = workshop_data_dict['workshop_name']
            workshop_name_code_dict[workshop_name] = workshop_code
    return workshop_name_code_dict


async def material_msg_handler(msg_data):
    global __material_config
    # get_logger().info("material msg : {}".format(msg_data))
    __material_config = msg_data['instance_list']
    get_logger().info('material config: {}'.format(__material_config))


def get_material_config():
    return __material_config


# 获取物料编号和编码的映射字典，ERP传过来的material_code表示物料编号，需要转成主数据编码
def get_material_id_code_dict():
    global __material_config
    material_id_code_dict = dict()
    if __material_config:
        for material_data in __material_config:
            material_identifier = material_data['identifier']
            material_code = material_data['code']
            material_id_code_dict[material_identifier] = material_code
    return material_id_code_dict


async def custom_field_msg_handler(msg_data):
    global __custom_field_config
    __custom_field_config = dict()
    # get_logger().info("custom fields msg : {}".format(msg_data))
    if msg_data[0]['children']:
        custom_field_node = msg_data[0]['children'][0]
        custom_field_class_code = custom_field_node['class_code']
        custom_field_instance_list = custom_field_node['instance_list']
        if custom_field_instance_list:
            for custom_field in custom_field_instance_list:
                field_name, field_code = custom_field['name'], custom_field['code']
                field_code_index = len(custom_field_class_code) + 1
                field_code = field_code[field_code_index:]
                __custom_field_config[field_code] = field_name
    get_logger().info('custom field config: {}'.format(__custom_field_config))


def get_custom_field_config():
    return __custom_field_config


plan_msg_handler = {'workshop_pl_info': plan_pl_msg_handler, 'material': material_msg_handler, 'dz_field_info': custom_field_msg_handler}
plan_msg_keys = list(plan_msg_handler.keys())

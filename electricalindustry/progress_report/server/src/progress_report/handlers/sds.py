from mg_app_framework import get_logger, unpack_consume_key
from progress_report.handlers.utils import log_exception

# 所有从主数据sds获取到的报工相关配置
__person_config = None
__group_config = None
__report_point_config = None


async def report_sds_msg_processor(data):
    try:
        for msg in data:
            organization_code, original_key = unpack_consume_key(msg['key'])
            # get_logger().info('current key is: {}'.format(msg['key']))
            # get_logger().info('current organization code is: {}'.format(organization_code))
            if original_key in report_msg_handler:
                await report_msg_handler[original_key](msg['data'])
    except Exception as e:
        log_exception(e, '处理sds消息异常')


# async def person_msg_handler(msg_data):
#     global __person_config
#     # get_logger().info("person msg : {}".format(msg_data))
#     __person_config = set_person_config(msg_data)
#     get_logger().info('person config: {}'.format(__person_config))
#
#
# def set_person_config(msg_data):
#     person_config = dict()
#     person_instance_list = msg_data['instance_list']
#     if person_instance_list:
#         for person_instance in person_instance_list:
#             person_code = person_instance['code']
#             person_config[person_code] = person_instance
#     return person_config
#
#
# def get_person_config():
#     return __person_config


async def report_group_msg_handler(msg_data):
    global __group_config
    # get_logger().info("report group msg : {}".format(msg_data))
    __group_config = set_group_config(msg_data)
    get_logger().info('group config: {}'.format(__group_config))


def set_group_config(msg_data):
    group_config = dict()
    # 用于组间根据工序序号排序
    group_seq_dict = dict()
    root_dir_children = msg_data[0]['children']
    if root_dir_children:
        # 获取产线节点
        product_line_node = root_dir_children[0]
        for product_line_instance in product_line_node['instance_list']:
            product_line_code = product_line_instance['code']
            group_config[product_line_code] = dict()
            # 获取分组节点
            group_node = product_line_instance['children'][0]
            if group_node:
                group_instance_list = group_node['instance_list']
                if group_instance_list:
                    for group_instance in group_instance_list:
                        group_code = group_instance['code']
                        group_name = group_instance['name']
                        group_config[product_line_code][group_code] = {'group_name': group_name}
                        group_detail_list = group_instance['children']
                        # 获取每个分组下工序和人员的信息
                        if group_detail_list:
                            for group_detail in group_detail_list:
                                detail_class_code = group_detail['class_code']
                                detail_list = group_detail['instance_list']
                                if detail_list:
                                    group_config[product_line_code][group_code][detail_class_code] = []
                                    if detail_class_code == 'process':
                                        # 随便取一个工序编码
                                        group_seq_dict[group_code] = detail_list[0]['sequence']
                                    for detail_info in detail_list:
                                        # 移除多余的children字段
                                        del detail_info['children']
                                        group_config[product_line_code][group_code][detail_class_code].append(detail_info)
                    if group_seq_dict:
                        seq_count = 0
                        ordered_group_list = [k[0] for k in sorted(group_seq_dict.items(), key=lambda x: int(x[1]))]
                        for group in ordered_group_list:
                            seq_count += 1
                            group_config[product_line_code][group]['seq'] = seq_count
    return group_config


def get_group_config():
    return __group_config


async def report_point_msg_handler(msg_data):
    global __report_point_config
    # get_logger().info("report point msg : {}".format(msg_data))
    __report_point_config = set_report_point_config(msg_data)
    get_logger().info('report point config: {}'.format(__report_point_config))


def set_report_point_config(msg_data):
    report_point_config = dict()
    root_dir_children = msg_data[0]['children']
    if root_dir_children:
        product_line_node = root_dir_children[0]
        for product_line_instance in product_line_node['instance_list']:
            product_line_code = product_line_instance['code']
            report_point_config[product_line_code] = []
            if product_line_instance['children']:
                report_point_list = product_line_instance['children'][0]['instance_list']
                if report_point_list:
                    for report_point_process in report_point_list:
                        process_code = report_point_process['code']
                        report_point_config[product_line_code].append(process_code)
    return report_point_config


def get_report_point_config():
    return __report_point_config


report_msg_handler = {'bg_fz': report_group_msg_handler, 'bg_gx': report_point_msg_handler}
report_msg_keys = list(report_msg_handler.keys())

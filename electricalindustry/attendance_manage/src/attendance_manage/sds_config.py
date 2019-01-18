from mg_app_framework import get_context, get_logger, SdsConfigBasic, get_handler, TaskKey, send_msg_to_sds, \
    unpack_consume_key, update_context

from attendance_manage.handlers.http_handler.common import sync_group_info
from attendance_manage.process.db_operator import get_target_mongo_collection


async def my_msg_process(data):
    for msg in data:
        _, origin_sds_key = unpack_consume_key(msg['key'])
        process_func = msg_consume_handler.setdefault(origin_sds_key, None)
        if process_func:
            await process_func(msg['data'])


async def init_product_line_info(msg):
    # 初始化所有产线信息
    get_logger().info('产线信息同步')
    get_logger().info(msg)

    # 更新库中数据
    col = get_target_mongo_collection('product_line')
    product_line_info = msg.setdefault('instance_list', [])
    all_product_line_code = []
    for p in product_line_info:
        all_product_line_code.append(p['code'])
        col.update({'code': p['code']}, {'$set': p}, upsert=True)

    # 移除多余产线信息
    col.remove({'code': {'$nin': all_product_line_code}})


async def init_person_info(msg):
    # 初始化所有人员信息
    get_logger().info('人员信息同步')
    get_logger().info(msg)

    code_2_name = []
    people = msg['instance_list']
    for each in people:
        person = {}
        person.update({
            'code': each['code'],
            'name': each['name']
        })
        code_2_name.append(person)
    update_context('person_info', code_2_name)
    # 更新库中数据
    col = get_target_mongo_collection('person')
    person_info = msg.setdefault('instance_list', [])
    all_person_code = []
    for p in person_info:
        all_person_code.append(p['code'])
        col.update({'code': p['code']}, {'$set': p}, upsert=True)

    # 在主数据上移除人员信息之后，此处先不做操作，避免出现人员工资计算问题


async def init_process_info(msg):
    # 初始化工序信息
    get_logger().info('工序信息同步')
    get_logger().info(msg)

    # 更新库中数据
    col = get_target_mongo_collection('process')
    process_info = msg.setdefault('instance_list', [])
    all_process_info_code = []
    for p in process_info:
        all_process_info_code.append(p['code'])
        col.update({'code': p['code']}, {'$set': p}, upsert=True)

    # 此处不做删除数据操作


async def init_fz_info(msg):
    # 初始化考勤分组
    get_logger().info('考勤分组数据同步')
    get_logger().info(msg)
    update_context('mdm_group_info', msg)

    # 更新数据库中数据
    sync_group_info(msg)


async def init_process_number(msg):
    # 初始化工序人数信息
    get_logger().info('工序点亮信息同步')
    get_logger().info(msg)

    person_col = get_target_mongo_collection('process')

    if msg:
        msg = msg[0]['children'][0]
        for threshold_info in msg.setdefault('instance_list', []):
            threshold_value = int(threshold_info['name'])
            process_list = threshold_info['children'][0].setdefault('instance_list', [])
            process_codes = [x['code'] for x in process_list]
            # 更新库中数据
            person_col.update_many({'code': {'$in': process_codes}}, {'$set': {'threshold_person_number': threshold_value}})


msg_consume_handler = {
    'product_line': init_product_line_info,
    'person': init_person_info,
    'process': init_process_info,
    'plan_kq': init_process_number,
    'kq_fz': init_fz_info,
}

my_consume_list = list(msg_consume_handler.keys())


class SdsConfig(SdsConfigBasic):
    def init_produce(self):
        return []

    def get_consume_list(self):
        return my_consume_list

    def get_organization_code(self):
        return 'organization_xldq'

    def get_produce_list(self):
        return self.init_produce()

    async def msg_process(self, data):
        await my_msg_process(data)

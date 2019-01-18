from mg_app_framework import get_context, get_logger, SdsConfigBasic, get_handler, TaskKey, send_msg_to_sds, \
    unpack_consume_key, update_context

from wage_settlement.process.sds_init import sync_materiel_group, sync_group_info, sync_timely_wage_info
from wage_settlement.process.db_operator import get_target_mongo_collection

async def my_msg_process(data):
    for msg in data:
        _, origin_sds_key = unpack_consume_key(msg['key'])
        process_func = msg_consume_handler.setdefault(origin_sds_key, None)
        if process_func:
            await process_func(msg['data'])


async def init_product_line_info(msg):
    # 初始化所有产线信息
    get_logger().info('产线信息同步')
    get_logger().debug(msg)

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
    get_logger().debug(msg)

    name_code_mapper = {}
    # 更新库中数据
    col = get_target_mongo_collection('person')
    person_info = msg.setdefault('instance_list', [])
    all_person_code = []
    for p in person_info:
        all_person_code.append(p['code'])
        col.update({'code': p['code']}, {'$set': p}, upsert=True)
        name_code_mapper.update({
            p['code']: p['name']
        })

    # 更新内存人员code/name映射
    update_context('person_code_name_mapper', name_code_mapper)
    # 在主数据上移除人员信息之后，此处先不做操作，避免出现人员工资计算问题


async def init_process_info(msg):
    # 初始化工序信息
    get_logger().info('工序信息同步')
    get_logger().debug(msg)

    # 更新库中数据
    col = get_target_mongo_collection('process')
    process_info = msg.setdefault('instance_list', [])
    all_process_info_code = []
    for p in process_info:
        all_process_info_code.append(p['code'])
        col.update({'code': p['code']}, {'$set': p}, upsert=True)
    update_context('process_info', process_info)
    # 此处不做删除数据操作


async def init_bg_info(msg):
    # 初始化报工分组
    get_logger().info('报工分组数据同步')
    get_logger().info(msg)

    # 更新数据库中数据
    sync_group_info(msg)


async def init_materiel_group_info(msg):
    # 同步物料分组信息
    get_logger().info('物料分组数据同步')
    get_logger().debug(msg)

    sync_materiel_group(msg)

async def init_timely_wage_info(msg):
    # 同步计时工资分组信息
    get_logger().info('计时工资数据同步')
    get_logger().info(msg)

    sync_timely_wage_info(msg)

    # 更新库中信息
    col = get_target_mongo_collection('timely_wage')

    refreshed_timely_wage_info = get_context('timely_wage_info')
    for k,v in refreshed_timely_wage_info.items():
        person_code = k
        wage_type = v
        # 删除该员工现有的计费模式并更新
        col.remove({'person': person_code, 'wage_type': {'$ne': wage_type}})
        col.update({'person': person_code}, {'$set': {'wage_type': wage_type}}, upsert=True)

msg_consume_handler = {
    'product_line': init_product_line_info,
    'person': init_person_info,
    'process': init_process_info,
    'bg_fz': init_bg_info,
    'materiel_group': init_materiel_group_info,
    'timely_wage': init_timely_wage_info
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

from mg_app_framework import get_logger, get_handler, TaskKey, get_store
import traceback
import tornado.httpclient as http_lib
import json
from enum import Enum, unique
from datetime import datetime
from pymongo import ASCENDING
import asyncio
from apscheduler.schedulers.tornado import TornadoScheduler


@unique
class PlanStatusType(Enum):
    # 状态包括未下发, 已下发, 进行中, 暂停, 已完工, 从ERP传过来的不可下发
    not_dispatched = 0
    dispatched = 1
    in_progress = 2
    paused = 3
    finished = 4
    cant_dispatch = 5


@unique
class PlanType(Enum):
    # 计划类型，包括erp导入和手工输入
    erp_import = 0
    manual_input = 1


@unique
class RestRequestType(Enum):
    post = 'POST'
    get = 'GET'


@unique
class ErpPlanStatus(Enum):
    can_dispatch = '可下发'
    cant_dispatch = '不可下发'
    finished = '已完成'


def get_plan_status_text(plan_status):
    plan_status_text_dict = {0: '未下发', 1: '已下发', 2: '进行中', 3: '暂停', 4: '已完工', 5: '不可下发'}
    if plan_status in plan_status_text_dict:
        return plan_status_text_dict[plan_status]
    return None

def log_exception(e, err_info):
    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    err_msg = '程序错误信息: {0}, 异常信息: {1}\n'.format(err_info, str(e))
    get_logger().error(err_msg)
    get_logger().error('\n')
    get_logger().error('traceback信息: {0}'.format(traceback_str))


# 获取计划管理的mongodb collection
def get_plan_db_collection():
    handler = get_handler(TaskKey.mongodb_async)
    return handler.plan_management.plan


async def send_request(url, request_data, request_type):
    response = None
    try:
        http_request = http_lib.HTTPRequest(url)
        http_request.method = request_type
        http_request.allow_nonstandard_methods = True
        if request_data:
            http_request.body = json.dumps(request_data, ensure_ascii=False)
        http_client = http_lib.AsyncHTTPClient()
        response = await http_client.fetch(http_request)
    except Exception as e:
        log_exception(e, '发送rest请求失败, url:{0}'.format(url))
    return response


# 获取今天某个产线上的所有计划
async def get_current_day_all_plans(product_line):
    current_date = str(datetime.now().date())
    current_day_plans = await get_all_plans_by_start_date(product_line, current_date)
    return current_day_plans


# 获取某一天某个产线上所有计划，不区分状态
async def get_all_plans_by_start_date(product_line, plan_start_date):
    plan_list = []
    plan_collection = get_plan_db_collection()
    # 目前方案改为获取所有计划在当日加工的计划，后续是否需要修改待定
    query = {'product_line_code': product_line, 'plan_start_date': plan_start_date}
    seq_num = 0
    async for document in plan_collection.find(query).sort('dispatch_time', ASCENDING):
        task_no = document['task_no']
        seq_num += 1
        material_name = document['material_name']
        material_code = document['material_code']
        plan_count = document['plan_count']
        qualified_count = document['qualified_count']
        unqualified_count = document['unqualified_count']
        plan_data = {'plan_no': task_no, 'sequence': seq_num, 'material_name': material_name, 'material_code': material_code, 'plan_count': plan_count, 'qualified_count': qualified_count, 'unqualified_count' : unqualified_count}
        plan_list.append(plan_data)
    return plan_list


# 计划修改后将所有某一天某个产线上的计划发往监控app
async def dispatch_plans_to_monitor_app(product_line, plan_start_date):
    try:
        plan_list = await get_all_plans_by_start_date(product_line, plan_start_date)
        pl_monitor_app_url = get_store().get_production_monitor_app_url()
        dispatch_api_url = '{}/api/monitor/recevie_plan/{}'.format(pl_monitor_app_url, product_line)
        await send_request(dispatch_api_url, plan_list, RestRequestType.post.value)
        get_logger().info('发送更新的计划数据到监控app成功, 产线:{}, 计划开工日期:{}, 数据:{}'.format(product_line, plan_start_date, plan_list))
    except Exception as e:
        log_exception(e, '下发计划到监控app产线:{}失败'.format(product_line))


# 去除显示在界面上时间的微秒
def polish_plan_display_time(plan_document):
    create_time = plan_document['create_time']
    modified_time = plan_document['modified_time']
    if create_time:
        plan_document['create_time'] = create_time[:create_time.find('.')]
    if modified_time:
        plan_document['modified_time'] = modified_time[:modified_time.find('.')]


async def dispatch_plans_check(task_no_list):
    query = {'task_no': {'$in': task_no_list}, 'plan_status': {'$nin': [PlanStatusType.not_dispatched.value, PlanStatusType.paused.value]}}
    plan_collection = get_plan_db_collection()
    error_msg = ''
    document = await plan_collection.find_one(query)
    if document:
        plan_status = document['plan_status']
        task_no = document['task_no']
        plan_status_text = get_plan_status_text(plan_status)
        error_msg = '任务单号:{}计划无法下发，当前该计划状态为:{}'.format(task_no, plan_status_text)
    return error_msg

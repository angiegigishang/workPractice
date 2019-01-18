from entities.task import Task
import json
import logging
import datetime
import asyncio
from networking.http_client import async_http_client, get_http_request, get_http_request_data
from sqlalchemy.orm import scoped_session
import configparser

# gloabl value
adder_days = -7
chage_datetime = None
locations_info = []
chage_time_file = ''

# config
work_order_sending_url = ''
sqlserver_host = ''
sqlserver_dbname = ''
sleep_mins = 0

erp_status = {1: "锁定", 2: "确认", 3: "下达", 4: "投放", 5: "流转", 6: "暂停", 7: "完工"}


async def find_and_send_task(session_factory, event_loop):
    try:
        global chage_datetime
        global problem_task_tags
        global work_order_sending_url
        session = scoped_session(session_factory)
        if work_order_sending_url == '':
            logging.info("Must firstly init work_order_handler")
            return

        while True:
            request_data = {"plan_list": []}
            # , Task.work_center.in_(locations_info)
            tasks = session.query(Task).filter(Task.chage_time > chage_datetime, Task.work_center.in_(locations_info)).order_by(Task.chage_time.asc()).limit(100)
            temp_time = chage_datetime
            for task in tasks:
                request_data['plan_list'].append(pkg_task(task))
                temp_time = task.chage_time
            try:
                result = await request_sending_task(request_data)
                print('{}--发送数据到计划管理app成功:{}'.format(str(datetime.datetime.now()), request_data))
                if result:
                    chage_datetime = temp_time
                    save_chage_time()
            except Exception as e:
                print(str(e))
                raise
            # 每sleep_mins分钟进行数据抽取
            for i in range(0, sleep_mins):
                await asyncio.sleep(60)
    except Exception as e:
        logging.info(e)
        await asyncio.sleep(60)
        asyncio.run_coroutine_threadsafe(find_and_send_task(session_factory, event_loop), event_loop)


async def request_sending_task(request_data):
    if len(request_data["plan_list"]) > 0:
        # 建立请求
        encode_request_data = get_http_request_data(request_data)
        request = get_http_request(work_order_sending_url, method='POST', body=encode_request_data)
        # 循环请求mes服务
        try:
            request_count = 0
            while True:
                request_count += 1
                response = await async_http_client.fetch(request)
                if response.error:
                    logging.info('origin mes server have error : ' + str(response.error))
                    if request_count > 5:
                        return False
                else:
                    data = json.loads(response.body.decode('utf-8'))
                    if data['code'] == 'success':
                        return True
                await asyncio.sleep(request_count*10)
        except Exception:
            raise

    return True


def convert_erp_status(ori):
    if ori in (2, 3, 4, 5):
        return "可下发"
    elif ori in (1, 6):
        return "不可下发"
    else:
        return "已完成"


def pkg_task(task):
    task_tag = {}
    try:
        task_tag['task_no'] = task.task_serial
        task_tag['task_type'] = task.task_type
        task_tag['task_date'] = task.task_date
        task_tag['material_code'] = task.product_code
        task_tag['material_name'] = task.product_name
        task_tag['material_spec'] = task.product_spec
        task_tag['material_unit'] = task.product_unit
        task_tag['plan_count'] = task.plan_num
        task_tag['plan_no'] = task.task_serial
        task_tag['plan_start_date'] = task.plan_start
        task_tag['plan_end_date'] = task.plan_end
        task_tag['real_start_date'] = task.real_start
        task_tag['real_end_date'] = task.real_end
        task_tag['workshop_name'] = task.work_center
        task_tag['create_time'] = task.chage_time
        task_tag['erp_plan_status'] = erp_status[int(task.plan_status)]
        task_tag['plan_status'] = convert_erp_status(int(task.plan_status))
    except Exception as e:
        print(str(e))

    return task_tag


def read_cfg(cfgpath):
    global sqlserver_host
    global sqlserver_dbname
    global work_order_sending_url
    global locations_info
    global adder_days
    global sleep_mins
    global chage_time_file

    try:
        conf = configparser.ConfigParser()
        conf.read(cfgpath + '/config.ini', encoding="utf-8-sig")

        # init sqlserver
        sqlserver_host = conf.get("sqlserver", "host")
        sqlserver_dbname = conf.get("sqlserver", "dbname")
        logging.info('db_host: {}, db_name: {}'.format(sqlserver_host, sqlserver_dbname))
        if sqlserver_dbname is None or sqlserver_host is None:
            logging.error("sqlserver_dbname is None or sqlserver_host is None")
            return False

        # init mes
        mes_url = conf.get("mes", "mes_url")
        task_api = conf.get("mes", "task_api")
        locations_name = conf.get("mes", "loc_name")
        if mes_url is None or task_api is None:
            logging.info("Close find_and_send_task because config.cfg's "
                         "mes_url or task_api is None")
            return False
        if locations_name is None:
            locations_name = "六车间,欣灵24轴全自动绕线机线"
        items = locations_name.split(',')
        for item in items:
            locations_info.append(item.encode('GBK'))
        work_order_sending_url = mes_url + task_api

        sleep_mins_str = conf.get("erp", "sleep_mins")
        adder_days = conf.get("erp", "adder_days")

        if sleep_mins_str is None:
            sleep_mins = 10
        else:
            sleep_mins = int(sleep_mins_str)
        if adder_days is None:
            adder_days = -7

        chage_time_file = cfgpath + '/chage_time'
        read_chage_time(cfgpath + '/chage_time')
    except Exception as e:
        print('读取配置read_cfg执行失败: {}'.format(str(e)))

    return True


def get_dbcfg():
    return sqlserver_host, sqlserver_dbname


def read_chage_time(filename):
    global chage_datetime
    f = None
    try:
        f = open(filename, 'r')
        chage_time = f.read()
        if chage_time is not None and chage_time is not '':
            chage_datetime = datetime.datetime.strptime(chage_time, "%Y-%m-%d %H:%M:%S")
        else:
            # 默认全量从7天前开始抽取计划
            chage_datetime = datetime.datetime.now() + datetime.timedelta(days=int(adder_days))
    except:
        if f:
            f.close()

    return


def save_chage_time():
    f = None
    try:
        f = open(chage_time_file, 'wt')
        f.write(chage_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    finally:
        if f:
            f.close()

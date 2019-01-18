from datetime import datetime
import calendar
from mg_app_framework import get_handler, TaskKey, get_logger, get_context, update_context

from attendance_manage.process.db_operator import get_target_mongo_collection


def get_current_on_work_info(pipeline_code=None):
    response = {}

    person_col = get_target_mongo_collection('person')
    all_person_cur = person_col.find({}, {'_id': 0, 'code': 1})
    all_person_code = [x['code'] for x in all_person_cur]
    col = get_target_mongo_collection('checkin_info')
    # 获取当前签到情况，此处时间起始点后期可能会调整
    now = datetime.now()
    begin_of_today = datetime(now.year, now.month, now.day)
    query_str = {'record_time': {'$gt': begin_of_today}}
    if pipeline_code:
        query_str.update({
            'pipeline_code': pipeline_code
        })
    today_on_work_cur = col.find(query_str, {'_id': 0, 'code': 1, 'on_work': 1})
    on_work_mapper = {}
    for c in today_on_work_cur:
        on_work_mapper.update({
            c['code']: c['on_work']
        })

    for p in all_person_code:
        response.update({
            p: on_work_mapper.setdefault(p, False)
        })

    return response


def get_process_threshold_info():
    # 获取所有工序阈值
    person_col = get_target_mongo_collection('process')

    all_process_info = person_col.find({}, {'_id': 0, 'threshold_person_number': 1, 'code': 1})
    response = {}
    for x in all_process_info:
        response.update({
            x['code']: x.setdefault('threshold_person_number', 0)
        })
    return response

def get_attendance_info_group_by_month(month_begin, month_end):
    checkin_info = get_target_mongo_collection('checkin_info')

    checkin_records_by_month = checkin_info.find({'record_time': {'$gte': month_begin, '$lt': month_end}},
                                                 {'_id': 0, 'code': 1, 'check_point': 1, 'pipeline_code': 1})
    checkin_records = {}
    for record in checkin_records_by_month:
        work_hours = calc_work_hours(record['check_point'])
        if record['code'] in checkin_records.keys():
            checkin_records.get(record['code']).append(work_hours)
        else:
            checkin_records[record['code']] = list()
            checkin_records[record['code']].append(work_hours)

    return checkin_records


def get_attendance_statistics(month_begin, month_end, threshold_hour):
    person_records_list = []
    # checkin_records = get_attendance_info_group_by_month(datetime(2019,1, 1), datetime(2019, 1, 5))
    checkin_records = get_attendance_info_group_by_month(month_begin, month_end)

    for key, value in checkin_records.items():
        tmp = {}
        absent = 0
        for work_hour in value:
            if work_hour < threshold_hour:
                absent += 1
        tmp['data'] = {'absent': absent, 'normal': len(value) - absent}
        tmp['name'] = get_name_by_code(key)
        person_records_list.append(tmp)
    return person_records_list


def calc_work_hours(check_point):
    seconds = (check_point[len(check_point) - 1] - check_point[0]).seconds
    hours = round(seconds / 3600, 1)
    return hours


def get_name_by_code(code):
    person_info_list = get_context('person_info')
    for person in person_info_list:
        if code == person['code']:
            return person['name']
    return 'Alien'


def sync_group_info(msg):
    on_work_mapper = get_current_on_work_info()

    pipeline_info = msg[0]['children'][0].setdefault('instance_list', [])
    get_logger().info('pipeline info')
    get_logger().info(pipeline_info)

    attendance_info = get_context('attendance_info')
    process_threshold_info = get_context('process_threshold')
    if not process_threshold_info:
        process_threshold = get_process_threshold_info()
        update_context('process_threshold', process_threshold)
        process_threshold_info = process_threshold

    for pipeline in pipeline_info:
        pipeline_code = pipeline['code']
        pipeline_group = pipeline['children']

        pipeline_process_in_memeory = []
        pipeline_process_codes_in_memeory = []
        group_info = []
        for group in pipeline_group[0].setdefault('instance_list', []):
            group_code = group['code']

            process_in_group = []
            person_in_group = []
            # 没有工序信息的默认排在后边
            sequence_flag = 99999
            for c in group.setdefault('children', []):

                if c['class_code'] == 'process':
                    # 处理分组中工序分组
                    process_list = c.setdefault('instance_list', [])
                    process_list = sorted(process_list, key=lambda x: int(x['sequence']))
                    for i, p in enumerate(process_list):
                        if i == 0:
                            sequence_flag = int(p['sequence'])
                        if p['code'] not in pipeline_process_codes_in_memeory:
                            pipeline_process_in_memeory.append([p['code'], p['name'], p['classify'] != '自动',
                                                                process_threshold_info.setdefault(p['code'], 0),
                                                                int(p['sequence'])])
                            pipeline_process_codes_in_memeory.append(p['code'])
                        process_in_group.append(p['code'])
                elif c['class_code'] == 'person':
                    # 处理分组中人员分组
                    person_list = c.setdefault('instance_list', [])
                    for p in person_list:
                        person_in_group.append({
                            'code': p['code'],
                            'name': p['name'],
                            'on_work': on_work_mapper.setdefault(p['code'], False)
                        })
            group_info.append({
                'processCodes': process_in_group,
                'groupCode': group_code,
                'members': person_in_group,
                'sequence_flag': sequence_flag
            })
        # 完成group_info的排序
        group_info = sorted(group_info, key=lambda x: x['sequence_flag'])
        for g in group_info:
            del g['sequence_flag']

        # 更新产线分组数据
        get_logger().info('更新产线分组数据')
        pipeline_checkin_info = attendance_info.setdefault(pipeline_code, {})
        pipeline_process_in_memeory = sorted(pipeline_process_in_memeory, key=lambda x: int(x[-1]))
        for x in pipeline_process_in_memeory:
            x.pop()
        pipeline_checkin_info.update({
            'processList': pipeline_process_in_memeory,
            'checkinInfo': group_info
        })

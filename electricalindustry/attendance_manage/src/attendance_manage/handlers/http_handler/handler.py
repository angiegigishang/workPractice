import calendar
from json import loads, dumps
from datetime import datetime
from dateutil import relativedelta

from mg_app_framework import HttpBasicHandler, MesCode, get_context, get_logger, get_handler, TaskKey

from attendance_manage.handlers.http_handler.common import get_current_on_work_info, sync_group_info,\
    get_attendance_statistics
from attendance_manage.handlers.http_handler.common import get_current_on_work_info, sync_group_info
from attendance_manage.process.external_api import push_attendance_info
from attendance_manage.process.db_operator import get_target_mongo_collection


class WebHandler(HttpBasicHandler):
    async def get_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success get data')

    async def post_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success post data')


class AllCheckinInfo(HttpBasicHandler):
    async def get_process(self, pipeline_code):
        attendance_info = get_context('attendance_info')
        print(attendance_info)
        try:
            self.send_response_data(MesCode.success, attendance_info.setdefault(pipeline_code, {}),
                                    'get attendance info successfully')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))


class OnworkCheckinInfo(HttpBasicHandler):
    # 只返回on_work人员
    async def get_process(self, pipeline_code):
        attendance_info = get_context('attendance_info')
        try:
            all_attendance_info = attendance_info.setdefault(pipeline_code, {})
            on_work_info = loads(dumps(all_attendance_info))
            for x in on_work_info.setdefault('checkinInfo', []):
                on_work_members = [w for w in x.setdefault('members', []) if w.setdefault('on_work', False)]
                x.update({
                    'members': on_work_members
                })
            self.send_response_data(MesCode.success, on_work_info,
                                    'get attendance info successfully')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))


class OnWorkInfo(HttpBasicHandler):
    async def get_process(self, pipeline_code):
        try:
            on_work_status = get_current_on_work_info(pipeline_code)
            on_work_person_codes = [k for k, v in on_work_status.items() if v]
            self.send_response_data(MesCode.success, on_work_person_codes, 'get on working person code list')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))


class CheckinInfo(HttpBasicHandler):
    async def post_process(self):
        try:
            request_body = loads(self.request.body)
            checkin_info = request_body['checkin_info']
            self.pipeline_code = request_body['pipeline_code']
            # 更新人员签到信息
            self.process_checkin_info(checkin_info)
            # 同步内存分组信息
            msg = get_context('mdm_group_info')
            sync_group_info(msg)
            attendance_info = get_context('attendance_info')
            # 返回给前端生产线最新成员分组信息
            self.send_response_data(MesCode.success,
                                    attendance_info.setdefault(self.pipeline_code, {}).setdefault('checkinInfo', {}),
                                    'success post data')
            await self.send_attendance_info_to_monitor()
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))

    def process_checkin_info(self, checkin_info):
        col = get_target_mongo_collection('checkin_info')

        now = datetime.now()
        begin_of_today = datetime(now.year, now.month, now.day)

        for i in checkin_info:
            person_code = i['code']
            on_work = i['on_work']
            now = datetime.now()
            if on_work:
                col.update({'code': person_code, 'record_time': {'$gt': begin_of_today}},
                           {'$set': {'code': person_code, 'on_work': True, 'record_time': now,
                                     'pipeline_code': self.pipeline_code},
                            '$push': {'check_point': now}}, upsert=True)
            else:
                col.update({'code': person_code, 'record_time': {'$gt': begin_of_today}},
                           {'$set': {'on_work': False, 'record_time': now},
                            '$push': {'check_point': now}})

    async def send_attendance_info_to_monitor(self):
        try:
            attendance_info = get_context('attendance_info')
            all_attendance_info = attendance_info.setdefault(self.pipeline_code, {})
            on_work_info = loads(dumps(all_attendance_info))
            for x in on_work_info.setdefault('checkinInfo', []):
                on_work_members = [w for w in x.setdefault('members', []) if w.setdefault('on_work', False)]
                x.update({
                    'members': on_work_members
                })
        except Exception as e:
            get_logger().exception(str(e))
        else:
            await push_attendance_info(self.pipeline_code, on_work_info)
            get_logger().info('push attendance info to monitor')
            get_logger().info(on_work_info)


class WorkStatInfo(HttpBasicHandler):
    async def get_process(self, month):
        logger = get_logger()
        try:
            stat_data = self.get_stat_test_data(month)
            self.send_response_data(MesCode.success, stat_data, "Success")
        except Exception as e:
            logger.exception(e)
            self.send_response_data(MesCode.success, {}, "Some Internal ERRORS occurred")

    def get_stat_test_data(self, month):
        year = int(month[:4])
        month = int(month[-2:])
        # month_range_0, month_range_1 = calendar.monthrange(year, month)
        month_begin = datetime.strptime('%d-%02d-01' % (year, month), '%Y-%m-%d')
        now = datetime.now()
        data_list = get_attendance_statistics(month_begin, now, threshold_hour=8)
        header_list = [{
                        'code': 'normal',
                        'name': '正常上班'
                        }, {
                        'code': 'absent',
                        'name': '迟到早退'}]
        report_stat_data = dict()
        report_stat_data['header_list'] = header_list
        report_stat_data['data_list'] = data_list
        return report_stat_data


class WorkingHoursHandler(HttpBasicHandler):
    async def post_process(self, *args, **kwargs):
        # request_body:
        # {
        #     'year': xxx,
        #     'month': xxx,
        #     'person_list': [
        #         {
        #             'person_code': xxx,
        #             'wage_type': xxx
        #         }
        #     ]
        # }
        request_body = loads(self.request.body)
        query_year = request_body['year']
        query_month = request_body['month']
        query_start_time = datetime(query_year, query_month, 1)
        query_end_time = query_start_time + relativedelta.relativedelta(months=1)
        query_person_info = request_body['person_list']
        response = {}
        for p in query_person_info:
            person_code = p['person_code']
            wage_type = p['wage_type']
            person_working_hour_info = self.process_working_hours(person_code, wage_type, query_start_time,
                                                                  query_end_time)
            response.update(person_working_hour_info)
        self.send_response_data(MesCode.success, response, 'get working hour successfully')

    def process_working_hours(self, person_code, wage_type, start_time, end_time):
        col = get_target_mongo_collection('checkin_info')

        person_working_hour_info = col.find({'code': person_code, 'record_time': {'$gt': start_time, '$lt': end_time}},
                                            {'_id': 0})
        person_working_total_amount = 0
        for i in person_working_hour_info:
            check_point = i['check_point']
            if check_point:
                first_check_in = check_point[0]
                last_check_in = check_point[-1]
                if first_check_in != last_check_in:
                    pass
                else:
                    if first_check_in.hour > 18:
                        continue
                    else:
                        last_check_in = datetime(first_check_in.year, first_check_in.month, first_check_in.day, 18)
                get_logger().info(
                    '{} check in at:{} and check out at:{}'.format(person_code, first_check_in, last_check_in))
                work_time_delta = last_check_in - first_check_in
                total_seconds = work_time_delta.total_seconds()
                # 通过该员工的工资计费方式计算工作时间
                if wage_type == 'hourly_wage':
                    # 时薪

                    total_hour = round(float(total_seconds / 3600), 2)
                    person_working_total_amount += total_hour
                if wage_type == 'dayly_wage':
                    # 日薪
                    if total_seconds / 3600 > 8:
                        person_working_total_amount += 1
                if wage_type == 'monthly_wage':
                    # 月薪
                    if total_seconds / 3600 > 8:
                        person_working_total_amount += 1 / 21.5
        return {
            person_code: person_working_total_amount
        }

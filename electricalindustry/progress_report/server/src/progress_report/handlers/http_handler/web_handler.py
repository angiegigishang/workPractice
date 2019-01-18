from mg_app_framework import HttpBasicHandler, MesCode, get_logger, get_store
from progress_report.handlers.sds import get_group_config, get_report_point_config
from progress_report.handlers.utils import log_exception, send_request, get_report_db_collection, get_current_month_date_range
from datetime import datetime, timedelta
from progress_report.handlers.test_utils import get_on_work_person_list_test, get_plan_data_test
import json
from collections import defaultdict



class EmployeeFetchHandler(HttpBasicHandler):
    async def get_process(self, product_line_code):
        try:
            person_info_list = []
            group_config = get_group_config()
            if product_line_code in group_config:
                all_group_data_dict = group_config[product_line_code]
                if all_group_data_dict:
                    # 获取在岗所有人员编码
                    on_duty_person_list = await self.get_on_duty_person_list(product_line_code)
                    for group_code, group_data in all_group_data_dict.items():
                        if group_data and 'person' in group_data:
                            # 仅返回所有在某个分组内的在岗人员
                            person_list = [{'name': person['name'], 'code': person['code']} for person in group_data['person'] if person['code'] in on_duty_person_list]
                            if person_list:
                                person_info = {'seq': group_data['seq'], 'group_code': group_code, 'member_list': person_list}
                                person_info_list.append(person_info)
                    if person_info_list:
                        # 根据组序号排序
                        person_info_list = sorted(person_info_list, key=lambda k: k['seq'])
                        for person_info in person_info_list:
                            del person_info['seq']
            get_logger().info('获取产线{}人员信息成功: {}'.format(product_line_code, person_info_list))
            self.send_response_data(MesCode.success, person_info_list, '')
        except Exception as e:
            log_exception(e, '获取产线:{}所有人员信息失败'.format(product_line_code))
            self.send_response_data(MesCode.fail, None, '获取产线:{}所有人员信息失败'.format(product_line_code))

    async def get_on_duty_person_list(self, product_line_code):
        # 获取在岗所有人员编码列表
        on_duty_person_list = []
        url = '{}/api/attendance_manage/pipeline/{}/on_work_info'.format(get_store().get_attendence_management_app_url(), product_line_code)
        response = await send_request(url, None, 'GET')
        if response:
            response_body = json.loads(response.body.decode('utf-8'))
            if response_body['code'] == MesCode.success:
                on_duty_person_list = response_body['data']
        return on_duty_person_list


class ProcessFetchHandler(HttpBasicHandler):
    async def get_process(self, product_line_code):
        try:
            process_info_list = []
            group_config = get_group_config()
            report_point_config = get_report_point_config()
            if product_line_code in group_config and product_line_code in report_point_config:
                all_group_data_dict = group_config[product_line_code]
                report_point_list = report_point_config[product_line_code]
                if all_group_data_dict:
                    for group_code, group_data in all_group_data_dict.items():
                        if group_data and 'process' in group_data:
                            process_data_list = []
                            original_process_data_list = group_data['process']
                            if original_process_data_list:
                                for origin_process_data in original_process_data_list:
                                    process_code, process_name, process_seq = origin_process_data['code'], origin_process_data['name'], origin_process_data['sequence']
                                    process_classify = origin_process_data['classify']
                                    if process_classify == '人工':
                                        process_type = 1
                                    else:
                                        process_type = 0
                                    is_report_point = 1 if process_code in report_point_list else 0
                                    process_data = {'name': process_name, 'code': process_code, 'seq_number': process_seq, 'type': process_type, 'is_report_point': is_report_point}
                                    process_data_list.append(process_data)
                            if process_data_list:
                                # 根据序号顺序排序，然后删除该字段
                                process_data_list = sorted(process_data_list, key=lambda k: int(k['seq_number']))
                                for process_data in process_data_list:
                                    del process_data['seq_number']
                            process_info = {'group_code': group_code, 'process_list': process_data_list}
                            process_info_list.append(process_info)
            get_logger().info('获取产线{}工序信息成功: {}'.format(product_line_code, process_info_list))
            self.send_response_data(MesCode.success, process_info_list, '')
        except Exception as e:
            log_exception(e, '获取产线:{}所有人员信息失败'.format(product_line_code))
            self.send_response_data(MesCode.fail, None, '获取产线:{}所有人员信息失败'.format(product_line_code))


class PlanFetchHandler(HttpBasicHandler):
    async def get_process(self, product_line_code, group_code, process_code):
        plan_info_list = []
        try:
            plan_data_list = await self.get_plan_data_list(product_line_code, process_code)
            if plan_data_list:
                for plan_data in plan_data_list:
                    plan_number, material_name, material_code = plan_data['plan_number'], plan_data['material_name'], plan_data['material_code']
                    plan_count = plan_data['plan_count']
                    total_plan_qualified_count = int(plan_data['total_plan_qualified_count']) if plan_data['total_plan_qualified_count'] else 0
                    total_plan_unqualified_count = int(plan_data['total_plan_unqualified_count']) if plan_data['total_plan_unqualified_count'] else 0
                    is_process_manual = await self.is_process_manual(product_line_code, group_code, process_code)
                    if is_process_manual:
                        # 人工工序使用计划监控数
                        current_qualified_count = total_plan_qualified_count
                        current_unqualified_count = total_plan_unqualified_count
                    else:
                        current_qualified_count = int(plan_data['current_qualified_count']) if plan_data['current_qualified_count'] else 0
                        current_unqualified_count = int(plan_data['current_unqualified_count']) if plan_data['current_unqualified_count'] else 0
                    plan_progress = plan_data['plan_progress']
                    current_group_count_dict, other_group_count_dict = await self.get_existing_report_data(plan_number, group_code, process_code)
                    # 计算还可报工的数量
                    remain_submit_qualified_count = current_qualified_count - other_group_count_dict['qualified_count']
                    remain_submit_unqualified_count = current_unqualified_count - other_group_count_dict['unqualified_count']
                    plan_info = {'plan_number': plan_number, 'material_name': material_name, 'material_code': material_code, 'plan_count': plan_count, 'qualified_count': total_plan_qualified_count,
                                 'unqualified_count': total_plan_unqualified_count, 'plan_progress': plan_progress,
                                 'report_data': {'current_detected_count': {'qualified_count': current_qualified_count, 'unqualified_count': current_unqualified_count},
                                                 'remain_submit_count': {'qualified_count': remain_submit_qualified_count, 'unqualified_count': remain_submit_unqualified_count},
                                                 'current_submitted_count': {'qualified_count': current_group_count_dict['qualified_count'], 'unqualified_count': current_group_count_dict['unqualified_count']}}}
                    plan_info_list.append(plan_info)
            self.send_response_data(MesCode.success, plan_info_list, '')
            get_logger().info('获取计划和当前报工点数据成功, 产线编码:{}, 组编码:{}, 数据:{}'.format(product_line_code, group_code, plan_info_list))
        except Exception as e:
            log_exception(e, '获取产线{}相关的所有计划数据列表失败'.format(product_line_code))

    async def get_plan_data_list(self, product_line_code, process_code):
        plan_data_list = []
        url = '{}/api/monitor/production_plan_data/{}/{}'.format(get_store().get_production_monitor_app_url(), product_line_code, process_code)
        response = await send_request(url, None, 'GET')
        if response:
            response_body = json.loads(response.body.decode('utf-8'))
            if response_body['code'] == MesCode.success:
                plan_data_list = response_body['data']
        return plan_data_list

    async def get_existing_report_data(self, plan_number, group_code, process_code):
        current_day = str(datetime.now().date())
        query = {'plan_number': plan_number, 'report_date': current_day, 'process_code': process_code}
        report_collection = get_report_db_collection()
        current_group_count_dict = {'qualified_count': 0, 'unqualified_count': 0}
        other_group_count_dict = {'qualified_count': 0, 'unqualified_count': 0}
        async for document in report_collection.find(query):
            doc_group_code = document['group_code']
            qualified_count, unqualified_count = document['qualified_count'], document['unqualified_count']
            if doc_group_code == group_code:
                current_group_count_dict['qualified_count'] += int(qualified_count)
                current_group_count_dict['unqualified_count'] += int(unqualified_count)
            else:
                other_group_count_dict['qualified_count'] += int(qualified_count)
                other_group_count_dict['unqualified_count'] += int(unqualified_count)
        return current_group_count_dict, other_group_count_dict

    async def is_process_manual(self, product_line_code, group_code, process_code):
        group_config = get_group_config()
        process_list = group_config[product_line_code][group_code]['process']
        manual_process_data = [process for process in process_list if process['code'] == process_code][0]
        is_manual = True if manual_process_data['classify'] == '人工' else False
        return is_manual


class ReportSaveHandler(HttpBasicHandler):
    async def post_process(self):
        """
        url: POST /api/progress_report/report/save

        前端发送到后端的请求数据结构:
        {
          "group_code": "group_code1", // 当前报工组编码
          "plan_number": "", //计划号
          "process_code": "", // 工序编码
          "material_name": "", //物料名
          "material_code": "", //物料编码
          "qualified_count": 50, //合格数
          "unqualified_count": 20 //不合格数
        }
        :return:
        {
            "code":"success",
            "info": "",
            "data": null
        }
        """
        report_data = self.data
        group_code, plan_number = self.data['group_code'], self.data['plan_number']
        process_code = self.data['process_code']

        try:
            current_day = str(datetime.now().date())
            report_time = str(datetime.now().replace(microsecond=0))
            report_data['report_date'] = current_day
            report_data['report_time'] = report_time
            report_collection = get_report_db_collection()
            check_existing_report_query = {'group_code': group_code, 'plan_number': plan_number, 'report_date': current_day}
            # 使用upsert方式插入新报工记录，如果存在则更新文档
            await report_collection.replace_one(check_existing_report_query, report_data, True)
            self.send_response_data(MesCode.success)
        except Exception as e:
            log_exception(e, '保存当前报工数据失败, 计划号:{}, 工序编码:{}'.format(plan_number, process_code))


class ReportStatFetchHandler(HttpBasicHandler):
    async def get_process(self, month):
        stat_data = self.get_stat_test_data()
        self.send_response_data(MesCode.success, stat_data, None)

    def get_stat_test_data(self):
        report_stat_data = {
            'header_list':
                [
                    {
                        'code': 'materiel_t901h40adc12v4_23',
                        'name': 'T901H40ADC12V 4脚 23规格'
                    },
                    {
                        'code': 'materiel_t901z30adc12v5_ynb',
                        'name': 'T901Z30ADC12V 5脚 永能标'
                    },
                    {
                        'code': 'materiel_t901h40adc12v4_ynb',
                        'name': 'T901H40ADC12V 4脚 永能标'
                    },
                ],
            'data_list':
                [
                    {
                        'name': ' 6T90报工组1',
                        'data':
                            {
                                'materiel_t901h40adc12v4_23': '1000/10',
                                'materiel_t901z30adc12v5_ynb': '2000/12'
                            }
                    },
                    {
                        'name': ' 6T90报工组2',
                        'data':
                            {
                                'materiel_t901h40adc12v4_23': '1100/3',
                                'materiel_t901z30adc12v5_ynb': '2200/4'
                            }
                    },
                    {
                        'name': ' 6T90报工组3',
                        'data':
                            {
                                'materiel_t901z30adc12v5_ynb': '2200/3',
                                'materiel_t901h40adc12v4_ynb': '3000/0'
                            }
                    },
                    {
                        'name': ' 6T90报工组4',
                        'data':
                            {
                                'materiel_t901h40adc12v4_23': '1200/1',
                                'materiel_t901h40adc12v4_ynb': '2900/2'
                            }
                    }
                ]
        }
        return report_stat_data


class CurrentMonthReportFetchHandler(HttpBasicHandler):
    async def get_process(self):
        report_info_list = []
        try:
            report_data_dict = await self.get_current_month_report_data()
            if report_data_dict:
                for group_code, group_report_dict in report_data_dict.items():
                    group_data = {'groupCode': group_code, 'report': []}
                    if group_report_dict:
                        for material_code, report in group_report_dict.items():
                            qualified_count, unqualified_count = report['qualified_count'], report['unqualified_count']
                            report_data = {'materielCode': material_code, 'qualified_count': qualified_count, 'unqualified_count': unqualified_count}
                            group_data['report'].append(report_data)
                    report_info_list.append(group_data)
            self.send_response_data(MesCode.success, report_info_list, '')
            get_logger().info('获取本月报工数据成功, 数据:{}'.format(report_info_list))
        except Exception as e:
            log_exception(e, '获取本月报工数据失败')

    async def get_current_month_report_data(self):
        report_data = {}
        first_date, last_date = get_current_month_date_range()
        report_collection = get_report_db_collection()
        query = {'$and': [{'report_date': {'$gte': first_date}}, {'report_date': {'$lte': last_date}}]}
        async for document in report_collection.find(query):
            group_code = document['group_code']
            material_code = document['material_code']
            qualified_count = document['qualified_count']
            unqualified_count = document['unqualified_count']
            if group_code not in report_data:
                report_data[group_code] = dict()
            if material_code not in report_data[group_code]:
                report_data[group_code][material_code] = {'qualified_count': 0, 'unqualified_count': 0}
            report_data[group_code][material_code]['qualified_count'] += qualified_count
            report_data[group_code][material_code]['unqualified_count'] += unqualified_count
        return report_data

class ReportDataPerMonthHandler(HttpBasicHandler):
    async def get_process(self):
        try:
            first_date, last_date = get_current_month_date_range()
            current_date = datetime.now().strftime('%Y-%m-%d')
            report_collection = get_report_db_collection()
            group_code_names_dict = {}
            for item in get_group_config().values():
                for k, v in item.items():
                    group_code_names_dict[k] = v['group_name']

            query_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
            query = {'report_date': {'$gte': first_date, '$lte': last_date}}
            async for document in report_collection.find(query):
                group_code = document['group_code']
                if group_code not in group_code_names_dict:
                    continue
                group_code = group_code_names_dict[group_code]
                report_date = document['report_date']
                unqualified_count = document['unqualified_count']
                qualified_count = document['qualified_count']

                query_data[report_date][group_code]['unqualified_count'] += unqualified_count
                query_data[report_date][group_code]['qualified_count'] += qualified_count

            return_data = dict()
            return_data['group_names'] = sorted(list(group_code_names_dict.values()))
            return_data['group_data'] = {}
            for date_item in self.date_iteration(first_date, current_date):
                return_data['group_data'][date_item] = query_data.get(date_item, {})

            self.send_response_data(MesCode.success, return_data, '大屏报工数据月度统计')
            get_logger().info('大屏报工数据月度成功, 数据:{}'.format(return_data))
        except Exception as e:
            log_exception(e, '获取大屏报工数据月度失败')
            self.send_response_data(MesCode.fail, {}, '获取大屏报工数据月度失败')

    def date_iteration(self, start_date, stop_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        stop = datetime.strptime(stop_date, "%Y-%m-%d")

        while start <= stop:
            yield start.strftime('%Y-%m-%d')
            start = start + timedelta(days=1)
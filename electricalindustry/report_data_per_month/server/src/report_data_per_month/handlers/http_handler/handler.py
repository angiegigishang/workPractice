from mg_app_framework import HttpBasicHandler, MesCode, get_logger
from report_data_per_month.handlers.utils import log_exception, get_report_db_collection, get_current_month_date_range
from datetime import datetime, timedelta
from collections import defaultdict
from report_data_per_month.handlers.sds import get_group_config

class ReportDataPerMonthHandler(HttpBasicHandler):
    async def get_process(self):
        try:
            first_date, last_date = get_current_month_date_range()
            current_date = datetime.now().strftime('%Y-%m-%d')
            report_collection = get_report_db_collection()
            group_code_names_dict = {}
            for item in get_group_config().values():
                for k,v in item.items():
                    group_code_names_dict[k] = v['name']

            query_data = defaultdict(lambda: defaultdict(lambda : defaultdict(int)))
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
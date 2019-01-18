from datetime import date

from mg_app_framework import HttpBasicHandler, MesCode, get_logger

from plan_management.handlers.sds import get_custom_field_config
from plan_management.handlers.utils import get_plan_db_collection, log_exception, PlanStatusType


class PlanHistoryHandler(HttpBasicHandler):

    async def get_process(self, start_date, end_date):
        """
        url: GET /api/plan_management/manage/plan/history/start_date/end_date
        :return:
        {
            "code":"success",
            "info": "",
            "data":
            [
                {
                    "task_no": "A190112099-00",
                    "material_name": "CH&YJ T901D40ADC24V-4",
                    "plan_count": 2000,
                    "plan_start_date": "2019-01-12 00:00:00",
                    "real_end_date": null,
                    "workshop_name": "六车间",
                    "create_time": "2019-01-17 09:06:20.355889",
                    "plan_status": 4,
                    "product_line_code": "",
                    "operator": "",
                    "modified_time": "",
                    "plan_type": 0,

                }
            ]
        }
        """
        if start_date == "" and end_date == "":
            # 默认获取所有已完成(状态码为4)或者无法下达(状态码为5)的历史任务
            query = {'$or': [{'plan_status': PlanStatusType.finished.value},
                     {'plan_status': PlanStatusType.cant_dispatch.value}]}
            await self.get_plan_list(query)
        else:
            today = date.today().strftime('%Y-%m-%d')
            if start_date > today or end_date > today:
                get_logger().info('起始或截止时间超过今日')
                self.send_response_data(MesCode.fail, None, '起始或截止时间不得超过今日')
            elif start_date > end_date:
                get_logger().info('起始时间大于截止时间')
                self.send_response_data(MesCode.fail, None, '起始时间不得大于截止时间')
            else:
                query = {'$or': [{'plan_status': PlanStatusType.finished.value},
                                 {'plan_status': PlanStatusType.cant_dispatch.value}],
                         "real_end_date": {'$gte': start_date, '$lte': end_date}}
                # 获取所有状态为已完成(状态码为4)并且完成时间在查询的时间段内的或者无法下达(状态码为5)的历史任务
                await self.get_plan_list(query)

    async def get_plan_list(self, query):
        plan_data_list = []
        plan_collection = get_plan_db_collection()
        columns = {"task_no": 1, "material_name": 1, "plan_count": 1, "plan_start_date": 1,
                   "workshop_name": 1, "product_line_code": 1, "operator": 1, "create_time": 1,
                   "modified_time": 1, "plan_status": 1, "plan_type": 1, "real_end_date": 1,
                   "_id": 0}
        for column in get_custom_field_config().keys():
            columns.update({column: 1})
        try:
            async for document in plan_collection.find(query, columns).sort("real_end_date", -1):
                plan_data_list.append(document)
            self.send_response_data(MesCode.success, plan_data_list, '获取历史任务成功')
            get_logger().info('获取历史任务成功, 数据: {}'.format(plan_data_list))
        except Exception as e:
            log_exception(e, '获取历史任务失败')
            self.send_response_data(MesCode.fail, None, '获取历史任务失败')

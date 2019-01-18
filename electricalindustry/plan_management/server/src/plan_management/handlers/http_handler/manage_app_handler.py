from mg_app_framework import HttpBasicHandler, MesCode, get_logger
from plan_management.handlers.utils import log_exception, get_plan_db_collection, get_current_day_all_plans, PlanStatusType
from pymongo import UpdateOne, ASCENDING
from datetime import datetime
import json


class PlanStatusUpdateHandler(HttpBasicHandler):
    async def post_process(self):
        """
        url: POST /api/plan_management/plan/status_update
        监控app发往计划管理app的数据结构:
        [
            {
                "plan_no": "A181120203-00",
                "status": 2, //2表示进行中，3表示暂停，4表示已完工
                "progress_detail":  //仅更新状态为暂停和已完工时传合格数和不合格数，对于进行中没有这个字段
                {
                    "qualified_count": 1000,
                    "unqualified_count": 2
                }
            }
        ]
        :return:
        {
            "code":"success",
            "info": "",
            "data": null
        }
        """
        req_data_list = json.loads(self.request.body)
        try:
            plan_collection = get_plan_db_collection()
            # 转存成字典方便操作
            status_data_dict = dict()
            for req_data in req_data_list:
                plan_no = req_data['plan_no']
                status_data_dict[plan_no] = req_data

            task_no_list = [status_data['plan_no'] for status_data in req_data_list]
            query = {'task_no': {'$in': task_no_list}}
            update_plan_list = []
            async for document in plan_collection.find(query):
                document_id = document['_id']
                task_no = document['task_no']
                status_data = status_data_dict[task_no]
                updated_status = status_data['status']
                update_clause = {'plan_status': updated_status}
                if updated_status == PlanStatusType.in_progress.value:
                    real_start_date = document['real_start_date']
                    if not real_start_date:
                        # 如果是计划刚开始加工了，则设置真实开工时间为当前日期
                        update_clause['real_start_date'] = str(datetime.now().date())
                if 'progress_detail' in status_data:
                    # 如果是暂停或者可完工，则会传过来合格数和不合格数
                    qualified_count = status_data['progress_detail']['qualified_count']
                    unqualified_count = status_data['progress_detail']['unqualified_count']
                    update_clause['qualified_count'] = qualified_count
                    update_clause['unqualified_count'] = unqualified_count

                update_data = UpdateOne({'_id': document_id}, {'$set': update_clause})
                update_plan_list.append(update_data)
            if update_plan_list:
                # 批量更新计划
                plan_collection.bulk_write(update_plan_list)
                self.send_response_data(MesCode.success, None, '')
                get_logger().info('更新计划状态成功: {}'.format(req_data_list))
        except Exception as e:
            log_exception(e, '更新计划状态数据失败')
            self.send_response_data(MesCode.fail, None, '更新计划状态数据失败: {}'.format(req_data_list))


class DispatchedPlanFetchHandler(HttpBasicHandler):
    async def get_process(self, product_line):
        """
        url: GET /api/plan_management/manage/(?P<product_line>.*)/dispatched_plan/list
        :return:
        [
            {
                "plan_no": "A181120203-00",
                "sequence": 1,  //计划之间的顺序
                "material_name": "T901H40ADC12V 4脚 23规格",
                "material_code": "materiel_t901h40adc12v4_23",
                "plan_count": 10000,
                "qualified_count": 1000,
                "unqualified_count": 2
            }
        ]
        """
        # 获取当日所有已下发到某个产线的计划
        current_date = str(datetime.now().date())
        try:
            plan_list = await get_current_day_all_plans(product_line)
            self.send_response_data(MesCode.success, plan_list, '')
            get_logger().info('成功获取:{}日所有已下发计划数据:{}'.format(current_date, plan_list))
        except Exception as e:
            log_exception(e, '获取{}计划数据失败'.format(current_date))
            self.send_response_data(MesCode.fail, None, '获取{}计划数据失败'.format(current_date))


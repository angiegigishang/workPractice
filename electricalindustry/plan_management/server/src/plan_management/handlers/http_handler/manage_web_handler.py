from mg_app_framework import HttpBasicHandler, MesCode, get_logger, loginrequired
from plan_management.handlers.utils import log_exception, get_plan_db_collection, PlanStatusType, PlanType, \
    polish_plan_display_time, dispatch_plans_to_monitor_app, dispatch_plans_check
from datetime import datetime
from pymongo import UpdateOne
from dateutil.relativedelta import relativedelta
from plan_management.handlers.sds import get_plan_pl_config, get_material_config, get_custom_field_config
import json
from pymongo import ASCENDING


class PlanFetchHandler(HttpBasicHandler):
    @loginrequired
    async def get_process(self):
        """
        url: GET /api/plan_management/manage/plan/list
        :return:
        {
            "code":"success",
            "info": "",
            "data":
             [
                {
                  "task_no": "11111",  //任务单号
                  "material_code": "557",  //物料编码
                  "material_name": "物料A", //物料名
                  "material_unit": "个", //物料单位
                  "plan_count": 100,  //计划数量
                  "plan_start_date": "2018-12-12",  //计划开工日期
                  "comment": "",  //备注信息
                  "workshop_name": "车间1",  //车间名
                  "workshop_code": "workshop_6", //车间编码
                  "product_line_code": "6t90",  //产线编码
                  "operator": "admin",   //录入人员
                  "create_time": "2018-12-10: 10:00:00",  //录入时间
                  "modify_time": "2018-12-20: 13:10:20",  //修改时间
                  "plan_status": 0,  //计划状态, 0表示未下发，1表示已下发
                  "erp_plan_status": 2, //ERP导入计划原状态, 2.确认, 3.下达, 4.投放, 5.流转
                  "plan_type": 0, //计划类型，0表示ERP导入，1表示自定义添加
                  "dzzd_task_type": "常规产品", //任务类型，定制字段
                  "dzzd_task_date": "2019-01-10", //开单日期,
                  "dzzd_plan_no": "11111", //计划单号, 定制字段
                  "dzzd_main_plan_no": "4545545",  //主计划号，定制字段
                  "dzzd_material_spec": "NNC",     //规格，定制字段
                  "dzzd_special_requirements": "" //特殊要求，定制字段
                }
             ]
        }
        """
        plan_data_list = []
        try:
            plan_collection = get_plan_db_collection()
            # 获取所有状态为未下发(0),已下发(1)和暂停的计划
            query = {'$or': [{'plan_status': PlanStatusType.not_dispatched.value}, {'plan_status': PlanStatusType.dispatched.value}, {'plan_status': PlanStatusType.paused.value}]}
            async for document in plan_collection.find(query):
                del document['_id']
                del document['plan_end_date']
                del document['real_start_date']
                del document['real_end_date']
                del document['qualified_count']
                del document['unqualified_count']
                polish_plan_display_time(document)
                plan_data_list.append(document)
            self.send_response_data(MesCode.success, plan_data_list, '')
            get_logger().info('获取所有管理计划成功, 数据: {}'.format(plan_data_list))
        except Exception as e:
            log_exception(e, '获取所有管理计划失败')
            self.send_response_data(MesCode.fail, None, '获取所有管理计划失败')


class PlanAddHandler(HttpBasicHandler):
    @loginrequired
    async def post_process(self):
        """
        url: POST /api/plan_management/manage/plan/add
        前端请求的数据结构:
        {
          "task_no": "11111",   //必填
          "material_code": "557", //必填，选择
          "material_name": "物料A",  //必填，选择
          "material_unit": "个", //必填，选择
          "plan_count": 100,  //必填
          "plan_start_date": "2018-12-12",
          "comment": "",
          "workshop_name": "车间1",  //必填，选择
          "workshop_code": "workshop_6",
          "main_plan_no": "4545545",
          "material_spec": "NNC",
          "special_requirements": ""
        }
        :return:
        {
            "code":"success",
            "info": "",
            "data":
            {
              "task_no": "11111",
              "material_code": "557",
              "material_name": "物料A",
              "material_unit": "个",
              "plan_count": 100,
              "plan_start_date": "2018-12-12",
              "comment": "",
              "workshop_name": "车间1",
              "workshop_code": "workshop_6",
              "product_line_code": "6t90",
              "operator": "admin",
              "create_time": "2018-12-10: 10:00:00",
              "modify_time": "2018-12-20: 13:10:20",
              "plan_status": "0",
              "plan_type": 0,
              "dzzd_task_type": "常规产品",
              "dzzd_task_date": "2019-01-10",
              "dzzd_plan_no": "11111",
              "dzzd_main_plan_no": "4545545",
              "dzzd_material_spec": "NNC",
              "dzzd_special_requirements": ""
            }
        }
        """
        try:
            req_data = self.data
            plan_collection = get_plan_db_collection()
            task_no = req_data['task_no']
            existing_plan = await plan_collection.find_one({'task_no': task_no})
            if existing_plan:
                get_logger().info('任务单号:{}对应的计划已存在'.format(task_no))
                self.send_response_data(MesCode.fail, None, '任务单号:{}对应的计划已存在'.format(task_no))
                return
            else:
                req_data['real_start_date'] = ''
                req_data['operator'] = await self.login_name
                req_data['create_time'] = str(datetime.now())
                req_data['modified_time'] = ''
                req_data['plan_status'] = PlanStatusType.not_dispatched.value
                req_data['plan_type'] = PlanType.manual_input.value
                req_data['plan_end_date'] = ''
                req_data['real_start_date'] = ''
                req_data['real_end_date'] = ''
                req_data['product_line_code'] = ''
                req_data['dispatch_time'] = ''
                req_data['erp_plan_status'] = ''
                req_data['qualified_count'] = 0
                req_data['unqualified_count'] = 0
                inserted_result = await plan_collection.insert_one(req_data)
                inserted_id = inserted_result.inserted_id
                get_logger().info('新增自定义计划成功:{}'.format(req_data))
                inserted_document = await plan_collection.find_one({'_id': inserted_id})
                del inserted_document['_id']
                del inserted_document['plan_end_date']
                del inserted_document['real_start_date']
                del inserted_document['real_end_date']
                del inserted_document['qualified_count']
                del inserted_document['unqualified_count']
                polish_plan_display_time(inserted_document)
                self.send_response_data(MesCode.success, inserted_document, '')
        except Exception as e:
            log_exception(e, '添加自定义计划失败')
            self.send_response_data(MesCode.fail, None, '添加自定义计划失败')


class PlanDispatchHandler(HttpBasicHandler):
    @loginrequired
    async def post_process(self):
        """
        url: POST /api/plan_management/manage/plan/dispatch
        前端请求后端的数据结构：
        {
            "task_no_list": ["task_no1", "task_no2"],   //需要下发的任务单号列表
            "task_seq_list": ["task_no3", "task_no2","task_no1", "task_no4"],  //所有当天该产线所有任务的生产顺序任务单号列表
            "product_line_code": "product_line_6t90",
            "plan_start_date": "2019-01-10"
        }

        :return:
        {
            "code":"success",
            "info": "",
            "data":
            [
                {
                    "task_no": "A181120203-00",
                    "task_type": "常规产品",
                    "task_date": "2019-01-10",
                    "material_code": "material_t901d40adc24v4",
                    "material_name": "T901D40ADC24V 4脚",
                    "material_spec": "NNC",
                    "material_unit": "个",
                    "plan_count": 4000,
                    "plan_no": "A181120203-00",
                    "plan_start_date": "2019-01-15",
                    "plan_end_date": "2019-01-16",
                    "real_start_date": "",
                    "real_end_date": "",
                    "workshop_name": "六车间",
                    "create_time": "2019-01-14 10:13:38.348108",
                    "erp_plan_status": "",
                    "plan_status": 1,
                    "main_plan_no": "",
                    "special_requirements": "",
                    "workshop_code": "workshop_6",
                    "comment": "",
                    "product_line_code": "product_line_6t90",
                    "operator": "admin",
                    "modified_time": "",
                    "dispatch_time": "2019-01-14 10:42:39.986123",
                    "qualified_count": 0,
                    "unqualified_count": 0,
                    "plan_type": 1
                }
            ]
        }
        """
        try:
            req_data = json.loads(self.request.body)
            task_no_list = req_data['task_no_list']
            task_seq_list = req_data['task_seq_list']
            pl_code = req_data['product_line_code']
            plan_start_date = req_data['plan_start_date']
            plan_collection = get_plan_db_collection()

            # 检查准备下发的计划是否为未下发或者暂停状态
            status_error_msg = await dispatch_plans_check(task_no_list)
            if status_error_msg:
                self.send_response_data(MesCode.fail, None, '下发计划失败: {}'.format(status_error_msg))
                get_logger().info('下发计划失败: {}'.format(status_error_msg))
                return
            # 计算需要下发的计划的顺序号
            seq_num = 0
            task_seq_dict = dict()
            for task_no in task_seq_list:
                seq_num += 1
                task_seq_dict[task_no] = seq_num

            update_plan_list = []
            query = {'task_no': {'$in': task_seq_list}}
            current_time = datetime.now()
            async for document in plan_collection.find(query):
                document_id = document['_id']
                modified_time = str(current_time)
                task_no = document['task_no']
                task_seq = task_seq_dict[task_no]
                update_clause = None
                if task_no in task_no_list:
                    # 如果是本次要下发的计划，则直接更新下发相关字段并赋予序号
                    dispatch_time = str(current_time)
                    update_clause = {'$set': {'dispatch_time': dispatch_time, 'modified_time': modified_time, 'plan_status': PlanStatusType.dispatched.value, 'plan_seq_no': task_seq, 'product_line_code': pl_code, 'plan_start_date': plan_start_date}}
                else:
                    # 如果是已下发的计划顺序调整了，则更新该计划顺序号
                    plan_status = document['plan_status']
                    plan_seq = document['plan_seq_no']
                    if plan_status == PlanStatusType.dispatched.value and plan_seq != task_seq:
                        update_clause = {'$set': {'plan_seq_no': task_seq}}
                if update_clause:
                    update_data = UpdateOne({'_id': document_id}, update_clause)
                    update_plan_list.append(update_data)
                # 批量下发时，目前通过给下一个计划的下发时间添加1微秒来区别顺序
                current_time = current_time + relativedelta(microseconds=+1)
            if update_plan_list:
                # 批量更新计划状态和时间
                plan_collection.bulk_write(update_plan_list)

                updated_documents_cursor = plan_collection.find({'task_no': {'$in': task_no_list}})
                updated_documents = []
                async for updated_document in updated_documents_cursor:
                    del updated_document['_id']
                    polish_plan_display_time(updated_document)
                    updated_documents.append(updated_document)
                self.send_response_data(MesCode.success, updated_documents, '')
                get_logger().info('下发计划成功: {}'.format(updated_documents))
                # 下发成功后更新改天该产线的计划数据到监控app
                await dispatch_plans_to_monitor_app(pl_code, plan_start_date)
            else:
                self.send_response_data(MesCode.fail, None, '下发计划失败: {}'.format(self.data))
                get_logger().info('下发计划失败: {}'.format(self.data))
        except Exception as e:
            log_exception(e, '下发计划失败: {}'.format(self.data))
            self.send_response_data(MesCode.fail, None, '下发计划失败: {}'.format(self.data))


class PlanDeleteHandler(HttpBasicHandler):
    @loginrequired
    async def post_process(self):
        """
        url: POST /api/plan_management/manage/plan/delete
        前端请求后端的数据结构：
        {
            "task_no": "11111"  //需要删除的计划任务单号
        }
        :return:
        {
            "code":"success",
            "info": "",
            "data": null
        }
        """
        try:
            req_data = self.data
            plan_collection = get_plan_db_collection()
            query = {'task_no': req_data['task_no']}
            document = await plan_collection.find_one(query)
            if document:
                plan_status = document['plan_status']
                plan_type = document['plan_type']
                if plan_type == PlanType.erp_import:
                    self.send_response_data(MesCode.fail, None, '删除计划失败: {}, 当前计划为erp导入计划'.format(self.data))
                    get_logger().info('删除计划失败: {}, 当前计划为erp导入计划'.format(self.data))
                elif plan_status == PlanStatusType.in_progress or plan_status == PlanStatusType.paused:
                    self.send_response_data(MesCode.fail, None, '删除计划失败: {}, 当前计划已开始加工'.format(self.data))
                    get_logger().info('删除计划失败: {}, 当前计划已开始加工'.format(self.data))
                else:
                    # 删除该计划，仅当该计划是自定义计划，且未开始加工才能删除
                    plan_collection.delete_one(query)
                    self.send_response_data(MesCode.success, None, '')
            else:
                self.send_response_data(MesCode.success, None, '删除计划失败: {}, 找不到当前计划记录'.format(self.data))
                get_logger().info('删除计划失败: {}, 找不到当前计划记录'.format(self.data))
        except Exception as e:
            log_exception(e, '删除计划失败: {}'.format(self.data))
            self.send_response_data(MesCode.fail, None, '删除计划失败: {}'.format(self.data))


class PlanRollbackHandler(HttpBasicHandler):
    @loginrequired
    async def post_process(self):
        """
        url: POST /api/plan_management/manage/plan/rollback
        前端请求后端的数据结构：
        {
            "task_no": "11111"  //需要回退的计划任务单号
        }
        :return:
        {
            "code":"success",
            "info": "",
            "data": null
        }
        """
        try:
            req_data = self.data
            plan_collection = get_plan_db_collection()
            task_no = req_data['task_no']
            query = {'task_no': task_no}
            document = await plan_collection.find_one(query)
            if document:
                plan_status = document['plan_status']
                if plan_status != PlanStatusType.dispatched.value:
                    self.send_response_data(MesCode.fail, None, '回退计划失败: {}, 当前计划状态不是已下发'.format(self.data))
                    get_logger().info('回退计划失败: {}, 当前计划状态不是已下发'.format(self.data))
                    return
                else:
                    qualified_count = document['qualified_count']
                    unqualified_count = document['unqualified_count']
                    if qualified_count == 0 and unqualified_count == 0:
                        update_plan_status = PlanStatusType.not_dispatched.value
                    else:
                        update_plan_status = PlanStatusType.paused.value
                    # 回退时更新计划状态, 清空产线信息和计划开始日期
                    current_time = datetime.now()
                    modified_time = str(current_time)
                    document_to_rollback = await plan_collection.find_one({'task_no': task_no})
                    if document_to_rollback:
                        # 回退前获取该计划之前下发的产线和开始日期，用于更新计划到监控app
                        pl_code = document_to_rollback['product_line_code']
                        plan_start_date = document_to_rollback['plan_start_date']
                        # 回退该计划
                        document_to_rollback['plan_status'] = update_plan_status
                        document_to_rollback['product_line_code'] = ''
                        document_to_rollback['plan_start_date'] = ''
                        document_to_rollback['dispatch_time'] = ''
                        document_to_rollback['modified_time'] = modified_time
                        await plan_collection.replace_one(query, document_to_rollback)
                        del document_to_rollback['_id']
                        polish_plan_display_time(document_to_rollback)
                        self.send_response_data(MesCode.success, document_to_rollback, '')
                        get_logger().info('回退计划:{}成功, 回退后数据: {}'.format(task_no, document_to_rollback))

                        # 回退成功后更新改天该产线的计划数据到监控app
                        await dispatch_plans_to_monitor_app(pl_code, plan_start_date)
            else:
                self.send_response_data(MesCode.fail, None, '回退计划失败: {}, 找不到当前计划记录'.format(self.data))
                get_logger().info('回退计划失败: {}, 找不到当前计划记录'.format(self.data))
        except Exception as e:
            log_exception(e, '回退计划失败: {}'.format(self.data))
            self.send_response_data(MesCode.fail, None, '回退计划失败: {}'.format(self.data))


class PlanConfigFetchHandler(HttpBasicHandler):
    @loginrequired
    async def get_process(self):
        """
        url: GET /api/plan_management/manage/plan/config
        :return:
        {
            "code":"success",
            "info": "",
            "data":
            {
                "material_config":
                [
                    {
                      "material_code": "557",
                      "material_name": "物料A"
                    }
                ],
                "workshop_config":
                [
                    {
                       "workshop_name": "六车间",
                       "workshop_code": "workshop_6",
                       "pl_list":
                       [
                          {
                            "product_line_code": "product_line_6t90",
                            "product_line_name": "T90继电器生产线"
                          }
                       ]
                    }
                ],
                "custom_fields":
                [
                    {
                        "field_name": "主任务计划号",
                        "field_code": "main_plan_no"
                    },
                    {
                        "field_name": "规格",
                        "field_code": "material_spec"
                    },
                    {
                        "field_name": "特殊要求",
                        "field_code": "special_requirements"
                    },
                ]
            }
        }
        """
        plan_config = dict()
        try:
            plan_pl_config = get_plan_pl_config()
            material_config = get_material_config()
            custom_field_config = get_custom_field_config()

            # 物料配置
            plan_config['material_config'] = material_config

            # 车间产线配置
            plan_config['workshop_config'] = []
            if plan_pl_config:
                for workshop_code, workshop_data_dict in plan_pl_config.items():
                    workshop_name = workshop_data_dict['workshop_name']
                    workshop_config = {'workshop_name': workshop_name, 'workshop_code': workshop_code, 'pl_list': []}
                    if workshop_data_dict['pl_data']:
                        for pl_code, pl_data_dict in workshop_data_dict['pl_data'].items():
                            pl_name = pl_data_dict['name']
                            pl_data = {'product_line_code': pl_code, 'product_line_name': pl_name}
                            workshop_config['pl_list'].append(pl_data)
                    plan_config['workshop_config'].append(workshop_config)

            # 自定义字段配置
            plan_config['custom_fields'] = []
            if custom_field_config:
                for field_code, field_name in custom_field_config.items():
                    field_config = {'field_code': field_code, 'field_name': field_name}
                    plan_config['custom_fields'].append(field_config)
            self.send_response_data(MesCode.success, plan_config, '')
            get_logger().info('获取计划配置成功:{}'.format(plan_config))
        except Exception as e:
            log_exception(e, '获取计划配置失败')
            self.send_response_data(MesCode.fail, None, '获取计划配置失败')


class RemainingDispatchedPlanFetchHandler(HttpBasicHandler):
    async def get_process(self, product_line, plan_start_date):
        """
        url: GET /api/plan_management/manage/(?P<product_line>.*)/(?P<plan_start_date>.*)/dispatched_plan/list
        :param product_line: 产线编码
        :param plan_start_date: 计划开始日期
        :return: 该产线在该计划开始日期当天其余所有已下发过的计划
        {
            "code":"success",
            "info": "",
            "data":
            [
                {
                    "task_no": "11111",
                    "material_name": "物料A",
                    "plan_status": 2, //已下发/1, 进行中/2, 已完工/4
                }
            ]
        }
        """
        plan_list = []
        try:
            # 获取该产线该天所有状态为已下发，进行中和已完工的计划
            query = {'$and': [{'$or': [{'plan_status': PlanStatusType.dispatched.value}, {'plan_status': PlanStatusType.in_progress.value},
                                       {'plan_status': PlanStatusType.finished.value}]}, {'product_line_code': product_line, 'plan_start_date': plan_start_date}]}
            plan_collection = get_plan_db_collection()
            async for document in plan_collection.find(query).sort('plan_seq_no', ASCENDING):
                task_no = document['task_no']
                material_name = document['material_name']
                plan_status = document['plan_status']
                plan_data = {'task_no': task_no, 'material_name': material_name, 'plan_status': plan_status}
                plan_list.append(plan_data)
            self.send_response_data(MesCode.success, plan_list, '')
            get_logger().info('获取产线:{}, 计划开工日期:{}其他已下发过的计划成功: {}'.format(product_line, plan_start_date, plan_list))
        except Exception as e:
            log_exception(e, '获取产线:{}, 计划开工日期:{}其他已下发过的计划失败'.format(product_line, plan_start_date))
            self.send_response_data(MesCode.fail, None, '获取产线:{}, 计划开工日期:{}其他已下发过的计划失败'.format(product_line, plan_start_date))


class PlanDispatchCheckHandler(HttpBasicHandler):
    async def post_process(self):
        """
        url: POST /api/plan_management/manage/plan/dispatch_check
        前端请求后端的数据结构：
        ["task_no1", "task_no2"]
        :return:
        {
            "code":"success",
            "info": "",  //失败会给出具体失败原因
            "data": null
        }
        """
        task_no_list = json.loads(self.request.body)
        try:
            # 检查准备下发的计划是否为未下发或者暂停状态
            error_msg = await dispatch_plans_check(task_no_list)
            if error_msg:
                self.send_response_data(MesCode.fail, None, error_msg)
                get_logger().info('下发计划前检查失败: {}'.format(error_msg))
            else:
                self.send_response_data(MesCode.success, None, '')
                get_logger().info('下发计划前检查成功')
        except Exception as e:
            log_exception(e, '检查即将下发计划异常:{}'.format(task_no_list))


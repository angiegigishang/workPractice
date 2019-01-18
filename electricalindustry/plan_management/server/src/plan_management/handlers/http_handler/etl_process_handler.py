from mg_app_framework import HttpBasicHandler, MesCode, get_logger
from plan_management.handlers.utils import log_exception, get_plan_db_collection, PlanStatusType, PlanType, ErpPlanStatus
from datetime import datetime
from pymongo import ReplaceOne
import json


class ErpPlanTransferHandler(HttpBasicHandler):
    async def post_process(self):
        """
        url: POST /api/plan_management/erp_plan/transfer
        发送数据app发往计划管理app数据结构:
        {
            "plan_list":
            [
                {
                    "task_no": "A181120203-00", //字段task_serial, 必要字段
                    "task_type": "常规产品",  //字段task_type, 可选字段
                    "task_date": "2019-01-09", //字段task_date， 可选字段
                    "material_code": "materiel_t901h40adc12v4_23", //字段product_code， 必要字段
                    "material_name": "T901H40ADC12V 4脚 23规格",  //字段product_name， 必要字段
                    "material_spec": "NNC", //字段product_spec, 可选字段
                    "material_unit": "个", //字段product_unit， 必要字段
                    "plan_count": 1000,  //字段plan_num， 必要字段
                    "plan_no": "A181120203-00",  //字段plan_serial, 可选字段
                    "plan_start_date": "2019-01-10", //字段plan_start， 必要字段
                    "plan_end_date": "2019-01-12",  //字段plan_end， 必要字段
                    "real_start_date": "2019-01-10", //字段real_start, 可选字段
                    "real_end_date": "2019-01-12", //字段real_end, 可选字段
                    "workshop_name": "六车间",  //字段work_center， 必要字段
                    "create_time": "2019-01-10", //字段chage_time， 必要字段
                    "erp_plan_status": "投放",  //字段plan_status对应状态文字(1.锁定，2.确认，3.下达，4.投放，5.流转，6.暂停, 7.完工), 可选字段
                    "plan_status": "可下发"  //3种状态，可下发，已完成和不可下发, 这个字段值由上一个字段erp_plan_status决定
                }
            ]
        }
        :return:
        {
            "code":"success",
            "info": "",
            "data": null
        }
        """
        from plan_management.handlers.sds import get_material_id_code_dict, get_workshop_name_code_dict, get_custom_field_config
        etl_req_data = json.loads(self.request.body)
        plan_data_list = etl_req_data['plan_list']
        plan_collection = get_plan_db_collection()
        try:
            if plan_data_list:
                material_id_code_dict = get_material_id_code_dict()
                workshop_name_code_dict = get_workshop_name_code_dict()
                custom_field_config = get_custom_field_config()
                plan_upsert_list = []
                for plan_data in plan_data_list:
                    task_no = plan_data['task_no']
                    existing_plan = await plan_collection.find_one({'task_no': task_no})
                    # 处理定制字段, 如果一个定制字段对应的计划不存在，且该字段不在请求数据字段中，则置空
                    if custom_field_config:
                        for field_code in custom_field_config:
                            if not existing_plan and field_code not in plan_data:
                                plan_data[field_code] = ''

                    # ERP传过来的物料编码对应主数据内的物料编号，需要转为对应的物料编码
                    # 暂时完全使用erp过来的编码，后期如果有需求更新再改
                    # material_identifier = plan_data['material_code']
                    # if material_identifier in material_id_code_dict:
                    #     material_code = material_id_code_dict[material_identifier]
                    # else:
                    #     # 如果物料编码找不到则直接保存
                    #     material_code = material_identifier
                    # plan_data['material_code'] = material_code

                    # 获取车间编码
                    workshop_name = plan_data['workshop_name']
                    workshop_code = workshop_name_code_dict[workshop_name]
                    plan_data['workshop_code'] = workshop_code

                    # ERP传过来的计划状态需要转为计划管理内部的状态值
                    plan_status = plan_data['plan_status']
                    if plan_status == ErpPlanStatus.can_dispatch.value:
                        plan_data['plan_status'] = PlanStatusType.not_dispatched.value
                    elif plan_status == ErpPlanStatus.cant_dispatch.value:
                        plan_data['plan_status'] = PlanStatusType.cant_dispatch.value
                    elif plan_status == ErpPlanStatus.finished.value:
                        plan_data['plan_status'] = PlanStatusType.finished.value

                    # 添加其他必须字段
                    plan_data['comment'] = ''
                    plan_data['product_line_code'] = ''
                    plan_data['operator'] = ''
                    # 录入时间写入当前时间
                    if not existing_plan:
                        # 仅当该计划不存在时写入录入时间
                        plan_data['create_time'] = str(datetime.now())
                        plan_data['modified_time'] = ''
                    else:
                        # 如果该计划已存在，则需要更新修改时间
                        plan_data['modified_time'] = str(datetime.now())
                    plan_data['dispatch_time'] = ''
                    plan_data['qualified_count'] = 0
                    plan_data['unqualified_count'] = 0
                    plan_data['plan_type'] = PlanType.erp_import.value

                    update_query = {'task_no': task_no}
                    plan_upsert_data = ReplaceOne(update_query, plan_data, upsert=True)
                    plan_upsert_list.append(plan_upsert_data)

                if plan_upsert_list:
                    # 批量更新计划
                    plan_collection.bulk_write(plan_upsert_list)
            self.send_response_data(MesCode.success, plan_data_list, '')
            get_logger().info('从ERP更新计划数据成功:{}'.format(plan_data_list))
        except Exception as e:
            log_exception(e, '从ERP更新计划数据失败')
            self.send_response_data(MesCode.fail, None, '从ERP更新计划数据失败')

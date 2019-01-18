from json import loads
from datetime import datetime

from mg_app_framework import HttpBasicHandler, MesCode, get_context, get_handler, TaskKey, get_logger

from wage_settlement.process.extrenal_api import get_report_info, get_working_hour_info
from wage_settlement.process.const_values import TIMELY_WAGE_TYPE_MAPPER, PEICE_WAGE
from wage_settlement.process.db_operator import get_target_mongo_collection


class WebHandler(HttpBasicHandler):
    async def get_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success get data')

    async def post_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success post data')


class MaterielGroupPriceHandler(HttpBasicHandler):
    # 返回或更新物料分组对应工序计件单价
    async def get_process(self, *args, **kwargs):
        # 尝试从请求url中获取get_argument，根据指定的员工返回对应的工序-物料单价内容
        person_code = self.get_argument('person_code', None)
        self.target_process_codes = None
        if person_code is not None:
            self.get_person_fz_group(person_code)

        # 数据库中信息
        col = get_target_mongo_collection('process_materiel_price')
        all_price_info = col.find({}, {'_id': 0, 'process': 1, 'materiel_group': 1, 'price': 1})
        all_price_info = list(all_price_info)

        process_info = get_context('process_info')
        materiel_group_info = get_context('materiel_group_info')

        response_columns = [{
            'name': 'process',
            'label': '工序',
            'field': 'process'
        }]
        response_mapper = []
        response_row_data = []
        for m in materiel_group_info:
            response_columns.append({
                'name': m['code'],
                'label': m['name'],
                'field': m['code']
            })
            response_mapper.append({
                'code': m['code'],
                'name': m['name'],
                'materiel_names': m['materiel_names']
            })

        for p in process_info:
            process_name = p['name']
            process_code = p['code']
            response_record = {
                'process': process_name,
                'process_code': process_code
            }

            # TODO: 此段代码需要优化
            if self.target_process_codes:
                if process_code in self.target_process_codes:
                    for m in materiel_group_info:
                        materiel_group_code = m['code']
                        materiel_group_name = m['name']
                        target_record = filter(
                            lambda x: x['process'] == process_code and x['materiel_group'] == materiel_group_code,
                            all_price_info)
                        try:
                            target_value = next(target_record)
                            response_record.update({
                                materiel_group_code: target_value.setdefault('price', '')
                            })
                        except Exception:
                            response_record.update({
                                materiel_group_code: ''
                            })
                    response_row_data.append(response_record)
            else:
                for m in materiel_group_info:
                    materiel_group_code = m['code']
                    materiel_group_name = m['name']
                    target_record = filter(
                        lambda x: x['process'] == process_code and x['materiel_group'] == materiel_group_code,
                        all_price_info)
                    try:
                        target_value = next(target_record)
                        response_record.update({
                            materiel_group_code: target_value.setdefault('price', '')
                        })
                    except Exception:
                        response_record.update({
                            materiel_group_code: ''
                        })
                response_row_data.append(response_record)

        response = {
            'columns': response_columns,
            'rows': response_row_data,
            'mapper': response_mapper
        }
        self.send_response_data(MesCode.success, response, 'get process/materiel_group price mapper succefully')

    async def post_process(self, *args, **kwargs):
        # 数据库中信息
        col = get_target_mongo_collection('process_materiel_price')

        request_body = loads(self.request.body)
        del request_body['process']
        process_code = request_body['process_code']
        del request_body['process_code']
        for k, v in request_body.items():
            col.update({'process': process_code, 'materiel_group': k}, {'$set': {'price': v}},
                       upsert=True)

        self.send_response_data(MesCode.success, None, 'update price info successfully')

    def get_person_fz_group(self, person_code):
        fz_group_info = get_context('group_info')
        for fz in fz_group_info:
            fz_members = fz['members']
            fz_process = fz['processCodes']
            for m in fz_members:
                if m['code'] == person_code:
                    self.target_process_codes = fz_process


class WageDetailHandler(HttpBasicHandler):
    async def get_process(self, *args, **kwargs):
        try:
            report_info = await get_report_info()
            individual_piece_wage = self.process_report_detail(report_info)
            individual_timely_wage = await self.process_timely_wage_detail()
            individual_piece_wage.extend(individual_timely_wage)
            self.send_response_data(MesCode.success, individual_piece_wage, 'get wage detail successfully')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))

    def process_report_detail(self, report_detail):
        # TODO: 此处需要将具体的工资计算方法加入，几个for循环可分别作为函数处理

        # 获取数据库链接
        col = get_target_mongo_collection('process_materiel_price')

        # 从内存中获取报工分组信息
        bg_group_info = get_context('group_info')
        materiel_group_info = get_context('materiel_group_info')
        individual_wage = []
        for g in report_detail:
            group_code = g['groupCode']
            target_group_info = filter(lambda x: x['groupCode'] == group_code, bg_group_info)
            target_group_members = []
            target_group_processes = []
            group_total_wage = 0
            group_total_materiel_amount = 0
            for x in target_group_info:
                target_group_members = x['members']
                target_group_processes = x['processCodes']
            for r in g['report']:
                # 查找物料分组，如果没有找到，使用默认分组
                try:
                    materiel_code = r['materielCode']
                    target_materiel = filter(lambda x: materiel_code in x['materiel_list'], materiel_group_info)
                    target_materiel_group_code = next(target_materiel)['code']
                except StopIteration:
                    get_logger().exception('materiel: {} get lost'.format(materiel_code))
                    # TODO:此处默认物料暂时写死，后边可以从主数据获取
                    target_materiel_group_code = 'materiel_group_instance_default'
                    get_logger().info('use code:{}'.format(target_materiel_group_code))

                materiel_amount = r['qualified_count']
                group_total_materiel_amount += materiel_amount
                group_materiel_price_info = col.find(
                    {'materiel_group': target_materiel_group_code, 'process': {'$in': target_group_processes}},
                    {'_id': 0})
                group_total_price = 0
                for p in group_materiel_price_info:
                    p_value = p.setdefault('price', 0)
                    if not p_value:
                        p_value = 0
                    group_total_price += float(p_value)
                get_logger().info('group: {} => total price: {}'.format(target_materiel_group_code, group_total_price))
                group_total_wage += group_total_price * materiel_amount

            get_logger().info('group: {} => total wage: {}'.format(group_code, group_total_wage))
            member_count = len(target_group_members)
            avg_wage = round(group_total_wage / member_count, 2)
            avg_amount = int(group_total_materiel_amount / member_count)
            for m in target_group_members:
                person_piece_wage = {
                    'wage': avg_wage,
                    'person_code': m['code'],
                    'person_name': m['name'],
                    'workshop': m['workshop'],
                    'pipeline': m['pipeline'],
                    'wage_type': PEICE_WAGE['name'],
                    'piece_amount': avg_amount,
                    'total_time': None,
                    'wage_code': 'piece'
                }
                individual_wage.append(person_piece_wage)
        return individual_wage

    async def process_timely_wage_detail(self):
        person_code_name_mapper = get_context('person_code_name_mapper')
        response = []
        # 获取数据库链接
        col = get_target_mongo_collection('timely_wage')

        all_timely_wage_detail = col.find({}, {'_id': 0})
        query_time = datetime.now()
        for d in all_timely_wage_detail:
            person_code = d['person']
            person_name = person_code_name_mapper[person_code]
            wage_type = d['wage_type']
            price = d['price']
            person_working_hour = await get_working_hour_info({
                'year': query_time.year,
                'month': query_time.month,
                'person_list': [
                    {
                        'person_code': person_code,
                        'wage_type': wage_type
                    }
                ]
            })
            person_wage = price * person_working_hour[person_code]
            # TODO:此处人员对应产线需要动态获取
            response.append({
                'wage': person_wage,
                'person_code': person_code,
                'person_name': person_name,
                'workshop': '六车间',
                'pipeline': 'T90继电器生产线',
                'wage_type': TIMELY_WAGE_TYPE_MAPPER[wage_type],
                'piece_amount': None,
                'total_time': person_working_hour[person_code],
                'wage_code': 'time'
            })
        return response




class TimelyWageHandler(HttpBasicHandler):
    async def get_process(self, *args, **kwargs):
        self.person_code = self.get_argument('person_code', None)
        timely_wage_info = self.get_timely_wage_info()
        self.send_response_data(MesCode.success, timely_wage_info, 'get timely_wage_info successfully')

    async def post_process(self, *args, **kwargs):
        try:
            self.process_timely_wage_info()
            self.send_response_data(MesCode.success, None, 'update wage info successfully')
        except Exception as e:
            self.send_response_data(MesCode.fail, None, str(e))

    def get_timely_wage_info(self):
        col = get_target_mongo_collection('timely_wage')

        # 获取人员列表
        person_code_name_mapper = get_context('person_code_name_mapper')

        all_info = []
        if self.person_code:
            all_timely_wage_info = col.find({'person': self.person_code}, {'_id': 0})
        else:
            all_timely_wage_info = col.find({}, {'_id': 0})
        for i in all_timely_wage_info:
            i_price = i.setdefault('price', '')
            p_code = i['person']
            p_name = person_code_name_mapper.get(p_code, '')
            wage_type_code = i['wage_type']
            wage_type_name = TIMELY_WAGE_TYPE_MAPPER.get(wage_type_code, '')
            all_info.append({
                'person_code': p_code,
                'person_name': p_name,
                'wage_code': wage_type_code,
                'wage_name': wage_type_name,
                'price': i_price
            })
        return all_info

    def process_timely_wage_info(self):
        request_body = loads(self.request.body)
        person_code = request_body['person_code']
        wage_code = request_body['wage_code']
        price = request_body['price']
        try:
            price = float(price)
        except:
            price = 0

        # 获取数据库handler
        col = get_target_mongo_collection('timely_wage')
        col.update({'person': person_code}, {'$set': {'wage_code': wage_code, 'price': price}})

        get_logger().info('update timely wage for {}'.format(person_code))

from mg_app_framework import update_context, get_logger


def sync_materiel_group(msg):
    materiel_group_list = []
    if msg[0]['children']:
        msg = msg[0]['children'][0].setdefault('instance_list', [])
        for g in msg:
            group_code = g['code']
            group_name = g['name']
            group_materiel_list = []
            group_materiel_name_list = []
            if g['children']:
                group_detail = g['children'][0].setdefault('instance_list', [])
                for x in group_detail:
                    group_materiel_list.append(x['code'])
                    group_materiel_name_list.append(x['name'])

                materiel_group_list.append({
                    'code': group_code,
                    'name': group_name,
                    'materiel_list': group_materiel_list,
                    'materiel_names': group_materiel_name_list
                })
        update_context('materiel_group_info', materiel_group_list)
        get_logger().info('materiel_group_info sync')
        get_logger().info(materiel_group_list)


def sync_group_info(msg):
    if msg[0]['children']:
        pipeline_info = msg[0]['children'][0].setdefault('instance_list', [])
        get_logger().info('pipeline info')

        group_info = []
        for pipeline in pipeline_info:
            pipeline_group = pipeline['children']
            pipeline_name = pipeline['name']

            pipeline_process_in_memeory = []
            pipeline_process_codes_in_memeory = []

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
                                'workshop': p['classify'],
                                'pipeline': pipeline_name
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

            get_logger().info('*' * 20)
            get_logger().info(group_info)

        update_context('group_info', group_info)


def sync_timely_wage_info(msg):
    msg = msg[0]['children']
    timely_wage_info = {}
    for m in msg:
        wage_type = m['directory_code']
        if m['children']:
            for p in m['children'][0].setdefault('instance_list', []):
                timely_wage_info.update({
                    p['code']: wage_type
                })

    update_context('timely_wage_info', timely_wage_info)
    get_logger().info(timely_wage_info)

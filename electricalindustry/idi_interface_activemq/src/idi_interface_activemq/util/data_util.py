from mg_app_framework import get_context,get_logger


def get_code_map_dict(product_line):
    # 从内存中获取信息
    response = {}
    pipeline_device_in_memory = get_context('pipeline_device')
    target_pipeline_info = pipeline_device_in_memory.get(product_line, {})
    pipeline_response = response.setdefault(product_line, {})
    for value in target_pipeline_info.values():
        process_list = value.setdefault('process', [])
        if process_list:
            process_code = process_list[0]['code']
        if process_code:
            point_response = {}
            point_list = value.setdefault('point', [])
            for p in point_list:
                if p['classify'] == '状态':
                    point_response.update({
                        'status': p['code']
                    })
                elif p['classify'] == '数量':
                    point_response.update({
                        'positive': p['code']
                    })
                elif p['classify'] == '不合格数':
                    point_response.update({
                        'negative': p['code']
                    })
            pipeline_response.update(
                {
                    process_code: point_response
                }
            )
    return response


def get_status_code_map(product_line):
    process_map_code_dict = get_code_map_dict(product_line)[product_line]
    # get_logger().info("process_map_code_dict~~~~~~~~~~~~~~~~~~~~~~~:%s",process_map_code_dict)
    status_process_map_dict = {}
    for process_code , item in process_map_code_dict.items():
        if "status" in item:
            status_code = item["status"]
            status_process_map_dict[status_code] = process_code
    return status_process_map_dict




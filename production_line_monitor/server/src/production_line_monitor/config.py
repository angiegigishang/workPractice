from os.path import dirname, realpath, basename, join
from mg_app_framework import AppType, AppConfigBasic, MongodbConfigBasic


class MongodbConfig(MongodbConfigBasic):
    def get_mongodb_host(self):
        # return "192.168.20.106,192.168.20.107,192.168.20.108"
        return "127.0.0.1"

    def get_mongodb_port(self):
        return "27017"


class ConfigStore(AppConfigBasic):
    # ==================== DON'T MODIFY THE CODE BETWEEN COMMENT LINE ====================

    work_dir = dirname(dirname(dirname(realpath(__file__))))
    app = basename(dirname(realpath(__file__)))
    log_path = join(work_dir, 'log', app + '.log')
    uuid_path = join(work_dir, '.appid')

    def get_module_dir(self):
        return dirname(realpath(__file__))

    def get_log_path(self):
        return self.log_path

    def get_uuid_path(self):
        return self.uuid_path

    def get_data(self):
        return self.data

    # ==================== DON'T MODIFY THE CODE BETWEEN COMMENT LINE ====================

    data = {
        'app_group': '乐清工业云',
        'app_name': '产线监控',
        'switch': True,
        'app_type': AppType.user,
        'config_create': True,
        'data': {
            'key_list': ['schedule_settings', 'idi_config'],
            'config_data': {
                'schedule_settings': {
                    'group_name': '运行设置',
                    'key_list': ['cron_set'],
                    'group_member': {
                        'cron_set': {
                            'key_name': '运行时间',
                            'key_type': 'cron',
                            'key_help': 'date时间设置,不填默认为立刻生效',
                            'value': {
                                'year': ['*'],
                                'month': ['*'],
                                'day': ['*'],
                                'day_of_week': ['*'],
                                'hour': ['*'],
                                'minute': ['*'],
                                'second': ['*/10']
                            }
                        }
                    }
                },
                'idi_config': {
                    'group_name': 'opc配置',
                    'key_list': ['onwork_attendance_url', 'idi_url', 'idi_lastest_url',
                                 'kpi_monitor_msg_post_url', 'idi_server_wsurl'],
                    'group_member': {
                        'onwork_attendance_url': {
                            'key_name': 'onwork_attendance_url',
                            'key_type': 'string',
                            'key_help': 'onwork_attendance_url',
                            'value': 'http://192.168.20.128:12020/api/attendance_manage/pipeline/{}/onwork_attendance'
                        },
                        'idi_url': {
                            'key_name': 'idi系统opc点位url设置',
                            'key_type': 'string',
                            'key_help': '通过idi系统获取opc点位数据',
                            'value': 'http://192.168.20.181:8081/api/v1/idi/history/datas'
                        },
                        'idi_lastest_url': {
                            'key_name': '历史数据N条查询接口',
                            'key_type': 'string',
                            'key_help': '访问历史数据接口code_list:[{code,start_time,end_time}...]',
                            'value': 'http://192.168.20.181:8081/api/v1/idi/lastest/history/tags'
                        },
                        'idi_server_wsurl': {
                            'key_name': 'interface_server_url',
                            'key_type': 'string',
                            'key_help': 'idi_server_ws',
                            'value': 'ws://192.168.20.181:8180/interfaceappconn'
                        },
                        'scheduling_instruction_url': {
                            'key_name': 'scheduling_instruction_url',
                            'key_type': 'string',
                            'key_help': 'scheduling_instruction',
                            'value': 'http://192.168.20.187:8194/api/v1/scheduling_instruction/msg/post'
                        },
                        'get_scheduling_instruction_url': {
                            'key_name': 'get_scheduling_instruction_url',
                            'key_type': 'string',
                            'key_help': 'scheduling_instruction',
                            'value': 'http://192.168.20.187:8194/api/v1/scheduling_instruction/get/lastest_instruction'
                        },
                        'idi_write_url': {
                            'key_name': 'idi_write_url',
                            'key_type': 'string',
                            'key_help': 'idi_write_url',
                            'value': 'http://192.168.20.181:8180/api/v1/idi/insert/datas'
                        },
                        'dispatched_plan_url': {
                            'key_name': 'get_plan_url',
                            'key_type': 'string',
                            'key_help': 'get_plan_url',
                            'value': 'http://192.168.20.140:9001/api/plan_management/manage/%s/dispatched_plan/list'
                        },
                        'update_plan_url': {
                            'key_name': 'update_plan_url',
                            'key_type': 'string',
                            'key_help': 'update_plan_url',
                            'value': 'http://192.168.20.140:9001/api/plan_management/plan/status_update'
                        },
                    }
                }
            }
        }
    }

    def get_admin_host(self):
        return '192.168.20.181'

    def get_app_port(self):
        return 8989

    def get_idi_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_url']['value']

    def get_idi_server_wsurl(self):
        # return self.data['data']['config_data']['idi_server_setting']['group_member']['websocket_url']['value']
        return self.data['data']['config_data']['idi_config']['group_member']['idi_server_wsurl']['value']

    def get_idi_server_wskey(self):
        # return self.data['data']['config_data']['idi_server_setting']['group_member']['websocket_url']['key_name']
        return self.data['data']['config_data']['idi_config']['group_member']['idi_server_wsurl']['key_name']

    def get_idi_lastest_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_lastest_url']['value']

    def get_scheduling_instruction_key(self):
        return self.data['data']['config_data']['idi_config']['group_member']['scheduling_instruction_url']['key_name']

    def get_scheduling_instruction_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['scheduling_instruction_url']['value']

    def get_get_scheduling_instruction_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['get_scheduling_instruction_url']['value']

    def get_idi_write_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_write_url']['value']

    def get_onwork_attendance_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['onwork_attendance_url']['value']

    def get_dispatched_plan_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['dispatched_plan_url']['value']

    def get_update_plan_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['update_plan_url']['value']


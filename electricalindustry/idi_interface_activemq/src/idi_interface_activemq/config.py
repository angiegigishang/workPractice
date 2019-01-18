from os.path import dirname, realpath, basename, join
from mg_app_framework import AppType, AppConfigBasic,MongodbConfigBasic


class MongodbConfig(MongodbConfigBasic):
    def get_mongodb_host(self):
        # return "192.168.20.106,192.168.20.107,192.168.20.108"
        return "localhost"

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
        'app_group': 'idi',
        'app_name': 'idi_interface_activemq',
        'switch': True,
        'app_type': AppType.date,
        'config_create': True,
        'data': {
            'key_list': ['schedule_settings','idi_config'],
            'config_data': {
                'schedule_settings': {
                    'group_name': '运行设置',
                    'key_list': ['date_set'],
                    'group_member': {
                        'date_set': {
                            'key_name': '运行时间',
                            'key_type': 'datetime',
                            'key_help': 'date时间设置,不填默认为立刻生效',
                            'value': None
                        }
                    }
                },
                'idi_config': {
                    'group_name': 'opc配置',
                    'key_list': ['idi_url', 'idi_write_url','idi_server_wsurl'],
                    'group_member': {
                        'idi_url': {
                            'key_name': 'idi系统opc点位url设置',
                            'key_type': 'string',
                            'key_help': '通过idi系统获取opc点位数据',
                            'value': 'http://192.168.102.231:8081/api/v1/idi/history/datas'
                        },
                        'idi_write_url': {
                            'key_name': 'idi_write_url',
                            'key_type': 'string',
                            'key_help': 'idi_write_url',
                            'value': 'http://192.168.20.252:9090/api/v1/idi/insert/datas'
                        },
                        'idi_server_wsurl': {
                            'key_name': 'interface_server_url',
                            'key_type': 'string',
                            'key_help': 'idi_server_ws',
                            'value': 'ws://192.168.20.181:8180/interfaceappconn'
                        },
                        'kpi_monitor_msg_post_url': {
                            'key_name': 'cfg_server1_url',
                            'key_type': 'string',
                            'key_help': 'kpi_monitor_msg_post url',
                            'value': 'http://192.168.20.6:8169/api/v1/kpi_monitor/msg/post'
                        },
                    }
                }
            }
        }
    }

    def get_admin_host(self):
        return '192.168.20.181'

    def get_app_port(self):
        return 8900


    def get_idi_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_url']['value']

    def get_idi_write_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_write_url']['value']

    def get_idi_server_wsurl(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_server_wsurl']['value']

    def get_idi_server_wskey(self):
        return self.data['data']['config_data']['idi_config']['group_member']['idi_server_wsurl']['key_name']

    def get_kpi_monitor_msg_post_url(self):
        return self.data['data']['config_data']['idi_config']['group_member']['kpi_monitor_msg_post_url']['value']

    def get_kpi_monitor_msg_post_key(self):
        return ""

    def get_scheduling_instruction_key(self):
        return ""

    def get_scheduling_instruction_url(self):
        return ""
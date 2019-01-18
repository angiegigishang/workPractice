from os.path import dirname, realpath, basename, join
from mg_app_framework import AppConfigBasic, AppType, MongodbConfigBasic, SdsConfigBasic, InitFuncBasic
from plan_management.handlers.sds import plan_msg_keys, plan_sds_msg_processor


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
        'app_name': '计划管理',
        'app_type': AppType.user,
        'config_create': True,
        'data': {
            'key_list': ['app_url_settings'],
            'config_data': {
                'app_url_settings': {
                    'group_name': 'electrical industry',
                    'key_list': ['production_monitor_url'],
                    'group_member': {
                        'production_monitor_url': {
                            'key_name': '生产监控app url',
                            'key_type': 'string',
                            'key_help': '生产监控app url',
                            'value': 'http://192.168.20.114:8989'
                        }
                    }
                }
            }
        }
    }

    def get_admin_host(self):
        return 'localhost'

    def get_app_port(self):
        return 9001

    def connect_admin(self):
        return False

    def get_login_switch(self):
        return False

    def cross_domain(self):
        return False

    def get_production_monitor_app_url(self):
        return self.data['data']['config_data']['app_url_settings']['group_member']['production_monitor_url']['value']


class MongodbConfig(MongodbConfigBasic):
    def get_mongodb_host(self):
        return "192.168.20.140"

    def get_mongodb_port(self):
        return '27017'


class SdsConfig(SdsConfigBasic):
    def get_consume_list(self):
        return plan_msg_keys

    def get_produce_list(self):
        return []

    def get_sds_host(self):
        return '192.168.20.181'

    async def msg_process(self, data):
        await plan_sds_msg_processor(data)

    def get_organization_code(self):
        return 'organization_xldq'


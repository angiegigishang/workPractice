from os.path import dirname, realpath, basename, join
from mg_app_framework import AppType, AppConfigBasic, MongodbConfigBasic


class MongoConfigStore(MongodbConfigBasic):

    def get_mongodb_host(self):
        return '192.168.20.120,192.168.20.170,192.168.20.183'
        # return 'localhost'

    def get_mongodb_port(self):
        return 27010


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
        'app_name': '考勤管理',
        'app_type': AppType.service,
        'config_create': True,
        'data': {
            'api': {
                'monitor_push': 'http://192.168.20.114:8989/api/monitor/recevie_checkin/{}'
            }
        }
    }

    def get_admin_host(self):
        return '192.168.20.125'

    def get_app_port(self):
        return 12020

    def connect_admin(self):
        return False

    def cross_domain(self):
        return False

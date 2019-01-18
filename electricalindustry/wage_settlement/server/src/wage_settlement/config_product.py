from os.path import dirname, realpath, basename, join
from mg_app_framework import AppConfigBasic, AppType, MongodbConfigBasic


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
        'app_name': '工资管理',
        'app_type': AppType.user,
        'config_create': True,
        'data': {
            'api': {
                'report': 'http://192.168.20.182:9000/api/progress_report/report/current_month',
                'working_hour': 'http://192.168.20.182:12020/api/attendance_manage/working_hours'
            }
        }
    }

    def get_admin_host(self):
        return '192.168.20.182'

    def get_app_port(self):
        return 11010

    def connect_admin(self):
        return True

    def cross_domain(self):
        return True

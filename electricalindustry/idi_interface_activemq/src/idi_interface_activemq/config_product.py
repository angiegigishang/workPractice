from os.path import dirname, realpath, basename, join
from mg_app_framework import AppType, AppConfigBasic


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
        'app_group': '',
        'app_name': '',
        'switch': False,
        'app_type': AppType.date,
        'config_create': True,
        'data': {
            'key_list': ['schedule_settings'],
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
                }
            }
        }
    }

    def get_admin_host(self):
        return 'localhost'

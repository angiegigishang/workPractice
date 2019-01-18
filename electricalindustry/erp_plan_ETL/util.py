import decimal
import datetime
import win32api
import win32con
import logging


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        # return obj.isoformat()
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def auto_run_in_windows(project_name, project_path):
    name = project_name  # 要添加的项值名称
    path = project_path  # 要添加的exe路径
    # 注册表项名
    key_name = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    # 异常处理
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,  key_name, 0,  win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(key)
        logging.info('自启动添加成功！')
    except Exception as e:
        logging.info(e)


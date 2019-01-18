import sqlalchemy
from sqlalchemy.orm import sessionmaker
import logging
import os
import sys
from handlers.work_order_handler import read_cfg, get_dbcfg, find_and_send_task
import asyncio
from threading import Thread


def set_log():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_name = 'xlgf_erp_cloud.log'
    logfile = log_name
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    # 设置日志
    set_log()
    try:
        logging.info("\n#######################"
                     "\n#### program start ####"
                     "\n#######################")

        project_path = os.path.realpath(sys.argv[0])

        # 设置自启动
        # util.auto_run_in_windows("xlgf_erp_cloud", project_path)

        logging.info("configure start")
        if read_cfg(os.path.dirname(project_path)) is False:
            return
        sqlserver_host, dbname = get_dbcfg()
        logging.info("configure end")

        logging.info("sqlserver connecting start")
        sqlserver_engine = sqlalchemy.create_engine(sqlserver_host + dbname + '?charset=GBK', pool_size=100)  # GBK
        Session = sessionmaker(bind=sqlserver_engine)
        logging.info("sqlserver connecting end")

        new_loop = asyncio.new_event_loop()
        t = Thread(target=start_loop, args=(new_loop,))
        t.start()
        logging.info("start find_and_send_task")
        asyncio.run_coroutine_threadsafe(find_and_send_task(Session, new_loop), new_loop)
        t.join()
    except Exception as e:
        logging.info(e)
        logging.info(str(e))
    finally:
        logging.info("program exit")


if __name__ == "__main__":
    main()

from sqlalchemy import Column, String, Numeric, INTEGER, DateTime
from entities.base import Base


class Task(Base):
    __tablename__ = 'vw_task_plan'
    task_type = Column(String(100), default='生产入库')            # 工单类型
    task_serial = Column(String(100), primary_key=True)           # 工单编号
    task_date = Column(String(30))                                # 开单日期
    product_code = Column(String(20))                             # 产品品号
    product_unit = Column(String(20))                             # 产品单位
    product_name = Column(String(60))                             # 产品品名
    product_spec = Column(String(60))                             # 产品规格
    work_center = Column(String(60))                              # 地点名称
    plan_num = Column(Numeric)                                    # 预计产量
    plan_status = Column(INTEGER)                                 # 工单状态(1.锁定，2.确认，3.下达，4.投放，5.流转，7.完工，6.暂停)
    plan_serial = Column(String(60))                              # 计划批号
    plan_start = Column(String(30))                               # 预计开工(YMD)
    plan_end = Column(String(30))                                 # 预计完工(YMD)
    real_start = Column(String(30))                               # 实际开工
    real_end = Column(String(30))                                 # 实际完工
    chage_time = Column(DateTime)                                 # 更新时间
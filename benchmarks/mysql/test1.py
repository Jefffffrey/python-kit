"""
1个并发
"""

import random

from sqlalchemy import create_engine

from utils import qps

engine = create_engine("mysql://root:@127.0.0.1:3306/employees", echo=False)


def read_data_v1(times):
    """最快的版本，QPS高达6000"""
    query = "select  emp_no from `employees` where emp_no = 30000"
    for _ in range(times):
        engine.execute(query)


def read_data_v2(times):
    """查找多个值"""
    query = "select * from `employees` where emp_no = 30000"
    for _ in range(times):
        engine.execute(query)


def read_data_v3(times):
    """随机id, JOIN语法"""
    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        engine.execute("".join(["select * from `employees` where emp_no = ", str(emp_no)]))


def read_data_v4(times):
    """随机id, +语法"""
    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        engine.execute("select SQL_NO_CACHE * from `employees` where emp_no = " + str(emp_no))


def read_data_v5(times):
    """随机id, format语法"""
    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        engine.execute("select  SQL_NO_CACHE * from `employees` where emp_no = {}".format(emp_no))


def read_data_v6(times):
    """随机id, JOIN语法, 异常处理"""
    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        error_count = 0
        while 1:
            try:
                engine.execute("".join(["select  SQL_NO_CACHE * from `employees` where emp_no = ", str(emp_no)]))
                break
            except Exception as e:
                print(e)
                error_count += 1
                if error_count > 100:
                    print(e)
                continue


read_data = read_data_v1

# 预热
qps(read_data, (30000,), number=30000)

qps(read_data, (1,), number=1)
qps(read_data, (10,), number=10)
qps(read_data, (100,), number=100)
qps(read_data, (1000,), number=1000)
qps(read_data, (10000,), number=10000)

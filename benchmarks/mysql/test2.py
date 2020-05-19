"""
MySQLdb
[python - Why is loading SQLAlchemy objects via the ORM 5-8x slower than rows via a raw MySQLdb cursor? - Stack Overflow](https://stackoverflow.com/questions/23185319/why-is-loading-sqlalchemy-objects-via-the-orm-5-8x-slower-than-rows-via-a-raw-my)
"""

import random

import MySQLdb

from utils import qps

db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="employees")
cur = db.cursor()


def read_data(times):
    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        cur.execute("".join(["select * from `employees` where emp_no = ", str(emp_no)]))
        cur.fetchall()


def read_data_v1(times):
    for _ in range(times):
        cur = db.cursor()
        emp_no = random.randint(10001, 499999)
        cur.execute("".join(["select * from `employees` where emp_no = ", str(emp_no)]))
        cur.fetchall()


read_data = read_data

# 预热
qps(read_data, (30000,), number=30000)

qps(read_data, (1,), number=1)
qps(read_data, (10,), number=10)
qps(read_data, (100,), number=100)
qps(read_data, (1000,), number=1000)
qps(read_data, (10000,), number=10000)

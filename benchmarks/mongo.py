import contextlib
import multiprocessing
import random
import sys
import time

from multiprocessing import Process as Process
# from threading import Thread as Process
import pymongo
from sqlalchemy import create_engine


class Object:
    pass


import MySQLdb


@contextlib.contextmanager
def timeit_cm(desc='', auto_print=True):
    """
    Args:
        desc: 打印的文字描述
        auto_print: 是否打印文字描述以及时间
    """
    start = time.time()
    result = Object()
    try:
        yield result
    except:
        raise
    else:
        end = time.time()
        result.elapsed = end - start
        if auto_print:
            print(desc + ': {}'.format(result.elapsed))
            sys.stdout.flush()


CONCUR = 16
TIMES = 3000


def read_data():
    # engine = create_engine("mysql://root:123456@192.168.31.27:3306/employees", echo=False)
    while 1:
        try:
            # engine = create_engine("mysql://root:123456@0.0.0.0:3307/employees", echo=False)

            # db = MySQLdb.connect(
            #     host="127.0.0.1",  # 主机名
            #     user="root",  # 用户名
            #     passwd="123456",  # 密码
            #     port=3307,
            #     db="employees")  # 数据库名称
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient.mydb.things

            # 查询前，必须先获取游标
            break
        except Exception as e:
            print('init error' + str(e))
            continue
    start = time.time()
    for _ in range(TIMES):
        emp_no = random.randint(10001, 499999)

        error_count = 0
        while 1:
            try:
                # cur = db.cursor()  # 游标放到这里更快！
                mydb.find_one({"emp_no": emp_no})
                # cur.fetchall()
                break
            except Exception as e:
                error_count += 1
                if error_count > 100:
                    print(e)
                continue
    end = time.time()
    # print(end - start)
    # print('平均', TIMES / (end - start))


pws = []
for i in range(CONCUR):
    pw = Process(target=read_data)
    pw.start()
    pws.append(pw)

start_ = time.time()
print('kaishi')

for dw in pws:
    dw.join()

print('end')
print(time.time() - start_)
print(CONCUR * TIMES)
print(CONCUR * TIMES / (time.time() - start_))

import random
import time

from multiprocessing import Process as Process

import MySQLdb


def read_data(TIMES):
    while 1:
        try:

            db = MySQLdb.connect(
                host="127.0.0.1",  # 主机名
                user="root",  # 用户名
                passwd="",  # 密码
                db="employees")  # 数据库名称
            cur = db.cursor()

            # 查询前，必须先获取游标
            break
        except Exception as e:
            print('init error' + str(e))
            continue
    for _ in range(TIMES):
        emp_no = random.randint(10001, 499999)
        error_count = 0
        while 1:
            try:
                cur.execute("select SQL_NO_CACHE * from `salaries` where emp_no = {} limit 1".format(emp_no))
                break
            except Exception as e:
                error_count += 1
                if error_count > 100:
                    print(e)
                continue


def stat():
    CONCUR = 10
    TIMES = 3000

    start_ = time.time()

    pws = []
    for i in range(CONCUR):
        pw = Process(target=read_data, args=(TIMES,))
        pw.start()
        pws.append(pw)

    for dw in pws:
        dw.join()

    print('总请求', CONCUR * TIMES)
    print('耗时', time.time() - start_)
    print('QPS', (CONCUR * TIMES) / (time.time() - start_))
    print('请求平均耗时', (time.time() - start_) / (CONCUR * TIMES) * 1000)


if __name__ == '__main__':
    stat()

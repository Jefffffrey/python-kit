"""
使用sqlalchemy
"""

import random
import time
from multiprocessing import Process

from sqlalchemy import create_engine

from utils import qps


def read_data(times):
    engine = create_engine("mysql://root:@127.0.0.1:3306/employees", echo=False)

    for _ in range(times):
        emp_no = random.randint(10001, 499999)
        engine.execute("".join(["select * from `employees` where emp_no = ", str(emp_no)]))
    del engine


def inner_qps(times):
    qps(read_data, (times,), number=times)


def run(concur, times):
    start = time.time()

    pws = []
    for i in range(concur):
        pw = Process(target=inner_qps, args=(times,))
        pw.start()
        pws.append(pw)

    # 不太准确，可能有的进程先完成了但是在这里等着，不过影响应该不大
    for dw in pws:
        dw.join()

    total = (concur * times)
    total_time = (time.time() - start)
    print({
        "qps": total / total_time,
        "total_time": total_time
    })


# 预热
# qps(read_data, (30000,), number=30000)

# run(1, 30000)

run(32, 10000)
#
# run(1, 10000)
# run(2, 10000)
# run(4, 10000)
# run(8, 10000)
# run(16, 10000)
# run(32, 10000)
# run(64, 10000)

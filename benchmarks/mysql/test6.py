"""
[Unix domain socket 和 TCP/IP socket 的区别 - Jamin Zhang](https://jaminzhang.github.io/network/the-difference-between-unix-domain-socket-and-tcp-ip-socket/)
[mysql 连接中 localhost 和 127.0.0.1 的区别 - Jamin Zhang](https://jaminzhang.github.io/mysql/the-difference-between-localhost-and-127-0-0-1-in-mysql-connection/)
"""

import time
from multiprocessing import Process

import MySQLdb

from utils import qps


def read_data(times):
    db = MySQLdb.connect(
        unix_socket="/tmp/mysql.sock",
        user="root",
        passwd="",
        db="employees")

    cur = db.cursor()
    qps(tast, (cur, times,), number=times)
    cur.close()
    db.close()


def tast(cur, times):
    query = "select emp_no from `employees` where emp_no = 30000"
    for _ in range(times):
        cur.execute(query)
        cur.fetchall()


def inner_qps(times):
    read_data(times)


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


run(2, 10000)
run(4, 10000)  # 这个最快6W，localhost
run(8, 10000)
run(16, 10000)  # 这个5W,127.0.0.1, localhost只有3W
run(32, 10000)  # 这个5W,127.0.0.1, localhost只有3W

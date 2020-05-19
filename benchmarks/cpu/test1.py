"""
占用CPU
"""

import time
from multiprocessing import Process


def inner_qps():
    a = 0
    for i in range(1_000_000_000):
        a += i


def run(concur):
    start = time.time()

    pws = []
    for i in range(concur):
        pw = Process(target=inner_qps)
        pw.start()
        pws.append(pw)

    for dw in pws:
        dw.join()

    total_time = (time.time() - start)
    print({
        "total_time": total_time
    })


# 预热
# qps(read_data, (30000,), number=30000)

# run(1, 30000)

run(16)
#
# run(1, 10000)
# run(2, 10000)
# run(4, 10000)
# run(8, 10000)
# run(16, 10000)
# run(32, 10000)
# run(64, 10000)

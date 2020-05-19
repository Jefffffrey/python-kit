import random
import time

from multiprocessing import Process as Process
import redis

CONCUR = 20
TIMES = 10000


def read_data():
    while 1:
        try:
            r = redis.Redis()
            break
        except Exception as e:
            print('init error' + str(e))
            continue
    for _ in range(TIMES):
        emp_no = random.randint(10001, 499999)

        error_count = 0
        while 1:
            try:
                r.hgetall(str(emp_no))
                break
            except Exception as e:
                error_count += 1
                if error_count > 100:
                    print(e)
                continue


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

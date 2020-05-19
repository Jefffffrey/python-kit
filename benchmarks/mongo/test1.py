import random
import time

from multiprocessing import Process as Process
import pymongo


class Object:
    pass


CONCUR = 20
TIMES = 3000


def read_data():
    while 1:
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient.mydb.things
            break
        except Exception as e:
            print('init error' + str(e))
            continue

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

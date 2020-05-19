import subprocess

from benchmarks.mysql.gen_html import gen


def test():
    times = 3000
    # cons = [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 128, 150, 200]
    # cons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 60, 80, 100, 120, 140]
    cons = [1, 2, 4, 8, 16, 32, 64, 128, 256, 300]
    totals, total_times, qpss, arts = [], [], [], []
    for con in cons:
        result = subprocess.check_output(['python3', 'benchmarks/mysql3.py', str(con), str(times)]).decode()
        try:
            total, total_time, qps, art = list(map(lambda line: line.strip(), result.strip().split('\n')))[1:]
        except Exception as e:
            print(result)
            print(e)
            raise
        total = float(total)
        total_time = float(total_time)
        qps = float(qps)
        art = float(art)
        totals.append(total)
        total_times.append(total_time)
        qpss.append(qps)
        arts.append(art)
    print(cons)
    print(qpss)
    print(arts)

    gen('MySQL压力测试', cons, totals, total_times, qpss, arts)


if __name__ == '__main__':
    test()

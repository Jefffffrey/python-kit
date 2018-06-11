# -*- coding:utf-8 -*-

import os
import subprocess

import prettytable

ppid = os.getppid()
cmd = os.readlink('/proc/{}/exe'.format(ppid))
if cmd.find('python') != -1:
    CHILD = True
else:
    CHILD = False

if CHILD:
    class TimeComparator:
        @staticmethod
        def compare(*args, **kwargs):
            pass
else:
    class TimeComparator:
        def __init__(self):
            pass

        @staticmethod
        def compare(*funcs, args=(), numbers=1, python='python3'):
            """用指定的python解释器执行多个函数，比较其执行时间
            Args:
                *funcs: 多个函数
                args: 参数
                numbers: 比较次数
                python: 解释器版本
            Output:
                (第一个函数所花时间,第二个函数所花时间,第三个函数所花时间,
                第二个和第一个相比的增幅(%)，第二个和第一个相比的增幅(%))
                summary:
                (平均值，平均值，平均值，平均值)
            """
            tb = prettytable.PrettyTable()
            field_names = ['']
            for func in funcs:
                field_names.append(func.__name__)
            field_names.extend(map(lambda x: '{}:1'.format(x + 1),
                                   range(1, len(funcs))))
            tb.field_names = field_names

            summary = [0] * (2 * len(funcs) - 1)
            for i in range(numbers):
                children = []
                for func in funcs:
                    child = subprocess.Popen([python],
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    func_module_file = __import__(func.__module__).__file__
                    dirname = os.path.dirname(func_module_file)
                    module_name = os.path.basename(func_module_file) \
                        .split('.')[0]
                    statements = """
import os
os.chdir('{dirname}')
import {module_name}
import contextlib
import time

class Object: pass

@contextlib.contextmanager
def timeit():
    start = time.time()
    result = Object()
    try:
        yield result
    except Exception as e:
        print(e)
        raise
    finally:
        end = time.time()
        result.elapsed = end - start

with timeit() as r:
    {module_name}.{func_name}{args}
print(r.elapsed)
        """.format(dirname=dirname, module_name=module_name,
                   func_name=func.__name__, args=args).encode()
                    child.stdin.write(statements)
                    child.stdin.close()
                    child.wait()
                    children.append(child)

                report = [i]
                for i_child, child in enumerate(children):
                    cmd_out = child.stdout.read()
                    elapsed = cmd_out.decode().split('\n')[-2].strip()
                    child.stdout.close()
                    try:
                        report.append('{:.3f}'.format(float(elapsed)))
                    except ValueError:
                        print(child.stderr.read())
                    summary[i_child] += float(elapsed)
                else:
                    for j in range(2, len(report)):
                        time1 = float(report[1])
                        time2 = float(report[j])
                        rate = (time2 - time1) / time1 * 100
                        report.append('{:.3f}'.format(rate))
                        summary[len(children) + j - 2] += float(rate)
                    tb.add_row(report)

                print(report)
            summary = list(map(lambda x: '{:.3f}'.format(x / numbers), summary))
            summary.insert(0, 'Summary')
            tb.add_row(summary)
            print(tb)

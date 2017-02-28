"""这个包是我在使用python的过程中积累下来的一些可以复用的代码
当前使用的python版本为python3.5,没有考虑对其他python版本的兼容性
"""
import operator
import os
import sys
import time
from contextlib import contextmanager
from io import StringIO

from . import date

__all__ = ['Base', 'timeit', 'suppress_stdout', 'stdout_to_string_io']


class Base:
    """
    参考：
        http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
        http://stackoverflow.com/questions/4522617/equality-of-python-classes-using-slots?noredirect=1&lq=1
    """

    def __eq__(self, other):
        """
        比较的时候：
            两个对象都是普通对象，且类型相同
            两个对象都是有slot的对象，类型相同
            两个对象都有slot和__dict__,类型相同
        对于slot的比较，之比较self本身的__slot__中存在的属性，不比较继承的部分
            参考:http://stackoverflow.com/questions/472000/usage-of-slots
        """
        if isinstance(other, self.__class__):
            slot_equal = True
            if hasattr(self, "__slots__"):
                attr_getters = [operator.attrgetter(attr) for attr in
                                self.__slots__]
                slot_equal = all(
                    getter(self) == getter(other) for getter in attr_getters)
            dict_equal = self.__dict__ == other.__dict__
            return slot_equal and dict_equal
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """如果要实现集合，字典键等地方的相等性判断需要实现该方法"""

    def __str__(self):
        result = []
        if hasattr(self, "__slots__"):
            attr_getters = [operator.attrgetter(attr) for attr in
                            self.__slots__]
            slots = [getter(self) for getter in attr_getters]
            result.append(str(slots))
        result.append(str(self.__dict__))
        return '\n'.join(result)


def timeit(func):
    def count(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        count._time = time.time() - start
        return res

    return count


@contextmanager
def suppress_stdout():
    stdout = None
    try:
        stdout, sys.stdout = sys.stdout, open(os.devnull, 'w')
        yield
    finally:
        sys.stdout = stdout


@contextmanager
def stdout_to_string_io():
    stdout = None
    string_io = StringIO()
    try:
        stdout, sys.stdout = sys.stdout, string_io
        yield string_io
    finally:
        sys.stdout = stdout
        string_io.close()

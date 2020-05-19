# -*- coding:utf-8 -*-

from __future__ import absolute_import

import contextlib
import operator
import os
import sys
import time
from contextlib import contextmanager
from io import StringIO

from utils.compat import PY3
from . import date

__version__ = '0.1.0'

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


def timeit(func, args=(), kwargs=None, number=1):
    if kwargs is None:
        kwargs = {}
    assert isinstance(kwargs, dict)
    print('{} args:{}, kwargs:{}, number:{}'.format(
        func.__name__, args, kwargs, number))
    start = time.time()
    while number:
        res = func(*args, **kwargs)
        number -= 1
    print('total time:{}'.format(time.time() - start))
    return res


def qps(func, args=(), kwargs=None, number=1):
    if kwargs is None:
        kwargs = {}
    assert isinstance(kwargs, dict)
    print('{} args:{}, kwargs:{}, number:{}'.format(
        func.__name__, args, kwargs, number))
    start = time.time()
    res = func(*args, **kwargs)
    total_time = time.time() - start
    print({
        "qps": number / total_time,
        "total_time": total_time
    })
    return res


class Object: pass


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


def pause():
    print('Pause progress {},press any key to continue'.format(os.getpid()))
    if compat.PY3:
        input()
    elif compat.PY2:
        raw_input()


class AutoCounter:
    """
    创建该对象后，每次调用+1，退出时显示结果
    """

    def __init__(self, desc=''):
        self.desc = desc
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1

    def __del__(self):
        print('autocounter: {}-{}'.format(self.desc, self.count))

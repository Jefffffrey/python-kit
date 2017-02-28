"""
提供了用于处理日期的操作:
    1. 日期加减法
    2. 日期的表现形式转化
"""

import datetime


def to_date(date):
    """转变为日期对象
    date可以字符串,可以是date对象
    Returns:
        返回date对象
    """
    assert isinstance(date, (str, datetime.date))

    if isinstance(date, str):
        try:
            year, month, day = map(int, date.split("-"))
            date = datetime.date(year, month, day)
        except:
            raise ValueError
    if isinstance(date, datetime.datetime):
        return date.date()
    return date


def to_stamp(date):
    """转变为date时间戳
    date可以字符串,可以是date对象
    Returns:
        返回date的时间戳,以-连接
    """
    assert isinstance(date, (str, datetime.date))

    if isinstance(date, datetime.date):
        return date.strftime("%Y-%m-%d")
    return date


def sub(first, second, return_type='date'):
    """对日期做减法
    日期可以是datetime.date类型或'2016-01-12'类型,数字可以是整数或者datetime.timedelta
        日期-数字:得到新的日期,字符串还是date类型取决于return_type设置
        日期-日期:得到间隔数字

    Args:
        first: 被减日期
        second: 减去的间隔或者日期
        return_type: 返回结果的类型,取值范围['date','str']
    """
    assert isinstance(first, (str, datetime.date))
    assert isinstance(second, (int, str, datetime.date))

    first = to_date(first)
    # 支持日期本身支持日期日期减法和日期间隔减法
    if isinstance(second, int):
        begin_date = first - datetime.timedelta(days=second)
        if return_type == 'date':
            return begin_date
        elif return_type == 'str':
            return to_stamp(begin_date)
        else:
            raise ValueError
    if isinstance(second, str):
        second = to_date(second)
    return (first - second).days


def today():
    return datetime.date.today()


def days_ago(date):
    """返回值:date在今天多少天前,负数表示之后,0表示今天"""
    assert isinstance(date, (datetime.date, str))

    date = to_date(date)

    return sub(today(), date)


def add(first, second, return_type='date'):
    """处理日期加法
    支持日期加数字,日期可以是字符串也可以是date类型
    Returns:
        date类型
    """
    assert isinstance(first, (str, datetime.date))
    assert isinstance(second, int)

    first = to_date(first)
    date = first + datetime.timedelta(days=second)
    if return_type == 'date':
        return date
    elif return_type == 'str':
        return to_stamp(date)
    else:
        raise ValueError

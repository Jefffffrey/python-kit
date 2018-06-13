from sys import getsizeof


def print_size_of(obj):
    if hasattr(obj, '__len__'):
        print('{}, length: {}, size: {}'.format(
            type(obj), len(obj), getsizeof(obj)))
    else:
        print('{}, size: {}'.format(
            type(obj), getsizeof(obj)))


print_size_of(None)
print_size_of(1)
print_size_of(10 ** 10)
print_size_of(10 ** 20)
print_size_of(1.0)
print_size_of(1.0 ** 10)
print_size_of(1.0 ** 20)

##
# 字符串，从49开始，每个元素+1
##
print_size_of('')
print_size_of('a')
print_size_of('ab')
print_size_of('abc')

##
# 列表，从64开始，每个元素+8
##
print_size_of([])  # 64
print_size_of([1])  # 72, 一个元素8额外字节
print_size_of(['abc'] * 3)  # 88
print_size_of([1] * 3)
print_size_of([None] * 3)
print_size_of(['abc', 'abc', 'abc'])
print_size_of(['abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz',
               'abcdefghijklmnopqrstuvwxyz'])

##
# 元组，从48开始，每个元素+8
##
print_size_of(tuple())  # 48
print_size_of((1,))  # 56, 一个元素8额外字节
print_size_of(('abc',))  # 56
print_size_of(('abc',) * 3)  # 72
print_size_of((1,) * 3)  # 72
print_size_of((None,) * 3)  # 72
print_size_of(('abc', 'abc', 'abc'))  # 72
print_size_of(('abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz',
               'abcdefghijklmnopqrstuvwxyz'))  # 72

##
# 集合,对空间进行了预分配
##
print_size_of(set())  # 224
print_size_of({1})  # 224
print_size_of({1, 2, 3})  # 224
print_size_of(set(range(6)))  # 736

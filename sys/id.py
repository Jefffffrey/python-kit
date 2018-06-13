##
# 整数，小整数id相同，大的不相同
##
print(id(10))
print(id(10))
print(id(10 ** 8))
print(id(10 ** 8))

##
# 字符串，id总是相同
##
print(id(''))
print(id(''))
print(id('a'))
print(id('a'))
print(id('abcdefghijklmnopqrstuvwxyz' * 100))
print(id('abcdefghijklmnopqrstuvwxyz' * 100))

##
# 列表乘法，id相同,　手动创建多个元素id不相同
##
a = [[]] * 3
print([id(i) for i in a])  # id相同
a = [[], [], []]
print([id(i) for i in a])  # id相同

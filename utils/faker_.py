from faker import Faker

_cache = []


def generate_tuple_list(length=1):
    """
    生成约定大小元组列表，大小为64+length*(8+104＋81*7)
    """
    global _cache

    cache_size = len(_cache)
    if cache_size < length:
        fake = Faker()

        for i in range(length - cache_size):
            elem = tuple(fake.md5() for _ in range(7))
            _cache.append(elem)
    return _cache[:length]


if __name__ == '__main__':
    from sys import getsizeof


    def print_size_of(obj):
        obj = obj[:]  # 减小list的大小
        list_size = getsizeof(obj)
        elem_size = getsizeof(obj[0]) * len(obj)
        md5_size = getsizeof(obj[0][0]) * len(obj[0]) * len(obj)
        res = list_size + elem_size + md5_size

        print(list_size, elem_size, md5_size, res, round(res / 1024 / 1024, 3))


    print_size_of(generate_tuple_list())
    # 72 104 567 743 0.001
    print_size_of(generate_tuple_list(2))
    # 80 208 1134 1422 0.001
    print_size_of(generate_tuple_list(100000))
    # 800064 10400000 56700000 67900064 64.755
    print_size_of(generate_tuple_list(200000))
    # 1600064 20800000 113400000 135800064 129.509
    print_size_of(generate_tuple_list(300000))
    # 2400064 31200000 170100000 203700064 194.264
    print_size_of(generate_tuple_list(155000))
    # 1240064 16120000 87885000 105245064 100.37

# see string/why/Q1.py for more information


def concat_str_by_list(num):
    s = []
    for i in range(num):
        s.append('string')
    return ''.join(s)


def concat_bytes_by_list(num):
    s = []
    for i in range(num):
        s.append(b'string')
    return b''.join(s)


def concat_bytearray_by_extend(num):
    s = bytearray()
    for i in range(num):
        s.extend(b'string')
    return s


def concat_str_by_plus_equal(num):
    s = ''
    for i in range(num):
        s += 'string'
    return s


def concat_bytes_by_plus_equal(num):
    s = b''
    for i in range(num):
        s += b'string'
    return s


def concat_bytearray_by_plus_equal(num):
    s = bytearray()
    for i in range(num):
        s += b'string'
    return s


if __name__ == '__main__':
    from utils.profile import TimeComparator

    tc = TimeComparator()
    tc.compare(concat_str_by_list, concat_str_by_plus_equal,
               concat_bytes_by_list,
               concat_bytes_by_plus_equal, concat_bytearray_by_extend,
               concat_bytearray_by_plus_equal,
               args=(100000,),
               numbers=3,
               python='python3')

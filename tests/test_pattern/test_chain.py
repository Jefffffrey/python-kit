import unittest

from kit import stdout_to_string_io
from kit.pattern.chain import coroutine


@coroutine
def chain1(successor=None):
    while True:
        msg = yield
        if msg:
            print(msg)
        else:
            successor.send(msg)


@coroutine
def chain2(successor=None):
    while True:
        msg = yield
        print('到末尾了')


pipe = chain1(chain2())


class MyTestCase(unittest.TestCase):
    def test_coroutine(self):
        with stdout_to_string_io() as string_io:
            pipe.send(0)
            # 使用的是这个去获取字符串的值
            contents = string_io.getvalue()
            self.assertEqual(contents, '到末尾了\n')

        with stdout_to_string_io() as string_io:
            pipe.send(1)
            contents = string_io.getvalue()
            self.assertEqual(contents, '1\n')


if __name__ == '__main__':
    unittest.main()

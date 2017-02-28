import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
# 添加utils包所在目录路径到模块搜索路径中
sys.path.insert(0, ROOT_DIR)
# 添加该选项，以便可以直接在tests目录外执行python -m tests
sys.path.insert(0, BASE_DIR)


def suite():
    loader = unittest.TestLoader()
    suite1 = loader.discover(r'')
    suite2 = loader.discover(r'test_os')
    return unittest.TestSuite([suite1, suite2])


if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=1)

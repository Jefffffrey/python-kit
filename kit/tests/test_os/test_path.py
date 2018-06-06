import sys
import unittest

from kit.os.path import is_ignore, abspath

_is_windows = sys.platform in ('win32', 'cygwin')


class TestPath(unittest.TestCase):
    @staticmethod
    def test_is_ignore():
        # 完整文件名
        assert is_ignore('idea', 'idea') == True
        assert is_ignore('idea', 'idea/') == False
        # 完整目录名
        assert is_ignore('idea/', 'idea/') == True
        if _is_windows:
            assert is_ignore('idea/', 'idea\\') == True
            assert is_ignore('idea\\', 'idea/') == True
            assert is_ignore('idea\\', 'idea\\') == True
        assert is_ignore('idea/', 'idea') == False
        # 使用*通配符的文件名
        assert is_ignore('b.py', '*.py') == True
        if _is_windows:
            assert is_ignore(r'E:\hello.py', '*.py') == True
            assert is_ignore(r'E:\hello.py', '*.pyc') == False
        # 使用*通配符的目录名
        assert is_ignore('aaa/', '*/') == True
        assert is_ignore('-test/', '*-test/') == True

    @staticmethod
    # https://docs.python.org/3/library/sys.html#sys.platform
    @unittest.skipIf(not _is_windows, 'Not on Windows')
    def test_abspath():
        assert abspath('..\hello', r'E:\MyComputer\Workspace\项目', ) == \
               r'E:\MyComputer\Workspace\hello'
        assert abspath('.\hello', r'E:\MyComputer\Workspace\项目') == \
               r"E:\MyComputer\Workspace\项目\hello"
        assert abspath('hello', r'E:\MyComputer\Workspace\项目') == \
               r"E:\MyComputer\Workspace\项目\hello"
        assert abspath('.', r'E:\MyComputer\Workspace\项目') == \
               r"E:\MyComputer\Workspace\项目"


if __name__ == '__main__':
    unittest.main()

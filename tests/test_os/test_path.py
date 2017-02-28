import unittest

from utils.os.path import is_ignore, abspath


class TestPath(unittest.TestCase):
    @staticmethod
    def test_is_ignore():
        # 完整文件名
        assert is_ignore('idea', 'idea') == True
        assert is_ignore('idea', 'idea/') == False
        # 完整目录名
        assert is_ignore('idea/', 'idea/') == True
        assert is_ignore('idea/', 'idea\\') == True
        assert is_ignore('idea\\', 'idea/') == True
        assert is_ignore('idea\\', 'idea\\') == True
        assert is_ignore('idea/', 'idea') == False
        # 使用*通配符的文件名
        assert is_ignore('b.py', '*.py') == True
        assert is_ignore(r'E:\hello.py', '*.py') == True
        assert is_ignore(r'E:\hello.py', '*.pyc') == False
        # 使用*通配符的目录名
        assert is_ignore('aaa/', '*/') == True
        assert is_ignore('-test/', '*-test/') == True

    @staticmethod
    def test_abspath():
        assert abspath('..\hello', r'E:\MyComputer\Workspace\项目', ) == r'E:\MyComputer\Workspace\hello'
        assert abspath('.\hello', r'E:\MyComputer\Workspace\项目') == r"E:\MyComputer\Workspace\项目\hello"
        assert abspath('hello', r'E:\MyComputer\Workspace\项目') == r"E:\MyComputer\Workspace\项目\hello"
        assert abspath('.', r'E:\MyComputer\Workspace\项目') == r"E:\MyComputer\Workspace\项目"


if __name__ == '__main__':
    unittest.main()

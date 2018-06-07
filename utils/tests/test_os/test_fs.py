import unittest

# noinspection PyProtectedMember
from utils.os.fs import _parser


class TestFS(unittest.TestCase):
    @staticmethod
    def test_parse():
        ignores = ('.git/', 'config.py', '*.txt', '.txt.link.god')
        res = _parser(ignores)
        targets = ({'.git'}, {'txt'}, {'config.py', '.txt.link.god'})
        assert res == targets


if __name__ == '__main__':
    unittest.main()

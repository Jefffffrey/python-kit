import unittest

from utils.class_property import ClassPropertyMetaClass, classproperty


# noinspection PyPropertyAccess
class TestClassproperty(unittest.TestCase):
    def test(self):
        # noinspection PyMethodParameters,PyPropertyDefinition
        class A(metaclass=ClassPropertyMetaClass):
            _a = 0

            @classproperty
            def a(cls):
                return cls._a

            @a.setter
            def a(cls, value):
                cls._a = value

        assert A.a == 0
        A.a = 2
        assert A.a == 2


if __name__ == '__main__':
    unittest.main()

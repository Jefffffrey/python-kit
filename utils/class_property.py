__all__ = ['ClassPropertyMetaClass', 'classproperty']


class ClassPropertyMetaClass(type):
    """修改默认的setattr方法调用

    参考:
        http://stackoverflow.com/questions/5189699/how-can-i-make-a-class-property-in-python
    """

    def __setattr__(self, key, value):
        if key in self.__dict__:
            obj = self.__dict__.get(key)
            if obj and type(obj) is classproperty:
                return obj.__set__(self, value)
        return super(ClassPropertyMetaClass, self).__setattr__(key, value)


class classproperty(object):
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, class_):
        return self.fget(class_)

    def __set__(self, class_, value):
        self.fset(class_, value)

    def setter(self, fset):
        return type(self)(self.fget, fset)

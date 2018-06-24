import types


def print_is_generator(gen):
    if isinstance(gen, types.GeneratorType):
        print(True)
    else:
        print(type(gen))


gen = (i for i in range(10))
print_is_generator(gen)


def foo():
    yield


print_is_generator(foo)
print_is_generator(foo())

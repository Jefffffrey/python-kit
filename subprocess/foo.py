from utils import timeit_cm


def countdown(n):
    while n:
        n -= 1


if __name__ == '__main__':
    with timeit_cm():
        countdown(10 ** 8)

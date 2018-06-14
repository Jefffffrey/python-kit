# https://faker.readthedocs.io/en/latest/providers.html
from faker import Faker

from utils import timeit

fake = Faker()

if __name__ == '__main__':
    timeit(fake.md5, number=10 ** 5)  # 0.6706490516662598
    timeit(fake.uuid4, number=10 ** 5)  # 0.7706490516662598
    timeit(fake.phone_number, number=10 ** 5)  # 6.451107501983643

# -*- coding:utf-8 -*-

import subprocess

child = subprocess.Popen(['python3'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
child.stdin.write(b'exec(open("foo.py").read())')
child.stdin.close()

child.wait()

print('Use exec' + child.stdout.read().decode())

#####################
child = subprocess.Popen(['python3'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
child.stdin.write(b"""
from utils import timeit_cm

def countdown(n):
    while n:
        n -= 1

if __name__ == '__main__':
    with timeit_cm():
        countdown(10 ** 8)
""")
child.stdin.close()
child.wait()

print("Don't use exec" + child.stdout.read().decode())

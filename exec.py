if __name__ == '__main__':
    import sys

    file = sys.argv[1]
    with open(file) as fp:
        code = fp.read()
        exec(code)

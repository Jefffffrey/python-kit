from pprint import pprint


class Averager:
    def __init__(self):
        self.matrix = [[]]
        self.i = 0
        self.end = False

    def add(self, *value):
        self.matrix[self.i].extend(value)

    def submit(self):
        self.i += 1
        self.matrix.append([])

    def summary(self):
        # 防止多次调用
        if self.end:
            return
        else:
            self.end = True

        width = len(self.matrix[0])
        height = len(self.matrix) - 1
        self.matrix[-1] = [None] * width
        for col in range(width):
            value = 0
            for row in range(height):
                value += float(self.matrix[row][col])
            else:
                self.matrix[-1][col] = round(value / height, 3)
        return self.matrix

    def report(self):
        self.summary()
        pprint(self.matrix)


if __name__ == '__main__':
    averager = Averager()
    """
    1     2       2
    2     3       1.5
    2     5       2.5
    -----------------
    1.667 3.333   2
    """
    averager.add('1', 2, 2)
    averager.submit()
    averager.add(2, 3, 1.5)
    averager.submit()
    averager.add(2, 5)
    averager.add(2.5)
    averager.submit()

    averager.summary()
    averager.report()
    """
    [['1', 2, 2], [2, 3, 1.5], [2, 5, 2.5], [1.667, 3.333, 2.0]]
    """

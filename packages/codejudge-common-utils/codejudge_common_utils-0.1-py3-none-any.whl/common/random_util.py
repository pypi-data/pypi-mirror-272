from random import randint


class RandomUtil(object):

    @classmethod
    def random_with_N_digits(cls, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

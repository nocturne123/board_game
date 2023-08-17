from itertools import zip_longest, chain

a = [1, 2, 3, 4]
b = [2, 4, 8, 16]
c = [3, 6, 9, 12]

d = zip_longest(a, b, c)
print(d)
e = [x for x in chain.from_iterable(d) if x is not None]
print(e)

def e_a():
    for i in range(3):
        print(f'a-{i}')
        yield i

def e_b():
    for i in range(5):
        print(f'b-{i}')
        yield i

def e_c():
    for i in range(7):
        print(f'c-{i}')
        yield i

def output():
    yield from e_a
    yield from e_b
    yield from e_c

output()
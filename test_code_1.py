"""
def index_words_iter(text):
    if text:
        yield 0
    for index,letter in enumerate(text):
        if letter == ' ':
            yield index +1

address = 'Four score and seven years ago...'

it = index_words_iter(address)
print(next(it))
print(next(it))

def move(period ,speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0

def render(delta):
    print(f'Delta:{delta:.1f}')

def run(func):
    for delta in func():
        render(delta)

def animate_composed():
    yield from move(4,5.0)
    yield from pause(3)
    yield from move(2,3.0)

run(animate_composed)
"""


def count_from1():
    for i in range(10):
        yield i


it = iter(count_from1())

it.send(None)

print(next(it))
print(next(it))

it.send(30)

print(next(it))
print(next(it))

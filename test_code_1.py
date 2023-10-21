class A:
    def __init__(self) -> None:
        self.num = 1


class B:
    def __init__(self, a) -> None:
        self.a = a


class C:
    def __init__(self, b) -> None:
        self.b = b
        self.a = b.a


a = A()
b = B(a)
c = C(b)

a.num = 2
print(c.a.num)

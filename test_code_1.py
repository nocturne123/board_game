class A:
    def __init__(self) -> None:
        self.a = 20
        self.b = 30

    def a_trans(self):
        self.b = self.a


a = A()
a.a_trans()
a.a += 1
print(a.a, a.b)

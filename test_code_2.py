class A:
    def __init__(self) -> None:
        self.a = 1
        self.say()

    def say(self):
        print(self.a)


class B(A):
    def __init__(self) -> None:
        super().__init__()

    def say(self):
        print("aaaaa")


b = B()

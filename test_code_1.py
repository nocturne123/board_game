class A:
    num = 0

    @staticmethod
    def add():
        A.num += 1


print(A.num)
A.add()
print(A.num)

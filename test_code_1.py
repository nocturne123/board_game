class A:
    hook_func = []

    def __init__(self):
        pass

    def func_op(self, a):
        a += 1


b = 2
A.func_op(b)
print(b)

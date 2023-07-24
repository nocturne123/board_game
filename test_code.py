class mynumber:
    def __init__(self,number):
        self.number = number
        
        self.sec = self.number * 2

a=mynumber(5)
print(a.sec)
a.number=6
print(a.sec)
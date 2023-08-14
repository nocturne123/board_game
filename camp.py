from collections import deque



class Camp(deque):
    def __init__(self,maxlen):
        super().__init__(maxlen=maxlen)

    def next_player(self):
        a=self.popleft()
        self.append(a)

    @property
    def active_member(self):
        return self[0]



a=Camp(maxlen=3)
a.extend(["a","b","c"])
print(a)
a.append("d")
print(a)
a.next_player()
print(a)

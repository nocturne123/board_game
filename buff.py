class Buff:
    def __init__(self, name, duration, effect):
        self.name = name
        self.duration = duration
        self.effect = effect

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

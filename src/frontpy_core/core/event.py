class Event:
    pass


class KeyEvent(Event):

    def __init__(self, *keys: str):
        self.keys = keys

    def __str__(self):
        return "<KeyEvent: " + '+'.join(self.keys) + ">"

    def __eq__(self, other):
        return isinstance(other, KeyEvent) and other.keys == self.keys

    def __hash__(self):
        return hash(str(self))

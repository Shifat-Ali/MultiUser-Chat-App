class NewConnection:
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def setName(self, name):
        self.name = name

    def __repr__(self):
        return f'connection({self.addr}, {self.name})'
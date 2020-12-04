class Cabinet:
    # Time in seconds
    def __init__(self, id: int, name: str, averageTime: int):
        self.query = list()
        self.averageTime = averageTime
        self.id = id

    def countTime(self, guest: Guest):
        for i in range(0, len(self.query)):
            if self.query[i].place > guest.place:
                return i * self.averageTime
        return len(self.query) * self.averageTime

    def addGuest(self, guest: Guest):
        for i in range(0, len(self.query)):
            if self.query[i].place > guest.place:
                self.query.insert(i, guest)
                break

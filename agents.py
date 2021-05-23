from enum import Enum


class TaxiState(Enum):
    occupied = 1
    free = 2


class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Agent - Position: (" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()


class Taxi(Agent):
    def __init__(self, x, y, identifier):
        super().__init__(x, y)
        self.identifier = identifier
        self.state = TaxiState.free

    def __str__(self):
        return "Taxi " + super().__str__() + "; ID: " +\
               str(self.identifier) + "; State: " + str(self.state)

    def __repr__(self):
        return self.__str__()

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1


class Client(Agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return "Client " + super().__str__()

    def __repr__(self):
        return self.__str__()

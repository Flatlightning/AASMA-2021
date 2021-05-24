from enum import Enum
import pathfind 
import math

class TaxiState(Enum):
    pickup = 1
    dropoff = 2
    free = 3


class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Agent - Position: (" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()


class Taxi(Agent):

    def __init__(self, x, y, identifier, board):
        super().__init__(x, y)
        self.identifier = identifier
        self.state = TaxiState.free
        self.taxi_list = []
        self.path = ''
        self.current_client = None
        self.available_clients = []
        self.board = board


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
    
    def find_path(self, goal_x, goal_y):
        self.path = pathfind.main_pathfinding(self.board.size, [self.x, self.y], [goal_x, goal_y]) #check size thingy
    
    def decide_waiting_zone():
        return

    def update_waiting_matrix():
        return

    def pickup_client(self, client):
        self.current_client = client

    def move_next_pos(self):
        if len(self.path) == 1:
            move, self.path = self.path[0], ''
        else:
            move, self.path = self.path[0], self.path[1:]

        if move == 'R':
            self.right
        elif move == 'L':
            self.left
        elif move == 'U':
            self.up
        elif move == 'D':
            self.down

    
    def receive_available_client(self, client):
        self.available_clients += [client]
    
    def add_taxi(self, taxi):
        self.taxi_list += [taxi]

    def remove_available_client(self, client):
        self.available_clients.remove(client)
    
    def is_closest(self, client):
        my_dist = self.eucl_dist(client)
        for taxi in self.taxi_list:
            if (taxi.eucl_dist(client) < my_dist):
                return False
            elif (taxi.eucl_dist(client) == my_dist and taxi.identifier < self.identifier):
                return False
        return True
    
    def eucl_dist(self, client):
        return math.sqrt(pow((self.x - client.x),2) + pow((self.y - client.y)))

    def decision_making(self):
        if self.state == TaxiState.free:
            if self.available_clients:
                for c in self.available_clients:
                    if(self.is_closest(c)):
                        self.state = TaxiState.pickup
                        self.current_client = c
                        self.find_path(self, self.current_client.goal_x, self.current_client.goal_y) #adaptar a cena do size
                        for taxi in self.taxi_list:
                            taxi.remove_available_client(c)
                        self.move_next_pos()
                        break
        elif self.state == TaxiState.pickup:
            self.move_next_pos()
            if self.path == '':
                self.state = TaxiState.dropoff
                self.find_path(self, self.current_client.goal_x, self.current_client.goal_y) #adaptar a cena do size
        elif self.state == TaxiState.dropoff:
            self.move_next_pos()
            if self.path == '':
                self.state = TaxiState.free
                self.current_client = None

class Client(Agent):
    def __init__(self, x, y, goal_x, goal_y):
        super().__init__(x, y)
        self.goal_x = goal_x
        self.goal_y = goal_y

    def __str__(self):
        return "Client " + super().__str__()

    def __repr__(self):
        return self.__str__()

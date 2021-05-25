from enum import Enum
import a_star
import math
import numpy as np
import random as rand

class TaxiState(Enum):
    pickup = 1
    dropoff = 2
    free = 3
    waiting = 4


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
        self.taxi_list = {}
        self.path = ''
        self.current_client = None
        self.available_clients = {}
        self.last_clients = []
        self.board = board
        self.quadrants = []
        self.quadrant_size = 0
        self.quadrant_probabilities = None
        self.calculate_quadrants()


    def __str__(self):
        return "Taxi " + super().__str__() + "; ID: " +\
               str(self.identifier) + "; State: " + str(self.state)

    def __repr__(self):
        return self.__str__()

    def up(self):
        self.board.update_log_text("MOVE TAXI - ID: " + str(self.identifier) + "; (" +
                    str(self.x) + ", " + str(self.y) + ") -> (" +
                    str(self.x) + ", " + str(self.y-1) + ")\n")
        self.y -= 1

    def down(self):
        self.board.update_log_text("MOVE TAXI - ID: " + str(self.identifier) + "; (" +
                    str(self.x) + ", " + str(self.y) + ") -> (" +
                    str(self.x) + ", " + str(self.y+1) + ")\n")        
        self.y += 1

    def left(self):
        self.board.update_log_text("MOVE TAXI - ID: " + str(self.identifier) + "; (" +
                    str(self.x) + ", " + str(self.y) + ") -> (" +
                    str(self.x-1) + ", " + str(self.y) + ")\n") 
        self.x -= 1

    def right(self):
        self.board.update_log_text("MOVE TAXI - ID: " + str(self.identifier) + "; (" +
                    str(self.x) + ", " + str(self.y) + ") -> (" +
                    str(self.x+1) + ", " + str(self.y) + ")\n")
        self.x += 1
    
    def calculate_quadrants(self):
        quadrant_area = self.board.board_size[0] * self.board.board_size[1]
        count = 0
        while not quadrant_area % 4:
            quadrant_area = quadrant_area // 4
            count += 2
        self.quadrant_size = int(math.sqrt(quadrant_area))     
        pos_x = 0                                         
        for i in range(count):
            pos_y = 0
            for i in range(count):
                self.quadrants += [Quadrant(pos_x, pos_y,pos_x + self.quadrant_size - 1, pos_y + self.quadrant_size - 1)]
                pos_y += self.quadrant_size
            pos_x += self.quadrant_size
        self.quadrant_probabilities = np.ones((len(self.quadrants),))

    def in_quadrant(self, client):
        x = client.x // self.quadrant_size
        y = client.y // self.quadrant_size
        return (x + (self.board.board_size[0]//self.quadrant_size) * y)
    
    def find_path(self, goal_x, goal_y):
        self.path = a_star.path_find(self.x, self.y, goal_x,  goal_y, self.board.board_size[0])
    
    def decide_waiting_spot(self):
        chosen_quadrant = np.random.choice(self.quadrants, p = (self.quadrant_probabilities/self.quadrant_probabilities.sum()))
        print(chosen_quadrant)
        x = rand.randrange(chosen_quadrant.x_start, chosen_quadrant.x_end)
        y = rand.randrange(chosen_quadrant.y_start, chosen_quadrant.y_end)
        print(x,y)
        return (x,y)

    def update_waiting_matrix(self, client):
        update_value = len(self.quadrants)
        self.last_clients += [client]
        print(self.quadrant_probabilities)
        self.quadrant_probabilities[(self.in_quadrant(client))] += update_value
        oldest_client = None

        # remove old information from probabilities 
        if len(self.last_clients) > 10:
            oldest_client = self.last_clients[0]
            self.quadrant_probabilities[(self.in_quadrant(oldest_client))] -= update_value
            self.last_clients = self.last_clients[1:]
        
        return

    def pickup_client(self, client):
        self.current_client = client

    def move_next_pos(self):
        if len(self.path) == 1:
            move, self.path = self.path[0], ''
        else:
            move, self.path = self.path[0], self.path[1:]

        if move == 'R':
            self.right()
        elif move == 'L':
            self.left()
        elif move == 'U':
            self.up()
        elif move == 'D':
            self.down()
        

    
    #def receive_available_client(self, client):
    #    self.available_clients += [client]
    
    def add_taxi(self, taxi):
        self.taxi_list[taxi.identifier] = taxi

    def add_client(self, client):
        self.available_clients[(client.x, client.y)] = client
        self.update_waiting_matrix(client)

    def remove_available_client(self, client):
        self.available_clients.pop((client.x, client.y))
    
    def is_closest(self, client):
        my_dist = self.eucl_dist(client)
        for taxi in self.taxi_list.values():
            if (taxi.eucl_dist(client) < my_dist):
                return False
            elif (taxi.eucl_dist(client) == my_dist and taxi.identifier < self.identifier):
                return False
        return True
    
    def eucl_dist(self, client):
        return math.sqrt(pow((self.x - client.x),2) + pow((self.y - client.y), 2))

    def decision_making(self):
        if self.state == TaxiState.pickup:
            self.move_next_pos()
            if self.path == '':
                self.board.update_board()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " PICKED UP CLIENT ON (" + str(self.current_client.x) +", "+ str(self.current_client.y) + ")\n")
                self.state = TaxiState.dropoff
                self.board.clients.pop((self.current_client.x, self.current_client.y))
                self.find_path(self.current_client.goal_x, self.current_client.goal_y)
                
        elif self.state == TaxiState.dropoff:
            self.move_next_pos()
            if self.path == '':
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " DROPPED CLIENT OFF\n")
                self.state = TaxiState.free
                self.current_client = None

        else:
            if self.available_clients:
                for c in self.available_clients.values():
                    if(self.is_closest(c)):
                        self.state = TaxiState.pickup
                        self.current_client = c
                        self.find_path(self.current_client.x, self.current_client.y)
                        for taxi in self.taxi_list.values():
                            taxi.remove_available_client(c)
                        self.remove_available_client(c)
                        self.move_next_pos()
                        break
            if self.state == TaxiState.free:
                if len(self.path) == 1:
                    self.move_next_pos()
                    self.state = TaxiState.waiting
                elif self.path == '':
                    wait_pos = self.decide_waiting_spot()
                    self.find_path(wait_pos[0], wait_pos[1])
                else:
                    self.move_next_pos()

class Client(Agent):
    def __init__(self, x, y, goal_x, goal_y):
        super().__init__(x, y)
        self.goal_x = goal_x
        self.goal_y = goal_y

    def __str__(self):
        return "Client " + super().__str__()

    def __repr__(self):
        return self.__str__()

class Quadrant():
    def __init__(self, x0, y0, x1, y1):
        self.x_start = x0
        self.x_end = x1
        self.y_start = y0
        self.y_end = y1

    def __str__(self):
        return "x between: " + str(self.x_start) + " and " + str(self.x_end) + " y between: " + str(self.y_start) + " and " + str(self.y_end)
    
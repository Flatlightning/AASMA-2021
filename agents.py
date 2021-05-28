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

class ClientState(Enum):
    unassigned = 1
    assigned = 2


class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Agent - Position: (" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()


class Taxi(Agent): #reactionary agent with no communication with other agents

    def __init__(self, x, y, identifier, board):
        super().__init__(x,y)
        self.identifier = identifier
        self.state = TaxiState.free
        self.path = ''
        self.current_client = None
        self.board = board


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

    def pickup_client(self): 
        if ((self.current_client.x, self.current_client.y) in self.board.clients.keys()):
                self.board.clients.pop((self.current_client.x, self.current_client.y))
                self.find_path(self.current_client.goal_x, self.current_client.goal_y)
        else:
            self.current_client = None

    def goto_client(self,client):
        self.current_client = client
        self.find_path(self.current_client.x, self.current_client.y)
        client.state = ClientState.assigned

    def dropoff_client(self):
        self.current_client = None

    def find_path(self, goal_x, goal_y):
        self.path = a_star.path_find(self.x, self.y, goal_x,  goal_y, self.board.board_size[0])

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
                
    def eucl_dist(self, pos):
        return math.sqrt(pow((self.x - pos[0]),2) + pow((self.y - pos[1]), 2))
    
    def find_closest_client(self):
        closest_client = None
        if (self.board.clients.values()):
            closest_client = list(self.board.clients.values())[0]
        for c in self.board.clients.values():
            if self.eucl_dist((closest_client.x,closest_client.y)) > self.eucl_dist((c.x,c.y)):
                closest_client = c
        if (closest_client):
            self.goto_client(closest_client)

    def decision_making(self): #change to pure reactionary behaviour
        if self.state == TaxiState.pickup:
            if self.path == '':
                self.board.update_board()
                self.pickup_client()
                print(self, self.current_client)
                if (self.current_client):
                    self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " PICKED UP CLIENT ON (" + str(self.current_client.x) +", "+ str(self.current_client.y) + ")\n")
                    self.state = TaxiState.dropoff
                else:
                    self.state = TaxiState.waiting
                    self.find_closest_client()
                    if (self.current_client):
                        self.state = TaxiState.pickup


            elif (not (self.current_client.x, self.current_client.y) in self.board.clients.keys()):
                self.current_client = None
                self.path = ''
                self.state = TaxiState.waiting
                self.find_closest_client()
                if (self.current_client):
                    self.state = TaxiState.pickup

            else:
                self.move_next_pos()
                
        elif self.state == TaxiState.dropoff:      
            if self.path == '':
                self.dropoff_client()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " DROPPED CLIENT OFF\n")
                self.state = TaxiState.waiting
            else:
                self.move_next_pos()

        else:
            self.find_closest_client()
            if (self.path):
                self.state = TaxiState.pickup
                self.move_next_pos()

class SmartTaxi(Taxi):
    def __init__(self, x, y, identifier, board):
        super().__init__(x,y, identifier, board)
        self.taxi_list = {} # maybe not in the superclass
        self.available_clients = {}
        self.last_clients = []
        self.quadrant_probabilities = np.ones((len(self.board.quadrants),))
        #tuple with assigned quadrant and position inside quadrant
        self.assigned_quadrant = None
        #works as a constant 
        self.max_capacity = 4 
        #maybe change this to board and save quadrants in board?

    def pickup_client(self, client):
        self.current_client = client
        self.assigned_quadrant = None
        self.find_path(self.current_client.x, self.current_client.y)
        for taxi in self.taxi_list.values():
            taxi.remove_available_client(client)
        self.remove_available_client(client)
        client.state = ClientState.assigned

    def is_closest(self, client):
        my_dist = self.eucl_dist((client.x, client.y))
        for taxi in self.taxi_list.values():
            if (taxi.state == TaxiState.free or taxi.state == TaxiState.waiting):
                if (taxi.eucl_dist((client.x, client.y)) < my_dist):
                    return False
                elif (taxi.eucl_dist((client.x, client.y)) == my_dist and taxi.identifier < self.identifier):
                    return False
        return True

    def add_client(self, client):
        self.available_clients[(client.x, client.y)] = client
        self.update_waiting_matrix(client)

    def add_taxi(self, taxi):
        self.taxi_list[taxi.identifier] = taxi

    def remove_available_client(self, client):
        if ((client.x, client.y) in self.available_clients.keys()):
            self.available_clients.pop((client.x, client.y))

    def in_quadrant(self, agent):
        x = agent.x // self.board.quadrant_size
        y = agent.y // self.board.quadrant_size
        return (x + (self.board.board_size[0]//self.board.quadrant_size) * y)
    
    def is_quadrant_full(self, quadrant_index):
        count = 0
        for t in self.taxi_list.values():
            if t.state == TaxiState.waiting and self.in_quadrant(t) == quadrant_index:
                count += 1
            if count == self.max_capacity:
                return True
        
        return False
    
    def update_waiting_matrix(self, client):
        update_value = len(self.board.quadrants)
        self.last_clients += [client]
        print("quadrant probabilities", self.quadrant_probabilities)
        self.quadrant_probabilities[(self.in_quadrant(client))] += update_value
        oldest_client = None

        # remove old information from probabilities 
        if len(self.last_clients) > 15:
            oldest_client = self.last_clients[0]
            self.quadrant_probabilities[(self.in_quadrant(oldest_client))] -= update_value
            self.last_clients = self.last_clients[1:]
        
        return

    
    def check_new_clients(self):
        for c in self.board.clients.values():
            if c.state == ClientState.unassigned:
                if not c in self.available_clients.values():
                    print("added ", c)
                    self.add_client(c)

            elif not c in self.last_clients:
                self.update_waiting_matrix(c)


    def decide_waiting_spot(self):
        #create a dictionary of quadrants and respective number of assigned taxis
        quadrants_capacity = {}
        for i in range(len(self.board.quadrants)):
            quadrants_capacity[i] = 0
        
        #fill quadrant capacity structure
        for t in self.taxi_list.values():
            if t.assigned_quadrant:
                quadrants_capacity[t.assigned_quadrant[0]] += 1
        
        #update quadrant probabilities so it doesn't include full quadrants
        biased_probabilities = self.quadrant_probabilities.copy()
        for q in quadrants_capacity.keys():
            if quadrants_capacity[q] == self.max_capacity:
                biased_probabilities[q] = 0
        
        #choose a possible quadrant and position inside said quadrant to wait for a client

        #check if there is a near taxi finishing a ride near the chosen position
        #if so, assign the chosen position to the other driver and choose another position to wait in
        
        while not self.assigned_quadrant:
            chosen_quadrant_id = np.random.choice(range(len(self.board.quadrants)), p = (biased_probabilities/biased_probabilities.sum()))
            chosen_quadrant = self.board.quadrants[chosen_quadrant_id]
            chosen_pos = (rand.randrange(chosen_quadrant.x_start, chosen_quadrant.x_end), rand.randrange(chosen_quadrant.y_start, chosen_quadrant.y_end))
            change_pos = False
            for t in self.taxi_list.values():
                if t.state == TaxiState.dropoff and self.eucl_dist(chosen_pos) > (t.eucl_dist(chosen_pos) + len(t.path)+ 1 ): # TODO add tolerance value
                    t.assigned_quadrant = (chosen_quadrant_id, chosen_pos)
                    #update capacities with most recent assignment
                    quadrants_capacity[chosen_quadrant_id] += 1
                    if quadrants_capacity[chosen_quadrant_id] == self.max_capacity:
                        biased_probabilities[chosen_quadrant_id] = 0
                    change_pos = True
            if not change_pos:
                self.assigned_quadrant = (chosen_quadrant_id, chosen_pos)
        
        print ("assigned quadrant: ", self.assigned_quadrant)
        return

    
    def decision_making(self):
        print(self.state)
        self.check_new_clients()
        if self.state == TaxiState.pickup:
            self.move_next_pos()
            if self.path == '':
                self.board.update_board()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " PICKED UP CLIENT ON (" + str(self.current_client.x) +", "+ str(self.current_client.y) + ")\n")
                self.state = TaxiState.dropoff
                self.board.clients.pop((self.current_client.x, self.current_client.y))
                self.find_path(self.current_client.goal_x, self.current_client.goal_y)
                
        elif self.state == TaxiState.dropoff:      
            if self.path == '':
                self.dropoff_client()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " DROPPED CLIENT OFF\n")
                self.state = TaxiState.free
                if (self.assigned_quadrant):
                    self.find_path(self.assigned_quadrant[1][0], self.assigned_quadrant[1][0])
            else:
                self.move_next_pos()

        else:
            print(self.available_clients)
            if self.available_clients:
                for c in self.available_clients.values():
                    if(self.is_closest(c)):
                        self.pickup_client(c)
                        self.state = TaxiState.pickup
                        self.move_next_pos()
                        break
            if self.state == TaxiState.free:
                if len(self.path) == 1:
                    self.move_next_pos()
                    self.state = TaxiState.waiting
                elif self.path == '':
                    self.decide_waiting_spot()
                    self.find_path(self.assigned_quadrant[1][0], self.assigned_quadrant[1][1])
                else:
                    self.move_next_pos()

class RandomTaxi(Taxi):
    def __init__(self, x, y, identifier, board):
        super().__init__(x, y, identifier, board)
        self.taxi_list = {}
        self.available_clients = {}
        self.assigned_waiting_spot = None

    def add_taxi(self, taxi):
        self.taxi_list[taxi.identifier] = taxi

    def add_client(self, client):
        self.available_clients[(client.x, client.y)] = client

    def remove_available_client(self, client):
        if ((client.x, client.y) in self.available_clients.keys()):
            self.available_clients.pop((client.x, client.y))

    def pickup_client(self, client):
        self.current_client = client
        self.assigned_waiting_pos = None
        self.find_path(self.current_client.x, self.current_client.y)
        for taxi in self.taxi_list.values():
            taxi.remove_available_client(client)
        self.remove_available_client(client)
        client.state = ClientState.assigned

    def is_closest(self, client):
        my_dist = self.eucl_dist((client.x, client.y))
        for taxi in self.taxi_list.values():
            if (taxi.state == TaxiState.free or taxi.state == TaxiState.waiting):
                if (taxi.eucl_dist((client.x, client.y)) < my_dist):
                    return False
                elif (taxi.eucl_dist((client.x, client.y)) == my_dist and taxi.identifier < self.identifier):
                    return False
        return True

    def check_new_clients(self):
        for c in self.board.clients.values():
            if c.state == ClientState.unassigned:
                if not c in self.available_clients.values():
                    self.add_client(c)

    def decide_waiting_spot(self):
        #create a dictionary of quadrants and respective number of assigned taxis
        self.assigned_waiting_spot = (rand.randrange(self.board.board_size[0]), rand.randrange(self.board.board_size[1]))
        print ("assigned position: ", self.assigned_waiting_spot)

    def decision_making(self):
        self.check_new_clients()
        if self.state == TaxiState.pickup:
            
            if self.path == '':
                self.board.update_board()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " PICKED UP CLIENT ON (" + str(self.current_client.x) +", "+ str(self.current_client.y) + ")\n")
                self.state = TaxiState.dropoff
                self.board.clients.pop((self.current_client.x, self.current_client.y))
                self.find_path(self.current_client.goal_x, self.current_client.goal_y)

            else:
                self.move_next_pos()
                
        elif self.state == TaxiState.dropoff:      
            if self.path == '':
                self.dropoff_client()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " DROPPED CLIENT OFF\n")
                self.state = TaxiState.free
            else:
                self.move_next_pos()

        else:
            print(self.available_clients)
            if self.available_clients:
                for c in self.available_clients.values():
                    if(self.is_closest(c)):
                        self.pickup_client(c)
                        self.state = TaxiState.pickup
                        self.move_next_pos()
                        break
            if self.state == TaxiState.free:
                if len(self.path) == 1:
                    self.move_next_pos()
                    self.state = TaxiState.waiting
                elif self.path == '':
                    self.decide_waiting_spot()
                    self.find_path(self.assigned_waiting_spot[0], self.assigned_waiting_spot[1])
                else:
                    self.move_next_pos()


class ClosestTaxi(Taxi):
    def __init__(self, x, y, identifier, board):
        super().__init__(x, y, identifier, board)
        self.taxi_list = {} 
        self.available_clients = {}
    
    def add_taxi(self, taxi):
        self.taxi_list[taxi.identifier] = taxi

    def add_client(self, client):
        self.available_clients[(client.x, client.y)] = client

    def remove_available_client(self, client):
        if ((client.x, client.y) in self.available_clients.keys()):
            self.available_clients.pop((client.x, client.y))

    def pickup_client(self, client):
        self.current_client = client
        self.assigned_quadrant = None
        self.find_path(self.current_client.x, self.current_client.y)
        for taxi in self.taxi_list.values():
            taxi.remove_available_client(client)
        self.remove_available_client(client)
        client.state = ClientState.assigned

    def is_closest(self, client):
        my_dist = self.eucl_dist((client.x, client.y))
        for taxi in self.taxi_list.values():
            if (taxi.state == TaxiState.free or taxi.state == TaxiState.waiting):
                if (taxi.eucl_dist((client.x, client.y)) < my_dist):
                    return False
                elif (taxi.eucl_dist((client.x, client.y)) == my_dist and taxi.identifier < self.identifier):
                    return False
        return True

    def check_new_clients(self):
        for c in self.board.clients.values():
            if c.state == ClientState.unassigned:
                if not c in self.available_clients.values():
                    self.add_client(c)

    def decision_making(self):
        print(self.state)
        self.check_new_clients()
        if self.state == TaxiState.pickup:    
            if self.path == '':
                self.board.update_board()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " PICKED UP CLIENT ON (" + str(self.current_client.x) +", "+ str(self.current_client.y) + ")\n")
                self.state = TaxiState.dropoff
                self.board.clients.pop((self.current_client.x, self.current_client.y))
                self.find_path(self.current_client.goal_x, self.current_client.goal_y)
                
            else:
                self.move_next_pos()
                
        elif self.state == TaxiState.dropoff:      
            if self.path == '':
                self.dropoff_client()
                self.board.update_log_text("TAXI - ID: " + str(self.identifier) + " DROPPED CLIENT OFF\n")
                self.state = TaxiState.waiting
            else:
                self.move_next_pos()

        else:
            print(self.available_clients)
            if self.available_clients:
                for c in self.available_clients.values():
                    if(self.is_closest(c)):
                        self.pickup_client(c)
                        self.state = TaxiState.pickup
                        self.move_next_pos()
                        break

class Client(Agent):
    def __init__(self, x, y, goal_x, goal_y):
        super().__init__(x, y)
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.state = ClientState.unassigned

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
    
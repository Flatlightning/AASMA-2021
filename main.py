from pathfind import main_pathfinding 
from agents import *
from board import *
import random
import tkinter as tk
import numpy as np
import threading
import subprocess
import sys
import time


def operations(size):
    print("Types of Agent:\n1: Reactive Agents with no communication\n2: Agents that don't choose a waiting spot\n3: Agents with a random waiting spot\n4: Agents that learn which are the optimal waiting spots")
    agent_type = input("Agent Type: ")
    nTaxis = input("Number of Taxis: ")
    random_generation = False
    random_clients = {}
    clients_coords = []
    if (agent_type == "1"):
        for i in range(int(nTaxis)):
            coords = input("Taxi coordinates" + str(i+1) + ": ")
            coords = coords.split(" ")
            board.add_taxi(Taxi(int(coords[0]), int(coords[1]), i+1, board))
    elif (agent_type == "2"):
        for i in range(int(nTaxis)):
            coords = input("Taxi coordinates" + str(i+1) + ": ")
            coords = coords.split(" ")
            board.add_taxi(ClosestTaxi(int(coords[0]), int(coords[1]), i+1, board))
    elif (agent_type == "3"):
        for i in range(int(nTaxis)):
            coords = input("Taxi coordinates" + str(i+1) + ": ")
            coords = coords.split(" ")
            board.add_taxi(RandomTaxi(int(coords[0]), int(coords[1]), i+1, board))
    elif (agent_type == "4"):
        for i in range(int(nTaxis)):
            coords = input("Taxi coordinates" + str(i+1) + ": ")
            coords = coords.split(" ")
            board.add_taxi(SmartTaxi(int(coords[0]), int(coords[1]), i+1, board))
    else:
        print("Invalid Option")
        return
    if (not agent_type == "1"):
        for taxi in board.taxis.values():
            for taxi2 in board.taxis.values():
                if taxi2.identifier != taxi.identifier:
                    taxi.add_taxi(taxi2)

    rnd = input("Random? (yes or no): ")
    if rnd == "yes":
        random_generation = True
        fst_focus_ind = None
        snd_focus_ind = None
        print("All quadrants:")
        for i in range(len(board.quadrants)):
            print (str(i) + ": " + str(board.quadrants[i]))

        if (len(board.quadrants) == 4):
            fst_focus_ind = input("Select the high client density quadrant: ")
        else:
            fst_focus_ind = input("Select the first high client density quadrant: ")
            snd_focus_ind = input("Select the second high client density quadrant: ")

        board.focus_quadrants += [board.quadrants[int(fst_focus_ind)]]
        if (snd_focus_ind):
            board.focus_quadrants += [board.quadrants[int(snd_focus_ind)]]

#-------------------------------------- RANDOM PIPELINE GENERATION--------------------------------------------

        #timesteps = input("Execution Time (in timesteps): ")
        #nClients = input("Number of Clients: ")
        #timestep_list = np.sort(np.random.randint(int(timesteps), size=(int(nClients))))
        #for ts in timestep_list:
        #    in_focus_quadrant = random.random()
        #    if (in_focus_quadrant <= 0.7):  #generate client in high density (focus) quadrant
        #        print("inside focus quadrant")
        #        if (snd_focus_quadrant): #when there are two focus quadrant make a 50/50 choice after the 70/30 choice
#
        #            if(random.random() <= 0.5):
        #                (x, y) = (random.randrange(fst_focus_quadrant.x_start, fst_focus_quadrant.x_end), random.randrange(fst_focus_quadrant.y_start, fst_focus_quadrant.y_end))
#
        #            else:
        #                (x, y) = (random.randrange(snd_focus_quadrant.x_start, snd_focus_quadrant.x_end), random.randrange(snd_focus_quadrant.y_start, snd_focus_quadrant.y_end))
#
        #        else: #when there is a single focus quadrant
        #            (x, y) = (random.randrange(fst_focus_quadrant.x_start, fst_focus_quadrant.x_end), random.randrange(fst_focus_quadrant.y_start, fst_focus_quadrant.y_end))
#
        #    else:   #generate random position anywhere on the grid
        #        (x, y) = (random.randrange(int(size)), random.randrange(int(size)))
        #
        #    random_clients[ts] = Client(x, y, random.randrange(int(size)), random.randrange(int(size)))
        #    clients_coords.append((x, y))
        #print(random_clients)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    elif rnd == "no":
        random_generation = False
    timestep = 0
    while True:
        input("timestep: " + str(timestep))
        if random_generation:
            board.generate_random_client()
            board.update_board()
            for taxi in board.taxis.values():
                taxi.decision_making()
            board.update_board()

        else:
            client = input("Client? ")
            if len(client) > 0:
                coords = input("Client coordinates: ")
                coords = coords.split(" ")
                destination = input("Client destination: ")
                destination = destination.split(" ")
                board.add_client(Client(int(coords[0]), int(coords[1]), int(destination[0]), int(destination[1])))
            for taxi in board.taxis.values():
                taxi.decision_making()
            board.update_board()
        timestep += 1

size = input("Grid size: ")
root = tk.Tk()
board = Board(root, (int(size), int(size)))
thread = threading.Thread(target=operations(size))
thread.start()
board.mainloop()

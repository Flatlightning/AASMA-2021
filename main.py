from pathfind import main_pathfinding 
from agents import *
from board import *
from random import randrange
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
    random = False
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
        random = True
        timesteps = input("Timesteps: ")
        nClients = input("Number of Clients: ")
        timestep_list = np.sort(np.random.randint(int(timesteps), size=(int(nClients))))
        for ts in timestep_list:
            (x, y) = (randrange(int(size)), randrange(int(size)))
            while ((x, y) in clients_coords):
                (x, y) = (randrange(int(size)), randrange(int(size)))
            random_clients[ts] = Client(x, y, randrange(int(size)), randrange(int(size)))
            clients_coords.append((x, y))
        print(random_clients)
    elif rnd == "no":
        random = False
    timestep = 0
    while True:
        enter = input("timestep: " + str(timestep))
        if random:
            if(timestep in random_clients.keys()):
                board.add_client(random_clients[timestep])
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

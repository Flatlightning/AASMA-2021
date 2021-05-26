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
    nTaxis = input("Number of Taxis: ")
    random = False
    random_clients = {}
    clients_coords = []
    for i in range(int(nTaxis)):
        coords = input("Coordenadas do taxi " + str(i+1) + ": ")
        coords = coords.split(" ")
        board.add_taxi(Taxi(int(coords[0]), int(coords[1]), i+1, board))
    
    for taxi in board.taxis.values():
        for taxi2 in board.taxis.values():
            if taxi2.identifier != taxi.identifier:
                taxi.add_taxi(taxi2)

    #board.add_client(Client(3, 3, 1, 1))
    #board.add_client(Client(2, 3, 3, 3))
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
                coords = input("Coordenadas do cliente: ")
                coords = coords.split(" ")
                destination = input("Destino do cliente: ")
                destination = destination.split(" ")
                board.add_client(Client(int(coords[0]), int(coords[1]), int(destination[0]), int(destination[1])))
            for taxi in board.taxis.values():
                taxi.decision_making()
            board.update_board()
        timestep += 1

    '''
    taxi.left()
    board.update_board()
    board.update_log_text("MOVE TAXI - ID: " + str(taxi.identifier) + "; (" +
                    str(taxi.x+1) + ", " + str(taxi.y) + ") -> (" +
                    str(taxi.x) + ", " + str(taxi.y) + ")\n")
    '''


size = input("Grid size: ")
root = tk.Tk()
board = Board(root, (int(size), int(size)))
thread = threading.Thread(target=operations(size))
thread.start()
board.mainloop()

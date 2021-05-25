from pathfind import main_pathfinding 
from agents import *
from board import *
import tkinter as tk
import threading
import subprocess
import sys
import time


def operations():
    nTaxis = input("Number of Taxis: ")
    for i in range(int(nTaxis)):
        coords = input("Coordenadas do taxi " + str(i+1) + ": ")
        coords = coords.split(" ")
        board.add_taxi(Taxi(int(coords[0]), int(coords[1]), i+1, board))
    
    for taxi in board.taxis.values():
        for taxi2 in board.taxis.values():
            if taxi2.identifier != taxi.identifier:
                taxi.add_taxi(taxi2)

    board.add_client(Client(3, 3, 1, 1))
    #board.add_client(Client(2, 3, 3, 3))
    while True:
        client = input("Client? ")
        print(type(client))
        if len(client) > 0:
            coords = input("Coordenadas do cliente: ")
            coords = coords.split(" ")
            destination = input("Destino do cliente: ")
            destination = destination.split(" ")
            board.add_client(Client(int(coords[0]), int(coords[1]), int(destination[0]), int(destination[1])))
        for taxi in board.taxis.values():
            taxi.decision_making()
        board.update_board()


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
thread = threading.Thread(target=operations)
thread.start()
board.mainloop()

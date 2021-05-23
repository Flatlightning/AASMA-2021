from pathfind import main_pathfinding 
from agents import *
import subprocess
import sys
import time

taxis = {}



size = input("Grid size: ")
nTaxis = input("Number of Taxis: ")
for i in range(int(nTaxis)):
    coords = input("Coordenadas do taxi " + str(i+1) + ": ")
    coords = coords.split(" ")
    taxis[i+1] = Taxi(int(coords[0]), int(coords[1]), i+1)

proc = subprocess.Popen([sys.executable, 'env.py', str(size), str(size)],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

for taxi in taxis.values():
    for t in taxis.values():
        if t.identifier != taxi.identifier:
            taxi.taxi_list.append(t)

for taxi in taxis.values():
    inp = 'taxi ' + str(taxi.identifier) + ' ' + str(taxi.x) + ' ' + str(taxi.y)+'\n'
    proc.stdin.write(inp)
proc.stdin.write("end taxis\n")



"""
    size = 7
    agent1_coords = [1, 1]
    agent1_dest = [4, 3]
    path = main_pathfinding(size, agent1_coords, agent1_dest)

    inp = 'taxi 1 '+str(agent1_coords[0]) + ' ' + str(agent1_coords[1])+'\n'
    inp2 = 'taxi 2 '+str(agent1_coords[0] + 1) + ' ' + str(agent1_coords[1] + 1)+'\n'

    proc = subprocess.Popen([sys.executable, 'env.py', str(size), str(size)],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    print(inp)
    print(inp2)
    proc.stdin.write(inp)
    proc.stdin.write(inp2)
    proc.stdin.write("end taxis\n")

    for move in path:
        print("move is "+ move)
        if move == "U":
            print("going " + move)
            proc.stdin.write('go 1 up\n')
            proc.stdin.write("end moves\n")
        elif move == "D":
            print("going " + move)
            proc.stdin.write('go 1 down\n')
            proc.stdin.write("end moves\n")
        elif move == "L":
            print("going " + move)
            proc.stdin.write('go 1 left\n')
            proc.stdin.write("end moves\n")
        elif move == "R":
            print("going " + move)
            proc.stdin.write('go 1 right\n')
            proc.stdin.write("end moves\n")
"""
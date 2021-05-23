import board
import sys
import threading
import tkinter as tk
from agents import *


# Receive Board Dimensions as Argument
if len(sys.argv) != 3:
    raise Exception("Invalid Board Dimensions Format")

try:
    length = int(sys.argv[1])
    width = int(sys.argv[2])
except ValueError:
    raise Exception("Invalid Board Dimensions")

board_size = (length, width)
# debug prints #
# print(board_size)
################


def wait_for_input():
    taxis = {}
    clients = {}

    # Create Taxis
    # taxi command format: taxi $id $x $y
    inp = input()
    inp = inp.split(" ")
    while inp != ["end", "taxis"]:
        if inp[0] != "taxi":
            raise Exception("Wrong command: Insert Taxi Info")
        if len(inp) != 4:
            raise Exception("Invalid Taxi Input Format")

        try:
            identifier = int(inp[1])
            x = int(inp[2])
            y = int(inp[3])
        except ValueError:
            raise Exception("Invalid Taxi Values")

        if x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]:
            raise Exception("Invalid Coordinates")

        if identifier in taxis.keys():
            raise Exception("Taxi ID already taken")

        gui.update_log_text("NEW TAXI - ID: " + str(identifier) + "; (" + str(x) + ", " + str(y) + ")\n")
        taxis[identifier] = Taxi(x, y, identifier)

        gui.update_board(taxis)

        # debug prints #
        # print([taxi for taxi in taxis.values()])
        ################

        inp = input()
        inp = inp.split(" ")

    # debug prints #
    # print("taxis insertion end")
    ################

    if len(taxis) == 0:
        raise Exception("No Taxi Created")

    # Create Clients and Move Taxis
    # client command format: client $x $y
    # go command format: goto $id up/down/left/right
    # pickup command format: pickup $id
    # free command format: free $id
    timestep = 1
    current_ts_moves = []
    log_text = "* TIMESTEP " + str(timestep) + " *\n"
    while True:
        inp = input()
        inp = inp.split(" ")

        if inp[0] == "client":
            if len(inp) != 3:
                raise Exception("Invalid Client Input Format")

            try:
                x = int(inp[1])
                y = int(inp[2])
            except ValueError:
                raise Exception("Invalid Client Values")

            if x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]:
                raise Exception("Invalid Coordinates")

            if (x, y) in clients.keys():
                raise Exception("Position Occupied by Another Client")

            log_text += "NEW CLIENT - (" + str(x) + ", " + str(y) + ")\n"
            clients[(x, y)] = Client(x, y)
        elif inp[0] == "go":
            if len(inp) != 3:
                raise Exception("Invalid Move Input Format")

            try:
                identifier = int(inp[1])
            except ValueError:
                raise Exception("Invalid Move Values")

            if not (inp[2] == "up" or inp[2] == "down" or inp[2] == "left" or inp[2] == "right"):
                raise Exception("Invalid Move Option")

            if identifier in current_ts_moves:
                raise Exception("Invalid Move: Taxi Already Moved in The Current Time Step")

            old_row = taxis[identifier].x
            old_column = taxis[identifier].y

            if inp[2] == "up":
                if taxis[identifier].y > 0:
                    taxis[identifier].up()
                else:
                    raise Exception("Invalid Move: Taxi Can Not Move Up")
            elif inp[2] == "down":
                if taxis[identifier].y < board_size[0]-1:
                    taxis[identifier].down()
                else:
                    raise Exception("Invalid Move: Taxi Can Not Move Down")
            elif inp[2] == "left":
                if taxis[identifier].x > 0:
                    taxis[identifier].left()
                else:
                    raise Exception("Invalid Move: Taxi Can Not Move Left")
            elif inp[2] == "right":
                if taxis[identifier].x < board_size[1]-1:
                    taxis[identifier].right()
                else:
                    raise Exception("Invalid Move: Taxi Can Not Move Right")

            log_text +=\
                "MOVE TAXI - ID: " + str(identifier) + "; (" + \
                str(old_row) + ", " + str(old_column) + ") -> (" + \
                str(taxis[identifier].x) + ", " + str(taxis[identifier].y) + ")\n"

            current_ts_moves.append(identifier)
        elif inp[0] == "pickup":
            if len(inp) != 2:
                raise Exception("Invalid Pickup Input Format")

            try:
                identifier = int(inp[1])
            except ValueError:
                raise Exception("Invalid Pickup Values")

            x = taxis[identifier].x
            y = taxis[identifier].y

            if x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]:
                raise Exception("Invalid Coordinates")

            if not (x, y) in clients.keys():
                raise Exception("Invalid Pickup: There is no Client at The Current Position")

            if not taxis[identifier].state == TaxiState.free:
                raise Exception("Invalid Pickup: The Selected Taxi is Occupied")

            log_text += "TAXI PICKUP - ID: " + str(identifier) + "\n"
            del clients[(x, y)]
            taxis[identifier].state = TaxiState.occupied
        elif inp[0] == "free":
            if len(inp) != 2:
                raise Exception("Invalid Free Input Format")

            try:
                identifier = int(inp[1])
            except ValueError:
                raise Exception("Invalid Free Values")

            log_text += "TAXI FREE - ID: " + str(identifier) + "\n"
            taxis[identifier].state = TaxiState.free
        elif inp == ["end", "moves"]:
            gui.update_board(taxis, clients)
            gui.update_log_text(log_text)
            timestep += 1
            log_text = "* TIMESTEP " + str(timestep) + " *\n"
            current_ts_moves = []
        else:
            raise Exception("Wrong command: Insert Client Info or Move Taxi")

        # debug prints #
        # print([client for client in clients.values()])
        # print([taxi for taxi in taxis.values()])
        ################


root = tk.Tk()
gui = board.Board(root, board_size)
thread = threading.Thread(target=wait_for_input)
thread.start()
gui.mainloop()

import tkinter as tk
from agents import *

SQUARE_SIDE = 30


class Board(tk.Frame):
    canvas = None
    board_size = None
    log_text = None

    def __init__(self, master, board_size):
        super().__init__(master)
        master.title("Test Environment - AASMA")
        self.board_size = board_size
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.grid(row=0, column=0)
        self.taxis = {}
        self.clients = {}
        # draw the grid
        self.update_board()
        # x numbers
        for i in range(self.board_size[0]):
            self.canvas.create_text((i * SQUARE_SIDE + SQUARE_SIDE / 2,
                                     self.board_size[1] * SQUARE_SIDE + SQUARE_SIDE / 2), text=str(i))
        # y numbers
        for i in range(self.board_size[1]):
            self.canvas.create_text((self.board_size[0] * SQUARE_SIDE + SQUARE_SIDE / 2,
                                     i * SQUARE_SIDE + SQUARE_SIDE / 2), text=str(i))

        self.log_text = tk.Text(master)
        self.log_text.grid(row=0, column=1)
        self.log_text.insert("end", "---------------\n- Command Log -\n---------------\n")

    def add_taxi(self, taxi):
        self.update_log_text("NEW TAXI - ID: " + str(taxi.identifier) + "; (" +
                             str(taxi.x) + ", " + str(taxi.y) + ")\n")
        self.taxis[taxi.identifier] = taxi
        self.update_board()

    def add_client(self, client):
        self.update_log_text("NEW CLIENT - (" + str(client.x) + ", " + str(client.y) + ")\n")
        self.clients[(client.x, client.y)] = client
        self.update_board()
        for taxi in self.taxis.values():
            taxi.add_client(client)

    def update_board(self):
        # draw the grid
        for i in range(self.board_size[0]):
            x = i * SQUARE_SIDE
            for j in range(self.board_size[1]):
                y = j * SQUARE_SIDE
                self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="white")

        # draw the clients
        for client in self.clients.values():
            x = client.x * SQUARE_SIDE
            y = client.y * SQUARE_SIDE
            self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="blue")

        # draw the taxis
        for taxi in self.taxis.values():
            x = taxi.x * SQUARE_SIDE
            y = taxi.y * SQUARE_SIDE
            # if the position is occupied by a client, represent the taxi as a triangle
            if self.clients is not None and (taxi.x, taxi.y) in self.clients.keys():
                points = [x, y, x + SQUARE_SIDE, y, x, y + SQUARE_SIDE]

                if taxi.state == TaxiState.free:
                    self.canvas.create_polygon(points, fill="orange")

                else:
                    self.canvas.create_polygon(points, fill="red")

                self.canvas.create_text((x + SQUARE_SIDE / 4,
                                         y + SQUARE_SIDE / 4),
                                        text=str(taxi.identifier))
            else:
                if taxi.state == TaxiState.free:
                    self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="orange")
                
                
                elif taxi.state == TaxiState.waiting:
                    self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="yellow")

                else:
                    self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="red")

                self.canvas.create_text((x + SQUARE_SIDE / 2,
                                         y + SQUARE_SIDE / 2),
                                        text=str(taxi.identifier))

        self.after(1000)

    def update_log_text(self, log_text):
        self.log_text.insert("end", log_text)

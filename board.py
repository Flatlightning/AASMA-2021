import tkinter as tk
from agents import *
import math

SQUARE_SIDE = 30
QUADRANT_COLOR_1 = "#cbe8f5"
QUADRANT_COLOR_2 = "#ddd5f0"

class Quadrant():
    def __init__(self, x0, y0, x1, y1):
        self.x_start = x0
        self.x_end = x1
        self.y_start = y0
        self.y_end = y1

    def __str__(self):
        return "x between: " + str(self.x_start) + " and " + str(self.x_end) + " y between: " + str(self.y_start) + " and " + str(self.y_end)


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
        self.quadrants = []
        self.quadrant_size = board_size[0]
        self.calculate_quadrants()
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
    
    def generate_random_client(self):
        return

    def update_board(self):
        # draw the grid
        quadrant_color = True
        quadrants_per_line = math.sqrt(len(self.quadrants))
        count_q = 0
        for q in self.quadrants:
            count_q += 1
            for i in range(q.x_start, q.x_end+1):
                x = i * SQUARE_SIDE
                for j in range(q.y_start, q.y_end+1):
                    y = j * SQUARE_SIDE
                    if quadrant_color:
                        self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill=QUADRANT_COLOR_1)
                    else:
                        self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill=QUADRANT_COLOR_2)
            if (count_q % quadrants_per_line):
                quadrant_color = not quadrant_color


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
                else:
                    self.canvas.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill="red")

                self.canvas.create_text((x + SQUARE_SIDE / 2,
                                         y + SQUARE_SIDE / 2),
                                        text=str(taxi.identifier))

        self.after(1000)

    def update_log_text(self, log_text):
        self.log_text.insert("end", log_text)

    def calculate_quadrants(self):
        quadrant_area = self.board_size[0] * self.board_size[1]
        count = 0
        while not quadrant_area % 4 and quadrant_area > 16:
            quadrant_area = quadrant_area // 4
            count += 2
        self.quadrant_size = int(math.sqrt(quadrant_area))     
        pos_y = 0                                         
        for i in range(count):
            pos_x = 0
            for i in range(count):
                self.quadrants += [Quadrant(pos_x, pos_y,pos_x + self.quadrant_size - 1, pos_y + self.quadrant_size - 1)]
                pos_x += self.quadrant_size
            pos_y += self.quadrant_size

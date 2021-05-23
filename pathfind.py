import queue
import subprocess
import sys

def createMaze(size):
    maze = []
    first_line = []
    for _ in range(size+2):
        first_line.append("#")

    maze.append(first_line)
    for x in range(size):
        middle_line = ["#"]
        for i in range(size):
            middle_line.append(" ")
        middle_line.append("#")
        maze.append(middle_line)
    last_line = []
    for _ in range(size + 2):
        last_line.append("#")
    maze.append(last_line)

    return maze


def printMaze(maze, path=""):
    for index in range(len(maze)):
        for x, pos in enumerate(maze[index]):
            if pos == "O":
                start_row = x
                start_col = index
                break

    i = start_row
    j = start_col
    pos = []
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.append([j, i])

    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if [j, i] in pos:
                if pos[-1] == [j, i]:
                    print("X ", end="")
                else:
                    print("+ ", end="")
            else:
                print(col + " ", end="")
        print()
        


def valid(maze, moves):
    for index in range(len(maze)):
        for x, pos in enumerate(maze[index]):
            if pos == "O":
                start_row = x
                start_col = index
                break

    i = start_row
    j = start_col
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == "#"):
            return False

    return True


def findEnd(maze, moves):
    for index in range(len(maze)):
        for x, pos in enumerate(maze[index]):
            if pos == "O":
                start_row = x
                start_col = index
                break

    i = start_row
    j = start_col
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if maze[j][i] == "X":
        print("Found: " + moves)
        printMaze(maze, moves)
        return True

    return False


# MAIN ALGORITHM

def main_pathfinding(size, start, end):
    nums = queue.Queue()
    nums.put("")
    add = ""
    maze = createMaze(size)
    start_row = start[0]
    start_col = start[1]
    end_row = end[0]
    end_col = end[1]

    maze[start_row][start_col] = "O"
    maze[end_row][end_col] = "X"

    printMaze(maze)


    while not findEnd(maze, add):
        add = nums.get()
        #print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)
    return add

size = 7
agent1_coords = [1, 1]
agent1_dest = [4, 3]
path = (main_pathfinding(size, agent1_coords, agent1_dest))

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


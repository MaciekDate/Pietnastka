import numpy as np
import time

# Default launch options
algo = "bfs"
order = "LRDU"
file = "puzzle.txt"

# Launch options (CMD)
# algo = sys.argv[1]
# order = sys.argv[2]
# file = sys.argv[3]

# Maximum depth of recursion
depth = 10

# Boards
final_board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
problem_board = np.loadtxt(file, skiprows=1, dtype=int)

# Find where are the blank space coordinates
where0 = np.where(problem_board == 0)
currentX = where0[0]
currentY = where0[1]

# BFS queues
queue = []
pathQueue = []
safeValve = 0
truePath = 'X'

# Global search stopper
proceed = True

# Path string
path = "X"


# Function to swap blank space with another in table
def swapper(x1, y1, x2, y2):  # Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
    temporary = problem_board[x1, y1]
    problem_board[x1, y1] = problem_board[x2, y2]
    problem_board[x2, y2] = temporary
    global currentX
    global currentY
    currentX = x2
    currentY = y2


# Deep first search
def dfs(array, origin, brake):
    global currentX
    global currentY
    global proceed
    global path
    global order
    # Check if current board is not a solution yet
    if np.array_equal(array, final_board):
        print("is equal")
        print(array)
        proceed = False
        return
    # If it's not the solution
    elif proceed:
        print("is not equal")
        print(array)
        print()
        # When we go beyond depth
        if brake > depth:
            print("Branch exhausted")
            print()
            return
        # Go through board with correct order
        for i in range(4):
            if order[i] == "R":
                if origin != 'L' and currentY + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper(currentX, currentY, currentX, currentY + 1)
                    path = path + "R"
                    dfs(array, 'R', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX, currentY - 1)
            elif order[i] == "L":
                if proceed and origin != 'R' and currentY - 1 >= 0:
                    swapper(currentX, currentY, currentX, currentY - 1)
                    path = path + "L"
                    dfs(array, 'L', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX, currentY + 1)
            elif order[i] == "D":
                if proceed and origin != 'U' and currentX + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper(currentX, currentY, currentX + 1, currentY)
                    path = path + "D"
                    dfs(array, 'D', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX - 1, currentY)
            elif order[i] == "U":
                if proceed and origin != 'D' and currentX - 1 >= 0:
                    swapper(currentX, currentY, currentX - 1, currentY)
                    path = path + "U"
                    dfs(array, 'U', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX + 1, currentY)

# Function to swap blank space with another in table
def swapper2_0(x, y, array): #Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
    whereis0 = np.where(array == 0)
    currentx = whereis0[0]
    currenty = whereis0[1]
    temporary = array[currentx, currenty]
    array[currentx, currenty] = array[currentx + x, currenty + y]
    array[currentx + x, currenty + y] = temporary


# Breadth first search
def bfs(array, origin):
    whereisE0 = np.where(array == 0)
    currentEX = whereisE0[0]
    currentEY = whereisE0[1]
    global proceed
    global queue
    global path
    global safeValve
    global truePath
    if np.array_equal(array, final_board):
        print("is equal")
        print(queue[0])
        queue.pop(0)
        truePath = pathQueue.pop(0)
        proceed = False
        return
    elif proceed and safeValve < 5000:
        print("is not equal")
        print(array)
        print()
        queue.pop(0)
        pathQueue.pop(0)
        if origin[-1] != 'L' and currentEY + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
            swapper2_0(0, 1, array)
            queue.append(np.array(array))
            originR = origin + "R"
            pathQueue.append(originR)
            #pathQueue.append("R")
            swapper2_0(0, -1, array)

        if proceed and origin[-1] != 'R' and currentEY - 1 >= 0:
            swapper2_0(0, -1, array)
            #path = path + "L"
            queue.append(np.array(array))
            originL = origin + "L"
            pathQueue.append(originL)
            #pathQueue.append("L")
            swapper2_0(0, 1, array)

        if proceed and origin[-1] != 'U' and currentEX + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
            swapper2_0(1, 0, array)
            #path = path + "D"
            queue.append(np.array(array))
            originD = origin + "D"
            pathQueue.append(originD)
            #pathQueue.append("D")
            swapper2_0(-1, 0, array)

        if proceed and origin[-1] != 'D' and currentEX - 1 >= 0:
            swapper2_0(-1, 0, array)
            #path = path + "U"
            queue.append(np.array(array))
            originU = origin + "U"
            pathQueue.append(originU)
            #pathQueue.append("U")
            swapper2_0(1, 0, array)
        safeValve += 1
        bfs(queue[0], pathQueue[0])


# Main function
if __name__ == '__main__':
    print("Final board:")
    print(final_board)

    print("\nCurrent board:")
    print(problem_board)

    print("\nCurrent position of blank space(X/Y):")
    print(currentX)
    print(currentY)

    # Count runtime of an algorithm
    start_time = time.time()
    queue.append(problem_board)
    pathQueue.append("X")
    print("\nAlgorithm start:")

    #UNCOMMENT FOR BFS
    # bfs(problem_board, truePath)
    # print(len(queue))
    # print(truePath)
    # queue.clear()
    # print(queue)
    # print()
    # print()

    #UNCOMMENT FOR DFS
    dfs(problem_board, 'N', 0)
    print(path)


    # Options (CMD)
    # print("\nAlgorithm: ", algo)
    # print("Order: ", order)
    # print("Board file: ", file)

    print("\n--- It took: %s seconds ---" % (time.time() - start_time))
import numpy as np
import time

# Maximum depth of recursion
depth = 20

# Boards
final_board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
problem_board = np.loadtxt("puzzle.txt", skiprows=1, dtype=int)

# Find where are the blank space coords
where0 = np.where(problem_board == 0)
currentX = where0[0]
currentY = where0[1]

varX = 0
varY = 0

# Global search stopper
proceed = True

# Function to swap blank space with another in table
def swapper(x1, y1, x2, y2): #Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
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
    global varX
    global varY
    global proceed
    if np.array_equal(array, final_board):
        print("is equal")
        print(array)
        proceed = False
        return
    elif proceed:
        print("is not equal")
        print(array)
        print()
        if brake > depth:
            print("Branch exhausted")
            print()
            return

        if  origin != 'L' and currentY + 1 <= 3:#ADD SPECIFIC VALUE READ FROM FILE!!!
            swapper(currentX, currentY, currentX, currentY + 1)
            dfs(array, 'R', brake + 1)
            swapper(currentX, currentY, currentX, currentY - 1)

        if origin != 'R' and currentY - 1 >= 0 :
            swapper(currentX, currentY, currentX, currentY - 1)
            dfs(array, 'L', brake + 1)
            swapper(currentX, currentY, currentX, currentY + 1)

        if origin != 'U' and currentX + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
            swapper(currentX, currentY, currentX + 1, currentY)
            dfs(array, 'D', brake + 1)
            swapper(currentX, currentY, currentX - 1, currentY)

        if origin != 'D' and currentX - 1 >= 0:
            swapper(currentX, currentY, currentX - 1, currentY)
            dfs(array, 'U', brake + 1)
            swapper(currentX, currentY, currentX + 1, currentY)


# main function
if __name__ == '__main__':
    print("Final board:")
    print(final_board)

    print("\nCurrent board:")
    print(problem_board)

    print("\nCurrent position of blank space(X/Y):")
    print(currentX)
    print(currentY)

    # Count runtime of an algorythm
    start_time = time.time()

    print("\nAlgorythm start:")
    dfs(problem_board, 'N', 0)

    print("--- It took: %s seconds ---" % (time.time() - start_time))
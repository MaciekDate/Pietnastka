import numpy as np

print("Wiadomosc testowa 24")

final_board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
depth = 20
currentX = 3
currentY = 2

varX = 0
varY = 0

problem_board = np.loadtxt("puzzle.txt", skiprows=1, dtype=int)



path = ""

def swapper(x1, y1, x2, y2): #Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
    temporary = problem_board[x1, y1]
    problem_board[x1, y1] = problem_board[x2, y2]
    problem_board[x2, y2] = temporary
    global currentX
    global currentY
    currentX = x2
    currentY = y2

def dfs(array, origin, brake):
    global currentX
    global currentY
    global varX
    global varY
    if np.array_equal(array, final_board):
        print("is equal")
        print(array)
        pass
    else:
        print("is not equal")
        print(array)
        print()
    if brake > 5:
        print("Branch exhausted")
        print()
    if  brake <= 5 and origin != 'L' and currentY + 1 <= 3:#ADD SPECIFIC VALUE READ FROM FILE!!!
        swapper(currentX, currentY, currentX, currentY + 1)
        dfs(array, 'R', brake + 1)
        swapper(currentX, currentY, currentX, currentY - 1)
    if brake <= 5 and origin != 'R' and currentY - 1 >= 0 :
        swapper(currentX, currentY, currentX, currentY - 1)
        dfs(array, 'L', brake + 1)
        swapper(currentX, currentY, currentX, currentY + 1)
    if brake <= 5 and origin != 'U' and currentX + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
        swapper(currentX, currentY, currentX + 1, currentY)
        dfs(array, 'D', brake + 1)
        swapper(currentX, currentY, currentX - 1, currentY)
    if brake <= 5 and origin != 'D' and currentX - 1 >= 0:
        swapper(currentX, currentY, currentX - 1, currentY)
        dfs(array, 'U', brake + 1)
        swapper(currentX, currentY, currentX + 1, currentY)


print()
print(problem_board)
print("!!!!START!!!!")
print()

dfs(problem_board, 'N', 0)
print(problem_board)
import numpy as np

print("Wiadomosc testowa 24")

final_board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
depth = 20
currentX = 3
currentY = 3
#print("Ukonczona ukladanka:")
#print(final_board)

problem_board = np.loadtxt("puzzle.txt", skiprows=1, dtype=int)
#print("Wczytana ukladanka:")
#print(problem_board)


def swapper(x1, y1, x2, y2):
    temporary = problem_board[x1, y1]
    problem_board[x1, y1] = problem_board[x2, y2]
    problem_board[x2, y2] = temporary
    global currentX
    global currentY
    currentX = x2
    currentY = y2

if (np.array_equal(problem_board, final_board)):
    print("is equal")
else:
    print("is not equal")

print()
print(problem_board)
print(currentY)
print()

swapper(currentX, currentY, currentX - 1, currentY)
if (np.array_equal(problem_board, final_board)):
    print("is equal")
else:
    print("is not equal")
print(problem_board)
print(currentY)
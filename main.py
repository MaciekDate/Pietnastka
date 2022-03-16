import numpy as np

print("Wiadomosc testowa 24")

final_board = np.array([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']])
depth = 20

print("Ukonczona ukladanka:")
print(final_board)

problem_board = np.loadtxt("puzzle.txt", skiprows=1, dtype=int)
print("Wczytana ukladanka:")
print(problem_board)

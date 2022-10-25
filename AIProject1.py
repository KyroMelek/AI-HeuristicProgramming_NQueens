# Constrained N-queens problem
# Kyrolos Melek
import pandas as pd
import csv

# Read in constrained n queens board from CSV (n =10, 1st queen at (0,0) for the example)
df = pd.read_csv("input.csv", header=None)
initialBoard = df.values.tolist()  # make it a list
resultBoard = initialBoard

N = len(initialBoard)


# check if a queen at [row][col] is attacked. We need to check only left for queen's safety.
def isSafe(board, row, col, N):
    # Check this row on left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper diagonal on left
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on left
    for i, j in zip(range(row+1, N, 1), range(col-1, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


# Returns (row, column) of first queen
def findLocationOfFirstQueen(board):
    rowLocation = 0
    for row in board:
        columnLocation = 0
        for column in row:
            if (column):
                return (rowLocation, columnLocation)
            else:
                columnLocation += 1
        rowLocation += 1


firstQueen = findLocationOfFirstQueen(initialBoard)


# Array of size n to keep track of attempts for each column
# If all columns, except initial condition queen, have reached n -1 attempts we have exhuasted all possible solutions
BoardColumnAttempts = []
for i in range(N):
    if (i == firstQueen[1]):
        BoardColumnAttempts.append(N)
    else:
        BoardColumnAttempts.append(0)


# Function to check for no solution
def haveExhaustedAllAttempts():
    for colAttempt in BoardColumnAttempts:
        if (colAttempt < N):
            return False
    return True


NoSolution = False


# Main recursive backtracking algorithim
def recursiveBacktracking(n, currentColumn, workingBoard):
    global NoSolution
    global BoardColumnAttempts
    if (haveExhaustedAllAttempts()):
        print("No solution for given inititial Condition")
        NoSolution = True
        return
    # Base Condition: if we have placed queens in all columns
    if (currentColumn == n):
        global resultBoard
        resultBoard = workingBoard
        return
    # If we have arrived at the initial condition queen, move onto the next column
    elif (currentColumn == firstQueen[1]):
        currentColumn += 1
        recursiveBacktracking(n, currentColumn, workingBoard)
        return
    # If we are at a column before that of the initial condition queen's col, we must also ensure that the initial condition queen is still safe
    # after placing a queen. Otherwise try another row for the current col
    elif (currentColumn < firstQueen[1]):
        successfullRowPlacement = False
        currentRow = 0

        rowCounter = 0
        lastAttemptedRow = -1
        # If there is already queen in this column, this means we have back tracked
        # Remove queen and continue onto the next row so we do not make the same mistake
        for row in workingBoard:
            if (row[currentColumn] == 1):
                row[currentColumn] = 0
                lastAttemptedRow = rowCounter
            rowCounter += 1

        for row in workingBoard:
            if (currentRow > lastAttemptedRow or lastAttemptedRow == -1):
                row[currentColumn] = 1
                BoardColumnAttempts[currentColumn] += 1
                if (isSafe(workingBoard, firstQueen[0], firstQueen[1], N) and isSafe(workingBoard, currentRow, currentColumn, N)):
                    currentColumn += 1
                    successfullRowPlacement = True
                    recursiveBacktracking(N, currentColumn, workingBoard)
                    return
                else:
                    row[currentColumn] = 0
            currentRow += 1
        # If we were not able to place a queen in the current column, backtrack one column
        if (not successfullRowPlacement):
            currentColumn -= 1
            if (currentColumn == firstQueen[1]):
                currentColumn -= 1
            recursiveBacktracking(N, currentColumn, workingBoard)
            return
    # if we are past the IC first queen, need only check safety of the current column placements
    elif (currentColumn > firstQueen[1]):
        successfullRowPlacement = False
        currentRow = 0

        rowCounter = 0
        lastAttemptedRow = -1
        # If there is already queen in this column, this means we have back tracked
        # Remove queen and continue onto the next row so we do not make the same mistake
        for row in workingBoard:
            if (row[currentColumn] == 1):
                row[currentColumn] = 0
                lastAttemptedRow = rowCounter
            rowCounter += 1

        for row in workingBoard:
            if (currentRow > lastAttemptedRow or lastAttemptedRow == -1):
                row[currentColumn] = 1
                BoardColumnAttempts[currentColumn] += 1
                if (isSafe(workingBoard, currentRow, currentColumn, N)):
                    currentColumn += 1
                    successfullRowPlacement = True
                    recursiveBacktracking(N, currentColumn, workingBoard)
                    return
                else:
                    row[currentColumn] = 0
            currentRow += 1
        # If we were not able to place a queen in the current column, backtrack one column
        if (not successfullRowPlacement):
            currentColumn -= 1
            if (currentColumn == firstQueen[1]):
                currentColumn -= 1
            recursiveBacktracking(N, currentColumn, workingBoard)
            return


recursiveBacktracking(N, 0, initialBoard)

if (not NoSolution):
    with open("solution.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(resultBoard)

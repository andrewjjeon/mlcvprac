from typing import List
from collections import deque

WIRE_CHARACTERS = {'|', '-'}
INPUT_CHARACTERS = ('A', 'B')
GATE_CHARACTER = 'G'
OUTPUT_CHARACTER = 'X'

def get_board(opname: str) -> str:
    # Read board from file

    with open(f"./circuits/{opname}.txt") as f:
        return f.read()

def gridify_board(board: str) -> List[List[str]]:
    # Return 2D char array representation of board

    return list(list(line) for line in board.split('\n'))

def evaluate_function(board: str, *inputs: bool) -> bool:
    # Given a board string, evaluate the boolean function with the
    # given inputs
    grid = gridify_board(board)
    h = len(grid)
    ws = []
    for row in grid:
        ws.append(len(row))
    w = max(ws) # rows are different so we need to make them all same length as max one
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for row in grid:
        row += [' '] * (w - len(row)) # make every row same length by adding spaces at end
    
    queue = deque()
    signal = {}

    for r in range(h):
        for c in range(w):
            if grid[r][c] == 'A':
                queue.append((r, c))
                signal[(r, c)] = inputs[0] # set 1st input A
            elif grid[r][c] == 'B':
                queue.append((r, c))
                signal[(r, c)] = inputs[1] # set 2nd input B
    
    while queue:
        (curr_r, curr_c) = queue.popleft()
        curr_signal = signal[(curr_r, curr_c)]

        for (dr, dc) in directions:
            nr, nc = curr_r + dr, curr_c + dc

            if (0 <= nr < h) and (0 <= nc < w):
                if (nr, nc) not in signal:
                    if (grid[nr][nc] == '-') or (grid[nr][nc] == '|'): # if its a wire
                        queue.append((nr, nc))
                        signal[(nr, nc)] = curr_signal

                    elif grid[nr][nc] == 'G':
                        above = (nr - 1, nc)
                        below = (nr + 1, nc)
                        output = (nr, nc + 1)
                        if above in signal and below in signal:
                            queue.append(output)
                            signal[(output)] = not(signal[(above)] and signal[(below)])

                    elif grid[nr][nc] == 'X':
                        signal[(nr, nc)] = curr_signal
                        return curr_signal


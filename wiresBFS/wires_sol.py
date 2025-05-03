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
    h, w = len(grid), max(len(row) for row in grid)
    for row in grid:
        row += [' '] * (w - len(row)) # add spaces to the end to make every row the same length

    signal = {} # signal mapping dict for every cell, also acts as visited set

    queue = deque() # queue to search every cell in order
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for r in range(h):
        for c in range(w):
            ch = grid[r][c]
            if ch == 'A':
                signal[(r, c)] = inputs[0] # put 1st input signal into A
                queue.append((r, c))
            elif ch == 'B':
                signal[(r, c)] = inputs[1] # put 2nd input signal into B
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        val = signal[(r, c)]
        ch = grid[r][c]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w) or (nr, nc) in signal: # if not valid cell, or visited already pass
                continue

            next_ch = grid[nr][nc]
            if next_ch in ['-', '|']: # if its a wire, signal doesn't change, since just a wire from input
                signal[(nr, nc)] = val
                queue.append((nr, nc))

            elif next_ch == 'G': # if gate, do the NAND operation
                top = (nr - 1, nc)
                bot = (nr + 1, nc)
                out = (nr, nc + 1)
                if top in signal and bot in signal and out not in signal:
                    nand_out = not (signal[top] and signal[bot])
                    signal[out] = nand_out
                    queue.append(out) # G doesn't have a signal, only cell after it

            elif next_ch == 'X':
                signal[(nr, nc)] = val
                return val
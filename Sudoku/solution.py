# Udacity Artificial Intelligence NanoDegree - January 2017 cohort
# solution.py
# Kirkland Poole
#
# Reference: Udacity.com Artifical Intelligence NanoDegree student on-line materials
# https://www.udacity.com/
#

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.

column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# square_units[1] = ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']
# This is the top left square.


diagonal_units = [ [a[0]+a[1] for a in zip(rows, cols)] ,
                                  [a[0]+a[1] for a in zip(rows, cols[::-1])] ]
# Reference: Udacity code review dated 2/1/2017
# Element example:
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# diagonal_units[1] = ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
# These are the boxes along the diagonals.

unitlist = row_units + column_units + square_units

unitlist_with_diaganoals = diagonal_units + row_units +\
                           column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """
    Go through all the boxes, and whenever there is a naked_twin,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in
    dictionary form with naked_twin values eliminated.
    """
    for c in cols:
        naked_twins_candidate = []
        naked_twins_candidate_row = []
        for r in rows:
            if len(values[r + c]) == 2:
                naked_twins_candidate_row.append(r)
                if (values[r + c] in naked_twins_candidate):
                    # Remove naked_twin values from rows
                    for rowLCV in rows:
                        # Don't remove naked_twin value
                        # from row with naked_twin
                        if not (rowLCV in naked_twins_candidate_row):
                            for digit in naked_twins_candidate:
                                values[rowLCV + c] =\
                                    values[rowLCV + c].replace(digit, '')
                else:
                    naked_twins_candidate = values[r + c]
    return values


def grid_values(grid):
    """Convert grid string into {<box>: <value>}
    dict with '123456789' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8',
        or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) +
                      ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever
    there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if
                     len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever
    there is a unit with a value that
    only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist_with_diaganoals:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice().
    If at some point, there is a box with
    no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions,
    the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys()
                     if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys()
                                    if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys()
                                   if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False
        # if there is a box with zero available values:
        if len([box for box in values.keys()
                if len(values[box]) == 0]):
            return False
    return values


def solve(grid):
    "Start the process to solve the sudoku puzzle"
    "given the unsolved puzzle in string or dictionary format."
    # Check if the grid is in string or dictionary format.
    if type(grid) == dict:
        grid = search(grid)
    else:
        grid = search(grid_values(grid))
    return grid


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

boxes = cross(rows, cols)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(grid_values(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

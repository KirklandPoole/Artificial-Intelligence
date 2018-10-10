import utils

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '.'.
    """
    chars = []
    for c in grid:
        chars.append(c)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
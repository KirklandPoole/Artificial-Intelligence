# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We use constraint propagation to solve the naked twins Sudoku problem by reducing the set of allowable numbers which can be used to solve the Sudoku puzzle for those regions where two or more squares could only take on the two values. By using these local constraints, the search space for possible solutions was reduced resulting in getting closer to a solution for the Sudoku puzzle.
										
To find and handled the naked_twins problem, a custom function was implemented. The custom function (naked_twins) would find the naked_twins and then remove the two values from its peers for the local constraint.

Furthermore, we used two functions (eliminate and only_choice) against the Sudoku puzzle until the puzzle was solved. The eliminate functions looked for a single value in a box and if one was found, it removed the value from all peers for the box. The only_choice function looked for the unique value which could only be assigned to a box in its unit, then removed the value from all the boxes in the unit.



# Question 2 (Diagonal Sudoku)
A: We use constraint propagation to solve the diagonal Sudoku problem by reducing the set of allowable numbers which can be used to solve the Sudoku puzzle along the diagonal. In addition to handling the standard case for rows, columns and 3x3 squares.

By extending the unit list (unit_llist) to include boxes alone the diagonals, we could apply constraint propagation against the new set of boxes in the unit list. And, by defining the unit list with the boxes along the diagonal first, the local constraints would be applied to the diagonals then to the other units.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
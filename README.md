# Backtrack_Robot
Implementation of the Backtrack algorithm; Exercise in Refactoring

### The scenario

A robot is in the top-left corner of a grid, and wants to travel to a given destination (r, c).
She can only move DOWN and to the RIGHT. Determine her path from (0,0) to (r,c).

### The hitch

There're obstacles!

To implement this, I let the user enter how many obstacles, and randomly disperse that many throughout the game board (the grid).

### Using the program

1. Run the interpreter

```bash
python3 backtrack.py
```

2. Give the robot its destination coordinates, and decide how many obstacles you want to place

[Imgur](http://i.imgur.com/SVmF7zs.png)

3. Press enter to see the board, and wait for the robot to find a path

<img src=http://imgur.com/jpsqRNp>

4. Check out your robot's path

<img src=http://imgur.com/uzFHErd>


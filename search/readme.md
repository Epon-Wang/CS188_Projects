# Project 1 - Search

This project is based on pacman, you can view the options of this platform by

```bash
python pacman.py -h
```
View the performance of each implemented algorithms by running the following examples
- **Depth First Search (DFS)**

    ```bash
    python pacman.py -l tinyMaze -p SearchAgent
    python pacman.py -l mediumMaze -p SearchAgent
    python pacman.py -l bigMaze -z .5 -p SearchAgent
    ```
- **Breadth First Search (BFS)**

    ```bash
    python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
    python eightpuzzle.py
    ```
- **Uniform-Cost Graph Search (UCS)**

    ```bash
    python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
    python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
    ```
- **A\* Search**

    ```bash
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    ```

View the implemented problem class & heuristic functions by running the following
- **Finding All the Corners**

    Find the shortest path through the maze that touches all four corners

    ```bash
    python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    ```
- **Heuristic Function for Corner-Finding Problem**

    ```bash
    python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
    ```
- **Eating All the Dots**

    Eating all the Pacman food in as few steps as possible

    ```bash
    python pacman.py -l trickySearch -p AStarFoodSearchAgent
    ```
- **Suboptimal Search**

    An agent that always greedily eats the closest dot

    ```bash
    python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
    ```
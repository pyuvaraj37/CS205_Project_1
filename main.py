from queue import PriorityQueue

class Node:
    def __init__(self, h, g, puzzle):
        self.h = h;
        self.g = g;
        self.puzzle = puzzle;
        self.parent = [];
        self.children = [];
        super().__init__();
         
    def setParent(self, parent):
        self.parent = parent; 

    def addChild(self, child):
        self.children.append(child); 

test_puzzle = [[1, 2, 0],
                [4, 5, 3]
                ,[7, 8, 6]];

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]];

actions = ['move_up', 'move_down', 'move_left', 'move_right'];

def transformPuzzle(puzzle, action):
    for i in puzzle:
        for j in puzzle[i]:
            if puzzle[i][j] == 0:
                zero = (i, j);
    if action == actions[0]:
        #Moving the missing tile up (zero tile)
        #Checking if it is a valid move, if not return false. 
        if zero[0] != 0:
            temp = puzzle[zero[0] - 1][zero[1]];
            puzzle[zero[0] - 1][zero[1]] = puzzle[zero[0]][zero[1]];
            puzzle[zero[0]][zero[1]] = temp; 
            return puzzle; 
        else:
            return False; 

    elif action == actions[1]:
        #Moving the missing tile down (zero tile)
        #Checking if it is a valid move, if not return false. 
        if zero[0] != len(puzzle) - 1:
            temp = puzzle[zero[0] + 1][zero[1]];
            puzzle[zero[0] + 1][zero[1]] = puzzle[zero[0]][zero[1]];
            puzzle[zero[0]][zero[1]] = temp; 
            return puzzle; 
        else:
            return False; 

    elif action == actions[2]:
        #Moving the missing tile left (zero tile)
        #Checking if it is a valid move, if not return false. 
        if zero[1] != 0:
            temp = puzzle[zero[0]][zero[1] - 1];
            puzzle[zero[0]][zero[1] - 1] = puzzle[zero[0]][zero[1]];
            puzzle[zero[0]][zero[1]] = temp; 
            return puzzle; 
        else:
            return False; 
    elif action == actions[3]:
        #Moving the missing tile left (zero tile)
        #Checking if it is a valid move, if not return false. 
        if zero[1] != len(puzzle[0]) - 1:
            temp = puzzle[zero[0]][zero[1] + 1];
            puzzle[zero[0]][zero[1] + 1] = puzzle[zero[0]][zero[1]];
            puzzle[zero[0]][zero[1]] = temp; 
            return puzzle; 
        else:
            return False; 

def checkGoalState(puzzle):
    if (goal_state == puzzle):
        return True;
    else:
        return False;

def Uniform_Cost_Search(puzzle): 
    print("Using UCS to solve the 8-Puzzle");
    node = Node(0, 1, puzzle);
    frontier = PriorityQueue(); 
    frontier.put(node.g, node);
    explored = []; 

    while (1):
        if (frontier.qsize == 0):
            return False; 
        node = frontier.get(); 
        explored.append[node];
        if (checkGoalState(node.puzzle)):
            return True;
        for action in actions:
            puzzle = transformPuzzle(node.puzzle, action)
            if (puzzle):
                childNode = Node(0, 1, puzzle);
                childNode.setParent(node);
                node.addChild(childNode);
                if (not checkFrontier(childNode, frontier) or not checkExplored(childNode, explored)):
                    frontier.put(childNode.g, childNode);



print("8-Puzzle");
testing = input("Are you going to be using a test puzzle? (1 for Yes, 0 for No): ");
if (int(testing) == 1): 
    print("Used for debugging");
    method = input("Which method to solve the 8-Puzzle will you use? (1 for UCS, 2 for A* MT, 3 for A* MD): ");
    if (int(method) == 1): Uniform_Cost_Search(test_puzzle);
else: 
    print("Input custom 8-PUzzle");

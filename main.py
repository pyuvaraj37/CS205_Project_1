from queue import PriorityQueue

class Node:
    def __init__(self, h, g, puzzle):
        self.h = h;
        self.g = g;
        self.puzzle = [x[:] for x in puzzle];
        self.parent = [];
        self.children = [];
        super().__init__();
         
    def setParent(self, parent):
        self.parent = parent; 

    def addChild(self, child):
        self.children.append(child); 
    
    def __eq__(self, other):
        return other;

    def __lt__(self, other):
        return other;

i_puzzle = [[8, 1, 2],
                [0, 4, 3]
                ,[7, 6, 5]];

easy_puzzle = [[1, 2, 3],
                [4, 5, 0]
                ,[7, 8, 6]];

simple_puzzle = [[0, 1, 2],
                [4, 5, 3]
                ,[7, 8, 6]];\

tough_puzzle = [[8, 7, 1],
                [6, 0, 2]
                ,[5, 4, 3]];

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]];

actions = ['move_up', 'move_down', 'move_left', 'move_right'];




def transformPuzzle(puzzle_org, action):
    puzzle = puzzle_org; 
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
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
    if (checkPuzzleEqual(puzzle, goal_state)):
        return True;
    else:
        return False;

def checkPuzzleEqual(a, b):
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != b[i][j]:
                return False;
    return True;

def checkFrontier(childNode, frontier):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            return True;  
    return False; 

def getFrontier(childNode, frontier):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            return node[1];  
    return False; 

def swapFrontierNode(childNode, frontier, newNode):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            node = (newNode.g + newNode.h ,newNode);  


def checkExplored(childNode, explored):
    for node in explored:
        if checkPuzzleEqual(node.puzzle, childNode.puzzle):
            return True;  
    return False; 

def getExplored(childNode, explored):
    for node in explored:
        if checkPuzzleEqual(node.puzzle, childNode.puzzle):
            return node;  
    return False;    

def Uniform_Cost_Search(puzzle, search): 
    
    if (search == 'UCS'):
        print("Using UCS to solve the 8-Puzzle");
        h = 0;
    elif(search == 'AMT'):
        print("Using AMT to solve the 8-Puzzle");
        h = missingTime(puzzle);
    elif(search == 'AMD'):
        print("Using AMD to solve the 8-Puzzle");
        h = manhattanDistance(puzzle);

    frontier = PriorityQueue(); 
    node = Node(h, 0, puzzle);
    frontier.put((0, node));
    explored = []; 
    
    while (frontier.qsize != 0):
    
        node_prioty, node = frontier.get(); 
        explored.append(node);
        
        if (checkGoalState(node.puzzle)):
            print("Solution found!");
            return True, node;
        else:
            for action in actions:
                print(action);
                
                print("Before transform: ");
                printPuzzle(node.puzzle);
                
                transformed_puzzle = transformPuzzle([x[:] for x in node.puzzle], action);

                if transformed_puzzle:
                    print("After transform: ");
                    printPuzzle(transformed_puzzle);
                else:
                    print("ILLEGAL MOVE");

                if (transformed_puzzle):

                    if (search == 'UCS'):
                        h = 0;
                    elif(search == 'AMT'):
                        h = missingTime(transformed_puzzle);
                    elif(search == 'AMD'):
                        h = manhattanDistance(transformed_puzzle);

                    childNode = Node(h, node.g + 1, transformed_puzzle);
                    if (not checkFrontier(childNode, frontier) or not checkExplored(childNode, explored)):
                        print("Node not explored or frontier");
                        frontier.put((childNode.g + childNode.h, childNode));
                    elif (checkFrontier(childNode, frontier) and getFrontier(childNode, frontier).g > childNode.g):
                        print("Frontier queue is not empty.")
                        swapFrontierNode(getFrontier(childNode, frontier), frontier, childNode);
    print("No Solution!");

def printPuzzle(puzzle):
    print(str(puzzle[0][0]) + " " + str(puzzle[0][1]) + " " + str(puzzle[0][2]));
    print(str(puzzle[1][0])+ " " + str(puzzle[1][1]) + " " + str(puzzle[1][2]));
    print(str(puzzle[2][0]) + " " + str(puzzle[2][1]) + " " + str(puzzle[2][2]));


print("8-Puzzle");
testing = input("Are you going to be using a test puzzle? (1 for Yes, 0 for No): ");
if (int(testing) == 1): 
    print("Used for debugging");
    method = input("Which method to solve the 8-Puzzle will you use? (1 for UCS, 2 for A* MT, 3 for A* MD): ");

    #printPuzzle(s_puzzle);

    if (int(method) == 1): 
        success, node = Uniform_Cost_Search(tough_puzzle);
    
    if success:
        print("Cost: " + str(node.g));
    else:
        print("Unsolvable!");

else: 
    print("Input custom 8-PUzzle");

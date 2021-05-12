from queue import PriorityQueue

####################################################
# Class to create tree structure
# Holding cost and heuristic information
# Puzzle in this case is the STATE
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
    
    # def __eq__(self, other):
    #     return other;

    def __lt__(self, other):
        if (self.g + self.h < other.g + other.h):
            return self; 
        return other;

####################################################
#Default Puzzles for debugging

impossible_puzzle = [[8, 1, 2],
                [0, 4, 3]
                ,[7, 6, 5]];

#Depth 1
one_puzzle = [[1, 2, 3],
                [4, 5, 0]
                ,[7, 8, 6]];

#Depth 2 
two_puzzle = [[1, 2, 3], 
                [4, 0, 6], 
                [7, 5, 8]];

#Depth 4 
four_puzzle = [[0, 1, 2],
                [4, 5, 3]
                ,[7, 8, 6]];

#Depth 8 
eight_puzzle = [[1, 3, 6],
                [5, 0, 2]
                ,[4, 7, 8]];

#Depth 16
sixteen_puzzle = [[1, 6, 7],
                [5, 0, 3]
                ,[4, 8, 2]];

#Depth 22
twentytwo_puzzle = [[8, 7, 1],
                [6, 0, 2]
                ,[5, 4, 3]];

####################################################

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]];

####################################################
#The operators for the puzzle
#Moving the missing space up, down, left or right. 
actions = ['move_up', 'move_down', 'move_left', 'move_right'];

####################################################
#Heuristic functions h(n) for Miss Placed Tile Heuristic and Manhattan Distance respectively. 

#Compares with the goal state to return h
#Goes through each of the elements and compares it will the goal state,
#any miss placed elements iterator a counter. 
def missPlacedTile(puzzle):
    missPlacedTile = 0; 
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != goal_state[i][j]:
                missPlacedTile+=1; 
    return missPlacedTile; 

#Compares with the goal state to return h
#If a element is not in the correct location, it divides the element by the * collumns for the row index, 
#then uses modulus to find the collumn index. Then taking the absolute different of the current row index and correct row index,
#and same for collumn indexes gives the Manhattan Distance
def manhattanDistance(puzzle):
    missPlacedTile = 0; 
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != goal_state[i][j]:
                wrongTile = puzzle[i][j];
                if wrongTile != 0:
                    row = wrongTile / len(puzzle);
                    mod = wrongTile % len(puzzle[i]);
                    if mod == 0:
                        col = len(puzzle[i]);
                    else: 
                        col = mod - 1; 
                
                    missPlacedTile += abs(i - row) + abs(j - col);
    return missPlacedTile; 

####################################################
#Helper Functions

#Transforms the puzzle, takes in an action which is one of the operators.
#Checking for valid moves
def transformPuzzle(puzzle, action): 
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

#Checks the puzzle against the goal state
def checkGoalState(puzzle):
    if (checkPuzzleEqual(puzzle, goal_state)):
        return True;
    else:
        return False;

#Checks the equavalency of two puzzles
def checkPuzzleEqual(a, b):
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != b[i][j]:
                return False;
    return True;

#To check if a state is already in the priority queue
def checkFrontier(childNode, frontier):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            return True;  
    return False; 

#Used after checkFrontier() to get the node that has a certain state
def getFrontier(childNode, frontier):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            return node[1];  
    return False; 

#Switch equavalent nodes, ideally the new node will have a lower h(n)
def swapFrontierNode(childNode, frontier, newNode):
    for node in frontier.queue:
        if checkPuzzleEqual(node[1].puzzle, childNode.puzzle):
            node = (newNode.g + newNode.h ,newNode);  

#Checking if a state has been explored
def checkExplored(childNode, explored):
    for node in explored:
        if checkPuzzleEqual(node.puzzle, childNode.puzzle):
            return True;  
    return False; 

#Used after checkExplored() to get the node that was explored already
def getExplored(childNode, explored):
    for node in explored:
        if checkPuzzleEqual(node.puzzle, childNode.puzzle):
            return node;  
    return False;    

#Print the entire puzzle
def printPuzzle(puzzle):
    print(str(puzzle[0][0]) + " " + str(puzzle[0][1]) + " " + str(puzzle[0][2]));
    print(str(puzzle[1][0])+ " " + str(puzzle[1][1]) + " " + str(puzzle[1][2]));
    print(str(puzzle[2][0]) + " " + str(puzzle[2][1]) + " " + str(puzzle[2][2]));

####################################################
#Main Algorithm

#Takes in the scrambled puzzle, and the type of search.
#UCS for Uniform Cost Search (h = 0)
#AMT for A* with Miss Placed Tile Heuristic
#AMD for A* with Manhattan Distance Heurstic
def Search(puzzle, search): 
    
    #Intializes the value of h by using the specified h(n)
    if (search == 'UCS'):
        print("Using UCS to solve the 8-Puzzle");
        h = 0;
    elif(search == 'AMT'):
        print("Using AMT to solve the 8-Puzzle");
        h = missPlacedTile(puzzle);  
    elif(search == 'AMD'):
        print("Using AMD to solve the 8-Puzzle");
        h = manhattanDistance(puzzle);

    #Intialize the frontier (priority queue) with the root node (intial puzzle state)
    #Intialize the explored list, and expansion counter
    frontier = PriorityQueue(); 
    node = Node(h, 0, puzzle);
    frontier.put((0, node));
    explored = []; 
    nodesExpanded = 0; 
    
    #Continue the search while new nodes are still available for expansion
    while (frontier.qsize != 0):
        
        #Pull the highest priority node
        node_prioty, node = frontier.get(); 
        explored.append(node);
        
        #Check the goal state
        if (checkGoalState(node.puzzle)):
            print("Solution found!");
            return True, node, nodesExpanded;
        else:
            #Expand all the possible operators
            for action in actions:
                # print(action);
                # print("Before transform: ");
                # printPuzzle(node.puzzle);
                
                #Transform the puzzle using the specific operator
                transformed_puzzle = transformPuzzle([x[:] for x in node.puzzle], action);

                # if transformed_puzzle:
                #     print("After transform: ");
                #     printPuzzle(transformed_puzzle);
                # else:
                #     print("ILLEGAL MOVE");

                #If the transformation was valid
                if (transformed_puzzle):
                    
                    #Calculate the heuristic for the specific method
                    if (search == 'UCS'):
                        h = 0;
                    elif(search == 'AMT'):
                        h = missPlacedTile(transformed_puzzle);
                    elif(search == 'AMD'):
                        h = manhattanDistance(transformed_puzzle);

                    #Create the child node
                    childNode = Node(h, node.g + 1, transformed_puzzle);
                    
                    #Check if the node is in the frontier, or have been explored before
                    if (not checkFrontier(childNode, frontier) or not checkExplored(childNode, explored)):
                        #print("Node not explored or in frontier..."); 
                        frontier.put((childNode.g + childNode.h, childNode));
                        nodesExpanded+=1;
                    #If a node with a similar state is in the frontier with a lower cost/heuristic
                    elif (checkFrontier(childNode, frontier) and getFrontier(childNode, frontier).g > childNode.g):
                        #print("State found in frontier for cheaper...")
                        swapFrontierNode(getFrontier(childNode, frontier), frontier, childNode);
                    #else: 
                        #print("Drop node!");
    print("No Solution!");
####################################################


#Driver
print("8-Puzzle");
testing = input("Are you going to be using a test puzzle? (1 for Yes, 0 for No): ");
puzzle = [];
if int(testing) == 1: 
    print("Used for debugging");
    depth = input("Choose the depth of the test puzzles: (1, 2, 4, 8, 16, 22): ");
    if int(depth) == 1:
        puzzle = one_puzzle; 
    elif int(depth) == 2:
        puzzle = two_puzzle; 
    elif int(depth) == 4:    
        puzzle = four_puzzle;
    elif int(depth) == 8:
        puzzle = eight_puzzle;
    elif int(depth) == 16:
        puzzle = sixteen_puzzle;
    elif int(depth) == 22:
        puzzle = twentytwo_puzzle; 
else: 
    print("Input custom 8-PUzzle");
    print("Enter each elements for a row, row by row with a space between the numbers. 0 for missing tile.");
    rowone = input("Input the first row: ");
    rowtwo = input("Input the first row: ");
    rowthree = input("Input the first row: ")
    puzzle = [[int(rowone[0]), int(rowone[2]), int(rowone[4])], [int(rowtwo[0]), int(rowtwo[2]), int(rowtwo[4])], [int(rowthree[0]), int(rowthree[2]), int(rowthree[4])]]
    

printPuzzle(puzzle);
method = input("Which method to solve the 8-Puzzle will you use? (1 for UCS, 2 for A* MT, 3 for A* MD): ");
if (int(method) == 1): 
    success, node, nodesExpanded = Search(puzzle, 'UCS');
elif (int(method) == 2):
    success, node, nodesExpanded = Search(puzzle, 'AMT');
elif (int(method) == 3):
    success, node, nodesExpanded = Search(puzzle, 'AMD');


if success:
    print("Moves needed/Depth: " + str(node.g));
    print("Nodes Expanded: " + str(nodesExpanded));
    
else:
    print("Unsolvable!");
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print(successorGameState)
        #print(newFood.asList())
        #print(newGhostStates)
        sum = []
        adding = 0
        for i in newFood.asList():
            xy1 = i
            xy2 = newPos
            total = abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
            if total < 4:
                adding += 1
            elif total < 12:
                adding += 0.25
        #power pellets are o's on the grid
        ghost = 0
        ghost_counter = 0
        for i in newGhostStates:
            xy1 = i.getPosition()
            xy2 = newPos
            total = abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
            if total < 4:
                ghost -= 50
            if newScaredTimes[ghost_counter] > total:
                ghost += 200
            ghost_counter += 1

        

        # for i in newGhostStates:
        #     xy1 = i.getPosition()
        #     xy2 = newPos
        #     total = abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
        #     if total - newScaredTimes:
        #         ghost -= 100

        return adding + successorGameState.getScore() + ghost

        # manhattanDistance from pacman and ghosts 

        # if new Ghost state is scared:
        #     check if distance is 1/2 to get to ghost
        #     if so add 500 to score
        
        # check distances from foods 
        #     manhattanDistance from pacman and food
        #     choose the minimum of the bunch . also thinking of average 
        
        # return sum of manhattanDistance1 + extra + manhattanDistance2
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        depthCounter = 1
        numGhosts =  gameState.getNumAgents() - 1
        depth = self.depth
        evalFunction = self.evaluationFunction
        def pacmanMax(gameState2: GameState,deep: int):
            possibleActions = gameState2.getLegalActions(0)
            maxValue = 0
            actionTaken = ""
            counter = 0
            #print(possibleActions)
            for action in possibleActions:
                if not counter:
                    maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep)
                    actionTaken = action
                else:
                    if maxValue[0] < ghostMin(gameState2.generateSuccessor(0,action),1,deep)[0]:
                        maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep)
                        actionTaken = action
                counter = counter + 1
            #print(maxValue)
        #     keeps track of which agents is time to moves
        #     returns max of two other functions - two different paths they can take
            if not counter:
                return (evalFunction(gameState2),actionTaken)
            return (maxValue[0],actionTaken)


        def ghostMin(gameState3: GameState, ghost: int,deep: int):
        #     keeps track of which agents is time to moves
        #     returns min of two other functions - two different paths they can take
            possibleActions = gameState3.getLegalActions(ghost)
            #stateList = []
            minValue = 0
            actionTaken = ""
            counter = 0
            # print(gameState.isLose())
            # print(gameState.isWin())
            for action in possibleActions:
                if numGhosts == ghost:
                    if depth == deep:
                        if not counter:
                            minValue = (evalFunction(gameState3.generateSuccessor(ghost,action)),action)
                            actionTaken = action
                        else:
                            if minValue[0] > evalFunction(gameState3.generateSuccessor(ghost,action)):
                                minValue = (evalFunction(gameState3.generateSuccessor(ghost,action)),action)
                                actionTaken = action
                    else:
                        if not counter:
                            minValue = pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1)
                            actionTaken = action
                        else:
                            if minValue[0] > pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1)[0]:
                                minValue = pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1)
                                actionTaken = action
                else:
                    if not counter:
                        minValue = ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep)
                        actionTaken = action
                    else:
                        if minValue[0] > ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep)[0]:
                            minValue = ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep)
                            actionTaken = action
                counter+=1
            #print((minValue,actionTaken),minValue)
            if not counter:
                return (evalFunction(gameState3),actionTaken)
            return (minValue[0],actionTaken)
        
        return pacmanMax(gameState,1)[1]

        #need to now return a list of the actions that lead to this best outcome


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        depthCounter = 1
        numGhosts =  gameState.getNumAgents() - 1
        depth = self.depth
        evalFunction = self.evaluationFunction
        def pacmanMax(gameState2: GameState,deep: int,alpha: float,beta: float):
            possibleActions = gameState2.getLegalActions(0)
            maxValue = 0
            actionTaken = ""
            counter = 0
            #print(possibleActions)
            for action in possibleActions:
                if not counter:
                    maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep,alpha,beta)
                    actionTaken = action
                else:
                    if maxValue[0] < ghostMin(gameState2.generateSuccessor(0,action),1,deep,alpha,beta)[0]:
                        maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep,alpha,beta)
                        actionTaken = action
                if maxValue[0] > beta:
                    return (maxValue[0],actionTaken) 
                alpha = max([alpha,maxValue[0]])
                counter = counter + 1
            #print(maxValue)
        #     keeps track of which agents is time to moves
        #     returns max of two other functions - two different paths they can take
            if not counter:
                return (evalFunction(gameState2),actionTaken)
            return (maxValue[0],actionTaken)


        def ghostMin(gameState3: GameState, ghost: int,deep: int,alpha: float,beta: float):
        #     keeps track of which agents is time to moves
        #     returns min of two other functions - two different paths they can take
            possibleActions = gameState3.getLegalActions(ghost)
            #stateList = []
            minValue = 0
            actionTaken = ""
            counter = 0
            # print(gameState.isLose())
            # print(gameState.isWin())
            for action in possibleActions:
                if numGhosts == ghost:
                    if depth == deep:
                        if not counter:
                            minValue = (evalFunction(gameState3.generateSuccessor(ghost,action)),action)
                            actionTaken = action
                        else:
                            if minValue[0] > evalFunction(gameState3.generateSuccessor(ghost,action)):
                                minValue = (evalFunction(gameState3.generateSuccessor(ghost,action)),action)
                                actionTaken = action
                    else:
                        if not counter:
                            minValue = pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1,alpha,beta)
                            actionTaken = action
                        else:
                            if minValue[0] > pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1,alpha,beta)[0]:
                                minValue = pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1,alpha,beta)
                                actionTaken = action
                else:
                    if not counter:
                        minValue = ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep,alpha,beta)
                        actionTaken = action
                    else:
                        if minValue[0] > ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep,alpha,beta)[0]:
                            minValue = ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep,alpha,beta)
                            actionTaken = action
                if minValue[0] < alpha:
                    return (minValue[0],actionTaken) 
                beta = min([beta,minValue[0]])
                counter+=1
            #print((minValue,actionTaken),minValue)
            if not counter:
                return (evalFunction(gameState3),actionTaken)
            return (minValue[0],actionTaken)
        
        return pacmanMax(gameState,1,float("-inf"),float("inf"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        depthCounter = 1
        numGhosts =  gameState.getNumAgents() - 1
        depth = self.depth
        evalFunction = self.evaluationFunction
        def pacmanMax(gameState2: GameState,deep: int):
            possibleActions = gameState2.getLegalActions(0)
            maxValue = 0
            actionTaken = ""
            counter = 0
            #print(possibleActions)
            for action in possibleActions:
                if not counter:
                    maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep)
                    actionTaken = action
                else:
                    if maxValue[0] < ghostMin(gameState2.generateSuccessor(0,action),1,deep)[0]:
                        maxValue = ghostMin(gameState2.generateSuccessor(0,action),1,deep)
                        actionTaken = action
                counter = counter + 1
            #print(maxValue)
        #     keeps track of which agents is time to moves
        #     returns max of two other functions - two different paths they can take
            if not counter:
                return (evalFunction(gameState2),actionTaken)
            return (maxValue[0],actionTaken)


        def ghostMin(gameState3: GameState, ghost: int,deep: int):
        #     keeps track of which agents is time to moves
        #     returns min of two other functions - two different paths they can take
            possibleActions = gameState3.getLegalActions(ghost)
            #stateList = []
            minValue = 0
            actionTaken = []
            counter = 0
            # print(gameState.isLose())
            # print(gameState.isWin())
            for action in possibleActions:
                if numGhosts == ghost:
                    if depth == deep:
                        minValue += evalFunction(gameState3.generateSuccessor(ghost,action))
                        actionTaken = actionTaken + [action]
                    else:
                        minValue += pacmanMax(gameState3.generateSuccessor(ghost,action),deep+1)[0]
                        actionTaken = actionTaken + [action]
                else:
                    minValue += ghostMin(gameState3.generateSuccessor(ghost,action),ghost+1,deep)[0]
                    actionTaken = actionTaken + [action]
                counter+=1
            #print((minValue,actionTaken),minValue)
            if not counter:
                return (evalFunction(gameState3),actionTaken)
            return (minValue/(counter),random.choice(actionTaken))
        
        return pacmanMax(gameState,1)[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

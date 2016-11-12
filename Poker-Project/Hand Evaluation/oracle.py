# -*- coding: utf-8 -*-
import random
"""
Created on Sat Nov 12 07:42:05 2016

@author: BehroozG
"""
def avg(L):
    total = (sum(L) + 0.0 ) / len(L)
    return total
    
class oraclePlayer:
    #role \in \{small blind, big blind\}
    def __init__(self, role, cash, bets):
        self.role = role                
        self.cash = cash     
        self.depth = 1000 #for now
    
    def getLegalAction(self, gameState):
        if gameState.gameStage == 0:
            if self.role == "small blind":
                return ["place half bet"]
            if self.role == "big blind":
                return ["place full bet"]
        if gameState.gameStage > 0 and gameState.gameStage < gameState.length:
            return ["check", "fold", "raise"]
        if gameState.gameStage == gameState.length:
            return ["showdown"]
        raise Exception("Not a valid State")
    
    # We can either use a NN or a rule that makes sense
    def evaluationFunction(state):
        return 0
        
    # receives a gameState. Based on the gameState, it returns an action.
    # action is a subset of {fold, place half bet, place full bet, check, raise [be a full bet], showdown}
    def bet(self, gameState):
        actions = self.getLegalAction(gameState)
        if len(actions) == 1:
            return actions[0]

        def v(state, playerIndex, depth):
            if state.isWin() or state.isLose():
                return state.getScore()
            if depth == 0:
                return self.evaluationFunction(state)
            if playerIndex == 0:
                legalActions = self.getLegalAction(gameState)
                rewardList = []
                for action in legalActions:
                    possibleStates = state.generateSuccessor(0, action)
                    possibleRewards = [v(s, 1, depth) for s in possibleStates]
                    rewardList.append(avg(possibleRewards))
                #stateList = [state.generateSuccessor(0, action) for action in legalActions]
                #rewardList = [v(s, 1, depth) for s in stateList]
                return max(rewardList)
            if playerIndex == 1:
                legalActions = state.getLegalActions(playerIndex)
                for action in legalActions:
                    possibleStates = state.generateSuccessor(1, action)
                    possibleRewards = [v(s, 0, depth - 1) for s in possibleStates]
                    rewardList.append(avg(possibleRewards))
                #stateList = [state.generateSuccessor(playerIndex, action) for action in legalActions]
                #rewardList = [v(s, 0, depth - 1) for s in stateList]
                return min(rewardList)                        
        choices = [(v(gameState.generateSuccessor(0, action), 0, self.depth), action) \
        for action in actions]
  #  print v(gameState, 0, self.depth)
        bestIndices = [index for index in range(len(choices)) if choices[index][0] == max(choices)[0]]
        chosenIndex = random.choice(bestIndices)
        output = choices[chosenIndex][1]
        return output           
        
    
    
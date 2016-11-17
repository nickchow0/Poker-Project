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
    def __init__(self, cash, bets):        
        self.cash = cash     
        self.depth = 1000 #for now
        
    # We can either use a NN or a rule that makes sense
    def evaluationFunction(state):
        return 0
        
    # receives a gameState. Based on the gameState, it returns an action.
    # action is a subset of # 0=1/2 bet, 1=full bet, 2=fold, 3=check, 4= call, 5=raise, 6=showdown
    def bet(self, gameState):
        actions = gameState.getLegalMoves(gameState)
        #if len(actions) == 1:
        #    return actions[0]
        if len(actions) == 0:
            raise Exception("No Actions Available")

        def v(state, playerIndex, depth):
            if state.isWin == 1 or state.isWin == -1:
                return state.get_score()
            
            if depth == 0:
                return self.evaluationFunction(state)
            currStage = state.getStage();            
            
            if playerIndex == 0:
                legalActions = state.getLegalMoves(playerIndex)
                rewardList = []
                for action in legalActions:
                    possibleStates = state.get_possible_successors(action, 0)
                    possibleRewards = []
                    for s in possibleStates:
                        newStage = s.getStage()
                        diff = newStage - currStage
                        reward = v(s, s.playerTurn, depth - diff) 
                        possibleRewards.append(reward)
                    rewardList.append(avg(possibleRewards))
                #stateList = [state.generateSuccessor(0, action) for action in legalActions]
                #rewardList = [v(s, 1, depth) for s in stateList]
                return max(rewardList)
            
            if playerIndex == 1:
                legalActions = state.getLegalMoves(playerIndex)
                rewardList = []
                for action in legalActions:
                    possibleStates = state.get_possible_successors(action, 1)
                    possibleRewards = []
                    for s in possibleStates:
                        newStage = s.getStage()
                        diff = newStage - currStage
                        reward = v(s, s.playerTurn, depth - diff) 
                        possibleRewards.append(reward)
                    rewardList.append(avg(possibleRewards))
                    #possibleRewards = [v(s, 0, depth - 1) for s in possibleStates]
                    #rewardList.append(avg(possibleRewards))
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
        
    
    
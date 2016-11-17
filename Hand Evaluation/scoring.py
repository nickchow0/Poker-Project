from holdem import Poker
from deck import Card
import sys, random, copy

class Scoring:
    def __init__(self):
        self.totalBet = 0
        self.bets = [[0,0,0,0],[0,0,0,0]]  # We can add this later        
            #card index = card symbol number * 14 + card number 
            #card symbols = [D,H,S,C]
        self.cardsLeftInDeck = range(2,15)+range(16,29)+range(30,43)+range(44,57)
            # Bet Formats [half Bet, Full Bet, Minimum Bet Raise] 
        self.betFormat = [2, 5, 5] 	# in principle this should be supplied
        
        self.folded = [0,0]
        self.gamelength = 4 
        
        self.stage = 0 # 0=preflop, 1=flop, 2=turn, 3= river, 4=end
        
        self.firstPlayer = 0 
        self.playerTurn = self.firstPlayer
        
        self.isWin = 0 # can be 1:win, 0:not ended, -1 : lost		
        self.actions = range(7) # 0=1/2 bet, 1=full bet, 2=fold, 3=check, 4= call, 5=raise, 6=showdown
        self.maxLastBet = 0        
        
        self.communityCards = []
        self.playerCards = []
        self.oppCards = []
        
        self.numberOfRaisesAllowed = 1
     #   self.decisionsRequired = 2

#   Gives all the possible choices of n cards from the current deck        
    def set_firstPlayer(self, int):
    	self.firstPlayer = int

    def add_player_cards(self, int):
        self.playerCards.append(int)

    def add_opp_cards(self, int):
        self.oppCards.append(int)

    def add_community_cards(self, int):
        self.communityCards.append(int)

    def giveAllPossibilities(self, n):        
        allChoices = []       
        def helper(self, n):
            global allChoices
            if n <= 0:
                return
            if n == 1:
                for i in self.cardsLeftInDeck:
                    allChoices.append([i])
                return
            temp = []
            for comb in allChoices:
                M = max(comb)                                
                for i in self.cardLeftInDeck:
                    if i > M:
                        tau = copy.deepcopy(comb)
                        tau.append(i)                        
                        temp.append(tau)
            allChoices = tau
            helper(n - 1)
        
        helper(n)
        return allChoices
    
    # This function advances the stage / changes the turn appropraitely    
    def advanceStage(self, n):        
        if n == 0: # Next stage
            self.stage += 1 #for now we only have one round of betting
            self.maxLastBet = 0
            self.playerTurn = self.firstPlayer
            self.numberOfRaisesAllowed = 2
        if n == 1: #advance turn
            if self.playerTurn == 0:
                self.playerTurn = 1
            else:
                self.playerTurn = 0        
                
    def getLegalMoves(self, playerInd):
        if self.stage == 4:
            return [6]
        if self.stage == 0 and self.maxLastBet == 0:
            if self.firstPlayer == playerInd:
                return [0]
            else:
                return [1]
        if self.maxLastBet == 0:
            return [2, 3, 5]
        if self.numberOfRaisesAllowed > 0:
            return [2, 4, 5]
        else:
            return [2, 4]

    def removeCardFromDeck(self, i):
        self.cardsLeftInDeck.remove(i)
    
    def get_score(self):
        if self.isWin == 1:
		return self.totalBet
        if self.isWin == -1:
		return -self.totalBet
        if self.isWin == 0:
           raise Exception("get_score Called on the state that is not terminal")

    def get_totalBet(self):
		return self.totalBet

    def makeBet(self, amount, player, roundNum):
		self.totalBet += amount
		self.bets[player][roundNum] += amount

    def fold(self, i):
		self.folded[i] = 1

    def allStillIn(self):
		return sum(self.folded) == 0

    def playerStillIn(self, i):
		return self.folded[i] == 0

    def totalBetForPlayer(self, i):
		return sum(self.bets[i])

    def setStage(self, newStage):
        self.stage = newStage

    def getStage(self):
        return self.stage
        
# Things that this function should do:
# Appropriately increase game stage
# return a list of possible successor states
# check if the game has ended --> update isWin accordingly
# 
    def get_possible_successors(self, action, playerIndex):
        if self.stage == 0 and action == 0: #small blind
            if (playerIndex != self.firstPlayer):
                raise Exception("Only the first player can post half bets")
            else:
                cp = copy.deepcopy(self)
                cp.bets[playerIndex][cp.stage] = cp.betFormat[0] 
                cp.advanceStage(1)
                cp.totalBet += cp.betFormat[0]                
                return [cp]                        
        
        if self.stage == 0 and action == 1:            
            if (playerIndex != self.firstPlayer): 
                cp = copy.deepcopy(self)
                cp.bets[playerIndex][cp.stage] = cp.betFormat[1] 
                cp.advanceStage(1)
                cp.totalBet += cp.betFormat[1]                
                return [cp]
            else:
                raise Exception("Only the second player can post full bets")

        #folding
        if action == 2:
            cp = copy.deepcopy(self)
            cp.advanceStage(0)            
            if playerIndex == 0:
                cp.isWin = 1
            else:
                cp.isWin = -1
                
        if action == 3: # check   
            allStates = []         
            if self.maxLastBet == 0 and self.firstPlayer != playerIndex:
                if self.stage == 0:
                    allPossibilities = self.giveAllPossibilities(3)
                if self.stage > 0 and self.stage < 3:
                    allPossibilities = self.giveAllPossibilities(1)
                if self.stage == 3:
                    cp = copy.deepcopy(self)
                    cp.advanceStage(0)
                    return [cp]                
                for i in allPossibilities:
                    cp = copy.deepcopy(self)                    
                    cp.advanceStage(0)
                    cp.communityCards += i
                    for j in i:
                        cp.removeCardFromDeck(j)
                    allStates.append(cp)
                return allStates
            cp = copy.deepcopy(self)
            cp.advanceStage(1)
            return [cp]
        # A Call
        if action == 4: #Assumption : A turn always ends with a call
            if self.maxLastBet <= 0:
                raise Exception("You cannot call when there has been no bets")
            
            allStates = []                                             
            if self.stage == 0:
                allPossibilities = self.giveAllPossibilities(3)
            if self.stage > 0 and self.stage < 3:
                allPossibilities = self.giveAllPossibilities(1)
            if self.stage == 3:
                cp = copy.deepcopy(self)
                cp.totalBet += self.maxLastBet
                cp.bets[playerIndex][cp.stage] = self.maxLastBet                    
                cp.advanceStage(0)                    
                return [cp]                

            for i in allPossibilities:
                cp = copy.deepcopy(self)                    
                cp.totalBet += self.maxLastBet
                cp.bets[playerIndex][cp.stage] = self.maxLastBet                    
                cp.advanceStage(0)
                cp.communityCards += i
                for j in i:
                    cp.removeCardFromDeck(j)
                allStates.append(cp)
            return allStates                                

        if action == 5: # Raise or Bet
            allStates = []
            if self.numberOfRaisesAllowed == 0:
                raise Exception("Can't Raise Anymore")
            cp = copy.deepcopy(self)
            cp.bets[playerIndex][cp.stage] = self.betFormat[2] + self.maxLastBet
            cp.maxLastBet += self.betFormat[2]
            self.totalBet += self.maxLastBet
            cp.numberOfRaisesAllowed -= 1
            cp.advanceStage(1)
            return [cp]
                 
        if action == 6: # showDown         
            if self.stage == self.gamelength:
                #convert back to cards
                community_cards = []
                player_cards = []
                opp_cards = []

                for integer in community_cards:
                    community_cards.append(Card(integer/14, integer%14))
                for integer in player_cards:
                    player_cards.append(Card(integer/14, integer%14))
                for integer in opp_cards:
                    opp_cards.append(Card(integer/14, integer%14))

                results = poker.determine_score(community_cards, [player_cards, opp_cards])
                winner = poker.determine_winner(results)

                if winner == 0:
                    self.isWin = 1
                else:
                    self.isWin = -1
            else:
                raise Exception("ShowDown has been called too early")
        
        
        
#from holdem import Poker
#import sys, random
#
#class Scoring:
#	def __init__(self):
#		self.totalBet = 0
#		self.bets = [[0,0,0,0],[0,0,0,0]] 
#            # Bet Formats [half Bet, Full Bet, ] 
#		self.folded = [0,0]
#            # 
#	def get_totalBet(self):
#		return self.totalBet
#	def makeBet(self, amount, player, roundNum):
#		self.totalBet += amount
#		self.bets[player][roundNum] += amount
#	def fold(self, i):
#		self.folded[i] = 1
#	def allStillIn(self):
#		return sum(self.folded) == 0
#	def playerStillIn(self, i):
#		return self.folded[i] == 0
#	def totalBetForPlayer(self, i):
#		return sum(self.bets[i])
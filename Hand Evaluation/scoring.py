from holdem import Poker
import sys, random, copy

class Scoring:
    def __init__(self):
        self.totalBet = 0
        self.bets = [[0,0,0,0],[0,0,0,0]] 
            #card index = card symbol number * 14 + card number 
            #card symbols = [D,H,S,C]
        self.cardsLeftInDeck = range(2,15)+range(16,29)+range(30,43)+range(44,57)
            # Bet Formats [half Bet, Full Bet, Minimum Bet Raise] 
        self.betFormat = [2, 5, 5] 	# in principle this should be supplied
        self.folded = [0,0]
        self.gamelength = 4 
        self.stage = 0 # 0=preflop, 1=flop, 2=turn, 3= river, 4=end
        self.firstPlayer = random.randint(0,1) 
        self.playerTurn = self.firstPlayer
        self.isWin = 0 # can be 1:win, 0:not ended, -1 : lost		
        self.actions = range(6) # 0=1/2 bet, 1=full bet, 2=fold, 3=check, 4=raise, 5=showdown
        self.maxLastBet = 0
    
#   Gives all the possible choices of n cards from the current deck        
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
        
    def advanceStage(self):        
        if self.playerTurn != self.firstPlayer:    
            self.stage += 1 #for now we only have one round of betting
            self.maxLastBet = 0
        if self.playerTurn == 0:
            self.playerTurn = 1
        else:
            self.playerTurn = 0        

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
                cp.advanceStage()
                cp.totalBet += cp.betFormat[0]
                cp.bets[playerIndex][cp.stage] = cp.betFormat[0] 
                return cp                        
        #add the cards!!    
        if self.stage == 0 and action == 1:            
            if (playerIndex != self.firstPlayer): # TO DO: give another round of betting!
                cp = copy.deepcopy(self)
                cp.advanceStage()
                cp.totalBet += cp.betFormat[1]
                cp.bets[playerIndex][cp.stage] = cp.betFormat[1] 
                return cp
            else:
                raise Exception("Only the second player can post full bets")

        #folding
        if action == 2:
            cp = copy.deepcopy(self)
            cp.advanceStage()            
            if playerIndex == 0:
                cp.isWin = 1
            else:
                cp.isWin = -1
                
        if action == 3: # check
            cp = copy.deepcopy(self)
            cp.advanceStage()
            
        if action == 4: #raise
            pass
        
        if action == 5: # showDown 
            pass
        if self.stage == self.gamelength:
            pass #go to showdown
        
        
        
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
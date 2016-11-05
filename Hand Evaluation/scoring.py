from holdem import Poker
import sys, random

class Scoring:
	def __init__(self):
		self.totalBet = 0
		self.bets = [[0,0,0,0],[0,0,0,0]]
		self.folded = [0,0]
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
from holdem import Poker
import sys, random

class player:
	def __init__(self, personality, own_cards, poker, dealer = 0, blind):
		self.balance = 1000
		self.personality = personality
		self.own_cards = own_cards
		self.poker = poker
		self.dealer = dealer
		self.blind = blind
		# # self.bets = []
		# if self.dealer != 1:
		# 	self.bets = [self.blind]
		print "player1 = " + str(own_cards)

	def get_balance(self):
		return self.balance

	def get_personality(self):
		return self.personality

	def is_dealer(self):
		return self.dealer

	# def get_bets(self):
	# 	return self.bets

	# def bet(amt):
	# 	self.bets.append(amt)
	# 	return self.bets

	# 
# from holdem import Poker
# import sys, random

class player:
	def __init__(self, personality, own_cards, blind, dealer = 0):
		self.balance = 1000
		self.personality = personality
		self.own_cards = [own_cards[0], own_cards[1]]
		# self.poker = poker
		self.dealer = dealer
		self.blind = blind
		# # self.bets = []
		# if self.dealer != 1:
		# 	self.bets = [self.blind]
		print "player = "
		print str(own_cards[0]) + ' ' + str(own_cards[1])

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
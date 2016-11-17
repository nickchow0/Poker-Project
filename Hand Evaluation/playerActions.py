def playerActions(personality, player, score):
	# baseline player
	if personality == 1:
		#if dealer/small blind, bet 0
		if player.is_dealer() == 1 and score.getStage() == 0:
			return "C"
		elif player.is_dealer() == 1 and score.getStage() != 0:
			return 0
		else:
			return "C"


		# # if betting second and other player bets more than you -> call
		# if 
		# # if betting second and other player checks -> check
		# return "C"


from scoring import Scoring
from holdem import Poker
import sys, random
from player import player
from oracle import oraclePlayer

debug = False    #Set to True to see the debug statements
number_of_players = 2
bigblind = 2
gameNumber = 0

player1 = player(0, [None, None], bigblind)
player2 = player(0, [None, None], bigblind)
oracle = oraclePlayer(1000, None)

while(True):
    gameNumber += 1
    print "Game %d" %gameNumber

    #set dealers
    if gameNumber %2 == 1:
        player1.set_dealer()
        player2.remove_dealer()
    else:
        player2.set_dealer()
        player1.remove_dealer()

    score = Scoring()

    score.set_firstPlayer(gameNumber%2-1)

    poker = Poker(number_of_players, debug)
    if not poker:
        sys.exit("*** ERROR ***: Invalid number of players. It must be between 2 and 22.")

    print "1. Shuffling"
    poker.shuffle()

    print "2. Cutting"
    if not poker.cut( random.randint(1,51) ):
        #Cannot cut 0, or the number of cards in the deck
        sys.exit("*** ERROR ***: Invalid amount entered to cut the deck.")    

    print "3. Distributing"
    players_hands = poker.distribute()
    player1.set_cards(players_hands[0])
    player2.set_cards(players_hands[1])

    if not players_hands:
        sys.exit("*** ERROR ***: Insufficient cards to distribute. ")

    print "4. Hands"
    print "-----------------------"
    for i, hand in enumerate(players_hands):
        text = "Player %d - " % (i+1)
        for card in hand:
            #removing cards from deck:
            j = card.getSymbol()*14 + card.getValue()
            score.removeCardFromDeck(j)
            if i == 0:
                score.add_player_cards(j)
            else:
                score.add_opp_cards(j)
            text += str(card) + "  "
        print text
    print "-----------------------"

    #Displays the Cards
    def display_community_cards(community_cards):
        text = "Community Cards - "
        for card in community_cards:
            text += str(card) + "  "
        print text  
        print "-----------------------"

    #i is player number - either 0 or 1
    def bet(i, round):
        if i == 0:
            action = oracle.bet(score) # 0=1/2 bet, 1=full bet, 2=fold, 3=check, 4= call, 5=raise, 6=showdown
            if action == 0:
                bet = bigblind/2
            elif action == 1:
                bet = bigblind
            elif action == 2:
                bet = "F"
            elif action == 3:
                bet = 0
            elif action == 4:
                bet = "C"
            elif action == 5:
                bet = 10
            elif action == 6:
                sys.exit("Error")
            amount = bet
            print "Player 1: Bet %d" %amount
            score.makeBet(amount, i, round)
            valid_responses = ["C", "F"]
            response = raw_input("Player 2: Call(C) or Fold(F): ")
            while response not in valid_responses:
                response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
            if response == "C":
                score.makeBet(amount, j, round)
            else:
                score.fold(j)
            print "Total bet so far is %d" % score.get_totalBet()
        else:
            amount = input("Player %d: Amount to Bet (0 to Check): " % (i+1)) 
            while type(amount) != int:
                amount = input("Amount to Bet (0 to Check): ")
            score.makeBet(amount, i, round)
            action = oracle.bet(score) # 0=1/2 bet, 1=full bet, 2=fold, 3=check, 4= call, 5=raise, 6=showdown
            if action == 0:
                bet = bigblind/2
            elif action == 1:
                bet = bigblind
            elif action == 2:
                bet = "F"
            elif action == 3:
                bet = 0
            elif action == 4:
                bet = "C"
            elif action == 5:
                bet = 10
            elif action == 6:
                sys.exit("Error")
            print bet
            if bet == "C":
                score.makeBet(amount, j, round)
            else:
                score.fold(j)
            print "Total bet so far is %d" % score.get_totalBet()






        # amount = input("Player %d: Amount to Bet (0 to Check): " % (i+1)) 
        # while type(amount) != int:
        #     amount = input("Amount to Bet (0 to Check): ")
        # score.makeBet(amount, i, round)
        # j = (i+1)%2
        # valid_responses = ["C", "F"]
        # response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
        # while response not in valid_responses:
        #     response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
        # if response == "C":
        #     score.makeBet(amount, j, round)
        # else:
        #     score.fold(j)
        # print "Total bet so far is %d" % score.get_totalBet()

    def modified_bet(i):
        j = (i+1)%2
        valid_responses = ["C", "F"]
        response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
        while response not in valid_responses:
            response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
        if response == "C":
            score.makeBet(bigblind/2, j, 0)
        else:
            score.fold(j)
        print "Total bet so far is %d" % score.get_totalBet()

    #Pre-Flop bets

    #blinds
    if player1.is_dealer():
        score.makeBet(bigblind/2, 0, 0)
        score.makeBet(bigblind, 1, 0)
    else:
        score.makeBet(bigblind/2, 1,0)
        score.makeBet(bigblind, 0, 0)   

    if player1.is_dealer():
        modified_bet(1)
    else:
        modified_bet(0)

    #Flop
    score.setStage(1)
    if score.allStillIn():
        print "5a - Flop"
        print "-----------------------"
        card = poker.getFlop()
        if not card:
            sys.exit("*** ERROR ***: Insufficient cards to distribute.")
        community_cards = card
        print community_cards
        for indiv_card in community_cards:
            j = indiv_card.getSymbol()*14 + indiv_card.getValue()
            score.removeCardFromDeck(j)
            score.add_community_cards(j)
        display_community_cards(community_cards)
        if player1.is_dealer():
            bet(0,1)
        else:
            bet(1,1)

    #Turn
    score.setStage(2)
    if score.allStillIn():
        print "5b - Turn"
        print "-----------------------"
        card = poker.getOne()
        j = card[0].getSymbol()*14 + card[0].getValue()
        score.removeCardFromDeck(j)
        score.add_community_cards(j)
        if not card:
            sys.exit("*** ERROR ***: Insufficient cards to distribute.")
        community_cards.extend( card )
        display_community_cards(community_cards)
        if player1.is_dealer():
            bet(0,2)
        else:
            bet(1,2)

    #River
    score.setStage(3)
    if score.allStillIn():
        print "5c - River"
        print "-----------------------"
        card = poker.getOne()
        j = card[0].getSymbol()*14 + card[0].getValue()
        score.removeCardFromDeck(j)
        score.add_community_cards(j)
        if not card:
            sys.exit("*** ERROR ***: Insufficient cards to distribute.")
        community_cards.extend( card ) 
        display_community_cards(community_cards)
        if player1.is_dealer():
            bet(0,3)
        else:
            bet(1,3)

    score.setStage(4)
    if score.allStillIn():
        print "6. Determining Score"
        try:
            results = poker.determine_score(community_cards, players_hands)
        except:
            sys.exit("*** ERROR ***: Problem determining the score.")

        print "7. Determining Winner"  
        try:
            winner = poker.determine_winner(results)
            print '123'
            print winner
        except:
            sys.exit("*** ERROR ***: Problem determining the winner.")

        #Checks to see if the hand has ended in tie and displays the appropriate message         
        tie = True
        try:
            len(winner)
        except:
            tie = False
        if not tie:
            counter = 0
            print "-------- Winner has Been Determined --------"
            for hand in players_hands:
                if counter == winner:
                    text = "Winner ** "
                else:
                    text = "Loser  -- " 
                for c in hand:
                    text += str(c) + "  "
                
                text += " --- " + poker.name_of_hand(results[counter][0])
                counter += 1
                print text
            if winner == 0:
                print "Player 1 won %d" %(score.get_totalBet() - score.totalBetForPlayer(0))
                print "Player 2 lost %d" %(score.totalBetForPlayer(1))
                player1.add_balance(score.get_totalBet() - score.totalBetForPlayer(0))
                player2.add_balance(-score.totalBetForPlayer(1))
                print "Player 1 now has $%d" %player1.get_balance()
                print "Player 2 now has $%d" %player2.get_balance()
            else:
                print "Player 1 lost %d" %(score.totalBetForPlayer(0))
                print "Player 2 won %d" %(score.get_totalBet() - score.totalBetForPlayer(1))
                player1.add_balance(-score.totalBetForPlayer(0))
                player2.add_balance(score.get_totalBet() - score.totalBetForPlayer(1))
                print "Player 1 now has $%d" %player1.get_balance()
                print "Player 2 now has $%d" %player2.get_balance()
        else: 
            counter = 0
            print "--------- Tie has Been Determined --------"
            for hand in players_hands:
                if counter in winner:
                    text = "Winner ** "
                else:
                    text = "Loser  -- " 
                for c in hand:
                    text += str(c) + "  "
                
                text += " --- " + poker.name_of_hand(results[counter][0])
                counter += 1
                print text
            print "Player 1 won 0"
            print "Player 2 won 0"
            print "Player 1 now has $%d" %player1.get_balance()
            print "Player 2 now has $%d" %player2.get_balance()
    else:
        #check who folded
        if score.playerStillIn(0):
            print "Player 1 won %d" %(score.get_totalBet() - score.totalBetForPlayer(0))
            print "Player 2 lost %d" %(score.totalBetForPlayer(1))
            player1.add_balance(score.get_totalBet() - score.totalBetForPlayer(0))
            player2.add_balance(-score.totalBetForPlayer(1))
            print "Player 1 now has $%d" %player1.get_balance()
            print "Player 2 now has $%d" %player2.get_balance()
        else:
            print "Player 1 lost %d" %(score.totalBetForPlayer(0))
            print "Player 2 won %d" %(score.get_totalBet() - score.totalBetForPlayer(1))
            player1.add_balance(-score.totalBetForPlayer(0))
            player2.add_balance(score.get_totalBet() - score.totalBetForPlayer(1))
            print "Player 1 now has $%d" %player1.get_balance()
            print "Player 2 now has $%d" %player2.get_balance()
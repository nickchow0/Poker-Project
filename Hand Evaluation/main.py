from scoring import Scoring
from holdem import Poker
import sys, random
from player import player

debug = False    #Set to True to see the debug statements
number_of_players = 2

score = Scoring()

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

# result = []
# for i, hand in enumerate(players_hands):
#     for card in hand:
#         result.append(card)
#     print text
player1 = player(0, players_hands[0], 100, dealer = 1) # self, personality, own_cards, poker, blind, dealer = 0
player2 = player(0, players_hands[1], 100) # self, personality, own_cards, poker, dealer = 0

if not players_hands:
    sys.exit("*** ERROR ***: Insufficient cards to distribute.")

print "4. Hands"
print "-----------------------"
for i, hand in enumerate(players_hands):
    text = "Player %d - " % (i+1)
    for card in hand:
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
    amount = input("Player %d: Amount to Bet (0 to Check): " % (i+1)) 
    while type(amount) != int:
        amount = input("Amount to Bet (0 to Check): ")
    score.makeBet(amount, i, round)
    j = (i+1)%2
    valid_responses = ["C", "F"]
    response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
    while response not in valid_responses:
        response = raw_input("Player %d: Call(C) or Fold(F): " % (j+1))
    if response == "C":
        score.makeBet(amount, j, round)
    else:
        score.fold(j)
    print "Total bet so far is %d" % score.get_totalBet()


#Pre-Flop bets
bet(0, 0)

#Flop
if score.allStillIn():
    print "5a - Flop"
    print "-----------------------"
    card = poker.getFlop()
    #print poker.getFlop()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards = card
    display_community_cards(community_cards)
    bet(1,1)

#Turn
if score.allStillIn():
    print "5b - Turn"
    print "-----------------------"
    card = poker.getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend( card )
    display_community_cards(community_cards)
    bet(0,2)

#River
if score.allStillIn():
    print "5c - River"
    print "-----------------------"
    card = poker.getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend( card ) 
    display_community_cards(community_cards)
    bet(1,3)

if score.allStillIn():
    print "6. Determining Score"
    try:
        results = poker.determine_score(community_cards, players_hands)
    except:
        sys.exit("*** ERROR ***: Problem determining the score.")

    print "7. Determining Winner"  
    try:
        winner = poker.determine_winner(results)
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
        else:
            print "Player 1 lost %d" %(score.totalBetForPlayer(0))
            print "Player 2 won %d" %(score.get_totalBet() - score.totalBetForPlayer(1)) 
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
else:
    #check if player 1 still in
    if score.playerStillIn(0):
        print "Player 1 won %d" %(score.get_totalBet() - score.totalBetForPlayer(0))
        print "Player 2 lost %d" %(score.totalBetForPlayer(1))
    else:
        print "Player 1 lost %d" %(score.totalBetForPlayer(0))
        print "Player 2 lost %d" %(score.get_totalBet() - score.totalBetForPlayer(1)) 

#!/usr/bin/python

import sys
import random
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep

# Class Declartion of the Card Ranks
class hand_ranks:
    STRAIGHT_FLUSH = "Straight Flush!!!"
    TRIPLE = "Triple!!"
    STRAIGHT = "Straight!"
    FLUSH = "Flush!"
    PAIR = "Pair"
    HIGH_CARD = "High Card"

# Class Declartion of the Card 
class card:
    suit = ''
    value = ''

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __str__(self):
        return "%s%s" % (self.suit, self.value)

    SUITS = ['D','C','H','S']
    VALUES = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']

# Class Declartion of the Deck 
class deck:
    cards = []
    isNew = None

    def __init__(self):
        self.isNew = True
        self.cards = []
        for suit in card.SUITS:
            for value in card.VALUES:
                self.cards.append(card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self):
        return self.cards.pop()

# Class Declartion of the Determine method to identify the CARD Winner
class determine:

    def determine(self, cards):

        analyzer = hand_analyzer(cards)
        straight_flush_analyzer = straight_flush(cards)
        three_of_a_kind_analyzer = triple(cards)
        straight_analyzer = straight(cards)
        flush_analyzer = flush(cards)
        pair_analyzer = pair(cards)
        high_card_analyzer = high(cards)

        high_card_analyzer.set_next(None)
        pair_analyzer.set_next(high_card_analyzer)
        flush_analyzer.set_next(pair_analyzer)
        straight_analyzer.set_next(flush_analyzer)
        three_of_a_kind_analyzer.set_next(straight_analyzer)
        straight_flush_analyzer.set_next(three_of_a_kind_analyzer)
        analyzer.set_next(straight_flush_analyzer)

        return analyzer.analyze()

# Class Declartion of the Analyser to identify the CARD Winner
class hand_analyzer(object):
    cards = None
    next_analizer = None

    def __init__ (self, cards):
        self.cards = cards
        self.next_analyzer = None

    def set_next(self, analyzer):
        self.next_analyzer = analyzer

    def analyze(self):
        if(len(self.cards) != 3):
            return "Invalid hand"

        if(self.next_analyzer is not None):
            return self.next_analyzer.analyze()

        return "Hand is good"

# Class to determine the flush
class flush(hand_analyzer):

    def analyze(self):
        if(self.cards[0].suit == self.cards[1].suit == self.cards[2].suit):
            return hand_ranks.FLUSH
        return super(flush, self).analyze()

# Class to determine the pair 
class pair(hand_analyzer):

    def analyze(self):
        if(self.cards[0].value == self.cards[1].value or
           self.cards[0].value == self.cards[2].value or
           self.cards[1].value == self.cards[2].value):
            return hand_ranks.PAIR
        return super(pair, self).analyze()

# Class to determine the high hard 
class high(hand_analyzer):

    def analyze(self):
        return hand_ranks.HIGH_CARD

# Class to determine the straight flush 
class straight_flush(hand_analyzer):

    def analyze(self):
        if(self.cards[0].suit == self.cards[1].suit == self.cards[2].suit):
            values = [card.VALUES.index(self.cards[0].value),
                      card.VALUES.index(self.cards[1].value),
                      card.VALUES.index(self.cards[2].value)]
            values.sort()
            if(values[2] - values[1] == 1 and values[1] - values[0] == 1):
                return hand_ranks.STRAIGHT_FLUSH
        return super(straight_flush, self).analyze()

# Class to determine the triple 
class triple(hand_analyzer):

    def analyze(self):
        if(self.cards[0].value == self.cards[1].value == self.cards[2].value):
            return hand_ranks.TRIPLE
        return super(triple, self).analyze()

# Class to determine the straight 
class straight(hand_analyzer):

    def analyze(self):
        values = [card.VALUES.index(self.cards[0].value),
                      card.VALUES.index(self.cards[1].value),
                      card.VALUES.index(self.cards[2].value)]
        values.sort()
        if(values[2] - values[1] == 1 and values[1] - values[0] == 1):
            return hand_ranks.STRAIGHT
        return super(straight, self).analyze()

# The Main Class that draws the GUI Window and handles the user interactions 
class GuiWindow(QtGui.QWidget):
   
    def __init__(self):
        super(GuiWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):

	# Determine the variables 
	self.dealer_hand= []
	self.current_hand = []
	dealer_result = ''
	player_result = ''
	self.hand_evaluate = determine()
	self.wDeck = deck()
	self.wDeck.shuffle()
        self.dealer_hand.append(self.wDeck.take_card())
        self.dealer_hand.append(self.wDeck.take_card())
        self.dealer_hand.append(self.wDeck.take_card())
        self.current_hand.append(self.wDeck.take_card())
        self.current_hand.append(self.wDeck.take_card())
        self.current_hand.append(self.wDeck.take_card())
        
	# Declare the labels
	self.l0 = QLabel("Computer")
        self.l1 = QLabel()
        self.l2 = QLabel()
        self.l3 = QLabel()
        self.l4 = QLabel()
        self.l5 = QLabel()
        self.l6 = QLabel()
        self.l7 = QLabel("User")

	# Declare the layout
	self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.vbox = QVBoxLayout()

	# Assigning the label variables
	if(len(self.current_hand) == 3):
            output = "%s%s.png - %s%s.png - %s%s.png - %s%s.png - %s%s.png - %s%s.png" % (self.current_hand[0].value, self.current_hand[0].suit,
                                          	self.current_hand[1].value, self.current_hand[1].suit,
                                        	self.current_hand[2].value, self.current_hand[2].suit,
        	                	        self.dealer_hand[0].value, self.dealer_hand[0].suit,
                	                        self.dealer_hand[1].value, self.dealer_hand[1].suit,
                        	                self.dealer_hand[2].value, self.dealer_hand[2].suit)
        #print (output)
        self.var1="%s%s.png"%(self.dealer_hand[0].value,self.dealer_hand[0].suit)
        self.var2="%s%s.png"%(self.dealer_hand[1].value,self.dealer_hand[1].suit)
        self.var3="%s%s.png"%(self.dealer_hand[2].value,self.dealer_hand[2].suit)
        self.var4="%s%s.png"%(self.current_hand[0].value,self.current_hand[0].suit)
        self.var5="%s%s.png"%(self.current_hand[1].value,self.current_hand[1].suit)
        self.var6="%s%s.png"%(self.current_hand[2].value,self.current_hand[2].suit)

	# Declare buttons
	self.showfold = QPushButton("Fold/GiveUp")
        self.showbeet = QPushButton("Play Bet")

	# Assigning the label value
	self.l1.setPixmap(QPixmap(self.var1))
        self.l2.setPixmap(QPixmap(self.var2))
        self.l3.setPixmap(QPixmap("red_back.png"))
        self.l4.setPixmap(QPixmap(self.var4))
        self.l5.setPixmap(QPixmap(self.var5))
        self.l6.setPixmap(QPixmap("red_back.png"))

        # first line widgets
        self.hbox1.addStretch(1)
	self.hbox1.addWidget(self.l1)
        self.hbox1.addWidget(self.l2)
        self.hbox1.addWidget(self.l3)
        
        # second line widgets
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.l4)
        self.hbox2.addWidget(self.l5)
        self.hbox2.addWidget(self.l6)
        
        # third line widgets
        self.hbox3.addStretch(1)
	self.hbox3.addWidget(self.showfold)
        self.hbox3.addWidget(self.showbeet)
        
	# add the vertical widgets
        self.vbox.addWidget(self.l0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addWidget(self.l7)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addStretch()
        self.showfold.clicked.connect(self.showcard)
        self.showbeet.clicked.connect(self.showmoney)

        self.setLayout(self.vbox) 
        
        self.setWindowTitle("Arelly's AI Poker Game")    
        self.show()

    # Method to show the card
    def showcard(self):
	self.l3.setPixmap(QPixmap(self.var3));
	self.l6.setPixmap(QPixmap(self.var6));
	self.dealer_result = self.hand_evaluate.determine(self.dealer_hand)
	self.player_result = self.hand_evaluate.determine(self.current_hand)
	print "###############################"
	print "######### FINAL RESULT ########"
	print "###############################"
	print "Computer Result: " + self.dealer_result
	a = self.getResultValue(self.dealer_result)
	print "User Result: " + self.player_result
	b = self.getResultValue(self.player_result)
	if (a<b):
	   print "COMPUTER WON!!"
	if (b<a):
	   print "USER WON!!"
	if (a==b):	   
	   print "GAME DRAW!!"
	
	self.showfold.setDisabled(True)
	self.showbeet.setDisabled(True)
        
    # Method to show the money 
    def showmoney(self):
	val = int(ante,10)
	print ""
	print ""
	print "###############################"
        print "User: Raising the Play Bet: $" + str(val+val)
	print "###############################"
	print ""
	print "###############################"
	print ("Computer: Thinking of raising the bet or folding")
	print "###############################"
	print ""
	for x in range(10):
	    sleep(0.5)
	    self.special_print('.')
 	print "."
	print ""
	print "###############################"
        print "Computer: Raising the Play Bet: $" + str(val+val)
	print "###############################"

	# The AI Engine
	if self.dealer_hand[0].suit == self.dealer_hand[1].suit:
	     self.temp = self.dealer_hand[2].suit
	     self.actual = "%s%s"%(self.dealer_hand[2].value,self.temp)
	     print "actual card: " + self.actual 
             self.dealer_hand[2].suit = self.dealer_hand[0].suit
             self.var3="%s%s.png"%(self.dealer_hand[2].value,self.dealer_hand[2].suit)
	     print "predicated card: " + self.var3 
	     if self.var3 == self.var1 or self.var3 == self.var2 or self.var3 == self.var4 or self.var3 == self.var5 or self.var3 == self.var6:
		 self.dealer_hand[2].suit = self.temp
                 self.var3="%s%s.png"%(self.dealer_hand[2].value,self.dealer_hand[2].suit)
		 
	if self.dealer_hand[0].value == self.dealer_hand[1].value:
	     self.temp = self.dealer_hand[2].value
	     self.actual = "%s%s"%(self.temp,self.dealer_hand[2].suit)
	     print "actual card: " + self.actual 
             self.dealer_hand[2].value = self.dealer_hand[0].value
             self.var3="%s%s.png"%(self.dealer_hand[2].value,self.dealer_hand[2].suit)
	     print "predicated card: " + self.var3 
	     if self.var3 == self.var1 or self.var3 == self.var2 or self.var3 == self.var4 or self.var3 == self.var5 or self.var3 == self.var6:
		 self.dealer_hand[2].value= self.temp
                 self.var3="%s%s.png"%(self.dealer_hand[2].value,self.dealer_hand[2].suit)
 
        # Revealing the card
	self.l3.setPixmap(QPixmap(self.var3));
	self.l6.setPixmap(QPixmap(self.var6));
	self.dealer_result = self.hand_evaluate.determine(self.dealer_hand)
	self.player_result = self.hand_evaluate.determine(self.current_hand)

	print ""
	print "###############################"
	print "######### FINAL RESULT ########"
	print "###############################"
	print "Computer Result: " + self.dealer_result
	a = self.getResultValue(self.dealer_result)
	print "User Result: " + self.player_result
	b = self.getResultValue(self.player_result)
	if (a<b):
	   print "COMPUTER WON!!"
	if (b<a):
	   print "USER WON!!"
	if (a==b):	   
	   print "GAME DRAW!!"
	
	# Disable the button after the result is displayed
	self.showfold.setDisabled(True)
	self.showbeet.setDisabled(True)

    # The method to print the thinking dots
    def special_print(self,value):
    	sys.stdout.write(value)
    	sys.stdout.flush()

    # The method to identify the index of the Result
    def getResultValue(self,value):
        RESULT = ['Straight Flush!!!','Triple!!','Straight!','Flush!','Pair','High Card']
	x = RESULT.index(value)
 	return x

# The Main Funcation where the program starts
def main():
    
    app = QtGui.QApplication(sys.argv)
    global ante
    ante=""
    while(not ante.isdigit()):
    	ante = raw_input("Enter the inital bet amount for User: $ ")
        if(not ante.isdigit()):
            print "Enter a number for initial bet amount."
        else:
	    print ""
	    print "###############################"
	    print "User's initial bet: $" + ante
	    print "###############################"
	    print ""
	    print "###############################"
	    print "Computer's initial bet: $" + ante
	    print "###############################"
            ex = GuiWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


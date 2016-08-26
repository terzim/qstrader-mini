import random
import decimal

from event import OrderEvent
from statistics import mean

D = decimal.Decimal
decimal.getcontext().prec = 7

class TestRandomStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                side = random.choice(["buy", "sell"])
                order = OrderEvent(
                    self.instrument, self.units, "market", side
                )
                self.events.put(order)

class RSIStrategy(object):
    def __init__(self, instrument, units, events, min_window = 40):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.min_window = min_window
        self.ticks = 0
        self.prices = []
        self.gains = []
        self.meangains = []
        self.losses = []
        self.meanlosses = []

    def pricelist(self,event):
        if event.type == 'TICK':
            self.ticks += 1
            self.prices.append(D(event.bid))
        return self.prices

    def average_gain(self):
        #gains = []
        #meangains = []
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) < 0:
                self.gains.append(D(0))
            else:
                self.gains.append(D(self.prices[x] - self.prices[x-1]))
        if len(self.prices) == (self.min_window + 1):
            meangain = D(mean(self.gains))
            self.meangains.append(meangain)
        elif len(self.prices) > (self.min_window + 1):
            meangain = D(((self.meangains[len(self.prices)-self.min_window-2]*(self.min_window-1)) + self.gains[len(self.prices)-2])/(self.min_window))
            self.meangains.append(meangain)
        #try:
            return self.meangains[len(self.prices)-self.min_window-1]
        #except IndexError:
        #    pass

    #computes the average loss given the string of prices
    def average_loss(self):
        #losses = []
        #meanlosses = []
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) > 0:
                self.losses.append(D(0))
            else:
                self.losses.append(D(self.prices[x-1] - self.prices[x]))
        if len(self.prices) == (self.min_window + 1):
            meanloss = D(mean(self.losses))
            self.meanlosses.append(meanloss)
        elif len(self.prices) > (self.min_window + 1):
            meanloss = D(((self.meanlosses[len(self.prices)-self.min_window-2]*(self.min_window-1)) + self.losses[len(self.prices)-2])/(self.min_window))
            self.meanlosses.append(meanloss)
        #try:
            return self.meanlosses[len(self.prices)-self.min_window-1]
        #except IndexError:
        #    pass
    
    #computes the Relative Strenght given the string of prices
    def RS(self):
        try:
            rs = D(self.average_gain() / self.average_loss())
            return rs    
        except:
            pass

    #finally, computes the RSI
    def RSI(self):
        try:
            rsi =  D(100 - (100/(1+self.RS())))
            return rsi
        except:
            pass
    
    def calculate_signals(self, event):
        if len(self.prices) > self.min_window:
            print(self.average_gain())
            print(self.average_loss())
                #print("meangains" + str(self.meangains))
                #print("meanlosses" + str(self.meanlosses))
            print(self.RSI())

        '''
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                side = random.choice(["buy", "sell"])
                order = OrderEvent(
                    self.instrument, self.units, "market", side
                )
                self.events.put(order)
        '''
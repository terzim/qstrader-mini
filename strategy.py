import random
import decimal

from event import OrderEvent
from statistics import mean

D = decimal.Decimal

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

#define automonously a new strategy, called RSI

class RSIStrategy(object):
    def __init__(self, instrument, units, events, min_window = 40, rsilowboundary = 20, rsiupboundary = 80):
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
        self.rsilist = []

    #append a price list to the RSI class. The price list
    #is formed with the avergae of "bid" and "ask" prices of every
    #tick event
    #TODO: redefine the price list with an autonomous data handler class
    def pricelist(self,event):
        if event.type == 'TICK':
            self.ticks += 1
            self.prices.append(D((event.bid+event.ask)/2))
        return self.prices

    #computes the average gain given the string of midprices
    #the first average gain is calculate with a simple average
    #the future average gains are rolling to smooth the RSI
    #TODO: clean some mess with indexation
    def average_gain(self):
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) <= 0:
                self.gains.append(D(0))
            else:
                self.gains.append(D(self.prices[x] - self.prices[x-1]))
        
        if len(self.prices) == (self.min_window + 1):
            meangain = D(mean(self.gains))
            self.meangains.append(meangain)
            return self.meangains[len(self.prices)-self.min_window-1]
        
        elif len(self.prices) > (self.min_window + 1):
            meangain = D(((self.meangains[len(self.prices)-self.min_window-2]*(self.min_window-1)) + self.gains[len(self.prices)-2])/(self.min_window))
            self.meangains.append(meangain)
            return self.meangains[len(self.prices)-self.min_window-1]

    #computes the average loss given the string of midprices.
    #works the same as for the average gains
    def average_loss(self):
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) >= 0:
                self.losses.append(D(0))
            else:
                self.losses.append(D(self.prices[x-1] - self.prices[x]))
        
        if len(self.prices) == (self.min_window + 1):
            meanloss = D(mean(self.losses))
            self.meanlosses.append(meanloss)
            return self.meanlosses[len(self.prices)-self.min_window-1]

        elif len(self.prices) > (self.min_window + 1):
            meanloss = D(((self.meanlosses[len(self.prices)-self.min_window-2]*(self.min_window-1)) + self.losses[len(self.prices)-2])/(self.min_window))
            self.meanlosses.append(meanloss)
            return self.meanlosses[len(self.prices)-self.min_window-1]
    
    #computes the Relative Strenght given the string of prices
    def RS(self):
        rs = D(self.average_gain() / self.average_loss())
        return rs    

    #finally, computes the RSI
    def RSI(self):
        rsi =  D(100 - (100/(1+self.RS())))
        self.rsilist.append(rsi)
        return rsi
    
    def print_signals(self,event):
        if len(self.prices) >= (self.min_window + 1):
            self.average_gain()
            self.average_loss
            self.RSI()
            print(meangains[-1])
            print(meanlosses[-1])
            print(rsilist[-1])        

    #TODO: this will provide the conditions under which the RSI will execute the order
    def calculate_signals(self, event):
        if len(self.rsilist) > self.min_window:
            halfminwin = int(self.min_window/2)
            quarterminwin = int(halfminwin/2)
            lastrsiwindow = self.rsilist[-halfminwin:]
            if all(x > self.rsiupboundary for x in lastrsiwindow[0:quarterminwin]):
                if all(x < self.rsiupboundary for x in lastrsiwindow[-quarterminwin:]):
                    order = OrderEvent(self.instrument, self.units, "market", "sell")
                    self.events.put(order)
            elif all(x < self.rsilowboundary for x in lastrsiwindow[0:quarterminwin]):
                if all(x > self.rsilowboundary for x in lastrsiwindow[-quarterminwin:]):
                    order = OrderEvent(self.instrument, self.units, "market", "buy")
                    self.events.put(order)
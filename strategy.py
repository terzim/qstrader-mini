import random
import decimal

from event import OrderEvent
from statistics import mean

D = decimal.Decimal

class Strategy:
    pass

class TestRandomStrategy(Strategy):
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

class RSIStrategy(Strategy):
    def __init__(self, instrument, units, events, min_window = 40, persistence = 3, rsilowboundary = 20, rsiupboundary = 80):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.min_window = min_window
        self.persistence = persistence
        self.rsilowboundary = rsilowboundary
        self.rsiupboundary = rsiupboundary
        self.ticks = 0
        self.prices = []
        self.gains = []
        self.meangains = []
        self.losses = []
        self.meanlosses = []
        self.rsilist = []

    #append a price list to the RSI class. The price list
    #is formed with the average of "bid" and "ask" prices of every
    #tick event
    #also creates list of losses and gains
    #TODO: redefine the price list with an autonomous data handler class
    def pricelist(self,event):
        if event.type == 'TICK':
            self.ticks += 1
            self.prices.append(D((event.bid+event.ask)/2))
            #return self.prices

    def gainsandlosses(self,event):
        if len(self.prices) >= 2:
            if (self.prices[-1] - self.prices[-2]) <= 0:
                self.gains.append(D(0))
                self.losses.append(D(self.prices[-2] - self.prices[-1]))
            else:
                self.gains.append(D(self.prices[-1] - self.prices[-2]))
                self.losses.append(D(0))

    #computes the average gain given the string of midprices
    #the first average gain is calculate with a simple average
    #the future average gains are rolling to smooth the RSI
    def average_gain(self):
        if len(self.prices) == (self.min_window + 1):
            meangain = D(mean(self.gains))
            self.meangains.append(meangain)
            return self.meangains[-1]
        
        elif len(self.prices) > (self.min_window + 1):
            meangain = D(((self.meangains[-1]*(self.min_window-1)) + self.gains[-1])/(self.min_window))
            self.meangains.append(meangain)
            return self.meangains[-1]

    #computes the average loss given the string of midprices.
    #works the same as for the average gains
    def average_loss(self):
        if len(self.prices) == (self.min_window + 1):
            meanloss = D(mean(self.losses))
            self.meanlosses.append(meanloss)
            return self.meanlosses[-1]

        elif len(self.prices) > (self.min_window + 1):
            meanloss = D(((self.meanlosses[-1]*(self.min_window-1)) + self.losses[-1])/(self.min_window))
            self.meanlosses.append(meanloss)
            return self.meanlosses[-1]
    
    #computes the RSI
    def RSI(self):
        rsi =  D(100 - (100/(1+(self.average_gain() / self.average_loss()))))
        self.rsilist.append(rsi)        
        return rsi    
    
    def print_signals(self,event):
        if len(self.prices) >= (self.min_window + 1):
            self.RSI()
            print("Last 5 gains " + ', '.join(map(str, self.gains[-5:])))
            print("Last 5 losses " + ', '.join(map(str, self.losses[-5:])))
            #print("Last 5 meangains " + ', '.join(map(str, self.meangains[-5:])))
            #print("Last 5 meanlosses " + ', '.join(map(str, self.meanlosses[-5:])))
            print("Last 5 RSIs " + ', '.join(map(str, self.rsilist[-5:])))

    #TODO: this will provide the conditions under which the RSI will execute the order
    def calculate_signals(self, event):
        if len(self.rsilist)>10:
            ordertype = "market"
            orderdirection = ["sell","buy"]
            #len(self.rsilist) > self.min_window:
            #halfminwin = int(self.min_window/2)
            #quarterminwin = int(halfminwin/2)
            #lastrsiwindow = self.rsilist[-halfminwin:]
            pers = int(self.persistence)
            if all(x > self.rsiupboundary for x in self.rsilist[-pers:]):
                order = OrderEvent(self.instrument, self.units, ordertype, orderdirection[0])
                self.events.put(order)
            elif all(x < self.rsilowboundary for x in self.rsilist[-pers:]):
                order = OrderEvent(self.instrument, self.units, ordertype, orderdirection[1])
                self.events.put(order)
            else:
                pass
        else:
            pass
import random

from event import OrderEvent
from statistics import mean


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
    def __init__(self, instrument, units, events, min_window = 200):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.min_window = min_window
        self.ticks = 0
        self.prices = []

    def pricelist(self,event):
        if event.type == 'TICK':
            self.ticks += 1
            self.prices.append(event.bid)
        return self.prices

    def average_gain(self):
        gains = []
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) < 0:
                gains.append(0)
            else:
                gains.append(self.prices[x] - self.prices[x-1])
        meangain = mean(gains)
        return meangain

    #computes the average loss given the string of prices
    def average_loss(self):
        losses = []
        for x in range(1,len(self.prices)):
            if (self.prices[x] - self.prices[x-1]) > 0:
                losses.append(0)
            else:
                losses.append(self.prices[x-1] - self.prices[x])
        meanloss = mean(losses)
        return meanloss

    #computes the Relative Strenght given the string of prices
    def RS(self):
        rs = self.average_gain() / self.average_loss()
        return rs 

    #finally, computes the RSI
    def RSI(self):
        rsi =  100 - (100/(1+self.RS()))
        return rsi

    def calculate_signals(self, event):
        if len(self.prices) > 20:
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
#-*- coding:utf-8 -*-

import threading
from FinalLogger import logger
from Strategy import Strategy

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct

class StrategyFairyFour(threading.Thread, Strategy):
    def __init__(self, tick):
        Strategy.__init__(self, tick)
        threading.Thread.__init__(self)

    def run(self):
        Strategy.strategy_state[self.tick.InstrumentID] = True

        daybar_list = self.getDayBarList()
        if not daybar_list:
            print 'Need one bar at least in database'
            return

        last_daybar = daybar_list[-1]
        #open, high, low, close, volume
        last_high = last_daybar[1]
        last_low = last_daybar[2]

        b_sendorder, s_sendorder = self.getSendOrderCount()

        if self.tick.LastPrice > last_high :
            if s_sendorder > 1 :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Close, 1, self.tick.UpperLimitPrice) # LastPrice
            elif b_sendorder < 1 :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, 1, self.tick.UpperLimitPrice)

        if self.tick.LastPrice < last_low :
            if b_sendorder > 1:
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Close, 1, self.tick.UpperLimitPrice)  # LastPrice
            elif s_sendorder < 1 :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, 1, self.tick.LowerLimitPrice)

        Strategy.strategy_state[self.tick.InstrumentID] = False

    def PrepareOrder(self, inst, direc, open_close, volume, price):
        order = self.formatOrder(inst, direc, open_close, volume, price)
        self.sendOrder(order)
















#-*- coding:utf-8 -*-

import threading
from FinalLogger import logger
from Strategy import Strategy

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct

class StrategyRBreaker(threading.Thread, Strategy):
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
        last_high, last_low, last_close = last_daybar[1:4]

        b_sendorder, s_sendorder = self.getSendOrderCount()
        holding = b_sendorder - s_sendorder
        # Bbreak > Ssetup > Senter >> Benter > Bsetup > Sbreak
        k = 0.2
        tr = last_high - last_low
        (Bbreak, Ssetup, Senter, Benter, Bsetup, Sbreak) = (last_close+3*k*tr, last_close+2*k*tr, last_close+1*k*tr, last_close-1*k*tr, last_close-2*k*tr, last_close-3*k*tr)

        if holding == 0 and self.tick.LastPrice > Bbreak :
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, 1, self.tick.UpperLimitPrice)
        if holding == 0 and self.tick.LastPrice < Sbreak:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, 1, self.tick.UpperLimitPrice)
        if holding > 0 and self.tick.LastPrice < Senter and self.tick.HighestPrice > Ssetup:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Close, 1, self.tick.UpperLimitPrice)
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, 1, self.tick.UpperLimitPrice)
        if holding < 0 and self.tick.LastPrice > Benter and self.tick.LowestPrice < Bsetup:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Close, 1, self.tick.LowerLimitPrice)
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, 1, self.tick.LowerLimitPrice)

        Strategy.strategy_state[self.tick.InstrumentID] = False

    def PrepareOrder(self, inst, direc, open_close, volume, price):
        order = self.formatOrder(inst, direc, open_close, volume, price)
        self.sendOrder(order)
















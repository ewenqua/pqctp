#-*- coding:utf-8 -*-

import threading
from FinalLogger import logger
from Strategy import Strategy
from Indicators import Indicators

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct

class StrategyRBreaker(threading.Thread, Strategy):
    def __init__(self, inst, volume = 1):
        Strategy.__init__(self, inst)
        threading.Thread.__init__(self)
        self.volume = volume
        self.InitIndicator()

    def InitIndicator(self):
        pass # no need to calculate indicator in this strategy

    def run(self):
        Strategy.strategy_state[self.tick.InstrumentID] = True
        daybar_list = Indicators.getDayBarList(self.tick.InstrumentID)
        if not daybar_list:
            print 'Need one bar at least in database'
            threading.Thread.__init__(self)
            Strategy.strategy_state[self.tick.InstrumentID] = False
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
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, self.volume, self.tick.UpperLimitPrice)
        if holding == 0 and self.tick.LastPrice < Sbreak:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, self.volume, self.tick.UpperLimitPrice)
        if holding > 0 and self.tick.LastPrice < Senter and self.tick.HighestPrice > Ssetup:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Close, self.volume, self.tick.UpperLimitPrice)
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, self.volume, self.tick.UpperLimitPrice)
        if holding < 0 and self.tick.LastPrice > Benter and self.tick.LowestPrice < Bsetup:
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Close, self.volume, self.tick.LowerLimitPrice)
            self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, self.volume, self.tick.LowerLimitPrice)

        # in case restart/reuse thread since python not support
        threading.Thread.__init__(self)
        Strategy.strategy_state[self.tick.InstrumentID] = False

    def PrepareOrder(self, inst, direc, open_close, volume, price):
        order = self.formatOrder(inst, direc, open_close, volume, price)
        self.sendOrder(order)
















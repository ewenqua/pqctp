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


class StrategyDoubleMA(threading.Thread, Strategy):
    def __init__(self, inst, fast = 7, slow = 25, volume = 1):
        Strategy.__init__(self, inst)
        threading.Thread.__init__(self)
        self.fast = fast
        self.slow = slow
        self.volume = volume
        self.InitIndicator()

    def InitIndicator(self):
        self.fast_MA = Indicators.getMA(self.inst, self.fast)
        self.slow_MA = Indicators.getMA(self.inst, self.slow)

    def run(self):
        Strategy.strategy_state[self.tick.InstrumentID] = True
        daybar_list = Indicators.getDayBarList(self.tick.InstrumentID)
        if len(daybar_list) < self.slow or self.slow_MA is None:
            print 'Need %d bars at least in database' % self.slow
            threading.Thread.__init__(self)
            Strategy.strategy_state[self.tick.InstrumentID] = False
            return

        #print 'self.slow_MA = ' + str(self.slow_MA)
        #atr = Indicators.getATR(self.tick.InstrumentID)
        #print 'self.atr = ' + str(atr)
        #hhv = Indicators.HHV(self.tick.InstrumentID, 20)
        #print 'the hhv = %d, index = %d ' %  hhv
        #llv = Indicators.LLV(self.tick.InstrumentID, 20)
        #print 'the llv = %d, index = %d ' %  llv

        b_sendorder, s_sendorder = self.getSendOrderCount()

        #if self.fast_MA[-1] > self.slow_MA[-1] and self.fast_MA[-2] < self.slow_MA[-2]:
        if self.fast_MA[-1] > self.slow_MA[-1]:
            if s_sendorder > 0 :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Close, s_sendorder, self.tick.UpperLimitPrice) # LastPrice
            elif b_sendorder < self.volume :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Buy, ApiStruct.OF_Open, self.volume-b_sendorder, self.tick.UpperLimitPrice)

        #if self.fast_MA[-1] < self.slow_MA[-1] and self.fast_MA[-2] > self.slow_MA[-2]:
        if self.fast_MA[-1] < self.slow_MA[-1]:
            if b_sendorder > 0:
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Close, s_sendorder, self.tick.UpperLimitPrice)  # LastPrice
            elif s_sendorder < self.volume :
                self.PrepareOrder(self.tick.InstrumentID, ApiStruct.D_Sell, ApiStruct.OF_Open, self.volume-s_sendorder, self.tick.LowerLimitPrice)

        # in case restart/reuse thread is not supported by python
        threading.Thread.__init__(self)
        Strategy.strategy_state[self.tick.InstrumentID] = False

    def PrepareOrder(self, inst, direc, open_close, volume, price):
        order = self.formatOrder(inst, direc, open_close, volume, price)
        self.sendOrder(order)
















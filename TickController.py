#-*- coding:utf-8 -*-

import threading
import time
from datetime import datetime
from copy import deepcopy
import os
from Strategy import Strategy
from StrategyRBreaker import StrategyRBreaker
from StrategyFairyFour import StrategyFairyFour
from FinalLogger import logger
from DatabaseController import DatabaseController
from Constant import inst_strategy, TICK_DIR

class TickController():
    inst_current_tick = {}

    def __init__(self):
        pass

    @staticmethod
    def selectStrategy(tick):
        strategy = None
        if inst_strategy[tick.InstrumentID] == 'StrategyRBreaker':
            strategy = StrategyRBreaker(tick)
        elif inst_strategy[tick.InstrumentID] == 'StrategyFairyFour':
            # add more strategy
            strategy = StrategyFairyFour(tick)
        else:
            print 'The strategy is not found! '

        return strategy

    @staticmethod
    def processTick(t):
        # important !!! otherwise use the same reference
        tick = deepcopy(t)

        if not Strategy.strategy_state.has_key(tick.InstrumentID) :
            Strategy.strategy_state[tick.InstrumentID] = False

        if Strategy.strategy_state[tick.InstrumentID] == False :
            strategy = TickController.selectStrategy(tick)
            strategy.start()
            #strategy.join()

        TickController.inst_current_tick[tick.InstrumentID] = tick
        TickController.saveTick(tick)

    @staticmethod
    def makeTickFilename(inst):
        today = time.strftime('%Y%m%d')
        if not os.path.exists(TICK_DIR+ inst):
            os.makedirs(TICK_DIR+ inst)
        return '%s%s/%s_tick.%s' % (TICK_DIR, inst, today, 'txt')

    @staticmethod
    def saveTick(tick):
        f = open(TickController.makeTickFilename(tick.InstrumentID), 'a+')
        try:
            f.write('%s,%.2f,%d,%s\n' % (datetime.now(), tick.LastPrice, tick.Volume, tick.InstrumentID))
        except Exception, e:
            print e
        f.close()

    @staticmethod
    def saveDayBar():
        for inst in TickController.inst_current_tick.keys() :
            tick = TickController.inst_current_tick[inst]
            DatabaseController.insert_DayBar(tick)












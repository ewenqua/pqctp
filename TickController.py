#-*- coding:utf-8 -*-

import time
from datetime import datetime
from copy import deepcopy
import os
from Strategy import Strategy
from FinalLogger import logger
from DatabaseController import DatabaseController
from Constant import TICK_DIR, inst_thread

class TickController():
    inst_current_tick = {}

    def __init__(self):
        pass

    @staticmethod
    def processTick(t):
        # important !!! otherwise use the same reference
        tick = deepcopy(t)

        if not Strategy.strategy_state.has_key(tick.InstrumentID) :
            Strategy.strategy_state[tick.InstrumentID] = False

        if Strategy.strategy_state[tick.InstrumentID] == False :
            strategy = inst_thread[tick.InstrumentID]
            strategy.setTick(tick)
            try:
                strategy.start()
            except Exception, e:
                print 'Ignore:', e
        #save ticks of every inst
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
            #update all indicators!!!
            inst_thread[inst].InitIndicator()












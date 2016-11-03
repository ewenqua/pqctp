#-*- coding:utf-8 -*-

from FinalLogger import logger
from Constant import OPEN,CLOSE,HIGH,LOW,database_map,suffix_list


class Indicators():
    @staticmethod
    def getMA(inst, period, price_type = CLOSE):
        daybar_list = Indicators.getDayBarList(inst)

        if len(daybar_list)-period <= 0:
            print 'period should be less than day bar count'
            return
        ma = []
        for i in range(len(daybar_list)-period+1):
            bars = daybar_list[i:period+i]
            sum = 0
            for b in bars:
                sum += b[price_type]
            ma.append(sum/period)
        return ma

    @staticmethod
    def getATR(inst, period = 26): # don't need price type
        daybar_list = Indicators.getDayBarList(inst)

        if len(daybar_list)-period <= 0:
            print 'period should be less than day bar count'
            return
        atr = []
        for i in range(len(daybar_list)-period+1):
            bars = daybar_list[i:period+i]
            sum = 0
            for j in range(len(bars)):
                tr = (bars[j][HIGH]-bars[j][LOW])
                if i > 0 :
                    tr = max((bars[j][HIGH]-bars[j][LOW]),abs(daybar_list[i+j-1][CLOSE]-bars[j][HIGH]),abs(daybar_list[i+j-1][CLOSE]-bars[j][LOW]))
                sum += tr
            atr.append(sum/period)
        return atr

    @staticmethod
    def HHV(inst, period, price_type = HIGH):
        daybar_list = Indicators.getDayBarList(inst)

        if len(daybar_list)-period <= 0:
            print 'period should be less than day bar count'
            return

        bars = daybar_list[len(daybar_list)-period:len(daybar_list)]
        highest = bars[0][HIGH]
        index = -period
        for i in range(len(bars)):
            if bars[i][HIGH] > highest:
                highest = bars[i][HIGH]
                index = i - period
        return highest,index

    @staticmethod
    def LLV(inst, period, price_type = LOW):
        daybar_list = Indicators.getDayBarList(inst)

        if len(daybar_list)-period <= 0:
            print 'period should be less than day bar count'
            return

        bars = daybar_list[len(daybar_list)-period:len(daybar_list)]
        lowest = bars[0][LOW]
        index = -period
        for i in range(len(bars)):
            if bars[i][LOW] < lowest:
                lowest = bars[i][LOW]
                index = i - period
        return lowest,index

    @staticmethod
    def getDayBarList(inst):
        return database_map[inst][suffix_list.index('_DayBar')]







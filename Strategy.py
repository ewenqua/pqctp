#-*- coding:utf-8 -*-

import threading
import time
from FinalLogger import logger
from DatabaseController import DatabaseController
from Constant import database_map, suffix_list

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct

mutex = threading.Lock()

class Strategy():
    traderSpi = None #TraderDelegate()
    strategy_state = {}

    def __init__(self, inst):
        self.inst = inst

    def setTick(self, tick):
        self.tick = tick

    def InitIndicator(self):
        raise Exception('Implement Exception','InitInitcator should be implement for customized strategy!')

    @staticmethod
    def setTraderSpi(spi):
        Strategy.traderSpi = spi

    def sendOrder(self, order):
        global mutex
        mutex.acquire()

        Strategy.traderSpi.ReqOrderInsert(order, Strategy.traderSpi.inc_request_id())
        DatabaseController.insert_SendOrder(order)

        print 'sendOrder = ' + order.InstrumentID + ' dir = ' + order.Direction + ' strategy = ' + self.__module__
        time.sleep(1)
        mutex.release()

    def formatOrder(self, inst, direc, open_close, volume, price):
        return ApiStruct.InputOrder(
            InstrumentID=inst,
            Direction=direc, # ApiStruct.D_Buy or ApiStruct.D_Sell
            OrderRef=str(Strategy.traderSpi.inc_request_id()),
            LimitPrice=price,
            VolumeTotalOriginal=volume,
            OrderPriceType=ApiStruct.OPT_LimitPrice,

            BrokerID=Strategy.traderSpi.broker_id,
            InvestorID=Strategy.traderSpi.investor_id,
            CombOffsetFlag=open_close, # OF_Open, OF_Close, OF_CloseToday
            CombHedgeFlag=ApiStruct.HF_Speculation,

            VolumeCondition=ApiStruct.VC_AV,
            MinVolume=1,
            ForceCloseReason=ApiStruct.FCC_NotForceClose,
            IsAutoSuspend=1,
            UserForceClose=0,
            TimeCondition=ApiStruct.TC_GFD,
        )

    def getSendOrderCount(self):
        sendorder_list = database_map[self.tick.InstrumentID][suffix_list.index('_SendOrder')]
        pos_buy, pos_sell = (0, 0)
        for sendorder in sendorder_list :
            if sendorder[1] == ApiStruct.D_Buy and sendorder[2] == ApiStruct.OF_Open :
                pos_buy += sendorder[4]
            if sendorder[1] == ApiStruct.D_Sell and sendorder[2] == ApiStruct.OF_Open:
                pos_sell += sendorder[4]
            if sendorder[1] == ApiStruct.D_Sell and sendorder[2] == ApiStruct.OF_Close:
                pos_buy -= sendorder[4]
            if sendorder[1] == ApiStruct.D_Buy and sendorder[2] == ApiStruct.OF_Close:
                pos_sell -= sendorder[4]
        return pos_buy, pos_sell






#-*- coding=utf-8 -*-

import time
from TickController import TickController
from FinalLogger import logger

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct, MdApi
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct, MdApi

class MdDelegate(MdApi):
    def __init__(self, instruments, broker_id, investor_id, passwd, *args,**kwargs):
        self.requestid=0
        self.instruments = instruments
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd

    def OnRspError(self, info, RequestId, IsLast):
        self.isErrorRspInfo(info)

    def isErrorRspInfo(self, info):
        if info.ErrorID !=0:
            logger.info('ErrorID=%d, ErrorMsg=%s' % info.ErrorID % info.ErrorMsg.decode('gbk'))
        return info.ErrorID !=0

    def OnFrontDisConnected(self, reason):
        logger.info('onFrontDisConnected, reason = %d' % reason)

    def OnHeartBeatWarning(self, time):
        logger.info('OnHeartBeatWarning, time = %s' % time)

    def OnFrontConnected(self):
        logger.info('OnFrontConnected')
        req = ApiStruct.ReqUserLogin(BrokerID=self.broker_id, UserID=self.investor_id, Password=self.passwd)
        self.requestid+=1
        r=self.ReqUserLogin(req, self.requestid)

    def OnRspUserLogin(self, userlogin, info, rid, is_last):
        if is_last and not self.isErrorRspInfo(info):
            self.SubscribeMarketData(self.instruments)

    def OnRtnDepthMarketData(self, DepthMarketData):
        TickController.processTick(DepthMarketData)

if __name__=="__main__":
    pass

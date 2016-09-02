#-*- coding=utf-8 -*-
from FinalLogger import logger
from DatabaseController import DatabaseController

import sys
if sys.platform == 'win32':
    from ctp_win32 import ApiStruct, TraderApi
elif sys.platform == 'linux2' :
    from ctp_linux64 import ApiStruct, TraderApi

class TraderDelegate(TraderApi):
    def __init__(self, broker_id='', investor_id='', passwd='', *args,**kwargs):
        self.requestid=0
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd

    def OnRspError(self, info, RequestId, IsLast):
        self.isErrorRspInfo(info)

    def isErrorRspInfo(self, info):
        if info.ErrorID !=0:
            logger.info('ErrorID=%d, ErrorMsg=%s' % (info.ErrorID, info.ErrorMsg.decode('gbk')))
        return info.ErrorID !=0

    def OnFrontDisConnected(self, reason):
        logger.info('onFrontDisConnected, reason = %d' % reason)

    def OnHeartBeatWarning(self, time):
        logger.info('OnHeartBeatWarning, time = %s' % time)

    def OnFrontConnected(self):
        logger.info('OnFrontConnected')
        req = ApiStruct.ReqUserLogin(BrokerID=self.broker_id, UserID=self.investor_id, Password=self.passwd)
        self.ReqUserLogin(req, self.inc_request_id())

    def OnRspUserLogin(self, userlogin, info, rid, is_last):
        if is_last and not self.isErrorRspInfo(info):
            logger.info('OnRspUserLogin %s' % is_last)
            req = ApiStruct.SettlementInfoConfirm(BrokerID=self.broker_id, InvestorID=self.investor_id)
            self.ReqSettlementInfoConfirm(req, self.inc_request_id())

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        if bIsLast and not self.isErrorRspInfo(pRspInfo):
            logger.info('OnRspOrderInsert %s' % pInputOrder.InstrumentID)

    def OnRtnTrade(self, pTrade):
        logger.info('OnRtnTrade %s' % str(pTrade))
        DatabaseController.insert_RtnOrder(pTrade)

    def inc_request_id(self):
        self.requestid += 1
        return self.requestid

if __name__=="__main__":
    pass
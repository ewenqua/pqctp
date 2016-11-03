#-*- coding=utf-8 -*-
#one inst -> one strategy/thread, and customized indicators
inst_strategy = {'cs1701': {'strategy':'StrategyRBreaker', 'volume':3},
                 'p1701': {'strategy':'StrategyFairyFour'},
                 'rb1701' : {'strategy':'StrategyDoubleMA', 'fast':7,'slow':30, 'volume':2},
                 }
#{'p1701', strategy_thread}
inst_thread = {}

# {'inst', [DayBar, SendOrder, RtnOrder]}
#             |_____[ bar1, bar2, bar3, ...]
#                      |_____(open, high, low, close, ...)
database_map = {}
suffix_list = ['_DayBar', '_SendOrder', '_RtnOrder']

BROKER_ID = "2071"
INVESTOR_ID = "60800130"
PASSWORD = "888888"
ADDR_MD = "tcp://180.169.112.50:41213"
#ADDR_MD = "tcp://front111.ctp.gtjafutures.com:41213"
ADDR_TRADE = "tcp://fz101.ctp.gtjafutures.com:41205"

TICK_DIR = './ticks/'
LOGS_DIR = './logs/'

OPEN,HIGH,LOW,CLOSE = range(4)





#-*- coding=utf-8 -*-

inst_strategy = {'cs1701': 'StrategyRBreaker', 'p1701': 'StrategyFairyFour', 'rb1701' : 'StrategyFairyFour'}

# {'inst', [DayBar, SendOrder, RtnOrder]}
#             |_____[ bar1, bar2, bar3, ...]
#                      |_____(open, high, low, close, ...)
database_map = {}
suffix_list = ['_DayBar', '_SendOrder', '_RtnOrder']

BROKER_ID = "2071"
INVESTOR_ID = "60800130"
PASSWORD = "888888"
#ADDR_MD = "tcp://fz101.ctp.gtjafutures.com:41213"
ADDR_MD = "tcp://front111.ctp.gtjafutures.com:41213"
ADDR_TRADE = "tcp://fz101.ctp.gtjafutures.com:41205"

TICK_DIR = './ticks/'
LOGS_DIR = './logs/'







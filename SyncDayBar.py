#-*- coding=utf-8 -*-
from FinalLogger import logger
from Constant import inst_strategy, suffix_list
import urllib
import json
import sqlite3

conn = sqlite3.connect('futures.db3', check_same_thread = False)
for i in inst_strategy.keys() :
    daybar_table = i + suffix_list[0]
    cmd = "DROP TABLE IF EXISTS " + daybar_table
    conn.execute(cmd)

    cmd = "CREATE TABLE IF NOT EXISTS " + daybar_table \
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, open DOUBLE NULL, high DOUBLE NULL, low DOUBLE NULL, close DOUBLE NULL, volume INTEGER NULL, TradingDay TEXT NULL, time TEXT NULL)"
    conn.execute(cmd)

if __name__=="__main__":
    # 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M1701'
    base_url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol='
    for symbol in inst_strategy.keys():
        url = base_url + symbol
        print 'url = ' + url
        results = json.load(urllib.urlopen(url))

        for r in results:
            # r -- ["2016-09-05","2896.000","2916.000","2861.000","2870.000","1677366"]  open, high, low, close
            conn.execute(
                "INSERT INTO %s (inst, open, high, low, close, volume, TradingDay,time) VALUES ('%s', %f, %f, %f, %f, %d, '%s','%s')"
                % (symbol + suffix_list[0], symbol, float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5]), r[0], '15:00:00'))
            conn.commit()

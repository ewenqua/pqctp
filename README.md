# pqctp
=====
python quant CTP

QQ交流群：273182530

用法
=====
环境：Windows 7 32位，或Linux 64位，python 2.7；其它环境可能有问题
库文件和源文件在一起，可以直接使用

运行：pqctp目录下，
执行 python SyncDayBar.py  #下载补全日K线
完成后，
执行 python main.py

功能：实现2个简单策略，只测试过模拟盘，实盘前需要仔细测试！


参考来源
=====

https://github.com/lovelylain/pyctp
-----
参考python库和python部分相关实现

https://github.com/zaviichen/pheux
-----
参考ctp接口的使用

注意
=====
如果自行编译库文件，python setup.py build

win32下:
-----
error: Unable to find vcvarsall.bat
-- 如果你安装的是 vc 2012版 SET VS90COMNTOOLS=%VS110COMNTOOLS%
-- 如果你安装的是 vc 2013版 SET VS90COMNTOOLS=%VS120COMNTOOLS%
linux64下：
-----
可能需要安装g++ 和 python-dev

# pqctp
=====
python quant CTP
qq交流群:273182530

用法
=====
环境：Windows 7 32位，或Linux 64位，python 2.7；其它环境可能有问题
库文件和源文件在一起，可以直接使用

运行：pqctp目录下，执行 python main.py

功能：实现2个简单策略，只测试过模拟盘，实盘还需要仔细打磨！


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
win32下执行:
error: Unable to find vcvarsall.bat

   如果你安装的是 2012 版 SET VS90COMNTOOLS=%VS110COMNTOOLS%
   如果你安装的是 2013版 SET VS90COMNTOOLS=%VS120COMNTOOLS%

linux64下：
可能需要安装g++ 和 python-dev

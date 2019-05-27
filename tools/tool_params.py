# -*- coding:utf-8  -*-
import logging
import os
import sys

LINUX = "linux"
WINDOWS = "windows"
SYSTEM = LINUX if sys.platform.startswith("linux") else WINDOWS  # 获取当前操作系统类型
ENCODING = 'utf-8'  # 字符编码默认即可
NONSENSE_ZERO = 0  # 无特殊意义 判断用
NONSENSE_ONE = 1  # 无特殊意义判断用
DEBUG = logging.DEBUG  # 默认参数 无需更改
INFO = logging.INFO  # 默认参数 无需更改
WARNING = logging.WARNING  # 默认参数 无需更改
ERROR = logging.ERROR  # 默认参数 无需更改
CRITICAL = logging.CRITICAL  # 默认参数 无需更改
TIMEOUT = 300  # ssh连接的超时时间
WAITTIME = 40  # adb reboot的等待时间 最好不要小于35秒
INTERVAL = 15  # 各项测试准备工作中的等待时间 可以适当改小 不推荐更改
COLD_WAIT_TIME = 120  # 切断电源后的等待时间
BOARD_LOG_DETAIL = {'ip': '10.239.50.17', 'port': 22, 'user': 'root', 'pwd': 'Intel@123'}  # 板子的ssh信息
HOST_LOG_DETAIL = {'ip': '10.239.50.119', 'port': 22, 'user': 'root', 'pwd': 'zhangxinhuicf'}  # 当前登录ubuntu主机ssh信息
ERROR_MSG = "CONNECTION FAILED,SOS_SHUTDONW"  # coldBoot重启后如果ubuntu ssh连接中断的报错提示
# DEVICE_ID = "R1J56Lacfb9436"  # 安卓的编号 adb devices可以查看
DEVICE_ID = "R1J56L20fb952c"  # 安卓的编号 adb devices可以查看
# 交互脚本路径如果在UBUNTU下执行默认即可,WINDOWS需要把scripts文件夹复制到UBUNTU的当前用户工作目录下
SCRIPTS_PATH = os.path.abspath('../scripts') if SYSTEM is LINUX else "/home/${USER}/scripts"


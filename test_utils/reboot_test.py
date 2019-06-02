# -*- coding:utf-8  -*-
from tools.ssh_connection import RemoteConn
from tools.tool_params import *
from tools.log import logger
import time
import re
import unittest
import os

# __author__ = 'zhangxinhuicf'
# __email__ = 'zhangxinhui'


class MyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def preparation(self, log_details=HOST_LOG_DETAIL, reeset=False):  # 不传reset是登录,传了True为reset ioc
        try:
            if os.system("ping -c 1 {}".format(log_details.get('ip'))) == 0:
                with RemoteConn(**log_details) as command_line:
                    if log_details is BOARD_LOG_DETAIL:
                            instance = command_line.command('acrnctl list')[1]
                            pattern = re.compile("There are no VMs")
                            need_create_instance = pattern.search(instance.read().decode(ENCODING))
                            empty_position = '{}{}{}{}{}{}{}'
                            cmd = empty_position.format('cp /usr/share/acrn/samples/apl-mrb/launch_uos.sh ~/;',
                                                        'acrnctl add ./launch_uos.sh -V 2;' if need_create_instance else 'whoami;',
                                                        'systemctl enable acrnd;',
                                                        'echo loop > /usr/lib/modules-load.d/loop.conf;',
                                                        'systemctl enable acrnlog;',
                                                        'crashlogctl enable;',
                                                        'sync;',
                                                        )
                            stdin, stdout, stderr = command_line.command(cmd)
                            error_msg, stdout_msg = stderr.read().decode(ENCODING), stdout.read().decode(ENCODING)
                            logger.info(stdout_msg) if stdout_msg else NONSENSE_ZERO
                            logger.error(error_msg) if error_msg else NONSENSE_ZERO
                    else:
                        logging_shell = "bash {}/reset.sh 1".format(SCRIPTS_PATH)
                        reset_shell = "bash {}/reset.sh".format(SCRIPTS_PATH)
                        shell_command = logging_shell if not reset else reset_shell
                        command_line.command(shell_command)

        except Exception as EXC:
            logger.error(EXC)
            if EXC == 'timed out':
                self.assertNotEqual(NONSENSE_ZERO, NONSENSE_ZERO, EXC)
            else:
                self.assertEqual(NONSENSE_ZERO, NONSENSE_ONE, EXC)

    def precondition(self):
        self.preparation(HOST_LOG_DETAIL, reset=True)
        time.sleep(INTERVAL)
        self.preparation(BOARD_LOG_DETAIL)
        self.preparation(HOST_LOG_DETAIL, reset=True)
        time.sleep(INTERVAL)

    def test_cold_boot(self):
        self.precondition()
        while True:
            with RemoteConn(**BOARD_LOG_DETAIL) as cmd_b:
                cmd_b.command("echo 8 8 8 8 > /proc/sys/kernel/printk")
            with RemoteConn(**HOST_LOG_DETAIL) as cmd_h:
                cmd_h.command("adb root;adb shell setprop power.sleepshutdown.cmd s5;")
                cmd_h.command("bash {}/restart_sos.sh".format(SCRIPTS_PATH))
                time.sleep(30)
                devices = cmd_h.command("adb devices")
                stdout, stderr = devices[1].read().decode(ENCODING), devices[2].read().decode(ENCODING)
                if stderr:
                    logger.error(stderr)
                logger.info(stdout)
                pattern = re.compile(DEVICE_ID)
                if not pattern.search(stdout):
                    try:
                        with RemoteConn(**BOARD_LOG_DETAIL) as cmd:
                            cmd.command("journalctl -b -1 -u acrnd.service >> journalctl.log")
                    except Exception as EXC:
                        logger.error(ERROR_MSG)
                        logger.error(EXC)
                    break

    def _test_warm_boot(self):
        self.precondition()
        with RemoteConn(**BOARD_LOG_DETAIL) as cmd_b:
            with RemoteConn(**HOST_LOG_DETAIL) as cmd_h:
                while True:
                    cmd_b.cQommand("echo 8 8 8 8 > /proc/sys/kernel/printk")
                    cmd_h.command("adb root;adb reboot;")
                    time.sleep(WAITTIME)
                    devices = cmd_h.command("adb devices")
                    stdout, stderr = devices[1].read().decode(ENCODING), devices[2].read().decode(ENCODING)
                    if stderr:
                        logger.error(stderr)
                    logger.info(stdout)
                    pattern = re.compile(DEVICE_ID)
                    if not pattern.search(stdout):
                        break

    def _test_s3_boot(self):
        self.precondition()
        while True:
            with RemoteConn(**BOARD_LOG_DETAIL) as cmd_b:
                cmd_b.command("echo 8 8 8 8 > /proc/sys/kernel/printk")
            with RemoteConn(**HOST_LOG_DETAIL) as cmd_h:
                cmd_h.command("adb root;adb shell setprop power.sleepshutdown.cmd s5;")
                cmd_h.command("bash {}/restart_sos.sh".format(SCRIPTS_PATH))
                time.sleep(30)
                devices = cmd_h.command("adb devices")
                stdout, stderr = devices[1].read().decode(ENCODING), devices[2].read().decode(ENCODING)
                if stderr:
                    logger.error(stderr)
                logger.info(stdout)
                pattern = re.compile(DEVICE_ID)
                if not pattern.search(stdout):
                    try:
                        with RemoteConn(**BOARD_LOG_DETAIL) as cmd:
                            cmd.command("journalctl -b -1 -u acrnd.service >> journalctl.log")
                    except Exception as EXC:
                        logger.error(ERROR_MSG)
                        logger.error(EXC)
                    break


if __name__ == '__main__':
    unittest.main()

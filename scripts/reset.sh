#!/bin/bash
if [ $# -gt 0 ]
then
	echo -e "r" > /dev/ttyUSB2
	sleep 6
	echo -e "n1\r" > /dev/ttyUSB2
	sleep 4
	echo -e "\r" > /dev/ttyUSB3
	echo -e "sos_console\r" > /dev/ttyUSB3
	sleep 4
	echo -e "root" > /dev/ttyUSB3
	sleep 4
	echo -e "intel-123" >/dev/ttyUSB3
	sleep 4
	echo -e "intel-123" >/dev/ttyUSB3
	sleep 4
	echo -e "root" > /dev/ttyUSB3
	sleep 4
	echo -e "intel-123" >/dev/ttyUSB3
	sleep 4
	echo -e "intel-123" >/dev/ttyUSB3
	sleep 4
	echo -e "root" > /dev/ttyUSB3
	sleep 4
	echo -e "intel-123" >/dev/ttyUSB3
else
	echo -e "r" > /dev/ttyUSB2
	sleep 6
	echo -e "n1\r" > /dev/ttyUSB2
	sleep 2
	echo -e "\r" > /dev/ttyUSB3
	echo -e "sos_console\r" > /dev/ttyUSB3
	sleep 4
fi

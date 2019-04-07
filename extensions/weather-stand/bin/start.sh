#!/bin/sh

cd "$(dirname "$0")"

# Shutdown as many services as possible
/etc/init.d/framework stop
/etc/init.d/powerd stop
/etc/init.d/phd stop
/etc/init.d/volumd stop
/etc/init.d/lipc-daemon stop
/etc/init.d/tmd stop
/etc/init.d/webreaderd stop
/etc/init.d/browserd stop
killall lipc-wait-event
/etc/init.d/pmond stop
/etc/init.d/cron stop
sleep 5

# Clean up display, show initialisation message
/usr/sbin/eips -c
/usr/sbin/eips -c
/usr/sbin/eips 11 18 'Kindle Weather Stand Project'
/usr/sbin/eips 15 19 'https://git.io/vDVgT'
/usr/sbin/eips 19 21 'Initialising...'

while true
do
    # Enable WiFi
    /usr/bin/lipc-set-prop com.lab126.cmd wirelessEnable 1
    sleep 30
    
    # Update weather
    ./weather-manager.sh
    
    # Disable WiFi, set wakeup alarm then back to sleep
    # Alarm is in seconds, so 3600 means it will wake it self up every hour
    /usr/bin/lipc-set-prop com.lab126.cmd wirelessEnable 0
    sleep 15
    echo "" > /sys/class/rtc/rtc1/wakealarm
    echo "+3600" > /sys/class/rtc/rtc1/wakealarm
    # Following line will put device into deep sleep until the alarm above is triggered
    echo mem > /sys/power/state
done

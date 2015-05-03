#!/bin/sh

# Adopted from https://github.com/mpetroff/kindle-weather-display
# First mntroot rw, then add following cronjob to /etc/crontab/root, then /etc/init.d/cron restart, finally mntroot ro
# 0 * * * * /bin/sh /mnt/us/weather-stand/update-weather.sh > /dev/null 2>&1
# BTW, I choose to put all files on USB drive instead of system partition. 

# Quit when detect a disable flag
if [ -e disable ]; then exit 0; fi

cd "$(dirname "$0")"

# Check battery capacity
BATTERY=`grep -o "[0-9]*" /sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity`
CURRENT=`cat /sys/devices/system/yoshi_battery/yoshi_battery0/battery_current`

if [ $BATTERY -le 10 ] && [ $CURRENT -le 0 ]; then
    if [ -e drained ]; then
        # If already drawn drained image, then just leave. 
        exit 0;
    else
        touch drained
        # If device just got low power, then draw drained image. 
        eips -c
        eips -c
        eips -g battery-drained.png
    fi
else
    # Delete previously added flag
    if [ -e drained ]; then rm -f drained; fi
    # Disable screensaver
    lipc-set-prop com.lab126.powerd preventScreenSaver 1
    # Get rid of old file first
    rm -f /tmp/crushed_weather.png
    # Enable Wi-Fi
    if [ -e wireless ]; then lipc-set-prop com.lab126.cmd wirelessEnable 1; fi
    # Loop test Internet connectivity
    INTERNETCOUNT=5
    while [ $INTERNETCOUNT -ne 0 ]; do
        ping -c 1 8.8.8.8
        PINGRESULT=$?
        if [ $PINGRESULT -eq 0 ]; then INTERNETCOUNT=1; fi
        INTERNETCOUNT=$(expr $INTERNETCOUNT - 1)
    done
    # Clear up the display
    eips -c
    eips -c
    if [ $PINGRESULT -eq 0 ]; then
        # Finally, let's get data and refresh
        if ./local/generate_png ; then
            eips -g /tmp/crushed_weather.png
        else
            eips -g weather-error.png
        fi
    else
        eips -g internet-error.png
    fi
    # Disable Wi-Fi
    if [ -e wireless ]; then lipc-set-prop com.lab126.cmd wirelessEnable 0; fi
fi
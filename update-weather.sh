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
	# Kill Kindle framework
	/etc/init.d/framework stop
    # Disable screensaver
    lipc-set-prop com.lab126.powerd preventScreenSaver 1
    # Get rid of old file first
    rm -f /tmp/crushed_weather.png
    # Clear up the display
    eips -c
    eips -c
	# Finally, let's get data and refresh
	if ./local/generate_png ; then
		eips -g /tmp/crushed_weather.png
	else
		eips -g weather-error.png
	fi
fi
#!/bin/sh

# Adopted from https://github.com/mpetroff/kindle-weather-display
# First mntroot rw, then add following cronjob to /etc/crontab/root, then /etc/init.d/cron restart, finally mntroot ro
# 0 * * * * /bin/sh /mnt/us/weather-stand/update-weather.sh > /dev/null 2>&1
# BTW, I choose to put all files on USB drive instead of system partition. 

# Please notice that from version 2.0 this script is no longer maintained. 

# Pushover userID and token. Leave empty if you are not using it. 
PO_TOKEN=""
PO_USER=""

# Function to kill all Kindle system services that useless
kill_kindle_system() {
    /etc/init.d/framework stop
    /etc/init.d/powerd stop
    /etc/init.d/cmd stop
    /etc/init.d/phd stop
    /etc/init.d/volumd stop
    /etc/init.d/lipc-daemon stop
    /etc/init.d/tmd stop
    /etc/init.d/webreaderd stop
    /etc/init.d/browserd stop
    killall lipc-wait-event
    /etc/init.d/pmond stop
    touch /tmp/weatherstand.killed
}

cd "$(dirname "$0")"

# Quit when detect a disable flag
if [ -e disable ]; then exit 0; fi

#Turn on Kindle if in sleep
lipc-set-prop com.lab126.powerd wakeUp 1

# Check battery capacity
BATTERY=`grep -o "[0-9]*" /sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity`
CURRENT=`cat /sys/devices/system/yoshi_battery/yoshi_battery0/battery_current`

if [ $BATTERY -le 10 ] && [ $CURRENT -le 0 ]; then
    if [ -e /tmp/weatherstand.drained ]; then
        # If already drawn drained image, then just leave. 
        exit 0;
    else
        touch /tmp/weatherstand.drained
        # If device just got low power, then draw drained image. 
        eips -c
        eips -c
        eips -g battery-drained.png
        # Send a push notification for battery low
        if [ ! -z $PO_TOKEN ] && [ ! -z $PO_USER ]; then
            RESULT=`cat /sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity`
            curl \
            -F "token=${PO_TOKEN}" \
            -F "user=${PO_USER}" \
            -F "message=Current battery level is ${RESULT}" \
            -F "title=Kindle is running out of power!" \
            -F "timestamp=$(date +%s)" \
            -F "priority=0" \
            "https://api.pushover.net/1/messages.json"
        fi
    fi
else
    # Delete previously added flag
    if [ -e /tmp/weatherstand.drained ]; then rm -f /tmp/weatherstand.drained; fi
    # Kill all useless system services
    if [ ! -e /tmp/weatherstand.killed ]; then kill_kindle_system; fi
    # Get rid of old file first
    rm -f /tmp/crushed_weather.png
    # Test network status
    ping -c 5 api.wunderground.com
    PINGSTATUS=$?
    if [ $PINGSTATUS -ne 0 ]; then
        # Clear up the display
        eips -c
        eips -c
        eips -g no-internet.png
        exit
    fi
    # Finally, let's get data and refresh
    if ./local/generate_png ; then
        # Clear up the display
        eips -c
        eips -c
        eips -g /tmp/crushed_weather.png
    else
        # Clear up the display
        eips -c
        eips -c
        eips -g weather-error.png
    fi
fi
#!/bin/sh

# Adopted from https://github.com/mpetroff/kindle-weather-display
# This script will only get and display weather template, it does
# not include any other things such as kill service. 

# Pushover userID and token. Leave empty if you are not using it. 
PO_TOKEN=""
PO_USER=""

cd "$(dirname "$0")"

# Quit when detect a disable flag
if [ -e disable ]; then exit 0; fi

# Check battery capacity
BATTERY=`grep -o "[0-9]*" /sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity`
CURRENT=`cat /sys/devices/system/yoshi_battery/yoshi_battery0/battery_current`

if [ $BATTERY -le 5 ] && [ $CURRENT -le 0 ]; then
    if [ -e /tmp/weather-battery-drained.flag ]; then
        # If already drawn drained message, then just leave. 
        exit 0;
    else
        touch /tmp/weather-battery-drained.flag
        # If device just got low power, then show charge message. 
        eips 0 38 '--------------- CHARGE BATTERY NOW ---------------'
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
    if [ -e /tmp/weather-battery-drained.flag ]; then rm -f /tmp/weather-battery-drained.flag; fi
    # Get rid of old file first
    rm -f /tmp/weather-crushed.png
    # Test network status
    ping -c 5 www.microsoft.com
    # For those living inside a wall, let's ping Microsoft instead of Google :D
    PINGSTATUS=$?
    if [ $PINGSTATUS -ne 0 ]; then
        eips 0 38 '------------- NO INTERNET CONNECTION -------------'
        exit
    fi
    # Finally, let's get data and refresh
    if ./weather-generator.sh ; then
        # Clear up the display
        eips -c
        eips -c
        eips -g /tmp/weather-crushed.png
    else
        eips 0 38 '------------ COULD NOT UPDATE WEATHER ------------'
    fi
fi

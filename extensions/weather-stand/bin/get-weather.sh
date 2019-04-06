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
    if [ -e /tmp/weatherstand.drained ]; then
        # If already drawn drained image, then just leave. 
        exit 0;
    else
        touch /tmp/weatherstand.drained
        # If device just got low power, then draw drained image. 
        eips -c
        eips -c
        eips -g battery-drained.png
        eips 48 39 'B' # TODO: Use text instead of picture?
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
        eips 48 39 'N' # TODO: Use text instead of picture?
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
        eips 48 39 'E' # TODO: Use text instead of picture?
    fi
fi

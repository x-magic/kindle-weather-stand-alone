#!/bin/sh

cd "$(dirname "$0")"

# Choose your favourite weather service
python weather-generator-darksky.py
#python weather-generator-openweathermap.py

# The script should output a svg file in tmp directory, check before conversion
if [ -e /tmp/weather-latest.svg ]; then
    ./rsvg-convert --background-color=white -o /tmp/weather-converted.png /tmp/weather-latest.svg
    rm -f /tmp/weather-latest.svg
    ./pngcrush -c 0 /tmp/weather-converted.png /tmp/weather-crushed.png
    rm -f /tmp/weather-converted.png
    exit 0;
else
    exit 1;
fi
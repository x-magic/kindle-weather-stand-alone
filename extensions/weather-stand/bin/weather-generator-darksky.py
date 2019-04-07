import codecs
import json
import urllib2
from datetime import datetime

import pytz

# Parameters
weather_key = ''  # Dark Sky API key
location_coord = ''  # Query location in coordinates, comma-separated, no space. e.g. '40.689233,-74.044557' for NYC
location_name = ''  # Query location in literal. Dark Sky API do not provide reverse geo-coding, you need to provide your own suburb name
unit_suite = 'auto'  # Unit of measurements, can be us (imperial), si (metric), ca (metric, but wind speed in kph) or auto (based on geo-location)
time_unit = 12  # Change to 24 if you want to use 23:59 timing
script_version = '3.0'


# Timezone processor
def utc_to_timezone(epoch, timezone_literal):
    utc = datetime.fromtimestamp(epoch, pytz.utc)
    return utc.astimezone(pytz.timezone(timezone_literal))


# Time formatter
def format_time(dt, output_format):
    if output_format is 'day':
        return dt.strftime('%A')
    elif output_format is 'hour':
        if time_unit is 12:
            return dt.strftime('%-I%p')
        else:
            return dt.strftime('%-H:%M')
    elif output_format is 'minute':
        if time_unit is 12:
            return dt.strftime('%I:%M%p')
        else:
            return dt.strftime('%-H:%M')
    return None


# Weather icon translation table
icon_def = {
    'clear-day': 'fair',
    'clear-night': 'fair',
    'rain': 'heavyrain',
    'snow': 'snow',
    'sleet': 'sleet',
    'wind': 'wind',
    'fog': 'fog',
    'cloudy': 'mostlycloudy',
    'partly-cloudy-day': 'partlycloudy',
    'partly-cloudy-night': 'partlycloudy',
    'hail': 'snow-freezingrain',
    'thunderstorms': 'thunderstorms',
    'tornado': 'tornado'
}

# Unit translation table
unit_def = {
    'ca': {'temp': 'C', 'speed': 'km/h'},
    'uk2': {'temp': 'C', 'speed': 'mph'},
    'us': {'temp': 'F', 'speed': 'mph'},
    'si': {'temp': 'C', 'speed': 'm/s'}
}

# Get battery percentage
battery_capacity = open('/sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity', 'r')

# Get weather data from API
weather_url = 'https://api.darksky.net/forecast/' + weather_key + '/' + location_coord + '?units=' + unit_suite
weather_response = urllib2.urlopen(weather_url)
weather_query = json.loads(weather_response.read())
weather_response.close()

weather_units = unit_def[weather_query['flags']['units']]
weather_timezone = weather_query['timezone']
weather_currently = weather_query['currently']
weather_hourly = weather_query['hourly']
weather_daily = weather_query['daily']

weather_data = {
    'VAR_TEMP_UNIT': weather_units['temp'],
    'VAR_LOCATION': location_name,
    'VAR_UPDATE_TIME': format_time(utc_to_timezone(weather_currently['time'], weather_timezone), 'minute'),
    'VAR_NOW_ICON': icon_def[weather_currently['icon']],
    'VAR_NOW_TEMP': int(round(weather_currently['temperature'])),
    'VAR_TODAY_HIGH': int(round(weather_daily['data'][0]['temperatureHigh'])),
    'VAR_TODAY_LOW': int(round(weather_daily['data'][0]['temperatureLow'])),
    'VAR_HOURLY_1_ICON': icon_def[weather_hourly['data'][1]['icon']],
    'VAR_HOURLY_1_TIME': format_time(utc_to_timezone(weather_hourly['data'][1]['time'], weather_timezone), 'hour'),
    'VAR_HOURLY_1_TEMP': int(round(weather_hourly['data'][1]['temperature'])),
    'VAR_HOURLY_2_ICON': icon_def[weather_hourly['data'][2]['icon']],
    'VAR_HOURLY_2_TIME': format_time(utc_to_timezone(weather_hourly['data'][2]['time'], weather_timezone), 'hour'),
    'VAR_HOURLY_2_TEMP': int(round(weather_hourly['data'][2]['temperature'])),
    'VAR_HOURLY_3_ICON': icon_def[weather_hourly['data'][3]['icon']],
    'VAR_HOURLY_3_TIME': format_time(utc_to_timezone(weather_hourly['data'][3]['time'], weather_timezone), 'hour'),
    'VAR_HOURLY_3_TEMP': int(round(weather_hourly['data'][3]['temperature'])),
    'VAR_HOURLY_4_ICON': icon_def[weather_hourly['data'][4]['icon']],
    'VAR_HOURLY_4_TIME': format_time(utc_to_timezone(weather_hourly['data'][4]['time'], weather_timezone), 'hour'),
    'VAR_HOURLY_4_TEMP': int(round(weather_hourly['data'][4]['temperature'])),
    'VAR_HOURLY_5_ICON': icon_def[weather_hourly['data'][5]['icon']],
    'VAR_HOURLY_5_TIME': format_time(utc_to_timezone(weather_hourly['data'][5]['time'], weather_timezone), 'hour'),
    'VAR_HOURLY_5_TEMP': int(round(weather_hourly['data'][5]['temperature'])),
    'VAR_DAILY_TOM_ICON': icon_def[weather_daily['data'][1]['icon']],
    'VAR_DAILY_TOM_DAY': format_time(utc_to_timezone(weather_daily['data'][1]['time'], weather_timezone), 'day'),
    'VAR_DAILY_TOM_HIGH': int(round(weather_daily['data'][1]['temperatureHigh'])),
    'VAR_DAILY_TOM_LOW': int(round(weather_daily['data'][1]['temperatureLow'])),
    'VAR_DAILY_TOM_COND': weather_daily['data'][1]['summary'],
    'VAR_DAILY_TOM_WIND_BEARING': weather_daily['data'][1]['windBearing'],
    'VAR_DAILY_TOM_WIND': ' at ' + str(int(round(weather_daily['data'][1]['windSpeed']))) + weather_units['speed'] + ", up to " + str(int(round(weather_daily['data'][1]['windGust']))) + weather_units['speed'],
    'VAR_DAILY_1_ICON': icon_def[weather_daily['data'][2]['icon']],
    'VAR_DAILY_1_DAY': format_time(utc_to_timezone(weather_daily['data'][2]['time'], weather_timezone), 'day'),
    'VAR_DAILY_1_HIGH': int(round(weather_daily['data'][2]['temperatureHigh'])),
    'VAR_DAILY_1_LOW': int(round(weather_daily['data'][2]['temperatureLow'])),
    'VAR_DAILY_2_ICON': icon_def[weather_daily['data'][3]['icon']],
    'VAR_DAILY_2_DAY': format_time(utc_to_timezone(weather_daily['data'][3]['time'], weather_timezone), 'day'),
    'VAR_DAILY_2_HIGH': int(round(weather_daily['data'][3]['temperatureHigh'])),
    'VAR_DAILY_2_LOW': int(round(weather_daily['data'][3]['temperatureLow'])),
    'VAR_DAILY_3_ICON': icon_def[weather_daily['data'][4]['icon']],
    'VAR_DAILY_3_DAY': format_time(utc_to_timezone(weather_daily['data'][4]['time'], weather_timezone), 'day'),
    'VAR_DAILY_3_HIGH': int(round(weather_daily['data'][4]['temperatureHigh'])),
    'VAR_DAILY_3_LOW': int(round(weather_daily['data'][4]['temperatureLow'])),
    'VAR_DAILY_4_ICON': icon_def[weather_daily['data'][5]['icon']],
    'VAR_DAILY_4_DAY': format_time(utc_to_timezone(weather_daily['data'][5]['time'], weather_timezone), 'day'),
    'VAR_DAILY_4_HIGH': int(round(weather_daily['data'][5]['temperatureHigh'])),
    'VAR_DAILY_4_LOW': int(round(weather_daily['data'][5]['temperatureLow'])),
    'VAR_DAILY_5_ICON': icon_def[weather_daily['data'][6]['icon']],
    'VAR_DAILY_5_DAY': format_time(utc_to_timezone(weather_daily['data'][6]['time'], weather_timezone), 'day'),
    'VAR_DAILY_5_HIGH': int(round(weather_daily['data'][6]['temperatureHigh'])),
    'VAR_DAILY_5_LOW': int(round(weather_daily['data'][6]['temperatureLow'])),
    'VAR_PROVIDER_STRING': 'Powered by Dark Sky',
    'VAR_BATTERY_CAPACITY': battery_capacity.read(),
    'VAR_VERSION': script_version
}

# Generate SVG file from template
output = codecs.open('weather-template.svg', 'r', encoding='utf-8').read()
for (key, value) in weather_data.items():
    output = output.replace(key, str(value))

codecs.open('/tmp/weather-latest.svg', 'w', encoding='utf-8').write(output)

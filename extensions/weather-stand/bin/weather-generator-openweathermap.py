import codecs
import json
import urllib2
from datetime import datetime

import pytz

# Parameters
weather_key = ''  # OpenWeatherMap API key
location_string = ''  # Location parameter, see below for details
# You can search for location with following ways:
# - By city name: city name and country code divided by comma, use ISO 3166 country codes. e.g. 'q=London,uk'
# - By city id: simply lookup your desired city in https://openweathermap.org/ and the city id will show up in URL field. e.g. 'id=2172797'
# - By geographic coordinates: by latitude and longitude. e.g. 'lat=35&lon=139'
# - By ZIP code: by zip/post code (if country is not specified, will search the USA). e.g. 'zip=94040,us'
unit_suite = 'metric'  # Unit of measurements, can be 'metric' or 'imperial'
time_unit = 12  # Change to 24 if you want to use 24-hour time (i.e. 23:59 instead of 11:59AM)
timezone_string = 'America/New_York'  # Desired timezone string, lookup at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
script_version = '3.0'


# Timezone processor
def utc_to_timezone(epoch):
    utc = datetime.fromtimestamp(epoch, pytz.utc)
    return utc.astimezone(pytz.timezone(timezone_string))


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


def hourly_to_daily(forecasts, now):
    daily = {}
    for day in forecasts:
        current_date = utc_to_timezone(day['dt'])
        delta = current_date.day - now.day

        try:
            daily[delta]
        except KeyError:
            daily[delta] = {
                'day': None,
                'temp_high': -99,
                'temp_low': 99,
                'weathers': {},
                'weather_id': 900,
                'weather': '',
                'weather_descriptions': [],
                'icon': None,
                'wind_bearing': 0,
                'wind_bearing_count': 0,
                'wind_max': 0,
                'wind_min': 255
            }

        daily[delta]['day'] = format_time(current_date, 'day')

        if day['main']['temp_max'] > daily[delta]['temp_high']:
            daily[delta]['temp_high'] = day['main']['temp_max']

        if day['main']['temp_min'] < daily[delta]['temp_low']:
            daily[delta]['temp_low'] = day['main']['temp_min']

        for weather in day['weather']:
            daily[delta]['weathers'][weather['id']] = weather

        daily[delta]['wind_bearing'] = daily[delta]['wind_bearing'] + day['wind']['deg']
        daily[delta]['wind_bearing_count'] = daily[delta]['wind_bearing_count'] + 1

        if day['wind']['speed'] > daily[delta]['wind_max']:
            daily[delta]['wind_max'] = day['wind']['speed']

        if day['wind']['speed'] < daily[delta]['wind_min']:
            daily[delta]['wind_min'] = day['wind']['speed']

    # Calculate Wind bearing and daily weather/icon
    for delta, day in daily.items():
        daily[delta]['wind_bearing'] = day['wind_bearing'] / day['wind_bearing_count']
        for weather_id, weather_info in day['weathers'].items():
            daily[delta]['weather_descriptions'].append(weather_info['description'])
            if daily[delta]['weather_id'] > weather_info['id']:
                daily[delta]['weather_id'] = weather_info['id']
                daily[delta]['icon'] = weather_info['icon']
        daily[delta]['weather'] = ', '.join(day['weather_descriptions']).capitalize()

    return daily


# Weather icon translation table
icon_def = {
    '01d': 'fair',
    '01n': 'fair',
    '02d': 'partlycloudy',
    '02n': 'partlycloudy',
    '03d': 'mostlycloudy',
    '03n': 'mostlycloudy',
    '04d': 'overcast',
    '04n': 'overcast',
    '09d': 'rain',
    '09n': 'rain',
    '10d': 'scartteredshowers',
    '10n': 'scartteredshowers',
    '11d': 'thunderstorms',
    '11n': 'thunderstorms',
    '13d': 'snow',
    '13n': 'snow',
    '50d': 'mist',
    '50n': 'mist',
}

# Unit translation table
unit_def = {
    'metric': {'temp': 'C', 'speed': 'm/s'},
    'imperial': {'temp': 'F', 'speed': 'mph'}
}

# Get battery percentage
battery_capacity = open('/sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity', 'r')

# Get weather data from API
weather_url = 'http://api.openweathermap.org/data/2.5/weather?APPID=' + weather_key + '&units=' + unit_suite + '&' + location_string
weather_response = urllib2.urlopen(weather_url)
weather_query = json.loads(weather_response.read())
weather_response.close()

forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?APPID=' + weather_key + '&units=' + unit_suite + '&' + location_string
forecast_response = urllib2.urlopen(forecast_url)
forecast_query = json.loads(forecast_response.read())
forecast_response.close()

current_datetime = utc_to_timezone(weather_query['dt'])
forecast_daily = hourly_to_daily(forecast_query['list'], current_datetime)
forecast_hourly = forecast_query['list']

weather_units = unit_def[unit_suite]

weather_data = {
    'VAR_TEMP_UNIT': weather_units['temp'],
    'VAR_LOCATION': weather_query['name'] + ', ' + weather_query['sys']['country'],
    'VAR_UPDATE_TIME': format_time(current_datetime, 'minute'),
    'VAR_NOW_ICON': icon_def[weather_query['weather'][0]['icon']],
    'VAR_NOW_TEMP': int(round(weather_query['main']['temp'])),
    'VAR_TODAY_HIGH': int(round(forecast_daily[0]['temp_high'])),
    'VAR_TODAY_LOW': int(round(forecast_daily[0]['temp_low'])),
    'VAR_HOURLY_1_ICON': icon_def[forecast_hourly[0]['weather'][-1]['icon']],
    'VAR_HOURLY_1_TIME': format_time(utc_to_timezone(forecast_hourly[0]['dt']), 'hour'),
    'VAR_HOURLY_1_TEMP': int(round(forecast_hourly[0]['main']['temp'])),
    'VAR_HOURLY_2_ICON': icon_def[forecast_hourly[1]['weather'][-1]['icon']],
    'VAR_HOURLY_2_TIME': format_time(utc_to_timezone(forecast_hourly[1]['dt']), 'hour'),
    'VAR_HOURLY_2_TEMP': int(round(forecast_hourly[1]['main']['temp'])),
    'VAR_HOURLY_3_ICON': icon_def[forecast_hourly[2]['weather'][-1]['icon']],
    'VAR_HOURLY_3_TIME': format_time(utc_to_timezone(forecast_hourly[2]['dt']), 'hour'),
    'VAR_HOURLY_3_TEMP': int(round(forecast_hourly[2]['main']['temp'])),
    'VAR_HOURLY_4_ICON': icon_def[forecast_hourly[3]['weather'][-1]['icon']],
    'VAR_HOURLY_4_TIME': format_time(utc_to_timezone(forecast_hourly[3]['dt']), 'hour'),
    'VAR_HOURLY_4_TEMP': int(round(forecast_hourly[3]['main']['temp'])),
    'VAR_HOURLY_5_ICON': icon_def[forecast_hourly[4]['weather'][-1]['icon']],
    'VAR_HOURLY_5_TIME': format_time(utc_to_timezone(forecast_hourly[4]['dt']), 'hour'),
    'VAR_HOURLY_5_TEMP': int(round(forecast_hourly[4]['main']['temp'])),
    'VAR_DAILY_TOM_ICON': icon_def[forecast_daily[1]['icon']],
    'VAR_DAILY_TOM_DAY': forecast_daily[1]['day'],
    'VAR_DAILY_TOM_HIGH': int(round(forecast_daily[1]['temp_high'])),
    'VAR_DAILY_TOM_LOW': int(round(forecast_daily[1]['temp_low'])),
    'VAR_DAILY_TOM_COND': forecast_daily[1]['weather'],
    'VAR_DAILY_TOM_WIND_BEARING': forecast_daily[1]['wind_bearing'],
    'VAR_DAILY_TOM_WIND': ' at ' + str(int(round(forecast_daily[1]['wind_min']))) + weather_units['speed'] + ", up to " + str(int(round(forecast_daily[1]['wind_max']))) + weather_units['speed'],
    'VAR_DAILY_1_ICON': icon_def[forecast_daily[2]['icon']],
    'VAR_DAILY_1_DAY': forecast_daily[2]['day'],
    'VAR_DAILY_1_HIGH': int(round(forecast_daily[2]['temp_high'])),
    'VAR_DAILY_1_LOW': int(round(forecast_daily[2]['temp_low'])),
    'VAR_DAILY_2_ICON': icon_def[forecast_daily[3]['icon']],
    'VAR_DAILY_2_DAY': forecast_daily[3]['day'],
    'VAR_DAILY_2_HIGH': int(round(forecast_daily[3]['temp_high'])),
    'VAR_DAILY_2_LOW': int(round(forecast_daily[3]['temp_low'])),
    'VAR_DAILY_3_ICON': icon_def[forecast_daily[4]['icon']],
    'VAR_DAILY_3_DAY': forecast_daily[4]['day'],
    'VAR_DAILY_3_HIGH': int(round(forecast_daily[4]['temp_high'])),
    'VAR_DAILY_3_LOW': int(round(forecast_daily[4]['temp_low'])),
    'VAR_DAILY_4_ICON': 'na',
    'VAR_DAILY_4_DAY': 'N/A',
    'VAR_DAILY_4_HIGH': 0,
    'VAR_DAILY_4_LOW': 0,
    'VAR_DAILY_5_ICON': 'na',
    'VAR_DAILY_5_DAY': 'N/A',
    'VAR_DAILY_5_HIGH': 0,
    'VAR_DAILY_5_LOW': 0,
    'VAR_PROVIDER_STRING': 'Powered by OpenWeatherMap',
    'VAR_BATTERY_CAPACITY': battery_capacity.read(),
    'VAR_VERSION': script_version
}

# Generate SVG file from template
output = codecs.open('weather-template.svg', 'r', encoding='utf-8').read()
for (key, value) in weather_data.items():
    output = output.replace(key, str(value))

codecs.open('/tmp/weather-latest.svg', 'w', encoding='utf-8').write(output)

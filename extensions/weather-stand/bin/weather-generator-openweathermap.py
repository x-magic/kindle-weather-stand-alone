import time
import codecs
import urllib2
import json

# Convert 24 hour to 12 hour number
def to12hrs(in24hrs):
    value = int(in24hrs)
    if (value == 0):
        return 12
    elif (value <= 12):
        return value
    elif (value > 12):
        return value - 12
    else:
        raise ValueError('Invalid parameter')

# Weather icon translation table
iconArray = {'chanceflurries':'blizzard','chancerain':'ra','chancesleet':'rasn','chancesnow':'sn','chancetstorms':'tsra','clear':'skc','cloudy':'ovc','flurries':'blizzard','fog':'fg','hazy':'mist','mostlycloudy':'bkn','mostlysunny':'sct','partlycloudy':'bkn','partlysunny':'sct','rain':'ra','sleet':'rasn','snow':'sn','sunny':'skc','tstorms':'tsra','nt_chanceflurries':'blizzard','nt_chancerain':'ra','nt_chancesleet':'rasn','nt_chancesnow':'sn','nt_chancetstorms':'tsra','nt_clear':'skc','nt_cloudy':'ovc','nt_flurries':'blizzard','nt_fog':'fg','nt_hazy':'mist','nt_mostlycloudy':'bkn','nt_mostlysunny':'sct','nt_partlycloudy':'bkn','nt_partlysunny':'sct','nt_rain':'ra','nt_sleet':'rasn','nt_snow':'sn','nt_sunny':'skc','nt_tstorms':'tsra'}

# Parameters
weatherKey = '' #WUnderground API key
timeKey    = '' #TimeZoneDB API key
location   = '' #Query location, can be pws (recommended) or coordinates
timezone   = '' #Timezone, check TimeZoneDB API manual for list of timezones
queryArray = ['geolookup','hourly','forecast10day']

# Get battery percentage
batt_capacity = open('/sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity', 'r')

# Get weather data from API
queries = {'geolookup':None,'hourly':None,'forecast10day':None}
for (query, result) in queries.items():
    weatherURL = 'http://api.wunderground.com/api/'+weatherKey+'/'+query+'/q/'+location+'.json'
    weatherContent = urllib2.urlopen(weatherURL)
    queries[query] = json.loads(weatherContent.read())
    weatherContent.close()

datetimeURL = 'http://api.timezonedb.com/v2/get-time-zone?key='+timeKey+'&format=json&by=zone&zone='+timezone
datetimeContent = urllib2.urlopen(datetimeURL)
datetime = json.loads(datetimeContent.read())
datetimeContent.close()
datetimeCurrent = time.gmtime(int(datetime['timestamp']))

# Create weather data matrix
weatherData = {}
weatherData['VAR_LOCATION']            = queries['geolookup']['location']['city']
weatherData['VAR_UPDATE_DAY']          = time.strftime('%a', datetimeCurrent)
weatherData['VAR_UPDATE_HOUR']         = time.strftime('%-I', datetimeCurrent)
weatherData['VAR_UPDATE_MINUTE']       = time.strftime('%M', datetimeCurrent)
weatherData['VAR_UPDATE_AMPM']         = time.strftime('%p', datetimeCurrent)
weatherData['VAR_TODAY_ICON']          = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][0]['icon']]
weatherData['VAR_TODAY_HIGH']          = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
weatherData['VAR_TODAY_LOW']           = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']
weatherData['VAR_DAILY_TOM_ICON']      = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['icon']]
weatherData['VAR_DAILY_TOM_DAY']       = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['date']['weekday']
weatherData['VAR_DAILY_TOM_HIGH']      = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['high']['celsius']
weatherData['VAR_DAILY_TOM_LOW']       = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['low']['celsius']
weatherData['VAR_DAILY_TOM_COND']      = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['conditions']
weatherData['VAR_DAILY_TOM_WIND_DIR']  = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['avewind']['dir']
weatherData['VAR_DAILY_TOM_WIND_DEG']  = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['avewind']['degrees']
weatherData['VAR_DAILY_TOM_WIND_LOW']  = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['avewind']['kph']
weatherData['VAR_DAILY_TOM_WIND_HIGH'] = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][1]['maxwind']['kph']
weatherData['VAR_DAILY_1_ICON']        = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][2]['icon']]
weatherData['VAR_DAILY_1_DAY']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][2]['date']['weekday']
weatherData['VAR_DAILY_1_HIGH']        = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][2]['high']['celsius']
weatherData['VAR_DAILY_1_LOW']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][2]['low']['celsius']
weatherData['VAR_DAILY_2_ICON']        = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][3]['icon']]
weatherData['VAR_DAILY_2_DAY']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][3]['date']['weekday']
weatherData['VAR_DAILY_2_HIGH']        = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][3]['high']['celsius']
weatherData['VAR_DAILY_2_LOW']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][3]['low']['celsius']
weatherData['VAR_DAILY_3_ICON']        = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][4]['icon']]
weatherData['VAR_DAILY_3_DAY']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][4]['date']['weekday']
weatherData['VAR_DAILY_3_HIGH']        = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][4]['high']['celsius']
weatherData['VAR_DAILY_3_LOW']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][4]['low']['celsius']
weatherData['VAR_DAILY_4_ICON']        = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][5]['icon']]
weatherData['VAR_DAILY_4_DAY']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][5]['date']['weekday']
weatherData['VAR_DAILY_4_HIGH']        = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][5]['high']['celsius']
weatherData['VAR_DAILY_4_LOW']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][5]['low']['celsius']
weatherData['VAR_DAILY_5_ICON']        = iconArray[queries['forecast10day']['forecast']['simpleforecast']['forecastday'][6]['icon']]
weatherData['VAR_DAILY_5_DAY']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][6]['date']['weekday']
weatherData['VAR_DAILY_5_HIGH']        = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][6]['high']['celsius']
weatherData['VAR_DAILY_5_LOW']         = queries['forecast10day']['forecast']['simpleforecast']['forecastday'][6]['low']['celsius']
weatherData['VAR_HOURLY_1_ICON']       = iconArray[queries['hourly']['hourly_forecast'][0]['icon']]
weatherData['VAR_HOURLY_1_TIME']       = str(to12hrs(queries['hourly']['hourly_forecast'][0]['FCTTIME']['hour']))+queries['hourly']['hourly_forecast'][0]['FCTTIME']['ampm']
weatherData['VAR_HOURLY_1_TEMP']       = queries['hourly']['hourly_forecast'][0]['temp']['metric']
weatherData['VAR_HOURLY_2_ICON']       = iconArray[queries['hourly']['hourly_forecast'][1]['icon']]
weatherData['VAR_HOURLY_2_TIME']       = str(to12hrs(queries['hourly']['hourly_forecast'][1]['FCTTIME']['hour']))+queries['hourly']['hourly_forecast'][1]['FCTTIME']['ampm']
weatherData['VAR_HOURLY_2_TEMP']       = queries['hourly']['hourly_forecast'][1]['temp']['metric']
weatherData['VAR_HOURLY_3_ICON']       = iconArray[queries['hourly']['hourly_forecast'][2]['icon']]
weatherData['VAR_HOURLY_3_TIME']       = str(to12hrs(queries['hourly']['hourly_forecast'][2]['FCTTIME']['hour']))+queries['hourly']['hourly_forecast'][2]['FCTTIME']['ampm']
weatherData['VAR_HOURLY_3_TEMP']       = queries['hourly']['hourly_forecast'][2]['temp']['metric']
weatherData['VAR_HOURLY_4_ICON']       = iconArray[queries['hourly']['hourly_forecast'][3]['icon']]
weatherData['VAR_HOURLY_4_TIME']       = str(to12hrs(queries['hourly']['hourly_forecast'][3]['FCTTIME']['hour']))+queries['hourly']['hourly_forecast'][3]['FCTTIME']['ampm']
weatherData['VAR_HOURLY_4_TEMP']       = queries['hourly']['hourly_forecast'][3]['temp']['metric']
weatherData['VAR_HOURLY_5_ICON']       = iconArray[queries['hourly']['hourly_forecast'][4]['icon']]
weatherData['VAR_HOURLY_5_TIME']       = str(to12hrs(queries['hourly']['hourly_forecast'][4]['FCTTIME']['hour']))+queries['hourly']['hourly_forecast'][4]['FCTTIME']['ampm']
weatherData['VAR_HOURLY_5_TEMP']       = queries['hourly']['hourly_forecast'][4]['temp']['metric']
weatherData['VAR_VERSION']             = '2.0'
weatherData['BATT_CAPACITY']           = batt_capacity.read()

# Generate SVG file from template
output = codecs.open('weather-template.svg', 'r', encoding='utf-8').read()

for (key, value) in weatherData.items():
    output = output.replace(key, str(value))

codecs.open('/tmp/latest_weather.svg', 'w', encoding='utf-8').write(output)
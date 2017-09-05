# Kindle Weather Stand Project

## TL;DR

![Screenshot](https://raw.githubusercontent.com/x-magic/kindle-weather-stand-alone/master/demo.jpg)

## More about this project
This is a sister project to [Kindle Weather Stand Project](https://github.com/x-magic/kindle-weather-display). The difference is that this version runs on Kindle alone without need of a server. 

From version 2.0 this project is based on KUAL. You need to jailbreak your Kindle and install KUAL to start weather stand. Cron-based script is still here but will not be maintained. 

A new method for saving power is introduced. On my Kindle 4, the new method can continue to update weather up to 4 weeks on a single charge, when weather data is updated every hour. 

Unfortunately even after I reduce the wakeup rate to 4 times a day, it still lasts around 4 weeks. Not sure if there's a better way to prolong the battery life. For more information, please refer to inline comments. 

Latest update also requires a TimeZoneDB API key since the new method will inevitably slow down Kindle's RTC, hence, we need a way to get correct time. (I wish Weather Underground API will give a timestamp with queries, but no luck)

## Files explained

 - All executables and required parts are in *kindle* folder
   - *update-weather.sh* is the cron job script. Details of usage are in the file
   - *get-weather.sh* is the script that KUAL launcher called. Details of usage are in the file
 - *exception-template.psd* is the psd template of all exception pictures. 

## What do you need?

 - A brain somewhat familiar with jailbroken Kindle, and Linux (Haha...)
 - A Kindle, of course (Kindle 4, silver or black should works the same, not tested on other model)
 - A [Weather Underground API](https://www.wunderground.com/weather/api) key (free tier is more than enough for single device usage)
 - A [TimeZoneDB API](https://timezonedb.com/api) key (free tier is enough)

## What to do next?

 - Clone the project
 - Have a look at various scripts and replace API keys in several files
 - Put files on Kindle
 - Launch program in KUAL
 - ???
 - PROFIT!

## For those who helped
This project include following components (in binary form) from [this link](http://www.mobileread.com/forums/showthread.php?t=200621) with some necessary modifications: 

 * pngcrush from fedora project repository [here](http://arm.koji.fedoraproject.org/koji/buildinfo?buildID=11465).
 * python 2.7 from [here](http://www.mobileread.com/forums/showthread.php?t=153930)
 * librsvg from [here](http://www.mobileread.com/forums/showpost.php?p=2743269&postcount=34)

These resources are all compiled binaries from open-source projects and included just for convenient distributions. If this cause any copyright infringement please contact me for removal. 

Code is released under MIT license and graphic components are released under CC0. Enjoy! 
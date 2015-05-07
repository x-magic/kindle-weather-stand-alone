# Kindle Weather Stand Project

## TL;DR
![Screenshot](https://raw.githubusercontent.com/x-magic/kindle-weather-stand-alone/master/demo.jpg)

## More about this project
This is a sister project to [Kindle Weather Stand Project](https://github.com/x-magic/kindle-weather-display). The difference is that this version runs on Kindle alone without need of a server. 

## Files explained

 - All executables and required parts are in *kindle* folder
   - *update-weather.sh* is the cron job script. Details of usage are in line 3 of the file
 - Battery usage statistics (with 1 minute and 5 minutes mixed data points) and a plot is available in *statistics* folder
 - *exception-template.psd* is the psd template of all exception pictures. 

## For those who helped
This project include following components (in binary form) from [this link](http://www.mobileread.com/forums/showthread.php?t=200621) with some necessary modifications: 

 * pngcrush from fedora project repository [here](http://arm.koji.fedoraproject.org/koji/buildinfo?buildID=11465).
 * python 2.7 from [here](http://www.mobileread.com/forums/showthread.php?t=153930)
 * librsvg from [here](http://www.mobileread.com/forums/showpost.php?p=2743269&postcount=34)

These resources are all compiled binaries from open-source projects and included just for convenient distributions. If this cause any copyright infringement please contact me for removal. 
#!/bin/sh

cd "$(dirname "$0")"

# Clean up display, show initialisation message
/usr/sbin/eips -c
/usr/sbin/eips -c
/usr/sbin/eips 11 18 'Kindle Weather Stand Project'
/usr/sbin/eips 15 19 'https://git.io/vDVgT'
/usr/sbin/eips 6 20 'This program will check prerequisites'
/usr/sbin/eips 9 21 'for Kindle Weather Stand Project'
/usr/sbin/eips 0 23 '--------------------------------------------------'
sleep 5

/usr/sbin/eips 0 24 'Checking if Python2 is installed...'
sleep 1
if python -c ""; then
	/usr/sbin/eips 36 24 'Installed'
else
	/usr/sbin/eips 36 24 'Failed'
	/usr/sbin/eips 0 25 'You need Kindle Python to use Weather Stand'
	/usr/sbin/eips 0 26 'www.mobileread.com/forums/showthread.php?t=195474'
	exit 1
fi

/usr/sbin/eips 0 25 'Checking if pytz is installed...'

if python -c "import pytz"; then
	/usr/sbin/eips 33 25 'Installed'
else
	/usr/sbin/eips 33 25 'Failed'
	/usr/sbin/eips 0 26 'Installing pytz...'
	if tar -xzf pytz-2018.9.tar.gz; then
		if cd pytz-2018.9; then
			if python setup.py install; then
				/usr/sbin/eips 19 26 'Done'
			else
				/usr/sbin/eips 19 26 'Failed'
				/usr/sbin/eips 0 27 'pytz installer failed to complete'
				/usr/sbin/eips 0 28 'Please install pytz manually'
				exit 1
			fi
		else
			/usr/sbin/eips 19 26 'Failed'
			/usr/sbin/eips 0 27 'Cannot start pytz installer'
			/usr/sbin/eips 0 28 'Please install pytz manually'
			exit 1
		fi
	else
		/usr/sbin/eips 19 26 'Failed'
		/usr/sbin/eips 0 27 'Cannot extract pytz installer'
		/usr/sbin/eips 0 28 'Please install pytz manually'
		exit 1
	fi
	/usr/sbin/eips 0 27 'Checking if pytz is installed correctly...'
	if python -c "import pytz"; then
		/usr/sbin/eips 43 27 'Done'
	else
		/usr/sbin/eips 43 27 'Failed'
		/usr/sbin/eips 0 28 'pytz is not correctly installed'
		/usr/sbin/eips 0 29 'Please install pytz manually'
		exit 1
	fi
fi

/usr/sbin/eips 0 37 'You are ready to start Weather Stand'
/usr/sbin/eips 0 38 'You may delete this checker program from KUAL'
/usr/sbin/eips 0 39 'Push Home button to back to Kindle home page'

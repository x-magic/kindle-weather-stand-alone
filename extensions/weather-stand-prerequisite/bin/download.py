import hashlib
import json
import ssl
import urllib2

pytz_url = 'https://pypi.python.org/pypi/pytz/json'
ssl_context = ssl._create_unverified_context()
pytz_response = urllib2.urlopen(pytz_url, context=ssl_context)
pytz_query = json.loads(pytz_response.read())

pytz_urls = pytz_query['urls']
pytz_md5 = ''

for item in pytz_urls:
    if item['packagetype'] == 'sdist' and item['python_version'] == 'source':
        pytz_download_url = item['url']
        pytz_md5 = str(item['digests']['md5']).lower()

tarball = urllib2.urlopen(pytz_download_url, context=ssl_context)
with open('pytz.tar.gz', 'wb') as file: 
    file.write(tarball.read())
    file.close()

hasher = hashlib.md5()
pytz_dl = open('pytz.tar.gz', 'rb')
pytz_dl_buffer = pytz_dl.read()
pytz_dl_hash = hasher.update(pytz_dl_buffer)
pytz_dl_md5 = str(hasher.hexdigest()).lower()

if pytz_md5 != pytz_dl_md5:
    raise Exception('Incomplete file download!')
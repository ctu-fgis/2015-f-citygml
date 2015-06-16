#!/usr/bin/python
import os
import zipfile
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

BASEURL = 'http://www.citygml.org/fileadmin/count.php?f=fileadmin/citygml/docs/'
FILES = [
    'geoRES_testdata_v1.0.0',
    'waldbruecke_v1.0.0',
]

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

for filename in FILES:
    if not os.path.exists(filename) and not os.path.exists(filename + '.gml'):
        if not os.path.exists(filename + '.zip'):
            print('Downloading {}'.format(filename))
            urlretrieve(BASEURL + filename + '.zip', filename + '.zip')
        print('Extracting {}'.format(filename))
        with zipfile.ZipFile(filename + '.zip', 'r') as zip:
            zip.extractall('.')

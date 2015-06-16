import os
import sys
import zipfile
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


BASEURL = 'http://www.citygml.org/fileadmin/count.php?f=fileadmin/citygml/docs/'
FILES = [
    'geoRES_testdata_v1.0.0',
    'waldbruecke_v1.0.0',
    'CityGML_2.0_Test_Dataset_2012-04-23',
    'Berlin_Alexanderplatz_v0.4.0',
]

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
pwd = os.getcwd()
os.chdir(os.path.join(dname, 'datasets'))

for filename in FILES:
    if not os.path.exists(filename) and not os.path.exists(filename + '.gml') and not os.path.exists(filename + '.xml'):
        if not os.path.exists(filename + '.zip'):
            print('Downloading {}'.format(filename))
            if filename == 'CityGML_2.0_Test_Dataset_2012-04-23':
                url = 'http://dl.dropbox.com/u/24313387/CityGML_2.0_Test_Dataset_2012-04-23.zip'
            else:
                url = BASEURL + filename + '.zip'
            urlretrieve(url, filename + '.zip')
        print('Extracting {}'.format(filename))
        with zipfile.ZipFile(filename + '.zip', 'r') as zip:
            zip.extractall('.')

os.chdir(pwd)

projdir = os.path.dirname(dname)
sys.path.insert(0, projdir)

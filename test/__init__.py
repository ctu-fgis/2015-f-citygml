import os
import sys

abspath = os.path.abspath(__file__)
testdir = os.path.dirname(abspath)
projdir = os.path.dirname(testdir)
sys.path.insert(0, projdir)

if not os.path.exists('test/datasets/geoRES_testdata_v1.0.0'):
    sys.stderr.write('You don\'t have files neccessary for testing\n')
    sys.stderr.write('Please read test/datasets/README.rst\n')
    exit(1)

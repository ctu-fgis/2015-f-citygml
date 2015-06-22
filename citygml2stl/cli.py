import sys

from . import citygml
from . import polygons
from . import stl
from . import __version__


try:
    unicode
except NameError:
    unicode = str


def main():
    """
    Simple CLI interafce for citygml2stl
    """

    if len(sys.argv) == 1 or '--help' in sys.argv or 'help' in sys.argv:
        print('CityGML {}'.format(__version__))
        print('Usage: {} [file [file [file...]]]'.format(sys.argv[0]))
        return 0

    ret = 0

    for ipath in sys.argv[1:]:
        if ipath.endswith('.xml') or ipath.endswith('.gml'):
            opath = ipath[:-3] + 'stl'
        else:
            opath = ipath + '.stl'

        print('Converting {} to {}'.format(ipath, opath))

        try:
            c = citygml.CityGML(ipath)
            with stl.StlFile(opath) as ofile:
                for obj in c.get_objects_of_types():
                    ofile.write_triangles(polygons.object2triangles(obj))
        except Exception as e:
            sys.stderr.write('Error: ' + unicode(e) + '\n')
            ret = 1

    return ret

import os
from lxml import etree

from . import exceptions


class CityGML(object):
    """
    Class providing an interface for extracting data from CityGML files
    """
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise exceptions.CityGMLInputError('{} does not exist'.format(filename))
        if os.path.isdir(filename):
            basename = os.path.basename(filename)
            inside = '{}/{}.xml'.format(filename, basename)
            if not os.path.exists(inside):
                raise exceptions.CityGMLInputError('{} does not exist'.format(inside))
            self.filename = inside
        else:
            self.filename = filename

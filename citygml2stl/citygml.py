import os
from lxml import etree

from . import exceptions


class CityGML(object):
    """
    Class providing an interface for extracting data from CityGML files
    """
    namespaces = [
        'http://www.opengis.net/citygml/1.0',
        'http://www.opengis.net/citygml/2.0',
    ]

    def __init__(self, filename):
        self.filename = self._get_xml_file(filename)
        self._parse_xml()

    def _get_xml_file(self, filename):
        if not os.path.exists(filename):
            raise exceptions.CityGMLInputError('{} does not exist'.format(filename))
        if os.path.isdir(filename):
            basename = os.path.basename(filename)
            inside = '{}/{}.xml'.format(filename, basename)
            if not os.path.exists(inside):
                raise exceptions.CityGMLInputError('{} does not exist'.format(inside))
            return inside
        return filename

    def _parse_xml(self):
        self.tree = etree.parse(self.filename)
        for ns in CityGML.namespaces:
            identifier = '//{{{}}}cityObjectMember'.format(ns)
            self.city_objects = self.tree.findall(identifier)
            if self.city_objects:
                self.namespace = ns
                return
        if not self.city_objects:
            raise exceptions.CityGMLInputError('Found no city objects in {}'.format(self.filename))

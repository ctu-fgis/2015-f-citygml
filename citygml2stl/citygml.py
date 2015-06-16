import os
from lxml import etree

from . import exceptions


class CityGML(object):
    """
    Class providing an interface for extracting data from CityGML files
    """
    namespaces = [
        'http://www.citygml.org/citygml/1/0/0',
        'http://www.opengis.net/citygml/1.0',
        'http://www.opengis.net/citygml/2.0',
    ]

    def __init__(self, filename):
        """
        Initialize the CityGML object by parsing the file located at the given path
        """
        self.filename = self._get_xml_file(filename)
        self._parse_xml()

    def _get_xml_file(self, filename):
        """
        Gets the XML file to parse
        """
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
        """
        Saves the parsed XML tree, CityGML namespace and list of city_objects
        """
        self.tree = etree.parse(self.filename)
        for ns in CityGML.namespaces:
            identifier = '//{{{}}}cityObjectMember'.format(ns)
            self.city_objects = self.tree.findall(identifier)
            if self.city_objects:
                self.namespace = ns
                return
        if not self.city_objects:
            raise exceptions.CityGMLInputError('Found no city objects in {}'.format(self.filename))

    def get_objects_of_types(self, *args):
        """
        Return a list of city objects of the given types
        """
        objects = []
        types = args
        for obj in self.city_objects:
            for child in obj:
                for t in types:
                    if str(child.tag).endswith('}' + t):
                        objects.append(child)
                        break
                if not types:
                    objects.append(child)
        return objects

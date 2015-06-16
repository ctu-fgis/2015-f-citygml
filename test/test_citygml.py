import pytest

from citygml2stl import citygml
from citygml2stl import exceptions


class TestCityGML(object):
    def test_open_gml_path(self):
        """
        Tests that opening an existing .gml file recognizes the .gml file as filename
        """
        path = 'test/datasets/waldbruecke_v1.0.0.gml'
        c = citygml.CityGML(path)
        assert c.filename == path

    def test_open_dir_path(self):
        """
        Tests that opening an existing directory with .xml file recognizes that file as filename
        """
        path = 'test/datasets/geoRES_testdata_v1.0.0'
        c = citygml.CityGML(path)
        assert c.filename == path + '/geoRES_testdata_v1.0.0.xml'

    def test_open_bogus_path(self):
        """
        Tests that opening a non-existing path fails
        """
        path = 'this/is/a/bogus/path'
        with pytest.raises(exceptions.CityGMLInputError):
            c = citygml.CityGML(path)

    def test_open_directory_without_xml(self):
        """
        Tests that opening a directory without a xml file fails
        """
        path = 'test/datasets'
        with pytest.raises(exceptions.CityGMLInputError):
            c = citygml.CityGML(path)

    @pytest.mark.parametrize(('filename', 'number'),
                             (('waldbruecke_v1.0.0.gml', 523),
                              ('geoRES_testdata_v1.0.0', 30),
                              ('CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml', 10),
                              ('Berlin_Alexanderplatz_v0.4.0.xml', 1123),))
    def test_number_of_city_objects(self, filename, number):
        """
        Tests the returned number of city objects
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        assert len(c.city_objects) == number

    @pytest.mark.parametrize(('filename', 'ns'),
                             (('Berlin_Alexanderplatz_v0.4.0.xml',
                               'http://www.citygml.org/citygml/1/0/0'),
                              ('geoRES_testdata_v1.0.0',
                               'http://www.opengis.net/citygml/1.0'),
                              ('CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml',
                               'http://www.opengis.net/citygml/2.0'),))
    def test_correct_ns_recognition(self, filename, ns):
        """
        Tests the extracted CityGML namespace is correct
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        assert c.namespace == ns

    @pytest.mark.parametrize(('query', 'number'),
                             ((('Railway',), 10),
                              (('Building',), 0),
                              (('Building', 'Railway'), 10),
                              (tuple(), 10)))
    def test_get_objects_of_types(self, query, number):
        """
        Test if get_objects_of_types() returns such objects
        """
        path = 'test/datasets/CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml'
        c = citygml.CityGML(path)
        assert len(c.get_objects_of_types(*query)) == number

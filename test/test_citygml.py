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
                             (('waldbruecke_v1.0.0.gml', 523), ('geoRES_testdata_v1.0.0', 30)))
    def test_number_of_city_objects(self, filename, number):
        """
        Tests the returned number of city objects
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        assert len(c.city_objects) == number

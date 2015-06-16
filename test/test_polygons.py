import pytest

from citygml2stl import citygml
from citygml2stl import polygons


class TestPolygons(object):
    @pytest.mark.parametrize(('filename', 'number'),
                             (('waldbruecke_v1.0.0.gml', 15),
                              ('geoRES_testdata_v1.0.0', 1142),
                              ('CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml', 10105),
                              ('Berlin_Alexanderplatz_v0.4.0.xml', 16),))
    def test_extract_polygons(self, filename, number):
        """
        Tests the returned number of extracted polygons
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        obj = c.get_objects_of_types()[0]
        assert len(polygons.Polygons.extract_polygons(obj)) == number

    @pytest.mark.parametrize(('filename', 'enumber', 'inumber'),
                             (('waldbruecke_v1.0.0.gml', 6, 0),
                              ('geoRES_testdata_v1.0.0', 19, 0),
                              ('CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml', 5, 0),
                              ('Berlin_Alexanderplatz_v0.4.0.xml', 4, 0),))
    def test_epoints_ipoints(self, filename, enumber, inumber):
        """
        Tests the returned number of extracted points
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        obj = c.get_objects_of_types()[0]
        polygon = polygons.Polygons.extract_polygons(obj)[0]
        e, i = polygons.Polygons.epoints_ipoints(polygon)
        assert len(e) == enumber
        assert len(i) == inumber

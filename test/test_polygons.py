import operator
import pytest

from citygml2stl import citygml
from citygml2stl import exceptions
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


class TestPlane(object):
    @classmethod
    def normalize(cls, planelist):
        """
        Normlaize a normal vector of plane represented in a list
        """
        size = sum(list(map(abs, planelist))[:3])
        for i in range(0, 3):
            planelist[i] /= float(size)
        return planelist

    @pytest.mark.parametrize(('points', 'result'),
                             (([[0, 0, 0], [0, 1, 0], [0, 0, 1]], [1, 0, 0, 0]),
                              ([[0, 0, 0], [0, 1, 0], [1, 0, 0]], [0, 0, 1, 0]),
                              ([[0, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 0]], [1, 1, 1, -1]),
                              ([[5, 5, 0], [0, 5, 5], [5, 0, 5]], [1, 1, 1, -250]),))
    def test_valid_plane_construction(self, points, result):
        """
        Test if constructing a plane from valid list of points works
        """
        plane = polygons.Plane(points)

        # test only the direction of normal vector and not the size
        planelist = TestPlane.normalize([plane.a, plane.b, plane.c, plane.d])
        result = TestPlane.normalize(result)

        # test for the negative orientation as well
        results = [result, list(map(operator.neg, result))]

        assert planelist in results

    def test_to_few_points(self):
        """
        Test if constructing a plane from two points raises an exception
        """
        with pytest.raises(exceptions.PlaneConstructionError):
            plane = polygons.Plane([[0, 0, 0], [1, 1, 1]])

    def test_all_same_points(self):
        """
        Test if constructing a plane from all points the same raises an exception
        """
        with pytest.raises(exceptions.PlaneConstructionError):
            plane = polygons.Plane([[0] * 3] * 20)

    def test_two_unique_points(self):
        """
        Test if constructing a plane from just two unique points raises an exception
        """
        with pytest.raises(exceptions.PlaneConstructionError):
            plane = polygons.Plane([[0] * 3, [1] * 3] * 10)

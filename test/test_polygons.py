import operator
import pytest

import p2t

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

    @pytest.mark.parametrize('filename',
                             ('waldbruecke_v1.0.0.gml',
                              'CityGML_2.0_Test_Dataset_2012-04-23/Part-3-Railway-V2.gml',
                              'Berlin_Alexanderplatz_v0.4.0.xml'))
    def test_triangulate(self, filename):
        """
        Tests the triangulation
        There is no way we can check the results, so just check it's going without error
        """
        path = 'test/datasets/' + filename
        c = citygml.CityGML(path)
        for obj in c.get_objects_of_types():
            polygons.object2triangles(obj)


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

    @classmethod
    def alike(cls, a, b):
        """
        Check if the points are almost the same
        """
        for i in range(3):
            if abs(a[i]-b[i]) > 0.0000001:
                return False
        return True

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

    def test_points_in_line(self):
        """
        Test if constructing a plane from points forming a line raises an exception
        """
        with pytest.raises(exceptions.PlaneConstructionError):
            plane = polygons.Plane([[-1]*3, [0]*3, [1]*3, [8]*3, [-3]*3, [50]*3, [100]*3, [-10]*3])

    @pytest.mark.parametrize(('points', 'longest'),
                             (([[0, 0, 0], [0, 1, 0], [0, 0, 1]], 0),
                              ([[0, 0, 0], [0, 0, 1], [1, 0, 0]], 1),
                              ([[0, 0, 0], [0, 1, 0], [1, 0, 0]], 2),))
    def test_longest_recognition(self, points, longest):
        """
        Test if the longest index is well recognized
        """
        plane = polygons.Plane(points)
        assert plane.longest == longest

    @pytest.mark.parametrize(('points', 'point3d', 'point2d'),
                             (([[1, 0, 0], [1, 1, 0], [1, 0, 1]], [1, 5, 4], [5, 4]),
                              ([[0, 8, 0], [0, 8, 1], [1, 8, 0]], [0, 8, 4], [0, 4]),
                              ([[0, 0, -2], [0, 1, -2], [1, 0, -2]], [-1.5, 5, -2], [-1.5, 5]),
                              ([[-5, 2, -2.5], [0, 8, -2], [14, 5.6, -2]], [14, 5.6, -2], None),))
    def test_to2D_to3D(self, points, point3d, point2d):
        """
        Test if the conversion to 2D and back to 3D works
        """
        plane = polygons.Plane(points)
        p = plane.to2D(point3d)
        # None as in don't care
        if point2d is not None:
            assert [p.x, p.y] == point2d
        p = plane.to3D(p)
        assert TestPlane.alike(p, point3d)

    @pytest.mark.parametrize(('points', 'cross'),
                             (([[1, 0, 0], [1, 1, 0], [1, 0, 1]], [-1, 0, 0]),
                              ([[0, 8, 0], [0, 8, 1], [1, 8, 0]], [0, -1, 0]),
                              ([[0, 0, -2], [0, 1, -2], [1, 0, -2]], [0, 0, 1]),
                              ([[-5, 2, -2.5], [0, 8, -2], [14, 5.6, -2]], [-1.2, -7, 96]),))
    def test_crosspoints(self, points, cross):
        """
        test calculating crossproduct from 3 points
        """
        assert TestPlane.alike(polygons.Plane.crosspoints(*points), cross)


class TestLine(object):
    @pytest.mark.parametrize(('points', 'point', 'on'),
                             (([[1, 0], [1, 1]], [1, -150], True),
                              ([[1, 0], [1, 1]], [0, -150], False),
                              ([[11, 11], [-0.01, -0.01]], [1000, 1000], True),))
    def test_points_on_line(self, points, point, on):
        points = map(lambda x: p2t.Point(*x), points)
        line = polygons.Line(*points)
        assert line.is_on(p2t.Point(*point)) == on

from citygml2stl import citygml
from citygml2stl import exceptions
from citygml2stl import polygons
from citygml2stl import stl


class TestStlFile(object):
    def test_stl_dummy(self):
        """
        Tests writing a dummy STL file and checks if it is parsable by ADMesh
        """
        triangles = [
            [[0, 0, 0], [0, 1, 0], [1, 0, 0]],
            [[0, 0, 0], [1, 0, 0], [0, 0, 1]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        ]
        with stl.StlFile('test/dummy.stl') as test:
            test.write_triangles(triangles)
        try:
            import admesh
        except ImportError:
            pass
        else:
            s = admesh.Stl('test/dummy.stl')
            s.repair()
            s.calculate_volume()
            assert s.stats['volume'] > 0.1666666
            assert s.stats['volume'] < 0.1666667

    def test_stl_berlin(self):
        """
        Exports Berlin as one large STL
        """
        c = citygml.CityGML('test/datasets/Berlin_Alexanderplatz_v0.4.0.xml')

        with stl.StlFile('test/berlin.stl') as berlin:
            for obj in c.get_objects_of_types('Building'):
                berlin.write_triangles(polygons.object2triangles(obj))

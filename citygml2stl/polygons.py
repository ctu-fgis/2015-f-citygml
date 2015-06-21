import operator

from . import exceptions


class Polygons(object):
    """
    Class representing a set of polygons
    """
    gml = 'http://www.opengis.net/gml'

    @classmethod
    def extract_polygons(cls, obj):
        """
        Extract a list of polygons from given object
        """
        return obj.findall('.//{{{}}}Polygon'.format(cls.gml))

    @classmethod
    def exterior_interiors(cls, polygon):
        """
        Extracts exterior rings and all interior rings from a polygon
        """
        # Only one exterior ring
        exterior = polygon.find('.//{{{}}}exterior'.format(cls.gml))
        # But any number of interior rings (even zero)
        interiors = polygon.findall('.//{{{}}}interior'.format(cls.gml))
        return exterior, interiors

    @classmethod
    def ring_to_points(cls, ring):
        """
        Gets a list of points from given ring
        """
        ret = []

        points = ring.findall('.//{{{}}}posList'.format(cls.gml)) or \
            ring.findall('.//{{{}}}pos'.format(cls.gml))

        for point in points:
            coords = point.text.split()
            for i in range(0, len(coords), 3):
                ret.append((float(coords[i]),
                            float(coords[i+1]),
                            float(coords[i+2])))
        return ret

    @classmethod
    def epoints_ipoints(cls, polygon):
        """
        Gets lists of exterior and interior points
        """
        exterior, interiors = cls.exterior_interiors(polygon)
        epoints = cls.ring_to_points(exterior)
        ipoints = []
        for ring in interiors:
            ipoints.append(cls.ring_to_points(ring))
        return epoints, ipoints


class Plane(object):
    """
    Class representing a 2D plane in a 3D coordinate space
    """

    def __init__(self, points):
        """
        Initialize the plane with a list of points (at least 3 different) positioned on it
        """
        p, q, r = Plane.three_different_points(points)

        u = tuple(map(operator.sub, p, q))
        v = tuple(map(operator.sub, r, q))
        self.a, self.b, self.c = Plane.cross(u, v)
        self.d = -p[0] * self.a - p[1] * self.b - p[2] * self.c

    @classmethod
    def three_different_points(cls, points):
        """
        Return three different points or raise an exception
        """
        if len(points) < 3:
            raise exceptions.PlaneConstructionError('At least 3 points have to be provided')
        p = points[0]
        q = r = None

        idx = 0
        while idx < len(points) - 1:
            idx += 1
            if p != points[idx]:
                q = points[idx]
                break
        if q is None:
            raise exceptions.PlaneConstructionError('All points are the same')

        while idx < len(points) - 1:
            idx += 1
            if p != points[idx] and q != points[idx]:
                r = points[idx]
                break
        if r is None:
            raise exceptions.PlaneConstructionError('There are only 2 unique points')

        return p, q, r

    @classmethod
    def cross(cls, u, v):
        """
        Calculate the cross product of two given vectors
        """
        return [u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0]]

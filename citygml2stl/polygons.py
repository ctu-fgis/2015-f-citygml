import operator

import p2t

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
                            float(coords[i + 1]),
                            float(coords[i + 2])))

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

    @classmethod
    def preprocess(cls, points):
        """
        Remove duplicte points from list and check if all the points aren't on the same line
        If they are, return empty list

        Unfortunately p2t.Points are not comparable, so it is done coordinate by coordinate

        It is crucial to deduplicate 2D points and not 3D points in case 2 different 3D points
        result to the same 2D point, which is possible due to float limitations
        """
        uniq = []
        is_line = True

        for point in points:
            is_uniq = True
            for candidate in uniq:
                if point.x == candidate.x and point.y == candidate.y:
                    is_uniq = False
                    break

            if is_uniq:
                uniq.append(point)

                if is_line:
                    if len(uniq) > 2:
                        if not line.is_on(point):
                            is_line = False
                    elif len(uniq) == 2:
                        line = Line(*uniq)

        if is_line:
            return []
        return uniq

    @classmethod
    def triangulate(cls, polygon):
        """
        Triangulate the given polygon
        """
        epoints, ipoints = cls.epoints_ipoints(polygon)
        plane = Plane(epoints)

        epoints = cls.preprocess(map(plane.to2D, epoints))
        if not epoints:
            return []
        cdt = p2t.CDT(epoints)

        for hole in ipoints:
            hole = cls.preprocess(map(plane.to2D, hole))
            if hole:
                cdt.add_hole(hole)

        triangles2d = cdt.triangulate()
        return [list(map(plane.to3D, [t.a, t.b, t.c])) for t in triangles2d]

    @classmethod
    def triangulate_all(cls, obj):
        """
        Triangulate all polygons from given object
        """
        triangles = []
        for polygon in cls.extract_polygons(obj):
            try:
                triangles += cls.triangulate(polygon)
            except exceptions.PlaneConstructionError:
                pass
        return triangles


def object2triangles(obj):
    """Shortcut to triangulation method from Polygons class"""
    return Polygons.triangulate_all(obj)


class Plane(object):
    """
    Class representing a 2D plane in a 3D coordinate space
    """

    def __init__(self, points):
        """
        Initialize the plane with a list of points (at least 3 different) positioned on it
        """
        p, q, r, c = Plane.three_different_points(points)

        c.append(-p[0] * c[0] - p[1] * c[1] - p[2] * c[2])
        self.a, self.b, self.c, self.d = c
        self.longest = self._longest()

    @classmethod
    def crosspoints(cls, p, q, r):
        """
        Calculate a cross porduct from 3 points
        """
        u = tuple(map(operator.sub, p, q))
        v = tuple(map(operator.sub, r, q))
        return Plane.cross(u, v)

    @classmethod
    def three_different_points(cls, points):
        """
        Return three different points and their cross product or raise an exception
        """
        if len(points) < 3:
            raise exceptions.PlaneConstructionError('At least 3 points have to be provided')
        p = points[0]
        q = r = c = None
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
                c = cls.crosspoints(p, q, r)
                if c[0] or c[1] or c[2]:
                    break
                else:
                    c = None

        if c is None:
            raise exceptions.PlaneConstructionError('All points form a line')
        return p, q, r, c

    def _longest(self):
        """
        Returns an index of the longest normal vector part
        """
        values = tuple(map(abs, [self.a, self.b, self.c]))
        return max(range(3), key=values.__getitem__)

    def to2D(self, point):
        """
        Get a 2D point from a 3D point by simply omitting the less significant coordinate
        Return an instance of poly2tri point because that's what we'll need
        """
        p = point[:self.longest] + point[self.longest+1:]
        return p2t.Point(*p)

    def to3D(self, point):
        """
        Get a 3D point from a 2D point by recalculating the omitted less significant coordinate
        """
        # set all the points we know and 1, the point we don't has unsignificant value
        po = [point.x, point.y if self.longest else point.x, point.y, 1]
        # save the plane to list so we can index it
        pl = [self.a, self.b, self.c, self.d]
        # x = -(y*b + z*c + 1*d) / a
        # etc...
        po[self.longest] = -sum(
            [pl[i] * po[i] for i in range(4) if i is not self.longest]) / pl[self.longest]
        return po[:3]

    @classmethod
    def cross(cls, u, v):
        """
        Calculate the cross product of two given vectors
        """
        return [u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0]]


class Line(object):
    """
    Class representing  line in a 2D space
    """
    def __init__(self, a, b):
        """
        Construct a line form 2 given points (have to be different)
        """
        self.line = [a.y - b.y, b.x - a.x, 0]
        self.line[2] = -self.line[0] * a.x - self.line[1] * a.y

    def is_on(self, point, tolerance=0.0000001):
        """
        Whether the given point is on the line
        """
        return abs(self.line[0] * point.x + self.line[1] * point.y + self.line[2]) < tolerance

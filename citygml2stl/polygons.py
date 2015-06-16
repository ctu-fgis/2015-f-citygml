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
            ipoints += cls.ring_to_points(ring)
        return epoints, ipoints
